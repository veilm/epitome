"""Build a portable inventory of embedded media referenced by captures."""

from __future__ import annotations

from collections import defaultdict
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from typing import Any
from urllib.parse import urlsplit


YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{6,}$")
PRESERVED_ITEM_FIELDS = ("status", "imported_files", "notes")


class EmbeddedMediaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.document_title_parts: list[str] = []
        self.in_title = False
        self.youtube: list[dict[str, str]] = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() != "iframe":
            return
        values = {name.lower(): value or "" for name, value in attrs}
        src = values.get("src", "")
        parsed = urlsplit(src)
        host = parsed.hostname or ""
        if host not in {
            "youtube.com",
            "www.youtube.com",
            "youtube-nocookie.com",
            "www.youtube-nocookie.com",
        }:
            return
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) < 2 or parts[0] != "embed" or not YOUTUBE_ID_RE.fullmatch(parts[1]):
            return
        self.youtube.append(
            {
                "video_id": parts[1],
                "embed_title": values.get("title", "").strip(),
                "embed_url": src,
            }
        )

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.document_title_parts.append(data)

    @property
    def document_title(self) -> str:
        return " ".join("".join(self.document_title_parts).split())


def _existing_items(output: Path) -> dict[tuple[str, str], dict[str, Any]]:
    if not output.exists():
        return {}
    try:
        data = json.loads(output.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {
        (item.get("provider", ""), item.get("video_id", "")): item
        for item in data.get("items", [])
        if item.get("provider") and item.get("video_id")
    }


def build_youtube_inventory(
    capture_roots: list[Path],
    *,
    source: str,
    media_root: str = "media/youtube",
    generated_at_unix: int | None = None,
    existing: dict[tuple[str, str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    articles_by_video: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    capture_runs: set[str] = set()

    for root in capture_roots:
        capture_runs.add(root.name)
        for manifest_path in sorted(root.rglob("manifest.json")):
            page_path = manifest_path.with_name("page.html")
            if not page_path.is_file():
                continue
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                html = page_path.read_text(encoding="utf-8", errors="replace")
            except (OSError, json.JSONDecodeError):
                continue
            article_url = manifest.get("final_url") or manifest.get("requested_url")
            if not article_url:
                continue
            parser = EmbeddedMediaParser()
            parser.feed(html)
            for embedded in parser.youtube:
                video_id = embedded["video_id"]
                current = {
                    "url": article_url,
                    "title": parser.document_title or article_url,
                    "embed_title": embedded["embed_title"],
                    "embed_url": embedded["embed_url"],
                    "capture_run": root.name,
                    "capture_page": str(manifest_path.parent.relative_to(root)),
                    "capture_started_at": int(manifest.get("capture_started_at", 0)),
                }
                previous = articles_by_video[video_id].get(article_url)
                if not previous or current["capture_started_at"] >= previous["capture_started_at"]:
                    articles_by_video[video_id][article_url] = current

    prior = existing or {}
    items = []
    for video_id, article_map in sorted(articles_by_video.items()):
        item: dict[str, Any] = {
            "provider": "youtube",
            "video_id": video_id,
            "watch_url": f"https://www.youtube.com/watch?v={video_id}",
            "status": "pending_download",
            "import_directory": f"{media_root.rstrip('/')}/{video_id}",
            "articles": sorted(article_map.values(), key=lambda article: article["url"]),
        }
        old = prior.get(("youtube", video_id), {})
        for field in PRESERVED_ITEM_FIELDS:
            if field in old:
                item[field] = old[field]
        items.append(item)

    article_urls = {
        article["url"]
        for item in items
        for article in item["articles"]
    }
    status_counts: dict[str, int] = defaultdict(int)
    for item in items:
        status_counts[item["status"]] += 1
    return {
        "schema_version": 1,
        "generated_at_unix": generated_at_unix or int(time.time()),
        "source": source,
        "capture_runs": sorted(capture_runs),
        "media_import_contract": {
            "root_relative_to_source_archive": media_root,
            "per_video_directory": f"{media_root.rstrip('/')}/{{video_id}}",
            "article_links": "items[].articles",
            "note": (
                "The external downloader may choose filenames and containers. "
                "Record imported filenames in each item's imported_files field."
            ),
        },
        "summary": {
            "videos": len(items),
            "articles": len(article_urls),
            "statuses": dict(sorted(status_counts.items())),
        },
        "items": items,
    }


def write_youtube_inventory(
    capture_roots: list[Path],
    output: Path,
    *,
    source: str,
    media_root: str = "media/youtube",
    generated_at_unix: int | None = None,
) -> dict[str, Any]:
    data = build_youtube_inventory(
        capture_roots,
        source=source,
        media_root=media_root,
        generated_at_unix=generated_at_unix,
        existing=_existing_items(output),
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data
