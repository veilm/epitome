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
from urllib.parse import parse_qsl, quote, urlencode, urljoin, urlsplit

from .assets import complete_body, discover_vimeo_video_asset


CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
CSS_IMPORT_RE = re.compile(
    r"(@import\s+)(?!url\()(['\"])(.*?)\2",
    re.IGNORECASE,
)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
TWITTER_BLOCKQUOTE_RE = re.compile(
    r'<blockquote\b[^>]*class=(["\'])[^"\']*\btwitter-(?:tweet|video)\b[^"\']*\1[^>]*>'
    r".*?</blockquote>",
    re.IGNORECASE | re.DOTALL,
)
TWITTER_STATUS_RE = re.compile(r"/(?:status|statuses)/(\d+)", re.IGNORECASE)
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


class _ScriptJSONExtractor(HTMLParser):
    def __init__(self, target_id: str) -> None:
        super().__init__(convert_charrefs=False)
        self.target_id = target_id
        self.depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "script":
            return
        values = {name.lower(): value or "" for name, value in attrs}
        if self.depth or values.get("id") == self.target_id:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)


def _disqus_thread_data(html: str) -> dict[str, Any] | None:
    parser = _ScriptJSONExtractor("disqus-threadData")
    parser.feed(html)
    if not parser.parts:
        return None
    try:
        value = json.loads("".join(parser.parts))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _static_disqus_comments(html: str) -> str:
    data = _disqus_thread_data(html)
    if not data:
        return ""
    response = data.get("response", {})
    posts = response.get("posts", []) if isinstance(response, dict) else []
    if not isinstance(posts, list):
        return ""
    thread = response.get("thread", {})
    cursor = data.get("cursor", {}) if data else {}
    total = cursor.get("total", len(posts)) if isinstance(cursor, dict) else len(posts)
    title = thread.get("clean_title") or thread.get("title") or "Archived discussion"
    comments = []
    for post in posts:
        if not isinstance(post, dict):
            continue
        author = post.get("author", {})
        if not isinstance(author, dict):
            author = {}
        author_name = author.get("name") or author.get("username") or "Anonymous"
        created_at = str(post.get("createdAt") or "")
        points = post.get("points")
        score = f" · {points} point{'s' if points != 1 else ''}" if isinstance(points, int) else ""
        depth = min(max(int(post.get("depth", 0) or 0), 0), 6)
        message = post.get("message") or post.get("raw_message")
        if not isinstance(message, str) or not message.strip():
            message = "<p><em>Deleted comment</em></p>"
        post_id = escape(str(post.get("id") or ""), quote=True)
        parent_id = escape(str(post.get("parent") or ""), quote=True)
        comments.append(
            f'<article class="epitome-disqus-comment" data-post-id="{post_id}" '
            f'data-parent-id="{parent_id}" style="margin-left:{depth * 1.5}rem">'
            f'<header><strong>{escape(str(author_name))}</strong>'
            f'<span>{escape(created_at)}{escape(score)}</span></header>'
            f'<div class="epitome-disqus-message">{message}</div></article>'
        )
    return (
        '<section id="epitome-disqus-comments">'
        f'<h2>{escape(str(title))} — {escape(str(total))} comments</h2>'
        '<p class="epitome-disqus-note">Static comments preserved by Epitome; '
        'interactive voting and replies are unavailable offline.</p>'
        f'{"".join(comments)}</section>'
        '<style id="epitome-disqus-style">'
        '#epitome-disqus-comments{box-sizing:border-box;color:#333;'
        'font:15px/1.5 system-ui,sans-serif;margin:0 auto;max-width:800px;padding:1rem}'
        '#epitome-disqus-comments h2{font-size:1.25rem;margin:.5rem 0}'
        '.epitome-disqus-note{color:#666;font-size:.85rem}'
        '.epitome-disqus-comment{border-top:1px solid #ddd;padding:1rem 0}'
        '.epitome-disqus-comment header{display:flex;gap:.5rem;justify-content:space-between}'
        '.epitome-disqus-comment header span{color:#666;font-size:.8rem}'
        '.epitome-disqus-message p:first-child{margin-top:.5rem}'
        '.epitome-disqus-message img{height:auto;max-width:100%}'
        '</style>'
    )


def _inject_static_disqus_comments(html: str) -> str:
    comments = _static_disqus_comments(html)
    if not comments:
        return html
    match = re.search(r"</body\s*>", html, re.IGNORECASE)
    if not match:
        return html + comments
    return html[: match.start()] + comments + html[match.start() :]


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


def resolve_byte_range(
    length: int,
    value: str | None,
    *,
    max_open_ended: int | None = None,
) -> tuple[int, int, int]:
    """Resolve one HTTP byte range as ``(status, start, end)``.

    Invalid syntax keeps the full response for compatibility with ordinary
    clients. A syntactically valid but unsatisfiable range returns status 416.
    """
    start = 0
    end = length - 1
    if not value:
        return 200, start, end
    match = re.fullmatch(r"bytes=(\d*)-(\d*)", value.strip())
    if not match:
        return 200, start, end
    first, last = match.groups()
    if not first and not last:
        return 200, start, end
    if first:
        start = int(first)
        end = int(last) if last else end
        if not last and max_open_ended:
            end = min(end, start + max_open_ended - 1)
    else:
        suffix = int(last)
        if suffix:
            start = max(0, length - suffix)
    end = min(end, length - 1)
    if length <= 0 or start > end or start >= length:
        return 416, 0, -1
    return 206, start, end


def normalize_url(value: str, base_url: str) -> str | None:
    value = value.strip()
    if not value or value.startswith(("data:", "blob:", "javascript:", "#")):
        return None
    resolved = quote(
        urljoin(base_url, value),
        safe=":/?#[]@!$&'()*+,;=%",
    )
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


def stable_resource_identity(url: str) -> str | None:
    """Return a stable lookup key for known expiring resource URLs."""
    parsed = urlsplit(url)
    if (parsed.hostname or "").lower() != "download.ssrn.com":
        return None
    abstract_id = next(
        (
            value
            for name, value in parse_qsl(parsed.query)
            if name.lower() == "abstractid" and value
        ),
        None,
    )
    if not abstract_id:
        return None
    return parsed._replace(
        scheme="https",
        query=urlencode({"abstractId": abstract_id}),
        fragment="",
    ).geturl()


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
        self.resource_aliases: dict[str, str] = {}
        self.vimeo_videos: dict[str, str] = {}
        self.twitter_quotes: dict[str, str] = {}

    @classmethod
    def from_roots(cls, roots: Iterable[Path]) -> "CaptureIndex":
        index = cls()
        for root in roots:
            index.add_root(root)
        index._index_vimeo_videos()
        index._index_twitter_quotes()
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
                record = ResourceRecord(
                    url=url,
                    body_path=metadata_path.with_name("response-body.bin"),
                    content_type=content_type,
                    headers=headers,
                    order=order,
                )
                self.resources[url] = record
                if identity := stable_resource_identity(url):
                    identity_current = self.resources.get(identity)
                    if identity_current is None or order >= identity_current.order:
                        self.resources[identity] = record

    def page(self, url: str) -> PageRecord | None:
        return self.pages.get(url)

    def resource(self, url: str) -> ResourceRecord | None:
        seen: set[str] = set()
        while url not in seen:
            seen.add(url)
            if resource := self.resources.get(url):
                return resource
            if identity := stable_resource_identity(url):
                if resource := self.resources.get(identity):
                    return resource
            replacement = self.resource_aliases.get(url)
            if not replacement:
                return None
            url = replacement
        return None

    def add_resource_aliases(self, aliases: dict[str, str]) -> None:
        """Add reviewed URL substitutions for resources lost at their origin."""
        for original, replacement in aliases.items():
            if not isinstance(original, str) or not isinstance(replacement, str):
                raise ValueError("resource aliases must map URL strings to URL strings")
            if not is_archival_url(original) or not is_archival_url(replacement):
                raise ValueError("resource aliases must contain archival HTTP(S) URLs")
            self.resource_aliases[original] = replacement

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

    def _index_twitter_quotes(self) -> None:
        """Recover static tweet text from pre-widget server HTML."""
        for resource in self.resources.values():
            if "html" not in resource.content_type.lower():
                continue
            try:
                html = resource.body_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if "twitter-tweet" not in html and "twitter-video" not in html:
                continue
            for match in TWITTER_BLOCKQUOTE_RE.finditer(html):
                quote_html = match.group(0)
                if status := TWITTER_STATUS_RE.search(quote_html):
                    self.twitter_quotes[status.group(1)] = quote_html

    def twitter_quote(self, status_id: str) -> str | None:
        return self.twitter_quotes.get(status_id)


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
        self.replaced_twitter_iframes = 0
        self.replaced_media_iframes = 0

    def _resource(self, value: str) -> str:
        url = normalize_url(value, self.base_url)
        return resource_path(url) if url else value

    def _link(self, value: str) -> str:
        url = normalize_url(value, self.base_url)
        if not url:
            return value
        if self.index.page(url):
            return replay_path(url)
        if self.index.resource(url):
            return resource_path(url)
        return unavailable_path(url)

    def _srcset(self, value: str) -> str:
        candidates = []
        # A URL itself may legally contain commas. Substack's image proxy uses
        # several comma-separated transformations inside every URL, while the
        # actual srcset candidates are separated by a comma followed by
        # whitespace. Splitting every comma corrupts those URLs into dozens of
        # bogus relative candidates.
        for candidate in re.split(r",(?=\s)", value):
            parts = candidate.strip().split(maxsplit=1)
            if not parts:
                continue
            url = normalize_url(parts[0], self.base_url)
            # Do not advertise responsive variants that are absent locally.
            # Browsers otherwise prefer a missing high-DPI/WebP candidate over
            # a complete captured `src`, leaving a blank image in replay.
            if not url or not self.index.resource(url):
                continue
            rewritten = resource_path(url)
            candidates.append(
                f"{rewritten} {parts[1]}" if len(parts) == 2 else rewritten
            )
        return ", ".join(candidates)

    def _should_drop_link(self, attrs: dict[str, str]) -> bool:
        rel = set(attrs.get("rel", "").lower().split())
        if rel & {"dns-prefetch", "modulepreload", "preconnect", "prefetch"}:
            return True
        # Preloads are only performance hints. Keeping captured absolute font,
        # style, image, or script preloads lets the offline replay contact the
        # production CDN before the localized real element is encountered.
        return "preload" in rel

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

        iframe_url = (
            normalize_url(attrs.get("src", ""), self.base_url)
            if tag == "iframe"
            else None
        )
        if iframe_url:
            parsed_iframe = urlsplit(iframe_url)
            host = (parsed_iframe.hostname or "").lower()
            path_parts = [part for part in parsed_iframe.path.split("/") if part]
            provider = None
            label = None
            wide = False
            if host in {
                "youtube.com",
                "www.youtube.com",
                "youtube-nocookie.com",
                "www.youtube-nocookie.com",
            } and len(path_parts) >= 2 and path_parts[0] == "embed":
                provider = "YouTube"
                label = f"video {path_parts[1]}"
                wide = True
            elif host == "embed.podcasts.apple.com":
                provider = "Apple Podcasts"
                label = "episode"
            elif host == "open.spotify.com" and "embed" in path_parts:
                provider = "Spotify"
                label = path_parts[-1] if path_parts else "episode"
            if provider:
                classes = "epitome-media-placeholder epitome-media-wide" if wide else "epitome-media-placeholder"
                self.output.append(
                    f'<figure class="{classes}" data-provider="{escape(provider, quote=True)}">'
                    f'<strong>{escape(provider)} {escape(label or "media")}</strong>'
                    '<span>Media is recorded for separate offline import.</span>'
                    f'<a href="{unavailable_path(iframe_url)}">Archived source reference</a>'
                    "</figure>"
                )
                self.replaced_media_iframes += 1
                return

        vimeo_video_url = None
        if (
            tag == "iframe"
            and iframe_url
            and (
                "vimeo" in attrs.get("title", "").lower()
                or urlsplit(iframe_url).hostname == "player.vimeo.com"
            )
        ):
            vimeo_video_url = self.index.vimeo_video(iframe_url)
            if vimeo_video_url:
                tag = "video"
                self.replaced_vimeo_iframes += 1
            else:
                self.output.append(
                    '<figure class="epitome-media-placeholder epitome-media-wide" '
                    'data-provider="Vimeo">'
                    '<strong>Vimeo video unavailable</strong>'
                    '<span>The live player exposed no preservable media.</span>'
                    f'<a href="{unavailable_path(iframe_url)}">Archived source reference</a>'
                    "</figure>"
                )
                self.replaced_media_iframes += 1
                return

        twitter_quote = None
        if tag == "iframe" and (status_id := attrs.get("data-tweet-id")):
            twitter_quote = self.index.twitter_quote(status_id)
            if twitter_quote:
                self.output.append(twitter_quote)
                self.replaced_twitter_iframes += 1
                return

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
        if tag == "head":
            # Consent controls captured in their initial state become inert once
            # replay strips scripts.  Keep the raw HTML untouched on disk, but
            # do not let an uncloseable overlay obscure the archived document.
            self.output.append(
                '<style id="epitome-replay-style">'
                '#consent-banner,[data-testid="consent-banner"]'
                '{display:none!important}'
                'figure[class*="post-video-container"]'
                '{height:auto!important;aspect-ratio:16/9}'
                '.transition_wrap{display:none!important}'
                'main>section[style*="visibility: hidden"],'
                'main .word[style*="visibility: hidden"]'
                '{visibility:visible!important;opacity:1!important;'
                'transform:none!important}'
                '.epitome-media-placeholder{align-items:center;border:1px solid #bbb;'
                'box-sizing:border-box;display:flex;flex-direction:column;gap:.5rem;'
                'justify-content:center;margin:1rem auto;max-width:100%;min-height:9rem;'
                'padding:1.5rem;text-align:center}'
                '.epitome-media-placeholder span{color:#666}'
                '.epitome-media-wide{aspect-ratio:16/9;height:auto!important;width:100%}'
                '</style>'
            )
        if tag == "style" and self.style_depth:
            self.style_depth -= 1
        if tag == "iframe" and self.replaced_vimeo_iframes:
            self.replaced_vimeo_iframes -= 1
            self.output.append("</video>")
            return
        if tag == "iframe" and self.replaced_twitter_iframes:
            self.replaced_twitter_iframes -= 1
            return
        if tag == "iframe" and self.replaced_media_iframes:
            self.replaced_media_iframes -= 1
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
    html = _inject_static_disqus_comments(html)
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
