"""Offline-only replay of Epitome browser captures."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape, unescape
from html.parser import HTMLParser
import base64
import ipaddress
import json
from pathlib import Path
import re
from typing import Any, Iterable
from urllib.parse import urljoin, urlsplit

from .assets import complete_body, discover_vimeo_video_asset


CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
CSS_IMPORT_RE = re.compile(
    r"(@import\s+)(?!url\()(['\"])(.*?)\2",
    re.IGNORECASE,
)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
FETCH_ATTRIBUTES = {
    "audio": {"src"},
    "embed": {"src"},
    "iframe": {"src"},
    "img": {"src", "data-src"},
    "input": {"src"},
    "object": {"data"},
    "source": {"src"},
    "track": {"src"},
    "video": {"poster", "src"},
}


def encode_url(url: str) -> str:
    return base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")


def decode_url(token: str) -> str:
    padding = "=" * (-len(token) % 4)
    return base64.urlsafe_b64decode(token + padding).decode()


def replay_path(url: str) -> str:
    return f"/replay/{encode_url(url)}"


def resource_path(url: str) -> str:
    return f"/resource/{encode_url(url)}"


def unavailable_path(url: str) -> str:
    return f"/unavailable/{encode_url(url)}"


def normalize_url(value: str, base_url: str) -> str | None:
    value = value.strip()
    if not value or value.startswith(("data:", "blob:", "javascript:", "#")):
        return None
    resolved = urljoin(base_url, value)
    parsed = urlsplit(resolved)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    return parsed._replace(fragment="").geturl()


def is_archival_url(value: str) -> bool:
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    if parsed.hostname.lower() == "localhost":
        return False
    try:
        return not ipaddress.ip_address(parsed.hostname).is_loopback
    except ValueError:
        return True


@dataclass(frozen=True)
class PageRecord:
    url: str
    title: str
    html_path: Path
    captured_at: int


@dataclass(frozen=True)
class ResourceRecord:
    url: str
    body_path: Path
    content_type: str
    headers: dict[str, str]
    order: int


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


class CaptureIndex:
    """Latest complete page and response records found below capture roots."""

    def __init__(self) -> None:
        self.pages: dict[str, PageRecord] = {}
        self.resources: dict[str, ResourceRecord] = {}
        self.vimeo_videos: dict[str, str] = {}

    @classmethod
    def from_roots(cls, roots: Iterable[Path]) -> "CaptureIndex":
        index = cls()
        for root in roots:
            index.add_root(root)
        index._index_vimeo_videos()
        return index

    def add_root(self, root: Path) -> None:
        if not root.exists():
            return
        for manifest_path in root.rglob("manifest.json"):
            self._add_page_manifest(manifest_path)
        for metadata_path in root.rglob("metadata.json"):
            if metadata_path.parent.parent.name == "network":
                self._add_resource(metadata_path)

    def _add_page_manifest(self, manifest_path: Path) -> None:
        html_path = manifest_path.with_name("page.html")
        if not html_path.exists():
            return
        try:
            manifest = _read_json(manifest_path)
        except (OSError, json.JSONDecodeError):
            return
        captured_at = int(manifest.get("capture_started_at", 0))
        title = manifest.get("title")
        if not title:
            try:
                with html_path.open(encoding="utf-8", errors="replace") as stream:
                    match = TITLE_RE.search(stream.read(256 * 1024))
                if match:
                    title = unescape(match.group(1)).strip()
            except OSError:
                pass
        if not title:
            title = urlsplit(
                str(manifest.get("final_url") or manifest.get("requested_url", ""))
            ).path
        urls = {
            value
            for value in (
                manifest.get("requested_url"),
                manifest.get("final_url"),
            )
            if isinstance(value, str) and value and is_archival_url(value)
        }
        for url in urls:
            current = self.pages.get(url)
            if current is None or captured_at >= current.captured_at:
                self.pages[url] = PageRecord(url, str(title), html_path, captured_at)

    def _add_resource(self, metadata_path: Path) -> None:
        try:
            metadata = _read_json(metadata_path)
        except (OSError, json.JSONDecodeError):
            return
        if not complete_body(metadata_path.parent, metadata):
            return
        try:
            headers = {
                str(name).lower(): str(value)
                for name, value in _read_json(
                    metadata_path.with_name("response-headers.json")
                ).items()
            }
        except (OSError, json.JSONDecodeError, AttributeError):
            headers = {}
        content_type = (
            headers.get("content-type")
            or str(metadata.get("contentType", ""))
            or "application/octet-stream"
        )
        order = metadata_path.stat().st_mtime_ns
        urls = {
            value
            for value in (metadata.get("url"), metadata.get("finalUrl"))
            if isinstance(value, str) and value and is_archival_url(value)
        }
        for url in urls:
            current = self.resources.get(url)
            if current is None or order >= current.order:
                self.resources[url] = ResourceRecord(
                    url=url,
                    body_path=metadata_path.with_name("response-body.bin"),
                    content_type=content_type,
                    headers=headers,
                    order=order,
                )

    def page(self, url: str) -> PageRecord | None:
        return self.pages.get(url)

    def resource(self, url: str) -> ResourceRecord | None:
        return self.resources.get(url)

    def unique_pages(self) -> list[PageRecord]:
        unique: dict[Path, PageRecord] = {}
        for page in self.pages.values():
            unique[page.html_path] = page
        return sorted(unique.values(), key=lambda page: page.url)

    def _index_vimeo_videos(self) -> None:
        for player_url, resource in self.resources.items():
            if urlsplit(player_url).hostname != "player.vimeo.com":
                continue
            try:
                html = resource.body_path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )
            except OSError:
                continue
            video_url = discover_vimeo_video_asset(html)
            if video_url and video_url in self.resources:
                self.vimeo_videos[player_url] = video_url

    def vimeo_video(self, player_url: str) -> str | None:
        return self.vimeo_videos.get(player_url)


def rewrite_css(css: str, base_url: str) -> str:
    def replace_url(match: re.Match[str]) -> str:
        url = normalize_url(match.group(2), base_url)
        if not url:
            return match.group(0)
        return f'url("{resource_path(url)}")'

    def replace_import(match: re.Match[str]) -> str:
        url = normalize_url(match.group(3), base_url)
        if not url:
            return match.group(0)
        return f'{match.group(1)}"{resource_path(url)}"'

    return CSS_IMPORT_RE.sub(replace_import, CSS_URL_RE.sub(replace_url, css))


class _HTMLRewriter(HTMLParser):
    def __init__(self, index: CaptureIndex, base_url: str):
        super().__init__(convert_charrefs=False)
        self.index = index
        self.base_url = base_url
        self.output: list[str] = []
        self.script_depth = 0
        self.style_depth = 0
        self.replaced_vimeo_iframes = 0

    def _resource(self, value: str) -> str:
        url = normalize_url(value, self.base_url)
        return resource_path(url) if url else value

    def _link(self, value: str) -> str:
        url = normalize_url(value, self.base_url)
        if not url:
            return value
        if self.index.page(url):
            return replay_path(url)
        return unavailable_path(url)

    def _srcset(self, value: str) -> str:
        candidates = []
        for candidate in value.split(","):
            parts = candidate.strip().split(maxsplit=1)
            if not parts:
                continue
            rewritten = self._resource(parts[0])
            candidates.append(
                f"{rewritten} {parts[1]}" if len(parts) == 2 else rewritten
            )
        return ", ".join(candidates)

    def _should_drop_link(self, attrs: dict[str, str]) -> bool:
        rel = set(attrs.get("rel", "").lower().split())
        if rel & {"dns-prefetch", "modulepreload", "preconnect"}:
            return True
        return "preload" in rel and attrs.get("as", "").lower() == "script"

    def _start(
        self,
        tag: str,
        attrs_list: list[tuple[str, str | None]],
        *,
        closed: bool,
    ) -> None:
        tag = tag.lower()
        if tag == "script":
            self.script_depth += 1
            return
        if self.script_depth:
            return
        attrs = {
            name.lower(): value
            for name, value in attrs_list
            if value is not None
        }
        if tag == "base":
            return
        if tag == "link" and self._should_drop_link(attrs):
            return
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            return

        vimeo_video_url = None
        if (
            tag == "iframe"
            and "vimeo" in attrs.get("title", "").lower()
            and (iframe_url := normalize_url(attrs.get("src", ""), self.base_url))
        ):
            vimeo_video_url = self.index.vimeo_video(iframe_url)
            if vimeo_video_url:
                tag = "video"
                self.replaced_vimeo_iframes += 1

        rendered_attrs = []
        for name, value in attrs_list:
            lower = name.lower()
            if lower.startswith("on") or lower in {"integrity", "nonce"}:
                continue
            if value is None:
                rendered_attrs.append(name)
                continue
            if vimeo_video_url and lower in {"allow", "loading", "src"}:
                continue
            if vimeo_video_url and lower == "class":
                value = " ".join(
                    item for item in value.split() if item != "opacity-0"
                )
            if tag == "img" and lower == "loading":
                value = "eager"
            if lower == "srcset":
                value = self._srcset(value)
            elif lower == "style":
                value = rewrite_css(value, self.base_url)
            elif lower in FETCH_ATTRIBUTES.get(tag, set()):
                value = self._resource(value)
            elif tag == "link" and lower == "href":
                rel = set(attrs.get("rel", "").lower().split())
                if rel & {"apple-touch-icon", "icon", "stylesheet"}:
                    value = self._resource(value)
            elif tag == "a" and lower == "href":
                value = self._link(value)
            elif tag == "form" and lower == "action":
                value = self._link(value)
            rendered_attrs.append(f'{name}="{escape(value, quote=True)}"')

        if vimeo_video_url:
            rendered_attrs.extend(
                [
                    f'src="{resource_path(vimeo_video_url)}"',
                    "controls",
                    "playsinline",
                    'preload="metadata"',
                ]
            )
        suffix = " /" if closed else ""
        attributes = f" {' '.join(rendered_attrs)}" if rendered_attrs else ""
        self.output.append(f"<{tag}{attributes}{suffix}>")
        if tag == "style":
            self.style_depth += 1

    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs, closed=False)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs, closed=True)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "script":
            if self.script_depth:
                self.script_depth -= 1
            return
        if self.script_depth:
            return
        if tag == "style" and self.style_depth:
            self.style_depth -= 1
        if tag == "iframe" and self.replaced_vimeo_iframes:
            self.replaced_vimeo_iframes -= 1
            self.output.append("</video>")
            return
        self.output.append(f"</{tag}>")

    def handle_data(self, data):
        if self.script_depth:
            return
        self.output.append(rewrite_css(data, self.base_url) if self.style_depth else data)

    def handle_entityref(self, name):
        if not self.script_depth:
            self.output.append(f"&{name};")

    def handle_charref(self, name):
        if not self.script_depth:
            self.output.append(f"&#{name};")

    def handle_comment(self, data):
        if not self.script_depth:
            self.output.append(f"<!--{data}-->")

    def handle_decl(self, decl):
        self.output.append(f"<!{decl}>")


def rewrite_html(html: str, base_url: str, index: CaptureIndex) -> str:
    rewriter = _HTMLRewriter(index, base_url)
    rewriter.feed(html)
    rewriter.close()
    return "".join(rewriter.output)


def archive_index_html(index: CaptureIndex) -> str:
    entries = []
    for page in index.unique_pages():
        label = page.title.strip("/") or page.url
        entries.append(
            f'<li><a href="{replay_path(page.url)}">{escape(label)}</a>'
            f"<small>{escape(page.url)}</small></li>"
        )
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Epitome archive</title>
<style>
body{{font:16px/1.5 system-ui;margin:3rem auto;max-width:70rem;padding:0 1.5rem}}
h1{{font-size:2rem}}li{{margin:1rem 0}}small{{display:block;color:#666}}
</style></head><body><h1>Epitome archive</h1>
<p>{len(entries)} captured pages available for offline replay.</p>
<ul>{''.join(entries)}</ul></body></html>"""


def unavailable_html(url: str) -> str:
    return f"""<!doctype html><meta charset="utf-8"><title>Not archived</title>
<style>body{{font:16px/1.5 system-ui;margin:4rem auto;max-width:50rem}}</style>
<h1>Not archived</h1><p>This link was intentionally kept offline:</p>
<p><code>{escape(url)}</code></p><p><a href="/">Return to the archive</a></p>"""
