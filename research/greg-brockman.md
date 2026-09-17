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

Observed inventory date: 2026-09-16.
