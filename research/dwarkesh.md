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
validated, the 183-URL first-party page scope is ready for a small bounded batch
after the active Peter Steinberger crawl completes.
