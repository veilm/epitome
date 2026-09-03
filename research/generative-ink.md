# Generative Ink

## Public validation and N+1 pilot

The canonical first-party site is `https://generative.ink/`. Its public home
rendered as `— Moire` with a small animated/image surface, no iframe, and
approximately 102 visible body characters. The public `/posts/` index rendered
with approximately 3,656 visible characters, 13 images, and no iframe. A
representative post at
`https://generative.ink/posts/anomalous-tokens-reveal-the-original-identities-of-instruct-models/`
rendered with approximately 15,375 visible characters, five headings, 24
links, two images, no iframe, and no video/audio element.

The seven-route pilot is prepared in ignored
`data/generative-ink-pilot.txt`. It uses the standard public settings: CDP
port 2103 only, 15-second settle, 120-second page limit, 400-asset limit,
two-second asset pacing, 90-second asset timeout, and 30 seconds between pages.
The exact YouTube/Twitter/X asset exclusions remain in force. At the pilot
boundary, require complete tab-closed manifests, substantive text, static and
animated/image classification, both image audits, and local-only replay of
early, index, long-post, image-rich, and category-like pages.

## Pilot result

The seven-route pilot completed at
`/mnt2/capsule/epitome/generative-ink/crawls/1788445420-pilot`. All seven
manifests are complete and tab-closed; `finish` reports `failures=0`. The
capture recorded 2,951 requests, 2,895 response bodies, 78,981,769 response
bytes, and 56 response-body error records. The statuses were 2,895 HTTP 200,
seven HTTP 302, 28 HTTP 404, 20 pending body reads, and one unknown. The 28
404s are the four missing favicon variants repeated once per page. The other
28 body-read records are the expected redirect/unfinished external CSS,
JavaScript, and font retrievals, plus the single unavailable CloudFront PDF
reference that also accounts for the one unknown asset outcome.

The capture discovered 3,803 asset references and attempted the bounded 400
per page, yielding 2,771 completed assets and 29 failures. The failures are
exactly the 28 first-party favicon 404s and the DNS-unavailable
`d4mucfpksywv.cloudfront.net` language-model PDF. There were zero exclusion
decisions and zero excluded-host asset results. The completed external assets
included the ordinary `cdnjs.cloudflare.com` flag resources and
`unpkg.com/scrollreveal`, plus public PDF references from
`intelligence.org` and `www.princeton.edu`; the first-party page, image, and
font resources were preserved as captured. The interactive-media ledgers
report zero discovered, embedded, activated, or result-level media. No
YouTube or Twitter/X downloader was invoked, and the public-only boundary was
not crossed.

Both primary-image and all-rendered-image audits report seven pages with zero
missing images, repairs, or repair failures. Local-only replays covered the
home animation surface (102 visible characters and one image), posts index
(3,656 characters and 13 images), anomalous-tokens long post (15,375
characters, five headings, and two images), simulators/reference post (82,754
characters, 26 headings, and four images), image-rich museum post (3,565
characters, 32 headings, and 32 images), and prophecies/category page (111,130
characters, 33 headings, and one image). All six replay documents retained
substantive content with zero broken images, frames, video, or audio. Their 91
resource requests were loopback-only, with zero production-origin requests.

The bounded Generative Ink pilot is complete; the active lane advances to the
prepared one-route `alien.v01d.zone` pilot.
