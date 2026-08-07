# Epitome archive status

Updated at Unix timestamp `1786127411` (2026-08-07 18:30 UTC).

“Complete” below means complete for the currently discovered and approved source
scope. Incremental recrawls and newly published pages remain ongoing archival
work.

| Source | Status | Current coverage | Remaining work |
| --- | --- | --- | --- |
| OpenAI public site | Complete | The approved public-site inventory has been captured to the private raw archive, deduplicated across crawl runs, and validated through offline replay. | Add future publications incrementally. Careers and job-history snapshots remain a separately scoped source. |
| Anthropic public site | Page archive complete; media active | The approved 160-URL batch has 160 complete page captures. HTML, article text, styles, and ordinary images replay locally. | Import 34 YouTube videos referenced by 22 articles. Two Claude 2 Vimeo embeds are no longer available upstream; their URLs and article context remain preserved. Continue toward the remainder of Anthropic's publication inventory only after media handling is integrated. |
| Claude.com blog | Validation | One blog page is captured as part of the Anthropic sample, and the full first-party blog inventory has been discovered. | Fix script-disabled Webflow rendering, validate representative pages and embedded media, then begin a bounded crawl. No broad Claude.com crawl has started. |
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

## Immediate next source

Claude.com is next. Its Webflow pages can capture content in a pre-animation
state (`opacity: 0`, `visibility: hidden`, and translated elements). Offline
replay removes scripts, so the replay layer must normalize that state before a
larger crawl is approved.
