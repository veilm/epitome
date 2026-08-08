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

## First varied batch

The first 15-page batch is stored at:

`/mnt2/capsule/epitome/peter-steinberger/crawls/1786164877`

All 15 manifests completed, all capture tabs closed, and the network logs had no
capture errors. Together with the representative validation capture, 16 of the
116 reviewed core identities are archived. Five varied replays—the homepage and
articles from 2014, 2016, 2020, and 2026—were checked at a 1440×900 desktop
viewport. Their text, ordinary images, old and current layouts, and long-form
content rendered locally, and the audit generated no production-origin network
requests.

Two inline image URLs returned HTTP 404 at the live origin:

- The 2016 iWork collaboration image was recovered from the article's surviving
  canonical copy on Nutrient. The substitute is preserved under
  `/mnt2/capsule/epitome/peter-steinberger/dependencies/` and a reviewed alias in
  `inventories/resource-aliases.json` restores it only when the original URL has
  no captured body.
- The 2020 `fruta-swiftui/instruments.png` image is absent from the current
  public source repository. Exact URL checks for both the current `steipete.me`
  location and the article's historical `steipete.com` source found no Wayback
  capture. It remains a documented one-image preservation gap; the rest of that
  10,384-character article and its other large screenshot replay correctly.

The 2016 page also exposed a generic replay defect: Twitter's script-built frame
became a blank rectangle when scripts were removed. Capture indexing now recovers
the original server-rendered `twitter-tweet` blockquote by status ID and replay
uses its preserved text in place of the iframe. The audited tweet now shows its
full quotation, author, link, and date without running Twitter code.

The next bounded batch should be selected against the full Peter archive root,
use a longer inter-page delay, and skip these 16 complete identities.
