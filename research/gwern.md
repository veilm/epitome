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
