# Greg Brockman blog

## Scope decision

Greg Brockman's public blog at `https://blog.gregbrockman.com/` is approved as
a low-risk source. Its rendered home page and rendered `/page/2` listing expose
17 canonical post URLs. The tracked scope in `sources/greg-brockman-blog.txt`
contains those posts plus the public home, feed, and second listing routes,
for 20 reviewed routes.

The site is a public SVBTLE-hosted blog with substantive post text, ordinary
static images, and no account or paywall requirement observed during inventory
review. The footer's X link is a reference only and is not part of the capture
scope.

## Capture plan

Run a bounded pilot covering home, feed, page 2, newest, middle, and oldest
post shapes. After image audits and local-only replays pass, capture the full
20-route reviewed list with archive-root deduplication. Future refreshes should
rediscover both rendered listing pages and capture only newly reviewed post
identities.

## Pilot validation

The seven-route pilot at `/mnt2/capsule/epitome/greg-brockman/crawls/1789604289-pilot`
completed with `finish.failures=0`; all seven manifests are complete and
tab-closed. The capture recorded 241 requests, 215 response bodies, zero
response-body errors, and only HTTP 200/204 responses. Asset handling recorded
134 discovered candidates, 35 attempted and completed assets, zero failures,
zero exclusions, and no interactive media. The exact prohibited-host result
URL audit was empty.

Both primary and all-rendered-image audits found zero missing images across
all seven pages. A local-only replay of home, feed, page 2, newest, middle,
image-bearing, and oldest routes preserved substantive text and rendered
images; its 144 requests stayed on `127.0.0.1` with no live-origin fallback.

The full deduplicated 20-route capture is therefore approved to proceed.

## Full capture result

The full run at `/mnt2/capsule/epitome/greg-brockman/crawls/1789605847-all-20`
captured the 13 routes not already covered by the pilot. It completed 13/13
with `finish.failures=0`; every new manifest is complete and tab-closed. The
new-route network ledger contains 521 requests, 463 response bodies, and two
response-level body errors: an unavailable CloudFront PDF referenced by *The
OpenAI Mission* (DNS failure) and a 301/response-body capture record on
`/define-cto-openai`. These are optional reference/redirect records; the
article pages themselves completed normally. The observed statuses were 476
HTTP 200, 43 HTTP 204, one HTTP 301, and one unresolved optional reference.

The new routes discovered 282 asset candidates, attempted 68, completed 67,
and recorded one failed optional CloudFront PDF asset; there were zero
prohibited-host exclusions and zero interactive-media activations. Primary and
all-rendered-image audits both found zero missing images across the 13 new
pages. The combined 20-route local replay covered structural, early, middle,
reference-heavy, image-bearing, and late routes; all 128 replay requests stayed
on `127.0.0.1` with no live-origin fallback.

The reviewed 20-route public archive is complete. Future refreshes should
rediscover both rendered listing pages and capture only newly reviewed post
identities.

Observed inventory date: 2026-09-16.
