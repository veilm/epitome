"""Bounded, browser-driven URL capture using cdp network-log."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time
from typing import Any
from urllib.parse import urlsplit

from . import cdp


SENSITIVE_REQUEST_HEADERS = {
    "authorization",
    "cookie",
    "proxy-authorization",
    "x-api-key",
}
SENSITIVE_RESPONSE_HEADERS = {"set-cookie", "set-cookie2"}


def validate_url(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must be an absolute http:// or https:// URL")
    return url


def url_slug(url: str) -> str:
    parsed = urlsplit(url)
    raw = f"{parsed.netloc}{parsed.path}".strip("/") or parsed.netloc
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", raw).strip("-.").lower()
    return (slug or "page")[:100]


def default_capture_dir(url: str, root: Path = Path("data/captures")) -> Path:
    return root / f"{int(time.time())}-{url_slug(url)}"


def _write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _start_network_log(session: str, output_dir: Path) -> subprocess.Popen[str]:
    command = [
        cdp.executable(),
        "network-log",
        "--session",
        session,
        "--dir",
        str(output_dir / "network"),
    ]
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def _stop_network_log(process: subprocess.Popen[str]) -> tuple[str, str, int]:
    if process.poll() is None:
        process.send_signal(signal.SIGINT)
    try:
        stdout, stderr = process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
    return stdout, stderr, process.returncode or 0


def redact_capture_headers(network_dir: Path) -> int:
    """Redact browser credentials while retaining header names and structure."""
    changed = 0
    for filename, sensitive in (
        ("request-headers.json", SENSITIVE_REQUEST_HEADERS),
        ("response-headers.json", SENSITIVE_RESPONSE_HEADERS),
    ):
        for path in network_dir.glob(f"*/{filename}"):
            try:
                headers = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            dirty = False
            for name in list(headers):
                if name.lower() in sensitive and headers[name] != "[redacted]":
                    headers[name] = "[redacted]"
                    changed += 1
                    dirty = True
            if dirty:
                _write_json(path, headers)
    return changed


def summarize_network(network_dir: Path) -> dict[str, Any]:
    captures = 0
    response_bodies = 0
    response_bytes = 0
    body_errors = 0
    hosts: dict[str, int] = {}
    statuses: dict[str, int] = {}
    for metadata_path in network_dir.glob("*/metadata.json"):
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        captures += 1
        parsed = urlsplit(metadata.get("url", ""))
        if parsed.netloc:
            hosts[parsed.netloc] = hosts.get(parsed.netloc, 0) + 1
        status = str(metadata.get("status", "unknown"))
        statuses[status] = statuses.get(status, 0) + 1
        if metadata.get("responseBodyError"):
            body_errors += 1
        body_path = metadata_path.with_name("response-body.bin")
        if body_path.exists():
            response_bodies += 1
            response_bytes += body_path.stat().st_size
    return {
        "requests": captures,
        "response_bodies": response_bodies,
        "response_bytes": response_bytes,
        "response_body_errors": body_errors,
        "hosts": dict(sorted(hosts.items())),
        "statuses": dict(sorted(statuses.items())),
    }


def summarize_crawl(crawl_dir: Path) -> dict[str, Any]:
    """Aggregate per-page manifests from a capture_urls run."""
    pages_dir = crawl_dir / "pages"
    page_summaries = []
    hosts: dict[str, int] = {}
    statuses: dict[str, int] = {}
    total_requests = 0
    total_bodies = 0
    total_body_bytes = 0
    total_body_errors = 0
    total_redactions = 0
    complete_pages = 0
    html_pages = 0
    read_pages = 0

    for manifest_path in sorted(pages_dir.glob("*/manifest.json")):
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        page_dir = manifest_path.parent
        network = manifest.get("network_summary", {})
        complete = bool(manifest.get("complete"))
        complete_pages += int(complete)
        html_pages += int((page_dir / "page.html").exists())
        read_pages += int((page_dir / "read.json").exists())
        total_requests += int(network.get("requests", 0))
        total_bodies += int(network.get("response_bodies", 0))
        total_body_bytes += int(network.get("response_bytes", 0))
        total_body_errors += int(network.get("response_body_errors", 0))
        total_redactions += int(manifest.get("redacted_header_values", 0))
        for host, count in network.get("hosts", {}).items():
            hosts[host] = hosts.get(host, 0) + int(count)
        for status, count in network.get("statuses", {}).items():
            statuses[status] = statuses.get(status, 0) + int(count)
        page_summaries.append(
            {
                "url": manifest.get("requested_url"),
                "complete": complete,
                "requests": int(network.get("requests", 0)),
                "response_bytes": int(network.get("response_bytes", 0)),
                "response_body_errors": int(network.get("response_body_errors", 0)),
                "duration_seconds": max(
                    0,
                    int(manifest.get("capture_finished_at", 0))
                    - int(manifest.get("capture_started_at", 0)),
                ),
            }
        )

    disk_bytes = sum(
        path.stat().st_size
        for path in crawl_dir.rglob("*")
        if path.is_file()
    )
    return {
        "crawl_dir": str(crawl_dir),
        "pages": len(page_summaries),
        "complete_pages": complete_pages,
        "pages_with_html": html_pages,
        "pages_with_read_json": read_pages,
        "requests": total_requests,
        "response_bodies": total_bodies,
        "response_bytes": total_body_bytes,
        "response_body_errors": total_body_errors,
        "redacted_header_values": total_redactions,
        "disk_bytes": disk_bytes,
        "hosts": dict(sorted(hosts.items(), key=lambda item: (-item[1], item[0]))),
        "statuses": dict(sorted(statuses.items())),
        "page_summaries": page_summaries,
    }


def capture_url(
    url: str,
    output_dir: Path,
    *,
    port: int = 2103,
    max_scrolls: int = 40,
    max_seconds: float = 90,
    settle_seconds: float = 2,
    keep_tab: bool = False,
) -> dict[str, Any]:
    """Capture one URL and return its manifest.

    The logger is attached while the tab is still about:blank, ensuring that the
    main document and initial dependencies are observed.
    """
    validate_url(url)
    if max_scrolls < 0:
        raise ValueError("max_scrolls must be non-negative")
    if max_seconds <= 0:
        raise ValueError("max_seconds must be positive")

    output_dir.mkdir(parents=True, exist_ok=False)
    network_dir = output_dir / "network"
    network_dir.mkdir()
    started_at = time.time()
    session = f"epitome-{int(started_at * 1000)}-{os.getpid()}"
    logger: subprocess.Popen[str] | None = None
    logger_result = ("", "", 0)
    failure: BaseException | None = None

    cdp.run(
        [
            "connect",
            "--session",
            session,
            "--port",
            str(port),
            "--new",
            "--new-url",
            "about:blank",
        ],
        timeout=15,
    )
    try:
        logger = _start_network_log(session, output_dir)
        time.sleep(0.4)
        if logger.poll() is not None:
            stdout, stderr = logger.communicate()
            raise RuntimeError(
                "cdp network-log exited before navigation: "
                + (stderr.strip() or stdout.strip())
            )

        cdp.eval_json(
            session,
            f"(location.href={json.dumps(url)}, true)",
            timeout=10,
        )
        cdp.run(
            ["wait", "--session", session],
            timeout=min(max_seconds, 45),
        )
        time.sleep(max(0, settle_seconds))

        previous_height = -1
        stable_height_count = 0
        scrolls = 0
        while scrolls < max_scrolls and time.time() - started_at < max_seconds:
            state = cdp.eval_json(
                session,
                "(()=>{const h=document.documentElement.scrollHeight;"
                "window.scrollBy(0,Math.max(600,innerHeight*.8));"
                "return {y:scrollY,height:h,viewport:innerHeight," 
                "bottom:scrollY+innerHeight>=h-4}})()",
                timeout=10,
            )
            scrolls += 1
            height = int(state.get("height", 0))
            stable_height_count = stable_height_count + 1 if height == previous_height else 0
            previous_height = height
            if state.get("bottom") and stable_height_count >= 2:
                break
            time.sleep(0.2)

        page = cdp.eval_json(
            session,
            "({url:location.href,title:document.title,"
            "html:document.documentElement.outerHTML})",
            timeout=30,
        )
        (output_dir / "page.html").write_text(page["html"], encoding="utf-8")
        read_result = cdp.run(
            ["read", "--session", session, "--json", "--wait"],
            timeout=30,
        )
        (output_dir / "read.json").write_text(read_result.stdout, encoding="utf-8")
    except BaseException as error:
        failure = error
    finally:
        if logger is not None:
            logger_result = _stop_network_log(logger)
        redacted = redact_capture_headers(network_dir)
        summary = summarize_network(network_dir)
        manifest = {
            "capture_started_at": int(started_at),
            "capture_finished_at": int(time.time()),
            "requested_url": url,
            "session": session,
            "port": port,
            "limits": {
                "max_scrolls": max_scrolls,
                "max_seconds": max_seconds,
                "settle_seconds": settle_seconds,
            },
            "redacted_header_values": redacted,
            "network_log_returncode": logger_result[2],
            "network_summary": summary,
            "complete": failure is None,
        }
        if logger_result[1].strip():
            manifest["network_log_stderr"] = logger_result[1].strip()
        if failure is not None:
            manifest["error"] = f"{type(failure).__name__}: {failure}"
        _write_json(output_dir / "manifest.json", manifest)

        if not keep_tab:
            cdp.eval_json(session, "(window.close(), true)", timeout=5)
        cdp.run(["disconnect", "--session", session], timeout=5, check=False)

    if failure is not None:
        raise failure
    return manifest
