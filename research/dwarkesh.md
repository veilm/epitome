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

Before a larger Dwarkesh batch, validate an essay-only post and an older
audio-first episode, then extend the media ledger to podcast audio and caption
files. Large video and audio downloads remain a separate downloader task rather
than part of the page crawl.
