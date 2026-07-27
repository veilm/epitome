"""Validated Codex-driven article summary orchestration."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
from typing import Any
from urllib.parse import urlsplit


VALID_STATUSES = {"complete", "error"}


def parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise ValueError("missing opening front-matter delimiter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing closing front-matter delimiter")
    metadata: dict[str, Any] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"invalid front-matter line: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_-]*", key):
            raise ValueError(f"invalid front-matter key: {key}")
        try:
            metadata[key] = json.loads(value)
        except json.JSONDecodeError:
            metadata[key] = value
    return metadata, text[end + 5 :].strip()


def validate_summary(text: str, source_url: str) -> tuple[dict[str, Any], str]:
    metadata, body = parse_front_matter(text)
    status = metadata.get("status")
    if status not in VALID_STATUSES:
        raise ValueError("status must be complete or error")
    confidence = metadata.get("confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
        raise ValueError("confidence must be numeric")
    if not 0 <= float(confidence) <= 1:
        raise ValueError("confidence must be between 0 and 1")
    if metadata.get("source_url") != source_url:
        raise ValueError("source_url does not match the requested article")
    if not isinstance(metadata.get("title"), str) or not metadata["title"].strip():
        raise ValueError("title must be a non-empty string")
    if not body:
        raise ValueError("summary body is empty")
    if status == "complete" and len(body) < 100:
        raise ValueError("complete summary body is suspiciously short")
    return metadata, body


def url_slug(url: str) -> str:
    parsed = urlsplit(url)
    raw = f"{parsed.netloc}{parsed.path}".strip("/") or parsed.netloc
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", raw).strip("-.").lower()
    return (slug or "article")[:160]


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def error_summary(
    source_url: str,
    title: str,
    reason: str,
    *,
    confidence: float = 1.0,
) -> str:
    return (
        "---\n"
        "status: error\n"
        f"confidence: {confidence:g}\n"
        f"title: {_yaml_string(title)}\n"
        f"source_url: {_yaml_string(source_url)}\n"
        "---\n\n"
        f"The summarization pipeline could not produce a valid summary: {reason}\n"
    )


def load_catalog(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError("summary catalog must be a JSON array")
    return value


def write_catalog(path: Path, entry: dict[str, Any]) -> None:
    entries = load_catalog(path)
    entries = [
        existing
        for existing in entries
        if existing.get("source_url") != entry["source_url"]
    ]
    entries.append(entry)
    entries.sort(key=lambda item: str(item.get("source_url", "")))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def summarize_article(
    input_path: Path,
    source_url: str,
    *,
    output_path: Path,
    catalog_path: Path,
    prompt_template_path: Path,
    model: str = "gpt-5.6-terra",
    reasoning_effort: str = "medium",
    timeout: float = 900,
    run_root: Path = Path("data/summary-runs"),
) -> dict[str, Any]:
    input_text = input_path.read_text(encoding="utf-8")
    input_metadata: dict[str, Any] = {}
    try:
        input_metadata, _ = parse_front_matter(input_text)
    except ValueError:
        pass
    fallback_title = str(input_metadata.get("title") or urlsplit(source_url).path)
    started_at = int(time.time())
    run_dir = run_root / f"{time.time_ns()}-{url_slug(source_url)}"
    run_dir.mkdir(parents=True)
    template = prompt_template_path.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="epitome-summary-") as temp:
        workspace = Path(temp)
        temporary_input = workspace / "input.md"
        temporary_output = workspace / "output.md"
        shutil.copyfile(input_path, temporary_input)
        prompt = template.format(
            input_path=temporary_input,
            output_path=temporary_output,
            source_url=source_url,
        )
        (run_dir / "prompt.txt").write_text(prompt, encoding="utf-8")
        shutil.copyfile(temporary_input, run_dir / "input.md")
        command = [
            "codex",
            "exec",
            "--ephemeral",
            "--skip-git-repo-check",
            "--ignore-user-config",
            "--ignore-rules",
            "--sandbox",
            "workspace-write",
            "--model",
            model,
            "--config",
            f'model_reasoning_effort="{reasoning_effort}"',
            "--config",
            'approval_policy="never"',
            "--cd",
            str(workspace),
            prompt,
        ]
        try:
            result = subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            stdout = result.stdout
            stderr = result.stderr
            returncode = result.returncode
        except subprocess.TimeoutExpired as error:
            stdout = error.stdout or ""
            stderr = error.stderr or ""
            returncode = 124
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        (run_dir / "codex.stdout").write_text(stdout, encoding="utf-8")
        (run_dir / "codex.stderr").write_text(stderr, encoding="utf-8")

        candidate = ""
        if temporary_output.exists():
            candidate = temporary_output.read_text(encoding="utf-8")
            (run_dir / "candidate.md").write_text(candidate, encoding="utf-8")
        try:
            if returncode:
                raise ValueError(f"Codex exited with status {returncode}")
            metadata, body = validate_summary(candidate, source_url)
        except (OSError, ValueError) as error:
            candidate = error_summary(source_url, fallback_title, str(error))
            metadata, body = validate_summary(candidate, source_url)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(candidate.rstrip() + "\n", encoding="utf-8")
    input_sha256 = hashlib.sha256(input_text.encode()).hexdigest()
    entry = {
        "confidence": float(metadata["confidence"]),
        "content_path": os.path.relpath(output_path, catalog_path.parent),
        "generated_at": int(time.time()),
        "input_characters": len(input_text),
        "input_sha256": input_sha256,
        "model": model,
        "reasoning_effort": reasoning_effort,
        "source_url": source_url,
        "status": metadata["status"],
        "title": metadata["title"],
    }
    write_catalog(catalog_path, entry)
    (run_dir / "run.json").write_text(
        json.dumps(
            {
                **entry,
                "codex_returncode": returncode,
                "duration_seconds": int(time.time()) - started_at,
                "output_path": str(output_path),
                "summary_characters": len(body),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return entry
