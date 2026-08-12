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
from .assets import complete_capture_assets


SENSITIVE_REQUEST_HEADERS = {
    "authorization",
    "cookie",
    "proxy-authorization",
    "x-api-key",
}
SENSITIVE_RESPONSE_HEADERS = {"set-cookie", "set-cookie2"}


def validate_url(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise ValueError("URL must be an absolute http:// or https:// URL")
    return url


def url_slug(url: str) -> str:
    parsed = urlsplit(url)
    raw = f"{parsed.netloc}{parsed.path}".strip("/") or parsed.netloc
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", raw).strip("-.").lower()
    return (slug or "page")[:100]


def default_capture_dir(url: str, root: Path = Path("data/captures")) -> Path:
    return root / f"{int(time.time())}-{url_slug(url)}"


def archival_url_key(url: str) -> str:
    """Normalize harmless URL spelling differences for capture deduplication."""
    parsed = urlsplit(validate_url(url))
    path = parsed.path.rstrip("/") or "/"
    return parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower(),
        path=path,
        fragment="",
    ).geturl()


def completed_capture_urls(roots: list[Path]) -> set[str]:
    """Return normalized page URLs backed by complete manifests and HTML."""
    result: set[str] = set()
    for root in roots:
        if not root.exists():
            continue
        manifest_paths = (
            Path(directory) / "manifest.json"
            for directory, _, filenames in os.walk(root, followlinks=True)
            if "manifest.json" in filenames
        )
        for manifest_path in manifest_paths:
            if not manifest_path.with_name("page.html").exists():
                continue
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if not manifest.get("complete"):
                continue
            for field in ("requested_url", "final_url"):
                value = manifest.get(field)
                if not isinstance(value, str):
                    continue
                try:
                    result.add(archival_url_key(value))
                except ValueError:
                    continue
    return result


def recommended_page_delay(url_count: int) -> float:
    """Scale the default inter-page pause as a bounded batch grows."""
    if url_count <= 10:
        return 10
    if url_count <= 20:
        return 15
    if url_count <= 40:
        return 20
    if url_count <= 80:
        return 30
    return 45


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
    asset_attempts = 0
    assets_completed = 0
    asset_failures = 0

    for manifest_path in sorted(pages_dir.glob("*/manifest.json")):
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        page_dir = manifest_path.parent
        network = manifest.get("network_summary", {})
        asset_completion = manifest.get("asset_completion", {})
        complete = bool(manifest.get("complete"))
        complete_pages += int(complete)
        html_pages += int((page_dir / "page.html").exists())
        read_pages += int((page_dir / "read.json").exists())
        total_requests += int(network.get("requests", 0))
        total_bodies += int(network.get("response_bodies", 0))
        total_body_bytes += int(network.get("response_bytes", 0))
        total_body_errors += int(network.get("response_body_errors", 0))
        total_redactions += int(manifest.get("redacted_header_values", 0))
        asset_attempts += int(asset_completion.get("attempted", 0))
        assets_completed += int(asset_completion.get("completed", 0))
        asset_failures += int(asset_completion.get("failed", 0))
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
                "asset_attempts": int(asset_completion.get("attempted", 0)),
                "assets_completed": int(asset_completion.get("completed", 0)),
                "asset_failures": int(asset_completion.get("failed", 0)),
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
        "asset_attempts": asset_attempts,
        "assets_completed": assets_completed,
        "asset_failures": asset_failures,
        "disk_bytes": disk_bytes,
        "hosts": dict(sorted(hosts.items(), key=lambda item: (-item[1], item[0]))),
        "statuses": dict(sorted(statuses.items())),
        "page_summaries": page_summaries,
    }


def activate_vimeo_embeds(
    session: str,
    *,
    delay_seconds: float = 2,
) -> dict[str, Any]:
    """Hydrate script-deferred Vimeo iframes while the network logger is live.

    Video components can leave iframe ``src`` blank, or leave only an empty
    placeholder, until interaction. React Flight data and Vimeo oEmbed requests
    still expose the URLs. Recover those URLs and assign them to the rendered
    media slots while the network logger is live.
    """
    result = cdp.eval_script(
        session,
        r"""(()=>{
const frames=[...document.querySelectorAll('iframe[title*="Vimeo" i]')];
const placeholders=[...document.querySelectorAll('[class*="e-videoEmbed"]')]
 .filter(node=>!node.querySelector('iframe,video'));
const chunks=[];
for(const script of document.scripts){
 const match=(script.textContent||"").match(/^self\.__next_f\.push\((.*)\)$/s);
 if(!match)continue;
 try{
  const item=JSON.parse(match[1]);
  if(typeof item?.[1]==="string")chunks.push(item[1]);
 }catch{}
}
const flight=chunks.join("");
const flightUrls=[...flight.matchAll(
 /"videoEmbedUrl":"(https:\/\/player\.vimeo\.com\/video\/.*?)"/g
)].map(match=>match[1].replaceAll("&amp;","&"));
const oembedUrls=performance.getEntriesByType("resource")
 .map(entry=>{
  try{
   const url=new URL(entry.name);
   if(url.hostname!=="vimeo.com"||!url.pathname.includes("/api/oembed"))return "";
   const embedded=url.searchParams.get("url")||"";
   return embedded.startsWith("https://player.vimeo.com/video/")?embedded:"";
  }catch{return "";}
 }).filter(Boolean);
const urls=[...new Set([...oembedUrls,...flightUrls])];
const slots=[...frames];
for(const placeholder of placeholders){
 const frame=document.createElement("iframe");
 frame.title="Video on Vimeo";
 frame.style.cssText="width:100%;height:100%;border:0";
 frame.allow="autoplay; fullscreen; picture-in-picture";
 placeholder.replaceChildren(frame);
 slots.push(frame);
}
const results=slots.map((frame,index)=>{
 const embeddedUrl=urls[index]||"";
 const hadSrc=Boolean(frame.getAttribute("src"));
 if(!hadSrc&&embeddedUrl)frame.src=embeddedUrl;
 return {
  embedded_url:embeddedUrl,
  hydrated:Boolean(!hadSrc&&embeddedUrl),
  src:frame.src,
  title:frame.title,
 };
});
return {discovered:slots.length,embedded_urls:urls.length,results};
})()""",
        timeout=10,
    )
    if delay_seconds and any(item.get("src") for item in result["results"]):
        time.sleep(delay_seconds)
    return {
        **result,
        "activated": sum(bool(item.get("src")) for item in result["results"]),
    }


def wait_for_document(session: str, *, max_seconds: float) -> dict[str, Any]:
    """Wait for navigation, tolerating dead subresources after DOM readiness.

    Old pages can remain at ``interactive`` forever when an image host has
    disappeared.  After the bounded full-load wait expires, accept a real,
    substantially parsed HTTP document so the later asset audit can record the
    broken dependency instead of discarding the entire page.
    """
    timeout = min(max_seconds, 45)
    try:
        cdp.run(
            ["wait", "--session", session, "--timeout", f"{timeout:g}s"],
            timeout=timeout + 5,
        )
        return {"state": "complete", "timed_out": False}
    except cdp.CdpError:
        state = cdp.eval_json(
            session,
            "({readyState:document.readyState,url:location.href,"
            "htmlLength:document.documentElement?.outerHTML.length||0})",
            timeout=10,
        )
        if (
            state.get("readyState") in {"interactive", "complete"}
            and str(state.get("url", "")).startswith(("http://", "https://"))
            and int(state.get("htmlLength", 0)) >= 512
        ):
            return {
                "state": state["readyState"],
                "timed_out": True,
                "html_length_at_timeout": int(state["htmlLength"]),
            }
        raise


def read_document(session: str) -> subprocess.CompletedProcess[str]:
    """Read the settled DOM without imposing a second full-load wait.

    ``wait_for_document`` has already applied the bounded readiness policy.
    Asking ``cdp read --wait`` again makes historical pages with dead
    subresources fail after their complete DOM has already been saved.
    """
    return cdp.run(["read", "--session", session, "--json"], timeout=30)


def capture_url(
    url: str,
    output_dir: Path,
    *,
    port: int = 2103,
    max_scrolls: int = 40,
    max_seconds: float = 90,
    settle_seconds: float = 2,
    keep_tab: bool = False,
    complete_assets: bool = True,
    max_assets: int = 50,
    max_asset_bytes: int = 500 * 1024 * 1024,
    asset_delay_seconds: float = 2,
    asset_timeout: float = 90,
    exclude_asset_hosts: set[str] | None = None,
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
    asset_completion: dict[str, Any] | None = None
    document_wait: dict[str, Any] | None = None
    final_page_url = url

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
        document_wait = wait_for_document(session, max_seconds=max_seconds)
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

        interactive_media = activate_vimeo_embeds(session)
        _write_json(output_dir / "interactive-media.json", interactive_media)
        page = cdp.eval_json(
            session,
            "({url:location.href,title:document.title,"
            "html:document.documentElement.outerHTML})",
            timeout=30,
        )
        final_page_url = page["url"]
        (output_dir / "page.html").write_text(page["html"], encoding="utf-8")
        read_result = read_document(session)
        (output_dir / "read.json").write_text(read_result.stdout, encoding="utf-8")
    except BaseException as error:
        failure = error
    finally:
        if logger is not None:
            logger_result = _stop_network_log(logger)
        if complete_assets and (output_dir / "page.html").exists():
            try:
                asset_completion = complete_capture_assets(
                    output_dir / "page.html",
                    network_dir,
                    final_page_url,
                    max_assets=max_assets,
                    max_bytes=max_asset_bytes,
                    delay_seconds=asset_delay_seconds,
                    timeout=asset_timeout,
                    exclude_hosts=exclude_asset_hosts,
                )
            except (OSError, ValueError) as error:
                asset_completion = {
                    "attempted": 0,
                    "completed": 0,
                    "failed": 1,
                    "error": f"{type(error).__name__}: {error}",
                }
            _write_json(output_dir / "asset-completion.json", asset_completion)
        redacted = redact_capture_headers(network_dir)
        summary = summarize_network(network_dir)
        manifest = {
            "capture_started_at": int(started_at),
            "capture_finished_at": int(time.time()),
            "requested_url": url,
            "final_url": final_page_url,
            "session": session,
            "port": port,
            "limits": {
                "max_scrolls": max_scrolls,
                "max_seconds": max_seconds,
                "settle_seconds": settle_seconds,
                "complete_assets": complete_assets,
                "max_assets": max_assets,
                "max_asset_bytes": max_asset_bytes,
                "asset_delay_seconds": asset_delay_seconds,
                "asset_timeout": asset_timeout,
                "exclude_asset_hosts": sorted(exclude_asset_hosts or set()),
            },
            "redacted_header_values": redacted,
            "network_log_returncode": logger_result[2],
            "network_summary": summary,
            "complete": failure is None,
        }
        if document_wait is not None:
            manifest["document_wait"] = document_wait
        if (interactive_path := output_dir / "interactive-media.json").exists():
            manifest["interactive_media"] = json.loads(
                interactive_path.read_text(encoding="utf-8")
            )
        if asset_completion is not None:
            manifest["asset_completion"] = {
                key: asset_completion.get(key)
                for key in (
                    "discovered",
                    "already_complete",
                    "attempted",
                    "completed",
                    "failed",
                    "excluded",
                    "downloaded_bytes",
                    "error",
                )
                if key in asset_completion
            }
        if logger_result[1].strip():
            manifest["network_log_stderr"] = logger_result[1].strip()
        if failure is not None:
            manifest["error"] = f"{type(failure).__name__}: {failure}"

        if not keep_tab:
            manifest["tab_closed"] = cdp.close_session_tab(session)
        else:
            manifest["tab_closed"] = False
            manifest["tab_kept"] = True
        cdp.run(["disconnect", "--session", session], timeout=5, check=False)
        _write_json(output_dir / "manifest.json", manifest)

    if failure is not None:
        raise failure
    return manifest
