"""Discover and recover referenced assets missing from a browser capture."""

from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlsplit
from urllib.request import Request, urlopen


DOWNLOAD_EXTENSIONS = {
    ".avi", ".csv", ".doc", ".docx", ".epub", ".gif", ".gz", ".jpeg",
    ".jpg", ".json", ".m4a", ".mkv", ".mov", ".mp3", ".mp4", ".mpeg",
    ".ogg", ".ogv", ".pdf", ".png", ".ppt", ".pptx", ".svg", ".tar",
    ".tif", ".tiff", ".tsv", ".wav", ".webm", ".webp", ".xls", ".xlsx",
    ".xml", ".zip",
}
RESOURCE_ATTRIBUTES = {
    "audio": ("src",),
    "embed": ("src",),
    "iframe": ("src",),
    "img": ("src", "data-src"),
    "input": ("src",),
    "object": ("data",),
    "script": ("src",),
    "source": ("src",),
    "track": ("src",),
    "video": ("src", "poster"),
}
SRCSET_TAGS = {"img", "source"}
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
CONTENT_RANGE_RE = re.compile(r"bytes\s+(\d+)-(\d+)/(\d+|\*)", re.IGNORECASE)
VIMEO_CONFIG_MARKER = "window.playerConfig = "
ASSET_PRIORITIES = {
    ".avi": 0,
    ".m4a": 0,
    ".mkv": 0,
    ".mov": 0,
    ".mp3": 0,
    ".mp4": 0,
    ".mpeg": 0,
    ".ogg": 0,
    ".ogv": 0,
    ".wav": 0,
    ".webm": 0,
    ".pdf": 1,
    ".epub": 1,
    ".doc": 1,
    ".docx": 1,
    ".ppt": 1,
    ".pptx": 1,
    ".xls": 1,
    ".xlsx": 1,
    ".gif": 2,
    ".jpeg": 2,
    ".jpg": 2,
    ".png": 2,
    ".svg": 2,
    ".tif": 2,
    ".tiff": 2,
    ".webp": 2,
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _normalize_url(value: str, base_url: str) -> str | None:
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


class _ResourceParser(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.urls: set[str] = set()

    def _add(self, value: str) -> None:
        url = _normalize_url(value, self.base_url)
        if url:
            self.urls.add(url)

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        values = {name.lower(): value for name, value in attrs if value is not None}
        tag = tag.lower()
        if tag == "base" and "href" in values:
            resolved = _normalize_url(values["href"], self.base_url)
            if resolved:
                self.base_url = resolved
            return
        for attribute in RESOURCE_ATTRIBUTES.get(tag, ()):
            if attribute in values:
                self._add(values[attribute])
        if tag == "link" and "href" in values:
            rel = set(values.get("rel", "").lower().split())
            if rel & {
                "apple-touch-icon",
                "icon",
                "manifest",
                "modulepreload",
                "preload",
                "stylesheet",
            }:
                self._add(values["href"])
        if tag in SRCSET_TAGS and "srcset" in values:
            for candidate in values["srcset"].split(","):
                self._add(candidate.strip().split()[0])
        if tag == "a" and "href" in values:
            path = urlsplit(values["href"]).path.lower()
            if "download" in values or any(path.endswith(ext) for ext in DOWNLOAD_EXTENSIONS):
                self._add(values["href"])


def discover_html_assets(html: str, base_url: str) -> set[str]:
    parser = _ResourceParser(base_url)
    parser.feed(html)
    return parser.urls


def discover_css_assets(css: str, base_url: str) -> set[str]:
    result = set()
    for match in CSS_URL_RE.finditer(css):
        url = _normalize_url(match.group(2), base_url)
        if url:
            result.add(url)
    return result


def discover_vimeo_progressive_asset(html: str) -> str | None:
    """Return the highest-resolution progressive file from Vimeo player HTML."""
    marker = html.find(VIMEO_CONFIG_MARKER)
    if marker < 0:
        return None
    try:
        config, _ = json.JSONDecoder().raw_decode(
            html[marker + len(VIMEO_CONFIG_MARKER) :]
        )
        progressive = config["request"]["files"]["progressive"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    candidates = [
        item
        for item in progressive
        if isinstance(item, dict)
        and isinstance(item.get("url"), str)
        and item["url"].startswith(("http://", "https://"))
    ]
    if not candidates:
        return None
    selected = max(
        candidates,
        key=lambda item: (
            int(item.get("height") or 0),
            int(item.get("width") or 0),
            int(item.get("bitrate") or 0),
        ),
    )
    return str(selected["url"])


def discover_vimeo_video_asset(html: str) -> str | None:
    """Return Vimeo's best directly playable source or its HLS master."""
    if progressive := discover_vimeo_progressive_asset(html):
        return progressive
    marker = html.find(VIMEO_CONFIG_MARKER)
    if marker < 0:
        return None
    try:
        config, _ = json.JSONDecoder().raw_decode(
            html[marker + len(VIMEO_CONFIG_MARKER) :]
        )
        hls = config["request"]["files"]["hls"]
        cdn = hls["cdns"][hls["default_cdn"]]
    except (json.JSONDecodeError, KeyError, TypeError):
        return None
    for key in ("avc_url", "url"):
        value = cdn.get(key)
        if isinstance(value, str) and value.startswith(("http://", "https://")):
            return value
    return None


def _headers(record_dir: Path) -> dict[str, str]:
    path = record_dir / "response-headers.json"
    if not path.exists():
        return {}
    try:
        return {str(k).lower(): str(v) for k, v in _json(path).items()}
    except (OSError, json.JSONDecodeError, AttributeError):
        return {}


def complete_body(record_dir: Path, metadata: dict[str, Any]) -> bool:
    """Return whether a response record contains its full declared entity."""
    body = record_dir / "response-body.bin"
    if not body.exists():
        return False
    try:
        status = int(metadata.get("status", 0))
    except (TypeError, ValueError):
        return False
    if not 200 <= status < 300:
        return False
    size = body.stat().st_size
    headers = _headers(record_dir)
    content_length = headers.get("content-length")
    content_encoding = headers.get("content-encoding", "identity").lower()
    if (
        content_encoding in {"", "identity"}
        and content_length
        and content_length.isdigit()
        and size != int(content_length)
    ):
        return False
    if status == 206:
        match = CONTENT_RANGE_RE.fullmatch(headers.get("content-range", "").strip())
        if not match or match.group(3) == "*":
            return False
        start, end, total = map(int, match.groups())
        return start == 0 and end + 1 == total and size == total
    return True


def captured_complete_urls(network_dir: Path) -> set[str]:
    result = set()
    for metadata_path in network_dir.glob("*/metadata.json"):
        try:
            metadata = _json(metadata_path)
        except (OSError, json.JSONDecodeError):
            continue
        if complete_body(metadata_path.parent, metadata):
            url = metadata.get("url")
            if isinstance(url, str):
                result.add(url)
            final_url = metadata.get("finalUrl")
            if isinstance(final_url, str):
                result.add(final_url)
    return result


def discover_capture_assets(page_html: Path, network_dir: Path, page_url: str) -> set[str]:
    urls = discover_html_assets(page_html.read_text(encoding="utf-8"), page_url)
    for metadata_path in network_dir.glob("*/metadata.json"):
        body_path = metadata_path.with_name("response-body.bin")
        if not body_path.exists():
            continue
        try:
            metadata = _json(metadata_path)
        except (OSError, json.JSONDecodeError):
            continue
        try:
            body = body_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        content_type = str(metadata.get("contentType", "")).lower()
        resource_url = str(metadata.get("url", page_url))
        if "css" in content_type:
            urls.update(discover_css_assets(body, resource_url))
        elif (
            "html" in content_type
            and urlsplit(resource_url).hostname == "player.vimeo.com"
        ):
            if video_url := discover_vimeo_video_asset(body):
                urls.add(video_url)
    return urls


def _record_name(url: str) -> str:
    parsed = urlsplit(url)
    raw = f"{parsed.netloc}{parsed.path}".strip("/") or parsed.netloc
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", raw).strip("-.").lower()
    return f"{time.time_ns()}-GET-{(slug or 'asset')[:140]}"


def asset_priority(url: str) -> tuple[int, str]:
    """Put audiovisual and document resources before incidental dependencies."""
    parsed = urlsplit(url)
    path = parsed.path.lower()
    if parsed.hostname == "player.vimeo.com" or path.endswith(".m3u8"):
        return 0, url
    priority = next(
        (value for extension, value in ASSET_PRIORITIES.items() if path.endswith(extension)),
        3,
    )
    return priority, url


def _download_asset(
    url: str,
    network_dir: Path,
    *,
    remaining_bytes: int,
    timeout: float,
) -> dict[str, Any]:
    parsed = urlsplit(url)
    if (
        parsed.path.lower().endswith(".m3u8")
        and parsed.hostname
        and parsed.hostname.endswith(".vimeocdn.com")
    ):
        return _download_hls_asset(
            url,
            network_dir,
            remaining_bytes=remaining_bytes,
            timeout=timeout,
        )

    record_dir = network_dir / _record_name(url)
    record_dir.mkdir()
    metadata: dict[str, Any] = {
        "method": "GET",
        "source": "asset-completion",
        "timestamp": int(time.time()),
        "url": url,
    }
    request_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "identity",
        "User-Agent": "Epitome archival research capture/0.1",
    }
    _write_json(record_dir / "request-headers.json", request_headers)
    temporary_body = record_dir / "response-body.partial"
    try:
        request = Request(url, headers=request_headers)
        with urlopen(request, timeout=timeout) as response:
            response_headers = {name.lower(): value for name, value in response.headers.items()}
            metadata.update(
                {
                    "contentType": response_headers.get("content-type", ""),
                    "finalUrl": response.url,
                    "status": str(response.status),
                }
            )
            _write_json(record_dir / "response-headers.json", response_headers)
            declared = response_headers.get("content-length", "")
            if declared.isdigit() and int(declared) > remaining_bytes:
                raise ValueError(
                    f"declared body is {declared} bytes; "
                    f"{remaining_bytes} bytes remain in the completion budget"
                )
            digest = hashlib.sha256()
            size = 0
            with temporary_body.open("wb") as stream:
                while chunk := response.read(1024 * 1024):
                    size += len(chunk)
                    if size > remaining_bytes:
                        raise ValueError(
                            f"body exceeded the remaining {remaining_bytes}-byte budget"
                        )
                    stream.write(chunk)
                    digest.update(chunk)
            temporary_body.replace(record_dir / "response-body.bin")
            metadata["responseBytes"] = size
            metadata["sha256"] = digest.hexdigest()
            if not complete_body(record_dir, metadata):
                raise ValueError("downloaded response is not a complete declared entity")
    except (HTTPError, URLError, OSError, ValueError) as error:
        temporary_body.unlink(missing_ok=True)
        (record_dir / "response-body.bin").unlink(missing_ok=True)
        if isinstance(error, HTTPError):
            metadata["status"] = str(error.code)
        metadata["responseBodyError"] = f"{type(error).__name__}: {error}"
        metadata["responseBytes"] = 0
    _write_json(record_dir / "metadata.json", metadata)
    return {
        "bytes": int(metadata.get("responseBytes", 0)),
        "complete": "responseBodyError" not in metadata,
        "error": metadata.get("responseBodyError"),
        "record": record_dir.name,
        "url": url,
    }


def _download_hls_asset(
    url: str,
    network_dir: Path,
    *,
    remaining_bytes: int,
    timeout: float,
) -> dict[str, Any]:
    """Losslessly remux a Vimeo HLS presentation into one archival MP4."""
    record_dir = network_dir / _record_name(url)
    record_dir.mkdir()
    metadata: dict[str, Any] = {
        "method": "GET",
        "source": "asset-completion-hls-remux",
        "timestamp": int(time.time()),
        "transform": "ffmpeg stream copy from adaptive HLS to MP4",
        "url": url,
    }
    request_headers = {
        "Accept": "*/*",
        "User-Agent": "Epitome archival research capture/0.1",
    }
    _write_json(record_dir / "request-headers.json", request_headers)
    temporary_body = record_dir / "response-body.partial"
    try:
        command = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "fatal",
            "-nostdin",
            "-y",
            "-i",
            url,
            "-map",
            "0:v:0",
            "-map",
            "0:a:0?",
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            "-f",
            "mp4",
            str(temporary_body),
        ]
        process = subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        deadline = time.monotonic() + timeout
        while process.poll() is None:
            if (
                temporary_body.exists()
                and temporary_body.stat().st_size > remaining_bytes
            ):
                process.kill()
                process.communicate()
                raise ValueError(
                    f"remuxed body exceeded the remaining "
                    f"{remaining_bytes}-byte budget"
                )
            if time.monotonic() >= deadline:
                process.kill()
                process.communicate()
                raise subprocess.TimeoutExpired(command, timeout)
            time.sleep(0.1)
        _, stderr = process.communicate()
        if process.returncode:
            detail = stderr.strip().splitlines()
            raise ValueError(detail[-1] if detail else "ffmpeg failed")
        size = temporary_body.stat().st_size
        if size > remaining_bytes:
            raise ValueError(
                f"remuxed body is {size} bytes; "
                f"{remaining_bytes} bytes remain in the completion budget"
            )
        digest = hashlib.sha256()
        with temporary_body.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
        temporary_body.replace(record_dir / "response-body.bin")
        metadata.update(
            {
                "contentType": "video/mp4",
                "finalUrl": url,
                "responseBytes": size,
                "sha256": digest.hexdigest(),
                "status": "200",
            }
        )
        _write_json(
            record_dir / "response-headers.json",
            {
                "content-length": str(size),
                "content-type": "video/mp4",
                "x-epitome-derived-from": "adaptive HLS",
            },
        )
    except (
        OSError,
        subprocess.SubprocessError,
        ValueError,
    ) as error:
        temporary_body.unlink(missing_ok=True)
        (record_dir / "response-body.bin").unlink(missing_ok=True)
        metadata["responseBodyError"] = f"{type(error).__name__}: {error}"
        metadata["responseBytes"] = 0
    _write_json(record_dir / "metadata.json", metadata)
    return {
        "bytes": int(metadata.get("responseBytes", 0)),
        "complete": "responseBodyError" not in metadata,
        "error": metadata.get("responseBodyError"),
        "record": record_dir.name,
        "url": url,
    }


def complete_capture_assets(
    page_html: Path,
    network_dir: Path,
    page_url: str,
    *,
    max_assets: int = 50,
    max_bytes: int = 500 * 1024 * 1024,
    delay_seconds: float = 2,
    timeout: float = 90,
) -> dict[str, Any]:
    """Recover referenced assets whose complete bodies are absent."""
    if max_assets < 0 or max_bytes < 0 or delay_seconds < 0 or timeout <= 0:
        raise ValueError("asset completion limits must be non-negative and timeout positive")
    discovered = discover_capture_assets(page_html, network_dir, page_url)
    already_complete = captured_complete_urls(network_dir)
    pending = set(discovered - already_complete)
    attempted_urls: set[str] = set()
    results = []
    downloaded_bytes = 0
    while (
        pending
        and len(results) < max_assets
        and downloaded_bytes < max_bytes
    ):
        url = min(pending, key=asset_priority)
        pending.remove(url)
        if results and delay_seconds:
            time.sleep(delay_seconds)
        result = _download_asset(
            url,
            network_dir,
            remaining_bytes=max_bytes - downloaded_bytes,
            timeout=timeout,
        )
        results.append(result)
        attempted_urls.add(url)
        downloaded_bytes += result["bytes"]
        if result["complete"] and urlsplit(url).hostname == "player.vimeo.com":
            body_path = network_dir / result["record"] / "response-body.bin"
            try:
                player_html = body_path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )
            except OSError:
                continue
            video_url = discover_vimeo_video_asset(player_html)
            if video_url:
                discovered.add(video_url)
                if (
                    video_url not in already_complete
                    and video_url not in attempted_urls
                ):
                    pending.add(video_url)
    return {
        "already_complete": len(discovered & already_complete),
        "attempted": len(results),
        "completed": sum(item["complete"] for item in results),
        "discovered": len(discovered),
        "downloaded_bytes": downloaded_bytes,
        "failed": sum(not item["complete"] for item in results),
        "limits": {
            "delay_seconds": delay_seconds,
            "max_assets": max_assets,
            "max_bytes": max_bytes,
            "timeout": timeout,
        },
        "results": results,
        "skipped": sorted(
            discovered - already_complete - attempted_urls,
            key=asset_priority,
        ),
    }
