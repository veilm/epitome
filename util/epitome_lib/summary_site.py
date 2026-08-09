"""Generate a dependency-free static browser for tracked article summaries."""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from .capture import archival_url_key
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


CRYSTAL_KINDS = (
    "facet-outline-color",
    "facet-outline-ink",
    "facet-outline-color-ghost",
    "facet-outline-ink-ghost",
    "prism-outline-color",
    "prism-outline-ink",
    "prism-outline-color-ghost",
    "prism-outline-ink-ghost",
    "outline-color",
    "outline-ink",
    "outline-dusk",
    "cathedral-adaptive",
    "cathedral-ink",
    "cathedral",
    "facet",
    "prism",
    "orbit",
)


def crystal_markup(kind: str) -> str:
    if kind not in CRYSTAL_KINDS:
        raise ValueError(f"unknown crystal kind: {kind}")
    if kind.startswith("facet-outline-") or kind.startswith("prism-outline-"):
        is_facet = kind.startswith("facet-")
        view_box = "0 0 30 28" if is_facet else "0 0 30 30"
        points = "15,1 29,27 1,27" if is_facet else "15,1 29,15 15,29 1,15"
        planes = "".join(
            f'<svg class="plane plane-{letter}" viewBox="{view_box}">'
            f'<polygon points="{points}"/></svg>'
            for letter in "abc"
        )
        return (
            f'<span class="crystal crystal-{kind}" data-crystal="{kind}" '
            f'aria-hidden="true">{planes}</span>'
        )
    if kind.startswith("cathedral"):
        shapes = '<polygon class="tri tri-a" points="21,7 35,32 7,32"/>' \
            '<polygon class="tri tri-b" points="21,7 35,32 7,32"/>'
        return (
            f'<span class="crystal crystal-svg crystal-{kind}" data-crystal="{kind}" '
            f'aria-hidden="true"><svg viewBox="0 0 42 42">{shapes}</svg></span>'
        )
    if kind.startswith("outline-"):
        shapes = "".join(
            f'<polygon class="tri tri-{letter}" points="21,6 36,32 6,32"/>'
            for letter in "abc"
        )
        return (
            f'<span class="crystal crystal-svg crystal-{kind}" data-crystal="{kind}" '
            f'aria-hidden="true"><svg viewBox="0 0 42 42">{shapes}</svg></span>'
        )
    return (
        f'<span class="crystal crystal-{kind}" data-crystal="{kind}" '
        'aria-hidden="true"><i></i><i></i><i></i></span>'
    )


EARLY_SETTINGS_SCRIPT = """<script>
(()=>{try{
 const saved=JSON.parse(localStorage.getItem('epitome-settings')||'{}');
 const theme=saved.theme||'system';
 document.documentElement.dataset.theme=theme==='system'
  ?(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'):theme;
 document.documentElement.dataset.logo=saved.logo||'cathedral-ink';
 document.documentElement.dataset.sourceBorder=saved.sourceBorder?'on':'off';
}catch(_){document.documentElement.dataset.theme='light';
 document.documentElement.dataset.logo='cathedral-ink';
 document.documentElement.dataset.sourceBorder='off'}})();
</script>"""


SETTINGS_SCRIPT = """<script>
const settingsKey='epitome-settings';
function readSettings(){try{return {...{theme:'system',logo:'cathedral-ink',sourceBorder:false},
 ...JSON.parse(localStorage.getItem(settingsKey)||'{}')}}catch(_){return {theme:'system',logo:'cathedral-ink',sourceBorder:false}}}
function applySettings(settings){
 const theme=settings.theme==='system'
  ?(matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light'):settings.theme;
 document.documentElement.dataset.theme=theme;
 document.documentElement.dataset.logo=settings.logo;
 document.documentElement.dataset.sourceBorder=settings.sourceBorder?'on':'off';
}
function saveSettings(patch){const settings={...readSettings(),...patch};
 localStorage.setItem(settingsKey,JSON.stringify(settings));applySettings(settings)}
const currentSettings=readSettings();applySettings(currentSettings);
document.querySelectorAll('[name="site-logo"]').forEach(input=>{
 input.checked=input.value===currentSettings.logo;
 input.addEventListener('change',()=>saveSettings({logo:input.value}));
});
const themeSetting=document.querySelector('#theme-setting');
if(themeSetting){themeSetting.value=currentSettings.theme;
 themeSetting.addEventListener('change',()=>saveSettings({theme:themeSetting.value}))}
const borderSetting=document.querySelector('#source-border-setting');
if(borderSetting){borderSetting.checked=currentSettings.sourceBorder;
 borderSetting.addEventListener('change',()=>saveSettings({sourceBorder:borderSetting.checked}))}
matchMedia('(prefers-color-scheme:dark)').addEventListener('change',()=>{
 if(readSettings().theme==='system')applySettings(readSettings())});
</script>"""


STYLE = """
:root{color-scheme:light;--ink:#202122;--quiet:#54595d;--line:#a2a9b1;
--faint:#eaecf0;--link:#36c;--visited:#6b4ba1;--panel:#eaf3ff;
--panel-line:#a2a9b1;--good:#14866d;--bad:#b32424;--bg:#fff;
--surface:#f8f9fa;--heading:#101418;--field:#fff;--mark-bg:#fff;--mark-ink:#202122}
html[data-theme="dark"]{color-scheme:dark;--ink:#eaecf0;--quiet:#aeb4ba;--line:#72777d;
--faint:#343a40;--link:#8ab4f8;--visited:#c6a0f6;--panel:#17263b;
--panel-line:#536b8a;--good:#5ad1b9;--bad:#ff7b7b;--bg:#101214;
--surface:#1b1e22;--heading:#f8f9fa;--field:#181b1f;--mark-bg:#f8f9fa;--mark-ink:#202122}
*{box-sizing:border-box}
html{background:var(--bg)}
body{margin:0;color:var(--ink);background:var(--bg);font:14px/1.6 Arial,Helvetica,sans-serif}
a{color:var(--link);text-decoration:none}a:visited{color:var(--link)}
a:hover{text-decoration:underline}
.site-header{height:74px;display:flex;align-items:center;gap:2rem;max-width:1352px;
margin:0 auto;padding:8px 28px;border-bottom:1px solid transparent}
.brand{display:flex;align-items:center;gap:10px;min-width:150px;color:var(--ink)!important}
.brand:hover{text-decoration:none}.brand-name{display:block;font:24px/1 Georgia,serif}
.crystal{position:relative;display:block;width:42px;height:42px;perspective:100px;
transform-style:preserve-3d;--crystal-cutout:var(--bg)}
.brand-mark{display:block;width:42px;height:42px;flex:0 0 42px}
.brand-mark .crystal{display:none}
html[data-logo="facet-outline-color"] .brand-mark .crystal-facet-outline-color,
html[data-logo="facet-outline-ink"] .brand-mark .crystal-facet-outline-ink,
html[data-logo="facet-outline-color-ghost"] .brand-mark .crystal-facet-outline-color-ghost,
html[data-logo="facet-outline-ink-ghost"] .brand-mark .crystal-facet-outline-ink-ghost,
html[data-logo="prism-outline-color"] .brand-mark .crystal-prism-outline-color,
html[data-logo="prism-outline-ink"] .brand-mark .crystal-prism-outline-ink,
html[data-logo="prism-outline-color-ghost"] .brand-mark .crystal-prism-outline-color-ghost,
html[data-logo="prism-outline-ink-ghost"] .brand-mark .crystal-prism-outline-ink-ghost,
html[data-logo="outline-color"] .brand-mark .crystal-outline-color,
html[data-logo="outline-ink"] .brand-mark .crystal-outline-ink,
html[data-logo="outline-dusk"] .brand-mark .crystal-outline-dusk,
html[data-logo="cathedral-adaptive"] .brand-mark .crystal-cathedral-adaptive,
html[data-logo="cathedral-ink"] .brand-mark .crystal-cathedral-ink,
html[data-logo="cathedral"] .brand-mark .crystal-cathedral,
html[data-logo="facet"] .brand-mark .crystal-facet,
html[data-logo="prism"] .brand-mark .crystal-prism,
html[data-logo="orbit"] .brand-mark .crystal-orbit{display:block}
.crystal-svg svg{display:block;width:100%;height:100%;overflow:visible}
.crystal-svg .tri{fill:none;stroke-width:1.45;vector-effect:non-scaling-stroke;
shape-rendering:geometricPrecision;transform-box:view-box;transform-origin:21px 21px}
.crystal-svg .tri-a{animation:outline-a 12s linear infinite}
.crystal-svg .tri-b{animation:outline-b 9s linear infinite}
.crystal-svg .tri-c{animation:outline-c 15s linear infinite}
.crystal-outline-ink .tri{stroke:var(--ink)}
.crystal-outline-color .tri-a{stroke:#3769b0}.crystal-outline-color .tri-b{stroke:#2ba8a0}
.crystal-outline-color .tri-c{stroke:#865db5}
.crystal-outline-dusk .tri-a{stroke:#5b6bd5}.crystal-outline-dusk .tri-b{stroke:#c25b85}
.crystal-outline-dusk .tri-c{stroke:#d19a38}
.crystal-cathedral-adaptive .tri-a{stroke:var(--link);stroke-width:1.6;opacity:.82}
.crystal-cathedral-adaptive .tri-b{stroke:var(--quiet);stroke-width:1.35;opacity:.52}
.crystal-cathedral-ink .tri-a{stroke:var(--ink);stroke-width:1.6;opacity:.86}
.crystal-cathedral-ink .tri-b{stroke:var(--ink);stroke-width:1.35;opacity:.45}
.crystal-cathedral .tri-a{stroke:#8b7355;stroke-width:1.6;opacity:.8}
.crystal-cathedral .tri-b{stroke:#6b635a;stroke-width:1.35;opacity:.5}
.crystal-cathedral .tri-a,.crystal-cathedral-adaptive .tri-a,.crystal-cathedral-ink .tri-a{
animation:outline-a 12s linear infinite}
.crystal-cathedral .tri-b,.crystal-cathedral-adaptive .tri-b,.crystal-cathedral-ink .tri-b{
animation:outline-b 8s linear infinite}
@keyframes outline-a{from{transform:rotate(0)}to{transform:rotate(360deg)}}
@keyframes outline-b{from{transform:rotate(34deg)}to{transform:rotate(-326deg)}}
@keyframes outline-c{from{transform:rotate(72deg)}to{transform:rotate(432deg)}}
.crystal[data-crystal^="facet-outline-"] .plane,
.crystal[data-crystal^="prism-outline-"] .plane{position:absolute;display:block;overflow:visible;
transform-style:preserve-3d}
.crystal[data-crystal^="facet-outline-"] .plane{inset:7px 6px;transform-origin:50% 64%}
.crystal[data-crystal^="prism-outline-"] .plane{inset:6px}
.crystal[data-crystal^="prism-outline-"] .plane-c{inset:11px}
.crystal[data-crystal^="facet-outline-"] polygon,
.crystal[data-crystal^="prism-outline-"] polygon{fill:var(--crystal-cutout);stroke:var(--outline-stroke);
stroke-width:1.4;stroke-linecap:round;stroke-linejoin:round;vector-effect:non-scaling-stroke;
shape-rendering:geometricPrecision}
.crystal[data-crystal$="-ghost"] polygon{fill:none}
.crystal[data-crystal*="-outline-ink"] .plane{--outline-stroke:var(--ink)}
.crystal[data-crystal*="-outline-color"] .plane-a{--outline-stroke:#3769b0}
.crystal[data-crystal*="-outline-color"] .plane-b{--outline-stroke:#2ba8a0}
.crystal[data-crystal*="-outline-color"] .plane-c{--outline-stroke:#865db5}
.crystal[data-crystal^="facet-outline-"] .plane-a{animation:orbit-a 9s linear infinite}
.crystal[data-crystal^="facet-outline-"] .plane-b{animation:orbit-b 11s linear infinite}
.crystal[data-crystal^="facet-outline-"] .plane-c{animation:orbit-c 13s linear infinite}
.crystal[data-crystal^="prism-outline-"] .plane-a{animation:prism-a 10s linear infinite}
.crystal[data-crystal^="prism-outline-"] .plane-b{animation:prism-b 14s linear infinite}
.crystal[data-crystal^="prism-outline-"] .plane-c{animation:prism-c 8s linear infinite}
.crystal-facet i{position:absolute;inset:7px 6px;background:linear-gradient(135deg,#fff 15%,#7baee8 52%,#3056a5);
clip-path:polygon(50% 0,100% 100%,0 100%);opacity:.62;transform-origin:50% 64%;
mix-blend-mode:multiply}
.crystal-facet i:nth-child(1){animation:orbit-a 9s linear infinite}
.crystal-facet i:nth-child(2){background:linear-gradient(135deg,#d9ffff,#5cc7c2 58%,#315fa5);
animation:orbit-b 11s linear infinite}
.crystal-facet i:nth-child(3){background:linear-gradient(135deg,#fff,#b8a0e8 58%,#3a67a8);
animation:orbit-c 13s linear infinite}
@keyframes orbit-a{from{transform:rotateX(58deg) rotateZ(0)}to{transform:rotateX(58deg) rotateZ(360deg)}}
@keyframes orbit-b{from{transform:rotateY(62deg) rotateZ(28deg)}to{transform:rotateY(62deg) rotateZ(388deg)}}
@keyframes orbit-c{from{transform:rotateX(72deg) rotateZ(66deg)}to{transform:rotateX(72deg) rotateZ(426deg)}}
.crystal-prism i{position:absolute;inset:6px;background:linear-gradient(145deg,#fff,#83b9f0 45%,#345aa8);
clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%);opacity:.62;mix-blend-mode:multiply}
.crystal-prism i:nth-child(1){animation:prism-a 10s linear infinite}
.crystal-prism i:nth-child(2){background:linear-gradient(145deg,#e9ffff,#5bc8bf,#3a5ca8);animation:prism-b 14s linear infinite}
.crystal-prism i:nth-child(3){inset:11px;background:linear-gradient(145deg,#fff,#baa3e7,#315fa5);animation:prism-c 8s linear infinite}
@keyframes prism-a{from{transform:rotate(0) scaleX(.72)}to{transform:rotate(360deg) scaleX(.72)}}
@keyframes prism-b{from{transform:rotate(45deg) scaleY(.72)}to{transform:rotate(405deg) scaleY(.72)}}
@keyframes prism-c{from{transform:rotate(90deg)}to{transform:rotate(450deg)}}
.crystal-orbit i{position:absolute;inset:8px 2px;border:2px solid #527bb9;border-radius:50%;opacity:.75}
.crystal-orbit i:nth-child(1){animation:ring-a 9s linear infinite}
.crystal-orbit i:nth-child(2){border-color:#4ab7ae;animation:ring-b 12s linear infinite}
.crystal-orbit i:nth-child(3){border-color:#9b82cf;animation:ring-c 15s linear infinite}
@keyframes ring-a{from{transform:rotate(0) scaleY(.38)}to{transform:rotate(360deg) scaleY(.38)}}
@keyframes ring-b{from{transform:rotate(60deg) scaleY(.38)}to{transform:rotate(420deg) scaleY(.38)}}
@keyframes ring-c{from{transform:rotate(120deg) scaleY(.38)}to{transform:rotate(480deg) scaleY(.38)}}
.site-search{display:flex;width:min(475px,40vw);height:34px}
.site-search input{min-width:0;flex:1;border:1px solid #72777d;padding:6px 10px;background:var(--field);color:var(--ink);
font:14px Arial,sans-serif}.site-search button{border:1px solid #72777d;border-left:0;
background:var(--surface);padding:0 14px;font-weight:700;color:var(--ink)}
.site-links{display:flex;gap:1rem;margin-left:auto;white-space:nowrap;font-size:13px}
.page-shell{max-width:1352px;margin:0 auto;padding:14px 28px 48px}
.page-title{font:29px/1.25 Georgia,"Times New Roman",serif;margin:0;
padding-bottom:3px;border-bottom:1px solid var(--line);color:var(--heading)}
.page-tabs{display:flex;justify-content:space-between;border-bottom:1px solid #c8ccd1;
height:33px;margin-bottom:9px}.tabs-left,.tabs-right{display:flex;gap:18px}
.page-tabs span,.page-tabs a{padding-top:7px}.page-tabs .selected{border-bottom:2px solid var(--ink);
color:var(--ink)}.site-note{margin:0 0 15px}
.notice{max-width:900px;margin:16px auto;padding:11px 18px;border:1px solid var(--panel-line);
background:var(--panel);display:grid;grid-template-columns:48px 1fr;gap:12px;align-items:center}
.notice .symbol{font:34px/1 Georgia,serif;color:#607d9f;text-align:center}
.notice p{margin:.25rem 0}.stats{display:flex;gap:1.5rem;color:var(--quiet)}
.list-heading{font:22px/1.35 Arial,sans-serif;margin:14px 0 0;padding:10px 14px;
border:1px solid var(--line);background:var(--surface)}
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
.infobox{align-self:start;margin-top:18px;border:1px solid var(--line);background:var(--surface);
padding:10px 12px;font-size:12px}.infobox h2{margin:0 0 8px;padding:5px;
background:var(--panel);text-align:center;font-size:15px}.infobox dl{margin:0}
.infobox dt{font-weight:700;margin-top:8px}.infobox dd{margin:1px 0;overflow-wrap:anywhere}
.infobox .status{font-size:13px}.article-back{display:block;margin-bottom:8px}
code,pre{font-family:ui-monospace,monospace}code{background:var(--surface);border:1px solid var(--faint);
padding:.05em .25em}pre{overflow:auto;background:var(--surface);border:1px solid var(--line);padding:1em}
.site-footer{max-width:1352px;margin:0 auto;padding:18px 28px 30px;border-top:1px solid var(--faint);
color:var(--quiet);font-size:12px}
.catalog-layout{display:grid;grid-template-columns:230px minmax(0,850px);gap:28px;align-items:start}
.filters{position:sticky;top:12px;border:1px solid var(--line);background:var(--surface);padding:13px 15px}
.filters h2{font:18px/1.3 Georgia,serif;margin:0 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}
.filter-group{border:0;margin:0 0 15px;padding:0}.filter-group legend{font-weight:700;margin-bottom:5px}
.filter-source{display:flex;align-items:center;gap:7px;padding:3px 0;cursor:pointer}
.filter-source input{margin:0}.filter-select{width:100%;padding:5px;border:1px solid #72777d;background:var(--field);color:var(--ink)}
.feed-toolbar{display:flex;align-items:baseline;justify-content:space-between;gap:1rem;
border-bottom:1px solid var(--line);padding:0 0 7px;margin-bottom:0}.feed-toolbar h2{font:22px Georgia,serif;margin:0}
.feed-count{color:var(--quiet);font-size:12px}.feed{list-style:none;margin:0;padding:0}
.feed-item{display:grid;grid-template-columns:42px minmax(0,1fr);gap:12px;padding:14px 4px;
border-bottom:1px solid var(--faint)}.feed-item[hidden]{display:none}
.source-mark{position:relative;display:flex;width:34px;height:34px;align-items:center;justify-content:center;
background:var(--mark-bg);color:var(--mark-ink);font:700 11px/1 Arial,sans-serif;letter-spacing:-.02em;border-radius:2px}
html[data-source-border="on"] .source-mark{border:1px solid #72777d}
.source-mark img{position:absolute;inset:0;width:100%;height:100%;padding:3px;object-fit:contain;background:var(--mark-bg);border-radius:1px}
.source-andrej-karpathy img,.source-peter-steinberger img{padding:0;object-fit:cover}
.source-openai{background:#e7f5ef}.source-anthropic{background:#f4eee7}.source-claude{background:#f8e7db}
.source-dario-amodei{background:#e9edf7}.source-andrej-karpathy{background:#f0e9f5}
.source-peter-steinberger{background:#e7f1f7}.source-dwarkesh{background:#f6efd9}.source-semianalysis{background:#ebeff1}
.feed-title{font:18px/1.35 Georgia,"Times New Roman",serif;margin:0 0 3px}
.feed-meta{display:flex;flex-wrap:wrap;gap:4px 8px;align-items:center;color:var(--quiet);font-size:12px}
.summary-link{display:inline-block;border:1px solid var(--line);background:var(--surface);padding:0 5px;font-weight:700}
.undated-note{max-width:46rem;color:var(--quiet);font-size:12px;margin:8px 0 0}
.empty-state{padding:30px 4px;color:var(--quiet)}
.settings-section{max-width:1000px;margin:24px 0}.settings-section>h2{font:22px/1.35 Georgia,serif;
border-bottom:1px solid var(--line);padding-bottom:4px}.logo-grid{display:grid;
grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:18px 0}
.logo-choice{position:relative;display:flex;min-height:174px;flex-direction:column;align-items:center;
justify-content:center;border:1px solid var(--line);background:var(--surface);padding:22px 14px;text-align:center;cursor:pointer}
.logo-choice:hover{border-color:var(--link)}.logo-choice:has(input:checked){outline:2px solid var(--link);outline-offset:1px}
.logo-choice input{position:absolute;top:10px;left:10px}.logo-choice .crystal{display:block;width:68px;height:68px;
margin:4px auto 14px;perspective:150px;--crystal-cutout:var(--surface)}
.logo-choice strong{font:17px/1.3 Georgia,serif}.logo-choice small{display:block;color:var(--quiet);margin-top:4px}
.setting-row{display:flex;align-items:center;justify-content:space-between;gap:28px;max-width:700px;
padding:14px 0;border-bottom:1px solid var(--faint)}.setting-row label{font-weight:700}
.setting-row p{margin:2px 0 0;color:var(--quiet)}.setting-control{display:flex;align-items:center;gap:12px;flex:0 0 auto}
.setting-control select{min-width:130px;padding:5px;border:1px solid var(--line);background:var(--field);color:var(--ink)}
@media(prefers-reduced-motion:reduce){.crystal i,.crystal .tri{animation-play-state:paused!important}}
@media(max-width:800px){.site-header{height:auto;flex-wrap:wrap;padding:10px 18px;gap:8px 18px}
.brand{min-width:0}.site-search{order:3;width:100%}.site-links{font-size:12px}
.page-shell{padding:14px 18px 36px}
.notice{display:block;padding:12px 14px}.notice .symbol{display:none}.stats{flex-wrap:wrap;gap:.3rem 1rem}
.summary-list{columns:1}.article-layout{display:block}.infobox{margin:18px 0}.tabs-right{display:none}
.catalog-layout{display:block}.filters{position:static;margin-bottom:20px}.feed-title{font-size:17px}
.logo-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.setting-row{align-items:flex-start}}
@media(max-width:460px){.logo-grid{grid-template-columns:1fr}}
"""


def _page(title: str, body: str) -> str:
    brand_marks = "".join(crystal_markup(kind) for kind in CRYSTAL_KINDS)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} — Epitome</title>{EARLY_SETTINGS_SCRIPT}<link rel="stylesheet" href="/style.css">
</head><body><header class="site-header">
<a class="brand" href="/" aria-label="Epitome home">
<span class="brand-mark">{brand_marks}</span>
<span class="brand-name">Epitome</span></a>
<form class="site-search" action="/" method="get">
<input type="search" name="q" placeholder="Search Epitome" aria-label="Search Epitome">
<button type="submit">Search</button></form>
<nav class="site-links" aria-label="Site"><a href="/settings.html">Settings</a></nav></header>
<div class="page-shell">{body}</div>
<footer class="site-footer">Epitome preserves source material and concise,
model-readable summaries for future research.</footer>
<script>
const form=document.querySelector('.site-search'),input=form?.querySelector('input');
const feed=document.querySelector('.feed'),count=document.querySelector('.feed-count');
const sourceInputs=[...document.querySelectorAll('[data-source-filter]')];
const summaryFilter=document.querySelector('#summary-filter'),sortSelect=document.querySelector('#sort-order');
function refresh(){{
 if(!feed)return;
 const query=(input?.value||'').trim().toLowerCase();
 const enabled=new Set(sourceInputs.filter(box=>box.checked).map(box=>box.value));
 const summary=summaryFilter?.value||'all';let visible=0;
 [...feed.children].forEach(item=>{{
  const matchesSource=enabled.has(item.dataset.source);
  const hasSummary=item.dataset.summary==='yes';
  const matchesSummary=summary==='all'||(summary==='with'&&hasSummary)||(summary==='without'&&!hasSummary);
  const matchesQuery=!query||item.textContent.toLowerCase().includes(query);
  item.hidden=!(matchesSource&&matchesSummary&&matchesQuery);if(!item.hidden)visible++;
 }});
 const direction=sortSelect?.value==='oldest'?1:-1;
 [...feed.children].sort((a,b)=>{{
  const ad=Number(a.dataset.published),bd=Number(b.dataset.published);
  if(ad<0&&bd>=0)return 1;if(bd<0&&ad>=0)return -1;
  return (ad-bd)*direction||a.dataset.title.localeCompare(b.dataset.title);
 }}).forEach(item=>feed.appendChild(item));
 if(count)count.textContent=`${{visible.toLocaleString()}} of ${{feed.children.length.toLocaleString()}} pages`;
 const empty=document.querySelector('.empty-state');if(empty)empty.hidden=visible!==0;
}}
form?.addEventListener('submit',event=>{{event.preventDefault();refresh()}});
input?.addEventListener('input',refresh);sourceInputs.forEach(box=>box.addEventListener('change',refresh));
summaryFilter?.addEventListener('change',refresh);sortSelect?.addEventListener('change',refresh);
refresh();
</script>{SETTINGS_SCRIPT}</body></html>"""


def _summary_path(catalog_path: Path, content_path: str) -> Path:
    root = catalog_path.parent.resolve()
    path = (catalog_path.parent / content_path).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"summary path escapes catalog directory: {content_path}")
    return path


def build_summary_site(
    catalog_path: Path,
    output_dir: Path,
    pages_catalog_path: Path | None = Path("site/catalog.json"),
) -> dict[str, int]:
    entries = json.loads(catalog_path.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError("summary catalog must be a JSON array")
    output_dir.mkdir(parents=True, exist_ok=True)
    article_dir = output_dir / "articles"
    article_dir.mkdir(exist_ok=True)
    for stale in article_dir.glob("*.html"):
        stale.unlink()
    (output_dir / "style.css").write_text(STYLE.strip() + "\n", encoding="utf-8")

    summaries_by_url: dict[str, dict[str, object]] = {}
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
<main><a class="article-back" href="/">← All archived pages</a>
<h1 class="page-title">{escape(str(metadata["title"]))}</h1>
<div class="page-tabs"><div class="tabs-left"><span class="selected">Summary</span>
<a href="{escape(source_url, quote=True)}" target="_blank" rel="noopener noreferrer">Source</a></div>
<div class="tabs-right"><span class="selected">Read</span><span>View record</span></div></div>
<p class="site-note">From Epitome, the machine-readable archive</p>
<div class="article-layout"><article class="article">
<div class="content">{markdown_to_html(body)}</div></article>
<aside class="infobox"><h2>Summary record</h2><dl>
<dt>Status</dt><dd><span class="status {status}">{escape(status)}</span></dd>
<dt>Status confidence</dt><dd>{confidence:.0%}</dd>
<dt>Model</dt><dd>{escape(str(entry.get("model", "unknown model")))}</dd>
<dt>Original publication</dt>
<dd><a href="{escape(source_url, quote=True)}" target="_blank" rel="noopener noreferrer">Original article ↗</a></dd>
</dl></aside></div></main>"""
        (article_dir / article_name).write_text(
            _page(str(metadata["title"]), article_body),
            encoding="utf-8",
        )
        summaries_by_url[archival_url_key(source_url)] = {
            "href": f"articles/{article_name}",
            "status": status,
            "title": str(metadata["title"]),
        }

    page_catalog: dict[str, object] = {"sources": [], "pages": []}
    if pages_catalog_path is not None and pages_catalog_path.exists():
        loaded = json.loads(pages_catalog_path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict) or not isinstance(loaded.get("pages"), list):
            raise ValueError("public page catalog must contain a pages array")
        page_catalog = loaded
    pages = list(page_catalog.get("pages", []))
    if not pages:
        pages = [
            {
                "captured_at": int(entry.get("generated_at", 0)),
                "published_at": None,
                "source": "other",
                "title": str(entry.get("title", entry["source_url"])),
                "url": str(entry["source_url"]),
            }
            for entry in entries
        ]
    source_records = {
        str(source["id"]): source
        for source in page_catalog.get("sources", [])
        if isinstance(source, dict) and "id" in source
    }
    source_records.setdefault("other", {"id": "other", "name": "Other"})
    initials = {
        "openai": "OA", "anthropic": "A", "claude": "C", "dario-amodei": "DA",
        "andrej-karpathy": "AK", "peter-steinberger": "PS", "dwarkesh": "DP",
        "semianalysis": "SA", "other": "·",
    }
    feed_items: list[str] = []
    dated_count = 0
    summarized_count = 0
    used_sources: set[str] = set()
    for page in pages:
        url = str(page["url"])
        source_id = str(page.get("source", "other"))
        used_sources.add(source_id)
        source_record = source_records.get(source_id, {})
        source_name = str(source_record.get("name", source_id))
        fallback = escape(initials.get(source_id, source_name[:2].upper()))
        logo_url = source_record.get("logo_url")
        logo = (
            f'<img src="{escape(str(logo_url), quote=True)}" alt="" '
            'loading="lazy" referrerpolicy="no-referrer" onerror="this.remove()">'
            if logo_url else ""
        )
        title = str(page.get("title") or url)
        published_at = page.get("published_at")
        if isinstance(published_at, int):
            dated_count += 1
            date_display = datetime.fromtimestamp(published_at, tz=timezone.utc).strftime("%Y-%m-%d")
            sort_date = published_at
        else:
            date_display = "Date unavailable"
            sort_date = -1
        summary = summaries_by_url.get(archival_url_key(url))
        summarized_count += int(summary is not None)
        summary_link = (
            f'<a class="summary-link" href="{escape(str(summary["href"]), quote=True)}">Summary</a>'
            if summary else ""
        )
        feed_items.append(
            f'''<li class="feed-item" data-source="{escape(source_id, quote=True)}"
data-summary="{"yes" if summary else "no"}" data-published="{sort_date}"
data-title="{escape(title.lower(), quote=True)}"><span class="source-mark source-{escape(source_id, quote=True)}"
aria-hidden="true"><span>{fallback}</span>{logo}</span><div>
<h3 class="feed-title"><a href="{escape(url, quote=True)}" target="_blank"
rel="noopener noreferrer">{escape(title)}</a></h3><div class="feed-meta">
<span>{escape(source_name)}</span><span aria-hidden="true">·</span><time>{date_display}</time>
{summary_link}</div></div></li>'''
        )
    source_filters = []
    for source_id in sorted(used_sources, key=lambda value: str(source_records.get(value, {}).get("name", value))):
        source_name = str(source_records.get(source_id, {}).get("name", source_id))
        source_filters.append(
            f'<label class="filter-source"><input type="checkbox" value="{escape(source_id, quote=True)}" '
            f'data-source-filter checked><span>{escape(source_name)}</span></label>'
        )
    index_body = f"""
<main><h1 class="page-title">Archived publications</h1>
<div class="page-tabs"><div class="tabs-left"><span class="selected">Main page</span>
<span>Discussion</span></div><div class="tabs-right"><span class="selected">Read</span>
<span>View history</span></div></div>
<p class="site-note">From Epitome, an index of historically valuable public sources</p>
<section class="notice"><div class="symbol" aria-hidden="true">◇</div><div>
<p><strong>Epitome’s publication catalog</strong> combines the pages preserved from
independent writers, research organizations, and company publications. Titles link to
their original public pages; available Epitome summaries are marked separately.</p>
<div class="stats"><span><strong>{len(pages):,}</strong> pages</span>
<span><strong>{len(used_sources)}</strong> sources</span><span><strong>{dated_count}</strong> dated</span>
<span><strong>{summarized_count}</strong> summarized</span></div></div></section>
<div class="catalog-layout"><aside class="filters" aria-label="Catalog filters"><h2>Filter</h2>
<fieldset class="filter-group"><legend>Sources</legend>{''.join(source_filters)}</fieldset>
<label class="filter-group"><strong>Summary</strong><select id="summary-filter" class="filter-select">
<option value="all">All pages</option><option value="with">With a summary</option>
<option value="without">Without a summary</option></select></label>
<label class="filter-group"><strong>Order</strong><select id="sort-order" class="filter-select">
<option value="newest">Newest first</option><option value="oldest">Oldest first</option>
</select></label></aside><section><div class="feed-toolbar"><h2>Publications</h2>
<span class="feed-count"></span></div><p class="undated-note">Publication dates come from
source metadata. Pages without a reliable publication date appear after dated entries.</p>
<ul class="feed">{''.join(feed_items)}</ul><p class="empty-state" hidden>No pages match these filters.</p>
</section></div></main>"""
    (output_dir / "index.html").write_text(
        _page("Archived publications", index_body),
        encoding="utf-8",
    )
    logo_options = (
        ("facet-outline-color", "Facet outline · color", "Facet’s original 3D movement with three colored outlines."),
        ("facet-outline-ink", "Facet outline · ink", "Facet’s original 3D movement in the page ink color."),
        ("facet-outline-color-ghost", "Facet ghost · color", "Transparent 3D Facet planes that pass through one another."),
        ("facet-outline-ink-ghost", "Facet ghost · ink", "Transparent 3D Facet planes in the page ink color."),
        ("prism-outline-color", "Prism outline · color", "Prism’s original 3D geometry with three colored outlines."),
        ("prism-outline-ink", "Prism outline · ink", "Prism’s original 3D geometry in the page ink color."),
        ("prism-outline-color-ghost", "Prism ghost · color", "Transparent Prism planes with colored outlines."),
        ("prism-outline-ink-ghost", "Prism ghost · ink", "Transparent Prism planes in the page ink color."),
        ("cathedral-adaptive", "Cathedral · adaptive", "Epitome link and quiet colors in Cathedral’s original emphasis ratio."),
        ("cathedral-ink", "Cathedral · ink", "Cathedral’s two triangles using strong and quiet page ink."),
        ("cathedral", "Cathedral · original", "The original warm gold and stone strokes on Epitome’s background."),
        ("outline-color", "Planar · cool", "Blue, turquoise, and purple outlines rotating in one plane."),
        ("outline-ink", "Planar · ink", "Monochrome outlines rotating in one plane."),
        ("outline-dusk", "Planar · dusk", "Indigo, rose, and amber outlines rotating in one plane."),
        ("facet", "Facet", "The translucent three-plane crystal."),
        ("prism", "Prism", "Nested crystalline diamonds."),
        ("orbit", "Orbit", "Three wireframe orbital planes."),
    )
    logo_choices = "".join(
        f'''<label class="logo-choice"><input type="radio" name="site-logo" value="{kind}">
{crystal_markup(kind)}<span><strong>{escape(name)}</strong>
<small>{escape(description)}</small></span></label>'''
        for kind, name, description in logo_options
    )
    preview_source = source_records.get("semianalysis", {})
    preview_url = escape(str(preview_source.get("logo_url", "")), quote=True)
    settings_body = f"""
<main><a class="article-back" href="/">← Archived publications</a>
<h1 class="page-title">Site settings</h1>
<div class="page-tabs"><div class="tabs-left"><span class="selected">Appearance</span></div></div>
<p class="site-note">Settings are saved in this browser and apply immediately.</p>
<section class="settings-section"><h2>Epitome mark</h2>
<div class="logo-grid" aria-label="Epitome logo choices">{logo_choices}</div></section>
<section class="settings-section"><h2>Appearance</h2>
<div class="setting-row"><div><label for="theme-setting">Color theme</label>
<p>Follow the device theme or choose light or dark explicitly.</p></div>
<div class="setting-control"><select id="theme-setting"><option value="system">System</option>
<option value="light">Light</option><option value="dark">Dark</option></select></div></div>
<div class="setting-row"><div><label for="source-border-setting">Borders around source logos</label>
<p>Add a one-pixel frame around each publication’s source mark.</p></div>
<div class="setting-control"><span class="source-mark source-semianalysis" aria-hidden="true">
<span>SA</span><img src="{preview_url}" alt="" onerror="this.remove()"></span>
<input id="source-border-setting" type="checkbox" aria-label="Borders around source logos"></div></div>
</section></main>"""
    settings_page = _page("Site settings", settings_body)
    (output_dir / "settings.html").write_text(settings_page, encoding="utf-8")
    # Keep the previous comparison URL useful for existing bookmarks.
    (output_dir / "logo-variants.html").write_text(settings_page, encoding="utf-8")
    return {
        "articles": len(entries),
        "pages": len(pages),
        "sources": len(used_sources),
        "complete": complete_count,
        "errors": error_count,
    }
