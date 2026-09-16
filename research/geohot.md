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
