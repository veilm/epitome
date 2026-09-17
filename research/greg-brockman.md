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

Observed inventory date: 2026-09-16.
