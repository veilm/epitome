# Peter Steinberger source reconnaissance

Investigated through Chromium on CDP port 2103 at Unix timestamp `1786162142`.
This defines a bounded first-party blog scope; it does not yet claim that every
Peter Steinberger publication, talk, social post, or project page is covered.

## Canonical properties

- `https://steipete.me/` is the canonical rendered blog. Requests to
  `steipete.net` redirect there.
- `https://steipete.me/robots.txt` names
  `https://steipete.me/sitemap-index.xml` as the sitemap entry point.
- `https://steipete.me/rss.xml` is the first-party RSS feed.
- `https://www.steipete.md/` is an official plain-Markdown mirror. A request for
  the representative post redirected to the same path with a `.md` suffix and
  returned `text/markdown`. It is a useful model-readable source, but it should
  supplement rather than replace preservation of the rendered site.
- The rendered site's footer links the public source repository at
  `https://github.com/steipete/steipete.me`. That repository is useful
  supplementary provenance, but the website capture remains the replay source.

## Inventory boundary

The sitemap index contained 413 URL identities across two sitemap documents at
the investigation timestamp:

- 112 individual `/posts/...` article URLs;
- 11 `/posts` archive-index pages, including the first page;
- 11 parallel `/page/...` archive-index pages;
- 275 tag pages; and
- the homepage, About, search, and tag-index pages.

The tracked first crawl scope in `sources/peter-steinberger-blog.txt` contains
116 URLs: the homepage, About, all-posts index, RSS feed, and all 112 individual
article URL identities. The redundant paginated indexes, search page, and tag
archives are intentionally deferred. They contain useful historical navigation
metadata and can be added as a second bounded phase after the primary content is
preserved.

Some recent articles have both year-prefixed and unprefixed sitemap identities.
Both are retained in the source list until capture and redirect manifests prove
which identities are aliases; deduplication should be based on completed final
URLs rather than guessed from similar slugs.

## Representative capture

`Shipping at Inference-Speed` was captured at:

`/mnt2/capsule/epitome/peter-steinberger/validation/1786162224`

The capture completed with 17 response bodies, 731,808 archived body bytes, and
all three initially missing referenced assets recovered. Desktop replay retained
the full 18,831-character article body, produced no visibly failed images, and
loaded browser resources only from `127.0.0.1:8013`.

The same article's Markdown mirror returned 20,610 characters of clean Markdown.
That makes the mirror a promising optional input for later extraction quality
checks, while the archived rendered page remains authoritative for visual and
asset preservation.

## Next crawl

After the active Karpathy crawl finishes, select against
`/mnt2/capsule/epitome/peter-steinberger` so the validated article is skipped.
Begin with a bounded varied batch and generous spacing, then audit old and new
site-era layouts before expanding through the remaining source list.
