"""Build a compact public-page catalog from private Epitome captures."""

from __future__ import annotations

from datetime import datetime, timezone
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlsplit

from .capture import archival_url_key


DATE_URL_RE = re.compile(r"/(20\d{2})/(0[1-9]|1[0-2])/([0-2]\d|3[01])(?:/|$)")
TEXT_DATE_RE = re.compile(
    r"^(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|"
    r"Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?) "
    r"[0-3]?\d, 20\d{2}$"
)
WHITESPACE_RE = re.compile(r"\s+")


class _HeadMetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.visible_dates: list[str] = []
        self.json_ld: list[str] = []
        self._inside_title = False
        self._inside_h1 = False
        self._inside_json_ld = False
        self._script_depth = 0
        self._style_depth = 0
        self._json_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "meta":
            key = (values.get("property") or values.get("name") or "").lower()
            content = values.get("content", "").strip()
            if key and content and key not in self.meta:
                self.meta[key] = content
        elif tag == "title":
            self._inside_title = True
        elif tag == "h1" and not self.h1_parts:
            self._inside_h1 = True
        elif tag == "time" and values.get("datetime"):
            # Keep fallback dates in document order. Recommendation cards often
            # contain later <time> tags that must not outrank earlier hero copy.
            self.visible_dates.append(values["datetime"])
        elif tag == "script" and "ld+json" in values.get("type", "").lower():
            self._inside_json_ld = True
            self._json_parts = []
            self._script_depth += 1
        elif tag == "script":
            self._script_depth += 1
        elif tag == "style":
            self._style_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._inside_title = False
        elif tag == "h1":
            self._inside_h1 = False
        elif tag == "script" and self._inside_json_ld:
            self._inside_json_ld = False
            self.json_ld.append("".join(self._json_parts))
            self._script_depth = max(0, self._script_depth - 1)
        elif tag == "script":
            self._script_depth = max(0, self._script_depth - 1)
        elif tag == "style":
            self._style_depth = max(0, self._style_depth - 1)

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self.title_parts.append(data)
        if self._inside_h1:
            self.h1_parts.append(data)
        if self._inside_json_ld:
            self._json_parts.append(data)
        if not self._script_depth and not self._style_depth:
            value = _clean_text(data)
            if TEXT_DATE_RE.fullmatch(value):
                self.visible_dates.append(value)


def _clean_text(value: str) -> str:
    return WHITESPACE_RE.sub(" ", value).strip()


def _walk_json(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_json(child)


def _parse_timestamp(value: object) -> int | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    formats = ("%b %d, %Y", "%B %d, %Y", "%Y-%m-%d")
    parsed: datetime | None = None
    for format_string in formats:
        try:
            parsed = datetime.strptime(raw, format_string).replace(tzinfo=timezone.utc)
            break
        except ValueError:
            pass
    if parsed is None:
        try:
            parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return int(parsed.timestamp())


def extract_page_metadata(html_path: Path, url: str) -> dict[str, object]:
    """Extract portable title/date metadata without retaining captured HTML."""
    parser = _HeadMetadataParser()
    # Metadata is normally in the head. The cap avoids reading multi-megabyte
    # hydrated documents merely to generate a small public index.
    with html_path.open(encoding="utf-8", errors="replace") as handle:
        parser.feed(handle.read(512 * 1024))

    title = next(
        (
            _clean_text(value)
            for value in (
                parser.meta.get("og:title", ""),
                parser.meta.get("twitter:title", ""),
                "".join(parser.h1_parts),
                "".join(parser.title_parts),
            )
            if _clean_text(value)
        ),
        urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1] or urlsplit(url).hostname or url,
    )

    published_candidates: list[object] = [
        parser.meta.get("article:published_time"),
        parser.meta.get("date"),
        parser.meta.get("datepublished"),
    ]
    for raw in parser.json_ld:
        try:
            document = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for item in _walk_json(document):
            item_type = item.get("@type")
            if isinstance(item_type, list):
                types = {str(value).lower() for value in item_type}
            else:
                types = {str(item_type).lower()}
            is_article = bool(
                types
                & {
                    "article",
                    "blogposting",
                    "newsarticle",
                    "report",
                    "scholarlyarticle",
                    "techarticle",
                }
            )
            if not is_article and not (
                isinstance(item.get("headline"), str) and "datePublished" in item
            ):
                continue
            published_candidates.extend(
                item.get(key) for key in ("datePublished", "dateCreated")
            )
            if title == url and isinstance(item.get("headline"), str):
                title = _clean_text(item["headline"])
    path_parts = [part for part in urlsplit(url).path.split("/") if part]
    if len(path_parts) >= 2:
        published_candidates.extend(parser.visible_dates)
    published_at = next(
        (parsed for value in published_candidates if (parsed := _parse_timestamp(value))),
        None,
    )
    if published_at is None and (match := DATE_URL_RE.search(urlsplit(url).path)):
        try:
            published_at = int(
                datetime(*(int(part) for part in match.groups()), tzinfo=timezone.utc).timestamp()
            )
        except ValueError:
            pass
    return {"title": title, "published_at": published_at}


def _source_for_url(url: str, sources: list[dict[str, object]]) -> dict[str, object] | None:
    hostname = (urlsplit(url).hostname or "").lower()
    for source in sources:
        hosts = [str(host).lower() for host in source.get("hosts", [])]
        if any(hostname == host or hostname.endswith(f".{host}") for host in hosts):
            return source
    return None


def _clean_source_title(title: object, source: dict[str, object]) -> str:
    value = _clean_text(str(title))
    for suffix in source.get("title_suffixes", []):
        suffix_text = str(suffix)
        if value.lower().endswith(suffix_text.lower()):
            value = value[: -len(suffix_text)].rstrip()
            break
    prefix = str(source.get("title_prefix", ""))
    if prefix and value.lower().startswith(prefix.lower()):
        value = value[len(prefix) :].lstrip()
    return value or str(source["name"])


def _path_matches(url: str, configured_paths: object) -> bool:
    path = urlsplit(url).path.rstrip("/") or "/"
    return path in {str(value).rstrip("/") or "/" for value in configured_paths or []}


def build_public_catalog(
    archive_root: Path,
    source_config_path: Path,
    output_path: Path,
) -> dict[str, int]:
    """Scan complete captures and write a deduplicated, portable JSON catalog."""
    config = json.loads(source_config_path.read_text(encoding="utf-8"))
    sources = config.get("sources") if isinstance(config, dict) else None
    if not isinstance(sources, list):
        raise ValueError("source config must contain a sources array")

    captures: dict[str, tuple[int, Path, dict[str, Any], dict[str, object]]] = {}
    malformed = 0
    for source in sources:
        source_root = archive_root / str(source["archive_directory"])
        if not source_root.exists():
            continue
        for directory, directories, filenames in os.walk(source_root, followlinks=True):
            directories[:] = [
                name
                for name in directories
                if name not in {"assets", "dependencies", "network"}
            ]
            if "manifest.json" not in filenames or "page.html" not in filenames:
                continue
            manifest_path = Path(directory) / "manifest.json"
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                malformed += 1
                continue
            if not manifest.get("complete"):
                continue
            url = manifest.get("final_url") or manifest.get("requested_url")
            if not isinstance(url, str) or _source_for_url(url, [source]) is None:
                continue
            if _path_matches(url, source.get("exclude_paths")):
                continue
            try:
                identity = archival_url_key(url)
            except ValueError:
                malformed += 1
                continue
            captured_at = int(manifest.get("capture_started_at", 0))
            previous = captures.get(identity)
            if previous is None or captured_at >= previous[0]:
                captures[identity] = (captured_at, Path(directory), manifest, source)

    entries: list[dict[str, object]] = []
    for identity, (captured_at, directory, manifest, source) in captures.items():
        url = str(manifest.get("final_url") or manifest.get("requested_url"))
        metadata = extract_page_metadata(directory / "page.html", url)
        if _path_matches(url, source.get("undated_paths")):
            metadata["published_at"] = None
        entries.append(
            {
                "captured_at": captured_at,
                "published_at": metadata["published_at"],
                "source": str(source["id"]),
                "title": _clean_source_title(metadata["title"], source),
                "url": identity,
            }
        )
    entries.sort(
        key=lambda entry: (
            int(entry["published_at"] or -1),
            int(entry["captured_at"]),
            str(entry["url"]),
        ),
        reverse=True,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    public_sources = []
    for source in sources:
        record = {"id": str(source["id"]), "name": str(source["name"])}
        if source.get("logo_url"):
            record["logo_url"] = str(source["logo_url"])
        public_sources.append(record)
    output_path.write_text(
        json.dumps({"sources": public_sources, "pages": entries}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return {
        "pages": len(entries),
        "sources": len({str(entry["source"]) for entry in entries}),
        "dated": sum(entry["published_at"] is not None for entry in entries),
        "malformed": malformed,
    }
