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
