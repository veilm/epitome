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
