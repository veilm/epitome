# George Hotz blog

## Scope decision

George Hotz's public Jekyll blog at `https://geohot.github.io/blog/` is an
approved low-risk source. The rendered homepage is the authoritative reviewed
inventory for this site: it exposed 143 canonical post URLs, ordered newest to
oldest, plus the public home, About, and feed routes. The feed is a limited
Jekyll feed and is not a complete post inventory.

The tracked scope is therefore 146 routes in `sources/geohot-blog.txt`:

- 143 canonical `/blog/jekyll/update/YYYY/MM/DD/*.html` posts;
- `/blog/`, `/blog/about/`, and `/blog/feed.xml` as structural verification
  routes.

## Boundary and observed shape

The site is public static/Jekyll content with substantive article text and
first-party image references on some posts. The reviewed newest, middle, and
oldest examples rendered article text successfully; the oldest example had
three first-party images. Footer social links, including Twitter/X, are
references only and must not be fetched as incidental media.

Keep the ordinary page lane public-only. Do not open account/authenticated
routes, invoke media downloaders, or intentionally fetch incidental media
variants. Apply the standard exact YouTube/Twitter/X asset exclusions.

## Capture plan

Run the bounded rendered pilot first across the structural routes and
newest/middle/oldest post shapes. After its audits and local-only replays pass,
capture the complete 146-route reviewed list with full-archive deduplication.
Future refreshes should rediscover the rendered homepage, compare canonical
post identities against the archive, and capture only newly reviewed public
identities.

Observed inventory date: 2026-09-16.

## Pilot result

The seven-route pilot at
`/mnt2/capsule/epitome/geohot/crawls/1789593539-pilot` completed with
`finish.failures=0`. All seven requested and final URLs stayed on
`geohot.github.io`; the ledger recorded 30 HTTP 200 responses and no
response-body errors. The pilot discovered 17 first-party assets, with zero
asset failures and zero policy exclusions, and recorded no interactive media.
The primary and all-rendered-image audits each reported seven pages and zero
missing images.

Representative loopback replays covered the home/index surface, the newest
post, a middle image-rich post, and the oldest image-rich post. They preserved
substantive text and rendered images locally. The replay network log contained
20 requests, all to `127.0.0.1:8127`; four optional social-icon requests
returned local 400s because their legacy relative SVG path was not rewritten,
but there was no live-origin fallback.

The complete reviewed archive is now ready to run as the next bounded capture:
the pilot routes will be deduplicated against the same archive root, and the
remaining reviewed routes will be captured with the same public-only limits.
