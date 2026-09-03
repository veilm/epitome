# Cyborgism Wiki

## Public validation and N+1 pilot

The canonical first-party site is `https://cyborgism.wiki/`. Its public home
rendered as `Home` with approximately 19,970 visible body characters, stable
first-party CSS/JavaScript, no iframe, and no account requirement for the
visible content. The home navigation exposes canonical wiki, glossary,
categories, profiles, all-hyphae, and bibliography routes. A representative
`https://cyborgism.wiki/hypha/cyborgism` page rendered as `Cyborgism` with
approximately 3,531 visible characters, five images, 43 links, and no iframe.
Login and random routes are excluded from the public archive.

The seven-route pilot is prepared in ignored
`data/cyborgism-wiki-pilot.txt`. It uses the standard public settings: CDP port
2103 only, 15-second settle, 120-second page limit, 400-asset limit, two-second
asset pacing, 90-second asset timeout, and 30 seconds between pages. The exact
YouTube/Twitter/X asset exclusions remain in force. At the pilot boundary,
require complete tab-closed manifests, substantive wiki text, image and
attachment classification, both image audits, and local-only replay of early,
middle, late, list/category, and image-bearing pages.

The next low-risk scope is prepared while this pilot runs: a seven-route
Generative Ink pilot covering the public home, posts index, about page,
prophecies, two representative posts, and an image-rich post. Its animated
home surface will be treated as a bounded static/image check; no external
media downloader is permitted.

## Pilot result

The seven-route pilot completed at
`/mnt2/capsule/epitome/cyborgism-wiki/crawls/1788441785-wiki-pilot`.
All seven manifests are complete and tab-closed; `finish` reports
`failures=0`. The capture recorded 87 requests, 80 response bodies,
60,347,830 response bytes, and seven response-body errors. Every error is the
same non-content `https://cyborgism.wiki/static/favicon.ico` 404, repeated
once per page. The home, hypha, glossary, categories, profiles, list, and
bibliography pages all have substantive saved text; the list is a structured
693-link page rather than an article.

The capture discovered 80 asset references and attempted 41: 34 completed and
seven failed. All seven failures are the same missing favicon; there were zero
exclusion decisions. The bibliography's three public PDF references from
`cba.mit.edu`, `content.wolfram.com`, and `files.eric.ed.gov` completed as
ordinary linked reference assets, while the local SVG icons also completed.
The interactive-media ledgers report zero discovered, embedded, activated, or
result-level media. No YouTube or Twitter/X downloader was invoked, and no
excluded-host URL appears in an asset or media result.

Both primary-image and all-rendered-image audits report seven pages with zero
missing images, repairs, or repair failures. Five patched local replays covered
the home (19,970 visible characters), image-bearing Cyborgism hypha (3,531
characters and five complete images), categories (628 characters), the long
all-hyphae list (14,177 characters and 693 links), and bibliography (3,357
characters and 87 links). Their 18 requests were all local 200s, with zero
response-body errors and zero production-origin requests.

The bounded Cyborgism pilot is complete; expansion of the wiki inventory is
deferred while the prepared Generative Ink pilot runs.
