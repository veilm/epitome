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

## Full capture result

The full run at `/mnt2/capsule/epitome/sam-altman/crawls/1789609315-all-136`
completed all 129 routes not covered by the pilot with `finish.failures=0`.
Together with the seven pilot routes, all 136 reviewed public routes have
complete, tab-closed manifests. The full run recorded 5,726 summarized
requests, 5,457 response bodies, and 138 response-level body errors. The
metadata records normalize to 137 HTTP 404 records and two pending records;
the two pending records are duplicate status records for the same old Google
image whose asset requests ultimately returned 404.

Asset handling recorded 4,668 discovered candidates, 2,207 attempted assets,
2,071 completed assets, 136 failed assets, zero policy exclusions, and
17,565,698 downloaded bytes. The 136 failures are fully classified: 129
repeated optional `https://blog.samaltman.com/assets/images/loading128.gif`
404s; two references to the same unavailable California housing PDF; two
references to the same unavailable Google-hosted image; two Box viewer
requests for the same unavailable public document view; and one 90-second
Google Fonts asset timeout. The four Box 404 response records and the two
pending Google-image records are repeated network-level observations of those
asset outcomes, not page-capture failures. All 129 page manifests remained
complete, and interactive media discovery/activation was zero.

The exact prohibited-host result audit was empty. Incidental share and
telemetry requests, including `platform.twitter.com`, two
`syndication.twitter.com` image/GIF records, and Facebook telemetry, were
observed as browser dependencies only; no social-media variants were
intentionally fetched and no YouTube/Twitter/X downloader was invoked.

Primary and all-rendered-image audits found the same two known missing legacy
Google-hosted images on `?page=5` and `/affordable-care`; all other audited
rendered images were present. These are classified source-side missing assets,
not capture-level failures. A 12-route local-only replay covered home, archive,
Atom feed, listing pages (including the missing-image page), newest, middle,
image/article, comment-bearing, old, missing-image article, and oldest shapes.
It preserved substantive text and local assets; all 362 replay metadata
records used `127.0.0.1`, with no live-origin request and no prohibited-host
result.

The reviewed 136-route public archive is therefore complete. Future refreshes
should re-review the home/archive/Atom and 13 listing views, deduplicate their
canonical post identities against this archive, and capture only genuinely new
public posts. Posthaven administrative/authentication paths remain excluded.
