# Dwarkesh Podcast source reconnaissance

Investigated through Chromium on CDP port 2103 at Unix timestamp `1786164897`.
This defines the first-party publication scope and a representative preservation
test. It does not include the separate YouTube channel or podcast-platform
copies as independent crawl sources.

## Discovery and scope

`https://www.dwarkesh.com/` is a custom-domain Substack publication. Its
`robots.txt` allows ordinary public crawling and identifies both
`sitemap.xml` and `news_sitemap.xml`. The main sitemap contained 181 URLs at the
investigation timestamp:

- 178 `/p/...` post identities;
- `/archive`;
- `/about`; and
- `/podcast`.

The tracked first-party scope in `sources/dwarkesh-podcast.txt` adds the homepage
and public RSS/podcast feed for 183 total URL identities. The feed is unusually
valuable preservation input: it includes episode metadata, audio enclosures,
descriptions, and podcast fields in addition to the rendered posts.

The homepage also exposes Podcast and Blog presentation sections, while the
sitemap provides the stable combined post inventory. Category, subscriber-chat,
and authenticated Substack surfaces are not part of this first public scope.

## Representative capture

The long Dario Amodei interview was captured at:

`/mnt2/capsule/epitome/dwarkesh/validation/1786164950`

The capture retained 343 response bodies totaling about 23 MB, the full rendered
transcript and discussion, and every 50 asset-completion request attempted after
the browser's 195 already-complete assets. The remaining discovered URLs were
mostly alternate responsive-image sizes, avatars, icons, and recommendation
thumbnails rather than missing article media.

Substack image-proxy URLs contain commas. The original replay parser split those
commas as if each transformation were a separate `srcset` candidate, breaking
visible images. The replay now splits only real comma-plus-whitespace candidate
boundaries and drops inert external preload hints. After that fix, all 72 page
images loaded, the long transcript and comments remained present, and the page
made no production-origin resource requests.

## Media boundary

The page has three related preservation representations of the interview:

- a primary Substack-hosted video with media ID
  `5723fd43-9712-418c-9427-9f60d7e5c03c`;
- a YouTube embed with ID `n1E9IZfvGMA`; and
- podcast audio and caption/transcription metadata present in Substack's page
  state and feed.

The normal browser capture only buffers video metadata and a few Mux segments;
that is not a durable copy of the full video. The pending hosted-video and
YouTube imports are tracked separately in
`inventories/dwarkesh-substack-video.json` and
`inventories/dwarkesh-youtube.json`. The generic media inventory utility now
understands Substack `<video>` IDs, posters, and HLS/MP4 source endpoints.

## Additional structural validations

Two additional variants were captured before approving page batches:

- The 2023 essay `Will scaling work?` is stored at
  `/mnt2/capsule/epitome/dwarkesh/validation/1786167000-will-scaling-work`.
  It retains 29,457 characters of rendered text and the article's figures. It
  also revealed that nominally essay-only posts may have a separate Substack
  article-voiceover audio asset, here media ID
  `76180006-2724-40f6-870c-f8f8c5780bb1`.
- The July 2020 audio-first episode `Tyler Cowen — The Great Reset` is stored at
  `/mnt2/capsule/epitome/dwarkesh/validation/1786167300-tyler-cowen`. It retains
  50,948 characters of page text, including the full written transcript, plus
  references to the original Substack podcast audio, YouTube, Apple Podcasts,
  and Spotify representations. Its audio media ID is
  `378ecee0-1abb-4023-9d1d-b3ea9ebaee5a`.

Both captures completed and closed their tabs. Their replays were visually
checked at 1440×900 and an attached CDP network log recorded zero requests away
from the local archive server. No discrete `<track>` caption files were exposed
by either page. The older episode's transcript is inline article content, while
the representative Dario video stores its timed transcript directly in the
captured DOM.

The replay audit exposed generic Substack defects and fixed them before a batch
begins:

- asset discovery no longer mistakes commas inside image-proxy transformations
  for `srcset` separators;
- replay advertises only responsive variants that actually exist in the local
  capture, falling back to the preserved base image rather than displaying a
  large blank area; and
- YouTube, Apple Podcasts, and Spotify script embeds become bounded, labelled
  offline placeholders instead of blank or pathologically tall frames while
  their media is pending separate import.

The tracked `inventories/dwarkesh-substack-audio.json` ledger currently records
the two validated audio assets, their referring articles, source endpoints,
caption-track lists, and embedded timed-transcript row counts. The YouTube
ledger now also includes the older Tyler episode. Full video and audio downloads
remain a separate downloader task rather than part of the page crawl.

With long video/transcript, essay/voiceover, and old audio-first variants now
validated, the 183-URL first-party page scope was approved for bounded batches.

## First bounded page batch

The selected 15-page pilot completed at:

`/mnt2/capsule/epitome/dwarkesh/crawls/1786182573`

All 15 manifests are complete and all capture tabs closed. Representative
homepage, essay, long video/transcript, old audio-first, and citation-heavy
replays were inspected at a 1440×900 desktop viewport. Article text, inline
transcripts, and ordinary images were intact, with no broken image elements.
The attached browser network log recorded 331 requests, all to the local replay
server and none to a production origin.

The only asset failure was an expired signed SSRN download URL on `Alex Imas and
Phil Trammell – What remains scarce after AGI?`. The stable SSRN abstract and a
fresh 7,223,859-byte PDF were captured under the source's private
`dependencies/` directory. Replay now gives expiring SSRN download URLs a
stable identity based on their path and `abstractId`, so the historical signed
link resolves to the recovered local PDF. A browser range request verified a
206 `application/pdf` response with the expected `%PDF-` signature.

Across the validation and pilot captures, the tracked media ledgers now contain
seven YouTube videos, nine Substack-hosted videos, and two Substack-hosted audio
assets. These remain explicit downloader imports rather than silent gaps in the
page archive. Eighteen of the 183 approved source identities are complete, and
the next deduplicated 30-page batch is selected in ignored crawl input data.

## Second bounded page batch

The next 30 deduplicated pages completed at:

`/mnt2/capsule/epitome/dwarkesh/crawls/1786187606`

All 30 manifests are complete, all capture tabs closed, and the crawl reported
zero page failures. It retained 9,108 response bodies totaling about 596 MiB.
One asset-completion request failed: an expired signed University of Queensland
PDF cited in the Michael Nielsen interview. The stable bibliographic record for
`Quantum Optical Fredkin Gate` is now preserved under `dependencies/`, but the
128 KiB paper itself remains unavailable: the repository requires AWS human
verification, the exact file has no Wayback snapshot, and the publisher asks
for institutional or subscriber authentication. This is an explicit outbound
citation recovery task rather than missing Dwarkesh page content.

A representative browser audit exposed 17 missing primary article images on
six pages. The 50-item completion budget had been exhausted on incidental and
responsive variants before reaching those rendered figures. Asset discovery
now identifies images inside `<article>`, prioritizes Substack's full-resolution
`data-attrs` source ahead of proxy/sidebar resources, and lets replay fall back
to that original when a generated proxy is absent. The reusable
`research/audit_capture_images` utility found and repaired only the 17 missing
resources (3,269,443 bytes). Its second pass reports zero missing article images
across all 30 pages.

Six repaired essay and interview replays were then checked in Chromium at a
1440×900 desktop viewport. Their article text ranged from 12,776 to 131,650
characters, all article images loaded, and long transcripts remained intact.
The attached offline network log recorded 4,854 requests, all to the local
server. Across the full 48-identity archive, media ledgers now track 22 YouTube
videos, 28 Substack videos, and three Substack audio assets. The next
deduplicated 45-page batch is selected.

## Third bounded page batch

The next 45 deduplicated pages completed at:

`/mnt2/capsule/epitome/dwarkesh/crawls/1786194586`

All 45 manifests are complete, all capture tabs closed, and the crawl reported
zero page or asset-completion failures. The primary-image audit found zero
missing rendered article images. Five desktop replays covered the standalone
`Notes on China` and `AI Firm` essays, the 195,241-character Scott
Alexander/Daniel Kokotajlo transcript, a 163,556-character video/transcript
page, and a short event announcement. All images loaded and the page layouts,
headings, comments, and long transcripts were intact.

The first strict replay-network pass exposed one general leak: captured HLS
playlists still contained absolute Mux child-playlist and segment URLs. Replay
now rewrites ordinary playlist lines plus `URI` attributes for keys and maps to
local resource routes. A repeated audit of two video-bearing pages recorded 141
requests, all to the local server. Uncaptured segments therefore fail closed
instead of consulting production; the preserved posters remain visible while
full durable playback awaits the explicit external-media imports.

Across the 93 completed source identities, the refreshed ledgers now track 53
YouTube videos, 61 Substack videos, and four Substack audio assets. The next
deduplicated 60-page batch is selected.
