"""Incremental publication discovery and capture planning."""

from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import time
from typing import Any, Callable
from urllib.parse import urlsplit, urlunsplit
from xml.etree import ElementTree

from . import cdp
from .capture import archival_url_key, completed_capture_urls, validate_url


READ_LISTING = r"""(()=>({
  finalUrl: location.href,
  text: document.body?.innerText || new XMLSerializer().serializeToString(document),
  links: [...document.querySelectorAll("a[href]")].map(a => a.href),
}))()"""


def clean_url(url: object, *, drop_query: bool = True) -> str:
    """Return a stable HTTP identity suitable for discovery comparison."""
    if not isinstance(url, str):
        raise ValueError("discovered URL is not text")
    parsed = urlsplit(validate_url(url.strip()))
    return urlunsplit(
        (
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path or "/",
            "" if drop_query else parsed.query,
            "",
        )
    )


def parse_sitemap(text: str) -> tuple[list[str], list[str]]:
    """Parse sitemap XML copied from Chromium's rendered XML viewer."""
    start = text.find("<")
    if start < 0:
        raise ValueError("rendered page contains no sitemap XML")
    root = ElementTree.fromstring(text[start:])
    name = root.tag.rsplit("}", 1)[-1]
    locations = [
        (node.text or "").strip()
        for node in root.iter()
        if node.tag.rsplit("}", 1)[-1] == "loc" and (node.text or "").strip()
    ]
    if name == "sitemapindex":
        return locations, []
    if name == "urlset":
        return [], locations
    raise ValueError(f"unsupported sitemap root {name!r}")


def filter_urls(urls: list[str], rule: dict[str, Any]) -> list[str]:
    """Normalize, scope, filter, and deduplicate discovered URLs."""
    allowed_hosts = [str(value).lower() for value in rule.get("hosts", [])]
    include = re.compile(str(rule["include_path_regex"])) if rule.get("include_path_regex") else None
    exclude = re.compile(str(rule["exclude_path_regex"])) if rule.get("exclude_path_regex") else None
    result: list[str] = []
    seen: set[str] = set()
    for raw in urls:
        try:
            url = clean_url(raw, drop_query=bool(rule.get("drop_query", True)))
        except ValueError:
            continue
        parsed = urlsplit(url)
        host = (parsed.hostname or "").lower()
        if allowed_hosts and not any(
            host == allowed or host.endswith(f".{allowed}") for allowed in allowed_hosts
        ):
            continue
        canonical_host = rule.get("canonical_host")
        if canonical_host:
            parsed = parsed._replace(netloc=str(canonical_host))
            url = parsed.geturl()
        if include and not include.search(parsed.path):
            continue
        if exclude and exclude.search(parsed.path):
            continue
        identity = archival_url_key(url)
        if identity in seen:
            continue
        seen.add(identity)
        result.append(url)
    return result


def new_urls(discovered: list[str], completed: set[str]) -> list[str]:
    return [url for url in discovered if archival_url_key(url) not in completed]


def inventory_urls(path: object) -> set[str]:
    if not path:
        return set()
    values = []
    for line in Path(str(path)).read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            values.append(archival_url_key(validate_url(value)))
    return set(values)


class BrowserDiscovery:
    """Reuse one disposable Chromium tab for every configured listing."""

    def __init__(self, port: int, delay_seconds: float = 1) -> None:
        self.port = port
        self.delay_seconds = delay_seconds
        self.session = f"epitome-refresh-{int(time.time() * 1000)}-{os.getpid()}"
        self.connected = False

    def __enter__(self) -> BrowserDiscovery:
        cdp.run(
            ["connect", "--session", self.session, "--port", str(self.port),
             "--new", "--new-url", "about:blank"],
            timeout=15,
        )
        self.connected = True
        return self

    def __exit__(self, *_: object) -> None:
        if self.connected:
            cdp.close_session_tab(self.session)
            cdp.run(["disconnect", "--session", self.session], timeout=5, check=False)

    def load(self, url: str, *, scroll: bool = False) -> dict[str, Any]:
        cdp.eval_json(self.session, f"(location.href={json.dumps(url)},true)", timeout=10)
        cdp.run(["wait", "--session", self.session, "--timeout", "45s"], timeout=50)
        if scroll:
            cdp.scroll_to_stable_bottom(
                self.session, max_scrolls=80, max_seconds=45, delay_seconds=0.25
            )
        if self.delay_seconds:
            time.sleep(self.delay_seconds)
        value = cdp.eval_script(self.session, READ_LISTING, timeout=20)
        if not isinstance(value, dict):
            raise ValueError("listing evaluation returned no document")
        return value

    def discover(self, rule: dict[str, Any]) -> list[str]:
        kind = str(rule.get("type", "links"))
        listing_urls = [str(value) for value in rule.get("urls", [])]
        if not listing_urls:
            raise ValueError("discovery rule has no urls")
        if kind == "links":
            found: list[str] = []
            for url in listing_urls:
                found.extend(self.load(url, scroll=bool(rule.get("scroll")))["links"])
            return filter_urls(found, rule)
        if kind != "sitemap":
            raise ValueError(f"unsupported discovery type {kind!r}")

        queue = deque(listing_urls)
        seen_sitemaps: set[str] = set()
        found = []
        max_sitemaps = int(rule.get("max_sitemaps", 50))
        while queue:
            sitemap = queue.popleft()
            if sitemap in seen_sitemaps:
                continue
            if len(seen_sitemaps) >= max_sitemaps:
                raise ValueError(f"sitemap limit exceeded ({max_sitemaps})")
            seen_sitemaps.add(sitemap)
            try:
                children, urls = parse_sitemap(str(self.load(sitemap).get("text", "")))
            except (ValueError, ElementTree.ParseError) as error:
                raise ValueError(f"{sitemap}: {error}") from error
            queue.extend(children)
            found.extend(urls)
        return filter_urls(found, rule)


def build_plan(
    config: dict[str, Any],
    archive_root: Path,
    discover: Callable[[dict[str, Any]], list[str]],
    *,
    selected_sources: set[str] | None = None,
    max_new: int = 100,
) -> dict[str, Any]:
    records = []
    for source in config.get("sources", []):
        source_id = str(source["id"])
        if selected_sources and source_id not in selected_sources:
            continue
        if source.get("skip_reason"):
            records.append({
                "id": source_id,
                "status": "skipped",
                "reason": str(source["skip_reason"]),
                "new_urls": [],
            })
            continue
        try:
            discovered = discover(source["discovery"])
            completed = completed_capture_urls(
                [archive_root / str(source["archive_directory"])]
            )
            known = inventory_urls(source.get("inventory"))
            uncaptured = new_urls(discovered, completed)
            pending = [
                url for url in uncaptured
                if not known or archival_url_key(url) not in known
            ]
            known_uncaptured = [
                url for url in uncaptured if archival_url_key(url) in known
            ]
            status = "ready" if len(pending) <= max_new else "over_limit"
            records.append({
                "id": source_id,
                "archive_directory": str(source["archive_directory"]),
                "status": status,
                "discovered": len(discovered),
                "completed_identities": len(completed),
                "new_count": len(pending),
                "new_urls": pending,
                "known_uncaptured_count": len(known_uncaptured),
                "known_uncaptured_urls": known_uncaptured,
                "capture": source.get("capture", {}),
            })
        except (OSError, ValueError, cdp.CdpError, ElementTree.ParseError) as error:
            records.append({
                "id": source_id,
                "status": "error",
                "error": str(error),
                "new_urls": [],
            })
    return {
        "created_at": int(time.time()),
        "created_at_iso": datetime.now(timezone.utc).isoformat(),
        "archive_root": str(archive_root),
        "sources": records,
        "new_count": sum(int(record.get("new_count", 0)) for record in records),
    }


def write_plan(plan: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=False)
    (output_dir / "plan.json").write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    for record in plan["sources"]:
        urls = record.get("new_urls", [])
        if urls:
            (output_dir / f"{record['id']}.txt").write_text(
                "".join(f"{url}\n" for url in urls), encoding="utf-8"
            )


def capture_plan(plan: dict[str, Any], output_dir: Path, *, port: int) -> None:
    runner = Path(__file__).resolve().parent.parent / "capture_urls"
    for record in plan["sources"]:
        urls = record.get("new_urls", [])
        if not urls or record.get("status") != "ready":
            continue
        source_id = str(record["id"])
        source_root = Path(plan["archive_root"]) / str(record["archive_directory"])
        capture_root = source_root / "refresh" / str(plan["created_at"])
        settings = record.get("capture", {})
        command = [
            str(runner),
            "--url-file", str(output_dir / f"{source_id}.txt"),
            "--output-root", str(capture_root),
            "--existing-root", str(source_root),
            "--max-urls", str(len(urls)),
            "--port", str(port),
            "--max-scrolls", str(int(settings.get("max_scrolls", 60))),
            "--max-seconds", str(float(settings.get("max_seconds", 120))),
            "--settle-seconds", str(float(settings.get("settle_seconds", 5))),
            "--max-assets", str(int(settings.get("max_assets", 500))),
            "--asset-delay-seconds", str(float(settings.get("asset_delay_seconds", 2))),
            "--delay-seconds", str(float(settings.get("delay_seconds", 90))),
        ]
        subprocess.run(command, check=True)
