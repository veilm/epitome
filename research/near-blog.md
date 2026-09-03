# near.blog

## Public validation and N+1 pilot

The canonical first-party site is `https://near.blog/`. Its public WordPress
home rendered as `near.blog` with approximately 2,102 visible body characters,
35 links, no images, and no iframe, video, or audio element. Representative
public routes are stable server-rendered pages: `/links/` is a 24,397-character
271-link index; `/things/` is a 10,308-character list with 69 images; and
`/heavenbanning/` is a 499-character illustrated post. Additional plain-text
posts include `/llms-are-strangely-shaped-tools/` (3,015 characters) and
`/2024-ai-reflections/` (10,255 characters). `/Glyptodons/` is a small
image-bearing post with one observed missing image, which is retained as a
bounded known-missing-image check.

The prepared N+1 pilot is in ignored `data/near-blog-pilot.txt`. It covers the
home, link index, list page, short illustrated post, two text posts, and the
known-missing-image post. The separate `/this-anime-does-not-exist/` page is
deferred because validation found direct video elements and many historical
`nearcyan.com` image references; it requires a separately bounded media scope.
No account or paywall bypass is in scope. The standard public settings apply:
CDP port 2103 only, 15-second settle, 120-second page limit, 400-asset limit,
two-second asset pacing, 90-second asset timeout, and 30 seconds between
pages. Exact YouTube/Twitter/X asset exclusions remain in force. At the pilot
boundary, require substantive text, image and missing-image classification,
media/redirect classification, and local-only replay with no live-origin
fallback.

## Seven-route pilot validation

The bounded pilot completed on 2026-09-03 at
`/mnt2/capsule/epitome/near-blog/crawls/1788452985-pilot`. All seven manifests
are complete and tab-closed; the terminal `finish` record reports
`failures=0`. The capture recorded 197 requests, 182 response bodies,
5,077,405 response bytes, and seven response-body errors. The statuses were
175 HTTP 200 page/dependency responses, eight HTTP 204 Cloudflare RUM beacon
records, and fourteen HTTP 403 records for the repeated `/matomo/m.js`
telemetry endpoint (one browser response and one asset-completion response per
route). The seven body errors are the asset-completion attempts for that same
Matomo endpoint; they do not affect the captured public documents.

Asset completion discovered 175 references and attempted all of them: 61
completed in this run, 107 were already complete, and seven failed. Every
asset failure is the same HTTP 403 Matomo telemetry script; there were zero
excluded assets and 2,748,284 downloaded bytes. The seven interactive-media
ledgers contain zero discovered, embedded, activated, or result-level media.
The 68 asset-result URLs are all first-party `near.blog` URLs; exact checks
found zero result URLs on the prohibited YouTube/Twitter/X hosts.

Both primary-image and all-rendered-image audits report seven pages, zero
missing images, zero repair attempts, and zero repair failures. Local-only
loopback replays covered all seven routes: the home, link index, 69-image
`/things/` list, illustrated `/heavenbanning/` post, two text articles, and
the known-missing-image `Glyptodons` post. They retained 499–24,397 visible
characters and 0–69 rendered images, with zero broken images, frames, video,
or audio elements. A CDP network logger recorded 107 requests, all to
`127.0.0.1:8034`, with zero non-loopback requests. This validates the bounded
WordPress capture and replay path; the direct-video
`/this-anime-does-not-exist/` route remains deferred to a separate media scope.
