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

## Second batch

The next 30 oldest uncaptured core identities were archived at:

`/mnt2/capsule/epitome/peter-steinberger/crawls/1786166787`

All 30 page manifests completed with zero capture errors. Twenty-nine recorded
tab closure directly; the one transient close failure was observed and closed
manually during the run, leaving the browser at its original three tabs. The CDP
helper now retries exact-session tab closure so a brief CLI collision does not
leave future capture tabs behind. The approved core scope is now 46/116 complete.

Seven asset-completion requests failed, but only three were inline page media:

- `swizzling-strict-msgSend.png` has an exact 2014 Wayback copy from the former
  `petersteinberger.com` origin;
- `UIPrinterSearchingView.png` has an exact 2014 copy from that origin; and
- `researchkit-animations.gif` has an exact 2015 copy from that origin.

All three historical bodies were imported through the browser under the private
`dependencies/` tree and are restored by reviewed aliases in
`inventories/resource-aliases.json`. The remaining failures are links rather
than inline media: three dead historical image URLs used as prose hyperlinks and
Apple's unavailable 2013 `Architecting_Modern_Apps_Part_2.pdf` citation. Their
original URLs and article context remain preserved for later citation recovery.

Five 1440×900 replays spanning 2012–2016 were inspected: `Moving On`, the two
restored 2014 image cases, `Researching ResearchKit`, and the media-heavy
`Running UI Tests on iOS With Ludicrous Speed`. All article text and inline
images rendered; the restored GIF animates; two old tweet embeds render their
preserved static quotations; and an archived 68.28-second Vimeo body reaches
browser ready-state 4 in a native local `<video>`. Vimeo recognition now uses
the player hostname as well as optional iframe titles, covering older titleless
embeds. The attached audit log contained 27 local requests and zero production-
origin requests or errors.

The next bounded batch should skip these 46 complete identities and use a longer
delay again. Seventy reviewed core identities remain.

## Third batch

The next 45 uncaptured core identities were archived at:

`/mnt2/capsule/epitome/peter-steinberger/crawls/1786170347`

All 45 manifests completed with zero page failures and recorded successful tab
closure, leaving only the browser's original three tabs. This raises approved
core coverage to 91/116 identities.

Four resource attempts failed in two articles. The 2018 Slack article's missing
`snooze.png` was recovered from its original PSPDFKit article as an exact 2018
Wayback body. Its linked emoji ZIP still exists under the corrected `/assets/img/`
path in Peter's public source tree and was captured there. Both private dependency
captures are restored by reviewed aliases in `inventories/resource-aliases.json`.
The article's Vimeo player returned HTTP 403 at the live source and exposed no
video body or progressive URL, so replay now replaces the otherwise misleading
internal 404 iframe with an explicit preservation-unavailable notice and retains
the source reference.

The 2020 `jailbreaking/hierarchy-spotify.png` screenshot is absent from the live
origin and every revision of the public source repository. Exact and wildcard
checks across `steipete.me`, `steipete.com`, and `petersteinberger.com` found no
Wayback body. It remains a documented second inline-image gap alongside the
earlier SwiftUI Instruments screenshot; the article's remaining images and all
9,371 characters of replay text are intact.

Five 1440×900 replays spanning 2016, 2018, 2020, and 2025 were inspected. The
recovered Slack screenshot and ordinary images render, the blocked Vimeo case is
clear rather than a broken frame, and the varied historical, image-heavy, and
current layouts retain their full text. The attached audit recorded 43 requests,
all to the local archive server, with no production-origin requests. The final
25 reviewed core identities remain.

## Final batch

The final 25 uncaptured core identities were archived at:

`/mnt2/capsule/epitome/peter-steinberger/crawls/1786176760`

All 25 manifests completed with successful tab closure and no page-level
capture errors. Selection against the full 116-URL source now returns zero
uncaptured identities. Together with the earlier runs, the reviewed core page
scope is complete.

The only initial asset failure was the 3h28m Vimeo workshop embedded in `The
Future of Vibe Coding`. Its adaptive stream exceeded the normal 90-second remux
limit, so a bounded single-page recovery with a one-hour media ceiling preserved
the full 2,350,638,280-byte H.264/AAC MP4 at:

`/mnt2/capsule/epitome/peter-steinberger/retries/1786180500-future-of-vibe-coding`

`ffprobe` reports 1920×1080 video and 12,503.72 seconds of video and audio. The
first replay attempt also exposed a general large-media defect: the HTTP server
read full resources into memory and answered Chromium's open-ended byte request
with the entire multi-gigabyte remainder. Replay now streams binary resources
from disk and caps open-ended responses to 16 MiB ranges. In a fresh Chromium
session the recovered video reached ready-state 4, reported its full duration
and dimensions, and advanced from 0 to 1.96 seconds during an actual play test.

Five final-batch pages were visually checked at 1440×900: the six-image
`Signature Flicker`, image-heavy `Peekaboo MCP`, the YouTube-bearing live Arena
session, the recovered long Vimeo workshop, and the unyeared Claude Code Army
alias. Images and full article text rendered, YouTube used the explicit
separate-import placeholder, and the long local video played. Both audit passes
made only localhost requests. Four pending YouTube identities across four
articles are recorded in `inventories/peter-steinberger-youtube.json`.
