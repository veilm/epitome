"""Small, dependency-free wrapper around the workstation's cdp CLI."""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from typing import Any, Sequence


class CdpError(RuntimeError):
    """Raised when a cdp subprocess fails or returns malformed output."""


def executable() -> str:
    path = shutil.which("cdp")
    if not path:
        raise CdpError("cdp is not in PATH")
    return path


def run(
    args: Sequence[str],
    *,
    input_text: str | None = None,
    timeout: float = 30,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    command = [executable(), *args]
    try:
        result = subprocess.run(
            command,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise CdpError(f"cdp command timed out: {' '.join(command)}") from error
    if check and result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise CdpError(f"cdp command failed ({result.returncode}): {detail}")
    return result


def eval_json(session: str, expression: str, *, timeout: float = 30) -> Any:
    result = run(
        ["eval", "--session", session, "--timeout", f"{timeout}s", expression],
        timeout=timeout + 5,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise CdpError("cdp eval returned invalid JSON") from error


def eval_script(session: str, source: str, *, timeout: float = 30) -> Any:
    result = run(
        ["eval", "--session", session, "--timeout", f"{timeout}s", "--stdin"],
        input_text=source,
        timeout=timeout + 5,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise CdpError("cdp eval script returned invalid JSON") from error


def close_session_tab(session: str, *, timeout: float = 10) -> bool:
    """Close the exact browser target saved in a CDP session."""
    try:
        result = run(
            ["tabs", "close", "--session", session],
            timeout=timeout,
            check=False,
        )
    except CdpError:
        return False
    return result.returncode == 0


def scroll_to_stable_bottom(
    session: str,
    *,
    max_scrolls: int = 40,
    max_seconds: float = 60,
    delay_seconds: float = 0.2,
) -> dict[str, int | bool]:
    """Trigger lazy content until the document bottom and height are stable."""
    if max_scrolls < 0 or max_seconds <= 0 or delay_seconds < 0:
        raise ValueError("scroll limits must be non-negative and max_seconds positive")
    started = time.monotonic()
    previous_height = -1
    stable_height_count = 0
    scrolls = 0
    state: dict[str, Any] = {"height": 0, "bottom": False}
    while scrolls < max_scrolls and time.monotonic() - started < max_seconds:
        state = eval_json(
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
        if delay_seconds:
            time.sleep(delay_seconds)
    return {
        "bottom": bool(state.get("bottom")),
        "height": int(state.get("height", 0)),
        "scrolls": scrolls,
    }
