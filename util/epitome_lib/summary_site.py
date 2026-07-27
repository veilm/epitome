"""Generate a dependency-free static browser for tracked article summaries."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from .summary import parse_front_matter, url_slug, validate_summary


LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
CODE_RE = re.compile(r"`([^`\n]+)`")
BOLD_RE = re.compile(r"\*\*([^*\n]+)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")


def inline_markdown(text: str) -> str:
    output = []
    position = 0
    for match in LINK_RE.finditer(text):
        output.append(escape(text[position : match.start()]))
        label, url = match.groups()
        parsed = urlsplit(url)
        if parsed.scheme in {"http", "https"}:
            output.append(
                f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'
            )
        else:
            output.append(escape(match.group(0)))
        position = match.end()
    output.append(escape(text[position:]))
    rendered = "".join(output)
    rendered = CODE_RE.sub(r"<code>\1</code>", rendered)
    rendered = BOLD_RE.sub(r"<strong>\1</strong>", rendered)
    return ITALIC_RE.sub(r"<em>\1</em>", rendered)


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    list_tag: str | None = None
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            output.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")
            paragraph.clear()

    def close_list() -> None:
        nonlocal list_tag
        if list_tag:
            output.append(f"</{list_tag}>")
            list_tag = None

    for line in lines:
        if line.startswith("```"):
            flush_paragraph()
            close_list()
            if in_code:
                output.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
                code_lines.clear()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            flush_paragraph()
            close_list()
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            output.append(
                f"<h{level}>{inline_markdown(heading.group(2))}</h{level}>"
            )
            continue
        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        numbered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if bullet or numbered:
            flush_paragraph()
            wanted = "ul" if bullet else "ol"
            if list_tag != wanted:
                close_list()
                list_tag = wanted
                output.append(f"<{wanted}>")
            output.append(
                f"<li>{inline_markdown((bullet or numbered).group(1))}</li>"
            )
            continue
        if line.startswith("> "):
            flush_paragraph()
            close_list()
            output.append(f"<blockquote>{inline_markdown(line[2:])}</blockquote>")
            continue
        paragraph.append(line.strip())

    if in_code:
        output.append(f"<pre><code>{escape(chr(10).join(code_lines))}</code></pre>")
    flush_paragraph()
    close_list()
    return "\n".join(output)


STYLE = """
:root{color-scheme:light;--muted:#666;--line:#ddd;--good:#28633f;--bad:#9b2c2c}
*{box-sizing:border-box}
body{font:16px/1.55 system-ui,sans-serif;margin:3rem auto;max-width:70rem;
padding:0 1.5rem;color:#171717;background:#fff}
a{color:#145a8d;text-underline-offset:.15em}
h1{font-size:2rem;margin:0 0 .75rem}h2{font-size:1.1rem;margin:0 0 .25rem}
h3{font-size:1rem}.intro{max-width:48rem;margin:.5rem 0;color:var(--muted)}
.stats{display:flex;gap:1.25rem;margin:1rem 0 2rem;color:var(--muted);font-size:.875rem}
.summary-list{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.summary-list li{padding:1rem 0;border-bottom:1px solid var(--line)}
.record-meta,.source{display:block;color:var(--muted);font-size:.8rem}
.source{margin-top:.15rem;overflow-wrap:anywhere}.status{font-weight:600}
.complete{color:var(--good)}.error{color:var(--bad)}
.article{max-width:48rem;margin:0 auto}.article nav{margin-bottom:2.5rem;font-size:.875rem}
.article>h1{margin-top:.65rem}.meta{display:flex;flex-wrap:wrap;gap:.4rem 1.25rem;
padding:0 0 1.25rem;border-bottom:1px solid var(--line);color:var(--muted);
font-size:.8rem}.content{padding-top:1rem}.content h2{font-size:1.35rem;margin-top:2.25rem}
.content h3{font-size:1.1rem;margin-top:1.75rem}.content p{margin:1rem 0}
.content blockquote{border-left:2px solid #aaa;margin:1.5rem 0;padding-left:1rem;color:#444}
code,pre{font-family:ui-monospace,monospace}pre{overflow:auto;background:#f4f4f4;padding:1rem}
@media(max-width:600px){body{margin-top:2rem}.stats{gap:.75rem;flex-wrap:wrap}}
"""


def _page(title: str, body: str) -> str:
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — Epitome</title><link rel="stylesheet" href="/style.css">
</head><body>{body}</body></html>"""


def _summary_path(catalog_path: Path, content_path: str) -> Path:
    root = catalog_path.parent.resolve()
    path = (catalog_path.parent / content_path).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"summary path escapes catalog directory: {content_path}")
    return path


def build_summary_site(catalog_path: Path, output_dir: Path) -> dict[str, int]:
    entries = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError("summary catalog must be a JSON array")
    output_dir.mkdir(parents=True, exist_ok=True)
    article_dir = output_dir / "articles"
    article_dir.mkdir(exist_ok=True)
    for stale in article_dir.glob("*.html"):
        stale.unlink()
    (output_dir / "style.css").write_text(STYLE.strip() + "\n", encoding="utf-8")

    cards = []
    complete_count = 0
    error_count = 0
    for entry in entries:
        source_url = str(entry["source_url"])
        summary_path = _summary_path(catalog_path, str(entry["content_path"]))
        metadata, body = validate_summary(
            summary_path.read_text(encoding="utf-8"),
            source_url,
        )
        status = metadata["status"]
        complete_count += int(status == "complete")
        error_count += int(status == "error")
        slug = url_slug(source_url)
        article_name = f"{slug}.html"
        confidence = float(metadata["confidence"])
        article_body = f"""
<main class="article"><nav><a href="/">← All summaries</a></nav>
<span class="status {status}">{escape(status)}</span>
<h1>{escape(str(metadata["title"]))}</h1>
<div class="meta"><span>{confidence:.0%} status confidence</span>
<span>{escape(str(entry.get("model", "unknown model")))}</span>
<a href="{escape(source_url, quote=True)}">Original OpenAI article ↗</a></div>
<article class="content">{markdown_to_html(body)}</article></main>"""
        (article_dir / article_name).write_text(
            _page(str(metadata["title"]), article_body),
            encoding="utf-8",
        )
        cards.append(
            f"""<li><h2><a href="articles/{article_name}">{
                escape(str(metadata["title"]))
            }</a></h2>
<span class="record-meta"><span class="status {status}">{status}</span>
 · {confidence:.0%} status confidence · {
                escape(str(entry.get("model", "unknown model")))
            }</span>
<small class="source">{escape(source_url)}</small></li>"""
        )
    index_body = f"""
<header><h1>Article summaries</h1><p class="intro">Compact, model-readable records of
OpenAI’s published articles, with extraction failures kept visible instead of
silently summarized.</p><div class="stats"><span>{len(entries)} records</span>
<span>{complete_count} complete</span><span>{error_count} need attention</span>
</div></header><main><ul class="summary-list">
{''.join(cards)}</ul></main>"""
    (output_dir / "index.html").write_text(
        _page("Article summaries", index_body),
        encoding="utf-8",
    )
    return {
        "articles": len(entries),
        "complete": complete_count,
        "errors": error_count,
    }
