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
:root{color-scheme:light;--ink:#202122;--quiet:#54595d;--line:#a2a9b1;
--faint:#eaecf0;--link:#36c;--visited:#6b4ba1;--panel:#eaf3ff;
--panel-line:#a2a9b1;--good:#14866d;--bad:#b32424}
*{box-sizing:border-box}
html{background:#fff}
body{margin:0;color:var(--ink);background:#fff;font:14px/1.6 Arial,Helvetica,sans-serif}
a{color:var(--link);text-decoration:none}a:visited{color:var(--visited)}
a:hover{text-decoration:underline}
.site-header{height:74px;display:flex;align-items:center;gap:2rem;max-width:1352px;
margin:0 auto;padding:8px 28px;border-bottom:1px solid transparent}
.brand{display:flex;align-items:center;gap:10px;min-width:205px;color:var(--ink)!important}
.brand:hover{text-decoration:none}.brand-name{display:block;font:24px/1 Georgia,serif;
font-variant:small-caps;letter-spacing:.04em}.brand-tagline{display:block;margin-top:3px;
color:var(--quiet);font:10px/1.2 Georgia,serif;letter-spacing:.03em}
.crystal{position:relative;width:42px;height:42px;perspective:100px;
transform-style:preserve-3d;filter:drop-shadow(0 1px 1px #8ea6c4)}
.crystal i{position:absolute;inset:7px 6px;background:linear-gradient(135deg,#fff 15%,#7baee8 52%,#3056a5);
clip-path:polygon(50% 0,100% 100%,0 100%);opacity:.62;transform-origin:50% 64%;
mix-blend-mode:multiply}
.crystal i:nth-child(1){animation:orbit-a 9s linear infinite}
.crystal i:nth-child(2){background:linear-gradient(135deg,#d9ffff,#5cc7c2 58%,#315fa5);
animation:orbit-b 11s linear infinite}
.crystal i:nth-child(3){background:linear-gradient(135deg,#fff,#b8a0e8 58%,#3a67a8);
animation:orbit-c 13s linear infinite}
.crystal:after{content:"";position:absolute;left:18px;top:17px;width:7px;height:7px;
background:#fff;transform:rotate(45deg);box-shadow:0 0 8px #fff}
@keyframes orbit-a{to{transform:rotateZ(360deg) rotateX(58deg)}}
@keyframes orbit-b{from{transform:rotateZ(28deg) rotateY(62deg)}to{transform:rotateZ(-332deg) rotateY(62deg)}}
@keyframes orbit-c{from{transform:rotateZ(66deg) rotateX(72deg)}to{transform:rotateZ(426deg) rotateX(72deg)}}
.site-search{display:flex;width:min(475px,40vw);height:34px}
.site-search input{min-width:0;flex:1;border:1px solid #72777d;padding:6px 10px;
font:14px Arial,sans-serif}.site-search button{border:1px solid #72777d;border-left:0;
background:#f8f9fa;padding:0 14px;font-weight:700;color:var(--ink)}
.site-links{display:flex;gap:1rem;margin-left:auto;white-space:nowrap;font-size:13px}
.page-shell{max-width:1352px;margin:0 auto;padding:14px 28px 48px}
.page-title{font:29px/1.25 Georgia,"Times New Roman",serif;margin:0;
padding-bottom:3px;border-bottom:1px solid var(--line);color:#101418}
.page-tabs{display:flex;justify-content:space-between;border-bottom:1px solid #c8ccd1;
height:33px;margin-bottom:9px}.tabs-left,.tabs-right{display:flex;gap:18px}
.page-tabs span,.page-tabs a{padding-top:7px}.page-tabs .selected{border-bottom:2px solid var(--ink);
color:var(--ink)}.site-note{margin:0 0 15px}
.notice{max-width:900px;margin:16px auto;padding:11px 18px;border:1px solid var(--panel-line);
background:var(--panel);display:grid;grid-template-columns:48px 1fr;gap:12px;align-items:center}
.notice .symbol{font:34px/1 Georgia,serif;color:#607d9f;text-align:center}
.notice p{margin:.25rem 0}.stats{display:flex;gap:1.5rem;color:var(--quiet)}
.list-heading{font:22px/1.35 Arial,sans-serif;margin:14px 0 0;padding:10px 14px;
border:1px solid var(--line);background:#f8f9fa}
.summary-list{columns:2;column-gap:3rem;margin:0;padding:12px 28px 18px 34px;
border:1px solid var(--line);border-top:0}
.summary-list li{break-inside:avoid;margin:0 0 14px;padding-left:2px}
.summary-list h2{display:inline;font-size:14px;font-weight:400;margin:0}
.record-meta,.source{display:block;color:var(--quiet);font-size:12px}
.source{max-width:34rem;overflow-wrap:anywhere}.status{font-weight:700}
.complete{color:var(--good)}.error{color:var(--bad)}
.article-layout{display:grid;grid-template-columns:minmax(0,880px) 260px;gap:32px;
justify-content:center}.article{min-width:0}.article .lead-row{display:flex;
justify-content:space-between;align-items:baseline;gap:1rem}
.article .content{font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.65}
.content h1,.content h2{font-family:Georgia,"Times New Roman",serif;font-weight:400;
border-bottom:1px solid var(--line);padding-bottom:3px}
.content h1{font-size:27px}.content h2{font-size:22px;margin:1.4em 0 .35em}
.content h3{font-size:17px;margin:1.3em 0 .25em}.content p{margin:.6em 0}
.content ul,.content ol{margin:.3em 0 .9em;padding-left:2.2em}
.content blockquote{border-left:3px solid var(--line);margin:1em 0;padding:.2em 1em;color:var(--quiet)}
.infobox{align-self:start;margin-top:18px;border:1px solid var(--line);background:#f8f9fa;
padding:10px 12px;font-size:12px}.infobox h2{margin:0 0 8px;padding:5px;
background:#dbeafe;text-align:center;font-size:15px}.infobox dl{margin:0}
.infobox dt{font-weight:700;margin-top:8px}.infobox dd{margin:1px 0;overflow-wrap:anywhere}
.infobox .status{font-size:13px}.article-back{display:block;margin-bottom:8px}
code,pre{font-family:ui-monospace,monospace}code{background:#f8f9fa;border:1px solid var(--faint);
padding:.05em .25em}pre{overflow:auto;background:#f8f9fa;border:1px solid var(--line);padding:1em}
.site-footer{max-width:1352px;margin:0 auto;padding:18px 28px 30px;border-top:1px solid var(--faint);
color:var(--quiet);font-size:12px}
@media(prefers-reduced-motion:reduce){.crystal i{animation:none!important}}
@media(max-width:800px){.site-header{height:auto;flex-wrap:wrap;padding:10px 18px;gap:8px 18px}
.brand{min-width:0}.site-search{order:3;width:100%}.site-links{font-size:12px}
.page-shell{padding:14px 18px 36px}
.notice{display:block;padding:12px 14px}.notice .symbol{display:none}.stats{flex-wrap:wrap;gap:.3rem 1rem}
.summary-list{columns:1}.article-layout{display:block}.infobox{margin:18px 0}.tabs-right{display:none}}
"""


def _page(title: str, body: str) -> str:
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — Epitome</title><link rel="stylesheet" href="/style.css">
</head><body><header class="site-header">
<a class="brand" href="/" aria-label="Epitome home">
<span class="crystal" aria-hidden="true"><i></i><i></i><i></i></span>
<span><span class="brand-name">Epitome</span>
<span class="brand-tagline">A living archive of machine intelligence</span></span></a>
<form class="site-search" action="/" method="get">
<input type="search" name="q" placeholder="Search Epitome" aria-label="Search Epitome">
<button type="submit">Search</button></form>
<nav class="site-links" aria-label="Site"><a href="/">Summaries</a></nav></header>
<div class="page-shell">{body}</div>
<footer class="site-footer">Epitome preserves source material and concise,
model-readable summaries for future research.</footer>
<script>
const params=new URLSearchParams(location.search),query=params.get("q");
if(query){{
 const input=document.querySelector('.site-search input'),items=document.querySelectorAll('.summary-list li');
 input.value=query;
 items.forEach(item=>item.hidden=!item.textContent.toLowerCase().includes(query.toLowerCase()));
 const heading=document.querySelector('.list-heading');
 if(heading) heading.textContent=`Search results for “${{query}}”`;
}}
</script></body></html>"""


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
<main><a class="article-back" href="/">← All summaries</a>
<h1 class="page-title">{escape(str(metadata["title"]))}</h1>
<div class="page-tabs"><div class="tabs-left"><span class="selected">Summary</span>
<a href="{escape(source_url, quote=True)}">Source</a></div>
<div class="tabs-right"><span class="selected">Read</span><span>View record</span></div></div>
<p class="site-note">From Epitome, the machine-readable archive</p>
<div class="article-layout"><article class="article">
<div class="content">{markdown_to_html(body)}</div></article>
<aside class="infobox"><h2>Summary record</h2><dl>
<dt>Status</dt><dd><span class="status {status}">{escape(status)}</span></dd>
<dt>Status confidence</dt><dd>{confidence:.0%}</dd>
<dt>Model</dt><dd>{escape(str(entry.get("model", "unknown model")))}</dd>
<dt>Original publication</dt>
<dd><a href="{escape(source_url, quote=True)}">Original OpenAI article ↗</a></dd>
</dl></aside></div></main>"""
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
<main><h1 class="page-title">Article summaries</h1>
<div class="page-tabs"><div class="tabs-left"><span class="selected">Main page</span>
<span>Discussion</span></div><div class="tabs-right"><span class="selected">Read</span>
<span>View history</span></div></div>
<p class="site-note">From Epitome, the machine-readable archive</p>
<section class="notice"><div class="symbol" aria-hidden="true">◇</div><div>
<p><strong>Article summaries</strong> are compact, model-readable records of
OpenAI’s published articles. Extraction failures remain visible instead of being
silently summarized.</p><div class="stats"><span><strong>{len(entries)}</strong> records</span>
<span><strong>{complete_count}</strong> complete</span>
<span><strong>{error_count}</strong> need attention</span></div></div></section>
<h2 class="list-heading">Summaries in Epitome</h2><ul class="summary-list">
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
