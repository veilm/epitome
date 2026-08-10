# Next static sources

Checked through Chromium/CDP on 2026-08-09 while the final SemiAnalysis batch
was running. This was a four-navigation reconnaissance only; no crawl was
started.

## Priority rule

After an active page crawl completes, prefer the easiest bounded static source
that is already understood. Twitter/X and YouTube are intentionally deferred:
they need source identity, media, incremental-update, and deletion-history
design rather than treatment as ordinary static pages.

## AI 2027

`https://ai-2027.com/` is the recommended next source. The rendered English
homepage contains the complete scenario and links to a summary, research
supplements, an about page, a first-party PDF, footnotes, alternate languages,
and AI 2040. The homepage exposed about 140 same-host links, many of which are
section anchors or translated variants rather than distinct English documents.

The site does not expose a usable `/sitemap.xml`, so its rendered navigation was
used as the bounded authority. The resulting 13-URL English inventory is tracked
in `sources/ai-2027.txt`: the main scenario, summary, research index, five
forecast supplements, slowdown and race endings, footnotes, about page, and
PDF. Old `/supplements/<name>` links redirect to the corresponding
`/research/<name>` pages and are excluded as aliases. Translations and the
separate `https://ai-2040.com/` site remain adjacent scopes so the first batch is
easy to audit.

### Homepage validation

The long homepage was captured through CDP at:

`/mnt2/capsule/epitome/ai-2027/validation/1786300694-home`

The manifest is complete and its tab closed. The run retained a 1.9 MB rendered
document and 114 responses (18,873,312 body bytes); bounded asset completion
recovered all 75 missing references with two-second spacing. Primary and
all-image audits report zero omitted ordinary images.

The first offline screenshot nevertheless exposed three broken timeline icons:
they were SVG `<image href>` resources, which the older replay rewriter did not
localize and the ordinary `<img>` audit could not see. Replay now localizes both
`href` and legacy `xlink:href` on SVG image elements, with a regression test.
The corrected desktop replay contains about 50,000 visible characters, 17
ordinary images, six localized SVG image instances, and zero broken ordinary
images. Its strict audit recorded 26 requests, all to the temporary local replay
server, and the audit tab was closed.

The page also offers a narrated-scenario MP3 and links to one YouTube companion
video. The initial MP3 range response timed out during network-body capture, so
both are explicit external imports in `inventories/ai-2027-media.json` rather
than being treated as complete page assets. The page archive is otherwise ready
for its small batch after SemiAnalysis; use the validated longer page budget
(120 scrolls and 120 seconds) for the scenario and endings.

### Completed bounded scope

The remaining 12 identities completed with 30-second inter-page spacing at:

`/mnt2/capsule/epitome/ai-2027/crawls/1786340042`

Together with the homepage pilot, all 13 approved identities have complete
manifests and closed capture tabs. There were no capture failures, and repeated
primary and all-rendered-image audits report zero missing resources. The PDF
capture contains the actual 8,863,479-byte PDF 1.7 document with 71 A4 pages,
not merely Chromium's viewer shell.

The first multi-page replay audit exposed one real script-disabled layout bug:
six Security Forecast images with the site's `h-[100%]` utility class expanded
to the entire grid-track height, creating roughly 25,874-pixel figures and large
blank gaps. A replay rule scoped to `ai-2027.com` now restores intrinsic image
height. Its dimensions match the live page, and a regression test prevents the
rule from affecting other sources.

The corrected desktop audit covered the scenario, summary, Security Forecast,
both endings, footnotes, and the locally served PDF. HTML pages retained
8,929–83,103 visible characters with zero broken images; the scenario graphs
and repaired security timelines render at their expected sizes. The strict log
recorded 692 requests to the temporary local server plus Chromium's internal
PDF-viewer stylesheet, with no production-origin request. Audit tabs were
closed afterward. The direct narration remains the only current non-YouTube
media import; YouTube was not fetched.

## Andrej Karpathy

`https://karpathy.ai/` is a distinct first-party property from the completed
`https://karpathy.github.io/` blog. It is not a second copy of that dated blog:
it is Karpathy's compact personal and educational homepage. The inspected page
links directly to three same-host resources:

- `https://karpathy.ai/zero-to-hero.html`
- `https://karpathy.ai/books.html`
- `https://karpathy.ai/stateofgpt.pdf`

Inventory and preserve this small property separately. Outbound YouTube,
GitHub, papers, and social links should remain provenance-bearing dependencies,
not silently expand the page scope.

The four reviewed first-party identities are tracked in
`sources/andrej-karpathy-site.txt`. Begin with the homepage as a bounded pilot,
then capture the two HTML resource pages and underlying presentation PDF if its
layout, assets, and offline replay validate normally. YouTube remains excluded
from the page crawl.

## Paul Graham

`https://paulgraham.com/articles.html` is a simple static essay index with about
249 same-host links and roughly 255 links overall at inspection time. It is a
good later static source, but larger than AI 2027. Build a reviewed essay list
from the index and separate books, Lisp/Arc material, FAQs, RSS, and other site
sections before crawling.

Y Combinator is deliberately not included in the current backlog expansion.

## Gwern

`https://gwern.net/` is a rich first-party index with about 555 same-host links
at inspection time. It spans major essays, a blog, site documentation, and a
large first-party document/link collection. Preserve it in reviewed families
rather than treating every internal link as one immediate crawl. Its static
presentation makes it tractable after inventorying, but its breadth puts it
behind the smaller AI 2027 and Karpathy scopes.

## Import AI

`https://importai.substack.com/` is Jack Clark's current Import AI newsletter
home. Chromium exposed the canonical URL and the publication title “Import AI |
Jack Clark | Substack.” Preserve it as a distinct writer/newsletter source with
an explicit relationship to Anthropic, not as part of the official company-site
inventory. Review the Substack archive, feeds, attachments, outbound papers,
and possible email/public-body differences before defining its batch.

## Scott Alexander's two archives

`https://slatestarcodex.com/` remains the historical Slate Star Codex site.
`https://www.astralcodexten.com/` is the successor Astral Codex Ten Substack,
whose rendered canonical metadata identifies Scott Alexander. They should be
inventoried and archived separately, with cross-era redirects and links
recorded so the public catalog can present the relationship without conflating
their identities.
