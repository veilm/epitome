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

Observed inventory date: 2026-09-16.
