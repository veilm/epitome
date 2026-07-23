"""Browser extraction orchestration and Markdown frontmatter helpers."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlsplit

from . import cdp
from .capture import url_slug
from .html_to_markdown import MarkdownRenderer, word_coverage


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
EXTRACTOR_PATH = REPOSITORY_ROOT / "research/extract_page.js"
RULES_PATH = REPOSITORY_ROOT / "research/site_rules.json"


def site_options(url: str, selector: str | None = None) -> dict[str, Any]:
    hostname = (urlsplit(url).hostname or "").lower()
    rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    options: dict[str, Any] = {
        "rootSelectors": [selector] if selector else [],
        "excludeSelectors": [],
        "excludeTextExact": [],
        "cutAtHeadings": [],
    }
    for site in rules.get("sites", []):
        suffix = site.get("host_suffix", "").lower()
        if hostname == suffix or hostname.endswith("." + suffix):
            if not selector:
                options["rootSelectors"].extend(site.get("root_selectors", []))
            options["excludeSelectors"].extend(site.get("exclude_selectors", []))
            options["excludeTextExact"].extend(site.get("exclude_text_exact", []))
            options["cutAtHeadings"].extend(site.get("cut_at_headings", []))
    return options


def extract_page(session: str, url: str, selector: str | None = None) -> dict[str, Any]:
    options = site_options(url, selector)
    source = EXTRACTOR_PATH.read_text(encoding="utf-8")
    source = source.replace("__EPITOME_OPTIONS__", json.dumps(options), 1)
    result = cdp.eval_script(session, source, timeout=45)
    if not isinstance(result, dict) or not result.get("contentHtml"):
        raise RuntimeError("browser extractor returned no content HTML")
    return result


def parse_timestamp(value: str) -> int | None:
    if not value:
        return None
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        parsed = None
        for date_format in ("%B %d, %Y", "%b %d, %Y"):
            try:
                parsed = datetime.strptime(normalized, date_format)
                break
            except ValueError:
                pass
        if parsed is None:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return int(parsed.timestamp())


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def frontmatter(extraction: dict[str, Any], captured_at: int) -> str:
    fields = [
        ("title", yaml_string(extraction.get("title", ""))),
        ("canonical_url", yaml_string(extraction.get("canonical", extraction.get("url", "")))),
        ("description", yaml_string(extraction.get("description", ""))),
        ("published_at", str(parse_timestamp(extraction.get("published", "")) or "null")),
        ("published_display", yaml_string(extraction.get("publishedDisplay", ""))),
        ("authors", json.dumps(extraction.get("authors", []), ensure_ascii=False)),
        ("language", yaml_string(extraction.get("language", ""))),
        ("captured_at", str(captured_at)),
        ("source_sha256", yaml_string(hashlib.sha256(extraction["contentHtml"].encode()).hexdigest())),
    ]
    return "---\n" + "\n".join(f"{key}: {value}" for key, value in fields) + "\n---\n\n"


def convert_extraction(extraction: dict[str, Any], captured_at: int) -> tuple[str, dict[str, Any]]:
    renderer = MarkdownRenderer(extraction.get("canonical") or extraction.get("url", ""))
    body = renderer.render(extraction["contentHtml"])
    markdown = frontmatter(extraction, captured_at) + body
    coverage = word_coverage(extraction.get("sourceText", ""), markdown)
    warnings = []
    if not extraction.get("title"):
        warnings.append("missing title")
    if len(body) < 200:
        warnings.append("body is unusually short")
    if coverage < 0.9:
        warnings.append(f"text coverage below 90% ({coverage:.1%})")
    missing_media = int(extraction.get("mediaWithoutSource", 0))
    document_characters = int(extraction.get("documentHtmlCharacters", 0))
    report = {
        "url": extraction.get("url"),
        "canonical_url": extraction.get("canonical"),
        "root_selector": extraction.get("rootSelector"),
        "source_text_characters": len(extraction.get("sourceText", "")),
        "markdown_characters": len(markdown),
        "document_html_characters": document_characters,
        "markdown_to_document_ratio": round(len(markdown) / document_characters, 6) if document_characters else None,
        "word_coverage": round(coverage, 6),
        "media_elements": int(extraction.get("mediaCount", 0)),
        "media_without_source": missing_media,
        "warnings": warnings,
    }
    return markdown, report


def default_markdown_path(url: str) -> Path:
    return Path("output/markdown") / f"{url_slug(url)}.md"


def default_artifact_dir(url: str, captured_at: int) -> Path:
    return Path("data/extractions") / f"{captured_at}-{url_slug(url)}"
