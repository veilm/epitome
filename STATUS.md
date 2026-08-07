# Epitome archive status

Updated at Unix timestamp `1786128347` (2026-08-07 18:45 UTC).

“Complete” below means complete for the currently discovered and approved source
scope. Incremental recrawls and newly published pages remain ongoing archival
work.

| Source | Status | Current coverage | Remaining work |
| --- | --- | --- | --- |
| OpenAI public site | Complete | The approved public-site inventory has been captured to the private raw archive, deduplicated across crawl runs, and validated through offline replay. | Add future publications incrementally. Careers and job-history snapshots remain a separately scoped source. |
| Anthropic public site | Page archive complete; media active | The approved 160-URL batch has 160 complete page captures. HTML, article text, styles, and ordinary images replay locally. | Import 34 YouTube videos referenced by 22 articles. Two Claude 2 Vimeo embeds are no longer available upstream; their URLs and article context remain preserved. Continue toward the remainder of Anthropic's publication inventory only after media handling is integrated. |
| Claude.com blog | Pilot archive complete; media active | The script-disabled Webflow replay defect is fixed. Five newly selected blog pages plus the earlier validation page render locally with complete article text and ordinary images; the pilot replay made no production-origin requests. | Import the 4 YouTube videos referenced by 3 pilot articles, then expand through the 155 currently uncaptured inventory URLs in reasonable, deduplicated batches. |
| Dario Amodei sources | Research | Personal-site and external-index gaps are documented. | Complete the reviewed canonical writing/interview inventory before capture. |
| Model-readable articles and summaries | Prototype | Extraction and Codex-driven summary flows work on bounded OpenAI and Anthropic samples. | Expand only after each source's archive completeness checks pass. |

## Active media import

The canonical pending-media ledger is
[`inventories/anthropic-youtube.json`](inventories/anthropic-youtube.json):

- 34 unique YouTube videos;
- 22 referring Anthropic articles;
- 34 entries currently marked `pending_download`; and
- stable import directories under `media/youtube/<video_id>` relative to the
  private Anthropic archive root.

The JSON maps shared videos to every referring article, so video files should be
stored once rather than duplicated per page. Large media remains private and
outside Git.

The Claude.com pilot has a separate ledger at
[`inventories/claude-youtube.json`](inventories/claude-youtube.json):

- 4 unique YouTube videos;
- 3 referring Claude.com articles; and
- 4 entries currently marked `pending_download` under the private Claude.com
  archive's `media/youtube/<video_id>` directories.

## Immediate next source

Claude.com is next. The replay layer now normalizes its captured pre-animation
state (`opacity: 0`, `visibility: hidden`, translated elements, and the black
transition overlay), and the five-page pilot passed visual and offline-network
checks. The next step is a larger but still bounded, deduplicated batch.
