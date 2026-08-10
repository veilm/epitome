# Media inventories

Tracked inventories bridge Epitome's page captures with external media download
systems. Large downloaded files remain outside Git; these small JSON files record
what is needed, where it should be imported, and every captured article that uses
it.

## Anthropic YouTube embeds

[`anthropic-youtube.json`](anthropic-youtube.json) contains one item per YouTube
video. Each item provides:

- the YouTube ID and watch URL;
- a stable import directory below the private Anthropic archive;
- every referring article, embed title, source iframe URL, and capture locator;
- a status field, initially `pending_download`; and
- optional `imported_files` and `notes` fields for the external downloader or a
  later import step.

On Delirium, `media/youtube/<video_id>` is relative to
`/mnt2/capsule/epitome/anthropic/`. The downloader may choose its own filenames
and containers inside that directory, then record them in `imported_files`.

Regenerate discovery data without losing existing status/import fields:

```sh
util/inventory_embedded_media \
  /mnt2/capsule/epitome/anthropic/crawls/1786067844 \
  /mnt2/capsule/epitome/anthropic/crawls/1786099713 \
  --source 'Anthropic public-site batch' \
  --media-root media/youtube \
  --output inventories/anthropic-youtube.json
```

The paths in this example describe Delirium's private archive, not portable
defaults in the capture utilities.

## Claude.com YouTube embeds

[`claude-youtube.json`](claude-youtube.json) uses the same schema for the
Claude.com blog. On Delirium, its `media/youtube/<video_id>` directories are
relative to `/mnt2/capsule/epitome/claude.com/`.

Regenerate it after additional Claude.com batches while preserving any existing
status/import fields:

```sh
util/inventory_embedded_media \
  /mnt2/capsule/epitome/claude.com/crawls/1786127775 \
  /mnt2/capsule/epitome/claude.com/crawls/1786137145 \
  /mnt2/capsule/epitome/claude.com/crawls/1786143499 \
  /mnt2/capsule/epitome/claude.com/crawls/1786148472 \
  /mnt2/capsule/epitome/claude.com/crawls/1786156382 \
  --source 'Claude.com blog batches' \
  --media-root media/youtube \
  --output inventories/claude-youtube.json
```

## Dwarkesh hosted and YouTube video

Dwarkesh Podcast pages can contain both a Substack-hosted primary video and a
YouTube copy. `dwarkesh-substack-video.json` records Substack media IDs, poster
URLs, HLS/MP4 source endpoints, referring posts, and stable import directories.
`dwarkesh-youtube.json` records the YouTube side using the existing schema.

Regenerate either ledger from completed Dwarkesh capture roots:

```sh
util/inventory_embedded_media \
  /mnt2/capsule/epitome/dwarkesh/validation/1786164950 \
  --provider substack \
  --source 'Dwarkesh Podcast validation' \
  --media-root media/substack \
  --output inventories/dwarkesh-substack-video.json

util/inventory_embedded_media \
  /mnt2/capsule/epitome/dwarkesh/validation/1786164950 \
  --provider youtube \
  --source 'Dwarkesh Podcast validation' \
  --media-root media/youtube \
  --output inventories/dwarkesh-youtube.json
```

The raw Substack page state and podcast feed also contain audio, captions, and
transcription metadata. Inventorying those is required before a large Dwarkesh
batch; the current hosted-media ledger covers video elements only.

## AI 2027 media

[`ai-2027-media.json`](ai-2027-media.json) records the narrated-scenario MP3,
its podcast distribution links, and the companion YouTube video exposed by the
validated homepage. Imports are relative to `/mnt2/capsule/epitome/ai-2027/`;
the page capture remains useful and offline without silently claiming those
large media items are complete.

## AI 2040 audio

[`ai-2040-audio.json`](ai-2040-audio.json) records the 64-minute Plan A
narration and its canonical Buzzsprout MP3 identity. Spotify, Apple Podcasts,
and the podcast feed are retained as alternate provenance. The direct audio is
an external-downloader task and was not fetched during page capture.
