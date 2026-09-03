# Gwern.net

## Public validation and N+1 pilot

Gwern.net was validated on 2026-09-03 as a large, first-party public site
whose link graph must be divided into bounded families. The homepage rendered
as `Essays · Gwern.net` with 13,265 visible characters, 12,935 article-text
characters, 560 links, and no images, broken images, frames, video, or audio.
The homepage exposed 458 same-origin link records and 409 unique same-origin
links after normalization. The visible graph includes essay, blog, document,
and fiction families, so the whole graph is explicitly out of scope for the
first capture.

The representative public routes were:

1. `https://gwern.net/` — homepage/index surface.
2. `https://gwern.net/about` — 74,188 visible characters, 73,859 article-text
   characters, 634 links, three images, and two known missing images.
3. `https://gwern.net/blog/index` — 6,156 visible characters, 5,957
   article-text characters, and 210 links.
4. `https://gwern.net/doc/newest/index` — 21,765 visible characters, 21,436
   article-text characters, and 326 links.
5. `https://gwern.net/scaling-hypothesis` — 109,883 visible characters,
   109,554 article-text characters, 686 links, ten images, and nine known
   missing images.
6. `https://gwern.net/fiction/walking` — 2,977 visible characters, four
   images, and one known missing image.
7. `https://gwern.net/blog/2026/face-training` — 8,770 visible characters,
   8,441 article-text characters, and 56 links.

The direct-video `https://gwern.net/embryo-selection` route was deliberately
deferred. Validation found 542,641 visible characters, 20 images with 19
known missing images, and one direct video; it belongs in a separately
bounded media scope rather than the ordinary page lane. The pilot has no
account or paywall bypass in scope. Validation observed 102 HTTP 200, ten
HTTP 204, and 27 pending network records; third-party hosts were limited to
the observed analytics/tagging and `invertornot.com` telemetry/reference
requests. No prohibited YouTube/Twitter/X URL was observed.

The prepared, ignored N+1 list is `data/gwern-pilot.txt`. It uses the standard
public settings: CDP port 2103 only, 15-second settle, 120-second page limit,
400-asset limit, two-second asset pacing, 90-second asset timeout, and 30
seconds between pages. Exact asset exclusions are
`www.youtube-nocookie.com`, `www.youtube.com`, `youtube.com`, `pbs.twimg.com`,
`video.twimg.com`, `twitter.com`, `www.twitter.com`, `x.com`, and `www.x.com`.
No YouTube or Twitter/X downloader may be invoked, and incidental media
variants are not intentionally fetched.

At the pilot boundary, require substantive text and image preservation,
classification of the known missing images, redirects, PDFs and other
dependency/media records, primary and all-rendered-image audits, and
representative local-only replays across the index/about, blog/document,
long-essay, fiction, and recent-blog shapes. Replays must show substantive
content and no live-origin fallback. The direct-video and larger media-heavy
families remain deferred until this bounded pilot passes.

## Seven-route pilot result

The bounded pilot completed on 2026-09-03 at
`/mnt2/capsule/epitome/gwern/crawls/1788457866-pilot`. All seven manifests are
complete and tab-closed; the `progress.jsonl` finish record reports
`failures=0`. The aggregate capture recorded 1,481 requests, 1,474 response
bodies, zero response-body errors, 183,825,839 response bytes, 1,474 HTTP 200
responses, and seven HTTP 204 telemetry responses. The observed hosts were
`gwern.net` (1,433 requests), `www.googletagmanager.com` (14),
`analytics.google.com` (7), `www.google-analytics.com` (7),
`www.google.ca` (7), `invertornot.com` (5), `arxiv.org` (4), and one request
each to `cdn.openai.com`, `www.andrew.cmu.edu`, `www.microsoft.com`, and
`www.princeton.edu`. The external requests are classified as telemetry,
first-party references, or linked public PDFs; they did not change the public
page boundary.

Per-page completion and asset outcomes were:

| Route | Requests / bodies / errors | Assets discovered / attempted / complete / existing / failed / excluded | Media |
| --- | ---: | ---: | --- |
| `/` | 199 / 198 / 0 | 189 / 173 / 173 / 16 / 0 / 0 | 0 discovered, 0 embedded, 0 activated |
| `/about` | 213 / 212 / 0 | 196 / 170 / 170 / 26 / 0 / 0 | 0 / 0 / 0 |
| `/blog/index` | 195 / 194 / 0 | 189 / 175 / 175 / 14 / 0 / 0 | 0 / 0 / 0 |
| `/doc/newest/index` | 216 / 215 / 0 | 203 / 179 / 179 / 24 / 0 / 0 | 0 / 0 / 0 |
| `/scaling-hypothesis` | 249 / 248 / 0 | 232 / 208 / 208 / 24 / 0 / 0 | 0 / 0 / 0 |
| `/fiction/walking` | 206 / 205 / 0 | 192 / 172 / 172 / 20 / 0 / 0 | 0 / 0 / 0 |
| `/blog/2026/face-training` | 203 / 202 / 0 | 193 / 175 / 175 / 18 / 0 / 0 | 0 / 0 / 0 |

Across the routes, asset completion discovered 1,394 references and attempted
1,252: 1,252 completed, 142 already complete, zero failed, zero excluded,
and 151,983,107 downloaded bytes. The eight non-Gwern asset-result URLs were
all public PDFs: four from arXiv and one each from OpenAI, Carnegie Mellon,
Microsoft, and Princeton. Every asset result was complete and there were zero
result URLs on the exact YouTube/Twitter/X exclusion hosts. The seven
interactive-media ledgers contain zero discovered, embedded, activated, or
result-level media. No downloader was invoked and no incidental media variant
was intentionally fetched.

Both primary-image and all-rendered-image audits report seven pages, zero
missing images, zero repair attempts, and zero repair failures. The validation
phase had identified candidate missing images on `/about`,
`/scaling-hypothesis`, and `/fiction/walking`; the captured responsive and
archived representations resolved them for offline replay. The known
`/embryo-selection` direct-video route was not included and remains deferred.

Local-only CDP replays covered all seven routes. They retained 6,156–109,883
visible characters and 0–10 rendered images per route; all seven had zero
broken images, frames, video, or audio elements. A replay network logger
recorded 216 requests, all to `127.0.0.1:8036`: 125 HTTP 200 responses, 15
HTTP 400 responses, and 76 pending local font reads when the logger stopped.
The 400s were repeated requests for the decorative root-relative
`/static/img/logo/logo-smooth.svg` and
`/static/img/ornament/sequential-nav-icons-arabesque.svg` references in the
replay layer, not substantive page or content-image failures. There were zero
non-loopback and zero production-origin requests, so no live-origin fallback
occurred.

The next bounded family is prepared in ignored
`data/gwern-major-essays-next-12.txt`. It contains twelve unique first-party
essay routes taken from the captured homepage inventory and deduplicated
against the seven-route pilot: `/lean-scaling`, `/guardian-angel`,
`/llm-catapult`, `/generating-style`, `/vaping`, `/rl-children`,
`/complement`, `/banner`, `/face`, `/subculture`, `/improvement`, and
`/math-error`. The direct-video `/embryo-selection` route, `/twitter`, and
other media-heavy or non-essay families remain excluded from this next page
lane. Before starting that family, repeat the standard 2103-only settings and
the exact eight-host exclusions, then require the same page, asset, media,
image-audit, and local-only replay checks.
