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
:root{color-scheme:light;--paper:#f5f1e8;--ink:#171714;--muted:#69675f;
--line:#d8d1c4;--accent:#235c4b;--good:#276749;--bad:#9b2c2c}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);
font:17px/1.68 Georgia,serif}a{color:var(--accent);text-underline-offset:.18em}
.shell{width:min(74rem,calc(100% - 2rem));margin:auto}.masthead{padding:4rem 0 2rem;
border-bottom:1px solid var(--line)}.eyebrow{font:700 .72rem/1.2 system-ui;
letter-spacing:.16em;text-transform:uppercase;color:var(--accent)}
h1,h2,h3{font-family:system-ui,sans-serif;line-height:1.08;letter-spacing:-.035em}
h1{font-size:clamp(2.5rem,7vw,5.8rem);margin:.3rem 0 1rem;max-width:14ch}
.intro{max-width:43rem;color:var(--muted);font-size:1.15rem}.stats{display:flex;gap:2rem;
font:600 .85rem system-ui;margin-top:2rem}.grid{display:grid;
grid-template-columns:repeat(auto-fit,minmax(18rem,1fr));gap:1px;background:var(--line);
border:1px solid var(--line);margin:2rem 0 5rem}.card{background:var(--paper);
padding:1.5rem;min-height:16rem;display:flex;flex-direction:column}.card h2{
font-size:1.45rem;margin:.7rem 0}.card p{color:var(--muted);margin:.25rem 0}
.card .open{margin-top:auto;font:700 .85rem system-ui}.badge{display:inline-flex;
width:max-content;border:1px solid currentColor;border-radius:99px;padding:.22rem .55rem;
font:700 .68rem system-ui;text-transform:uppercase;letter-spacing:.08em}
.complete{color:var(--good)}.error{color:var(--bad)}.article{width:min(48rem,
calc(100% - 2rem));margin:0 auto;padding:3rem 0 7rem}.article nav{
font:700 .8rem system-ui;margin-bottom:3rem}.article h1{font-size:clamp(2.2rem,6vw,4rem)}
.meta{display:flex;flex-wrap:wrap;gap:.8rem 1.5rem;padding:1rem 0 2rem;
border-bottom:1px solid var(--line);font:600 .8rem system-ui;color:var(--muted)}
.content{padding-top:1.5rem}.content h2{font-size:1.7rem;margin-top:2.4rem}
.content h3{font-size:1.3rem;margin-top:2rem}.content p{margin:1.15rem 0}
.content blockquote{border-left:3px solid var(--accent);margin:1.5rem 0;padding-left:1.2rem}
code,pre{font-family:ui-monospace,monospace}pre{overflow:auto;background:#e9e3d7;padding:1rem}
@media(max-width:600px){.masthead{padding-top:2.5rem}.stats{gap:1rem;flex-wrap:wrap}}
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
<span class="badge {status}">{escape(status)}</span>
<h1>{escape(str(metadata["title"]))}</h1>
<div class="meta"><span>{confidence:.0%} status confidence</span>
<span>{escape(str(entry.get("model", "unknown model")))}</span>
<a href="{escape(source_url, quote=True)}">Original OpenAI article ↗</a></div>
<article class="content">{markdown_to_html(body)}</article></main>"""
        (article_dir / article_name).write_text(
            _page(str(metadata["title"]), article_body),
            encoding="utf-8",
        )
        description = (
            "Summary available."
            if status == "complete"
            else "The source extraction needs attention before summarization."
        )
        cards.append(
            f"""<article class="card"><span class="badge {status}">{status}</span>
<h2>{escape(str(metadata["title"]))}</h2><p>{escape(description)}</p>
<p>{confidence:.0%} status confidence</p>
<a class="open" href="articles/{article_name}">Read record →</a></article>"""
        )
    index_body = f"""
<header class="masthead"><div class="shell"><div class="eyebrow">Epitome index</div>
<h1>Article summaries</h1><p class="intro">Compact, model-readable records of
OpenAI’s published articles, with extraction failures kept visible instead of
silently summarized.</p><div class="stats"><span>{len(entries)} records</span>
<span>{complete_count} complete</span><span>{error_count} need attention</span>
</div></div></header><main class="shell"><section class="grid">
{''.join(cards)}</section></main>"""
    (output_dir / "index.html").write_text(
        _page("Article summaries", index_body),
        encoding="utf-8",
    )
    return {
        "articles": len(entries),
        "complete": complete_count,
        "errors": error_count,
    }
