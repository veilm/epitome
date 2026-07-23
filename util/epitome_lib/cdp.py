"""Small, dependency-free wrapper around the workstation's cdp CLI."""

from __future__ import annotations

import json
import shutil
import subprocess
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

