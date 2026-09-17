# Sam Altman blog

## Scope decision

Sam Altman's public blog at `https://blog.samaltman.com/` is approved as a
low-risk source. The rendered homepage links to 13 paginated public listing
views, from the home page through `?page=13`; those views expose 121 unique
post URLs after normalizing legacy HTTP links to HTTPS and deduplicating
overlaps. The public `/archive` and `/posts.atom` routes are retained as
structural/feed verification routes.

The tracked scope in `sources/sam-altman-blog.txt` is 136 routes: 121
canonical posts, the home/archive/feed routes, and the 12 non-home paginated
listing routes. The Atom feed observed during review contained 30 recent
entries and is not used as the sole inventory. The archive page supplies
dated navigation but the paginated listings provide the reviewed article
identities.

## Boundary and observed shape

The site is public Posthaven-hosted content with substantive post text and
some images/embedded frames. Posthaven dashboard, sign-in, logout, and other
administrative paths were excluded; external references are not expanded.
Application/authenticated access is not needed for the public posts. Keep the
public-only boundary and treat any monetization, telemetry, or embedded-media
requests as optional dependencies to classify rather than grounds to cross an
access boundary.

## Capture plan

Run a bounded pilot across the home/archive/feed/listing surfaces and
newest/middle/oldest post shapes. After representative image/media audits and
local-only replays pass, capture the full 136-route reviewed list with
archive-root deduplication. Future refreshes should review all 13 listing
views, compare canonical post identities against the archive, and capture only
new public posts.

## Pilot validation

The seven-route pilot at `/mnt2/capsule/epitome/sam-altman/crawls/1789607898-pilot`
completed with `finish.failures=0`; all seven manifests are complete and
tab-closed. It recorded 276 requests, 264 response bodies, and six repeated
response-level 404s for the optional legacy
`/assets/images/loading128.gif` path. Asset handling recorded 222 discovered
candidates, 103 attempted, 97 completed, six failed (the same missing loading
GIF), zero prohibited-host exclusions, and no interactive media. The exact
prohibited-host result URL audit was empty.

Primary and all-rendered-image audits found zero missing images across the
seven pages. A local-only replay of the home, archive, Atom feed, newest,
middle, old, and oldest routes preserved substantive text and rendered images;
its 138 requests stayed on `127.0.0.1` with no live-origin fallback. The pilot
therefore approves the full deduplicated 136-route public scope, while keeping
Posthaven administrative/authentication paths excluded.

Observed inventory date: 2026-09-16.
