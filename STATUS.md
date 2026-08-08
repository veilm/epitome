# Epitome archive status

Updated at Unix timestamp `1786162073` (2026-08-08 04:07 UTC).

“Complete” below means complete for the currently discovered and approved source
scope. Incremental recrawls and newly published pages remain ongoing archival
work.

| Source | Status | Current coverage | Remaining work |
| --- | --- | --- | --- |
| OpenAI public site | Complete | The approved public-site inventory has been captured to the private raw archive, deduplicated across crawl runs, and validated through offline replay. | Add future publications incrementally. Careers and job-history snapshots remain a separately scoped source. |
| Anthropic public site | Page archive complete; media active | The approved 160-URL batch has 160 complete page captures. HTML, article text, styles, and ordinary images replay locally. | Import 34 YouTube videos referenced by 22 articles. Two Claude 2 Vimeo embeds are no longer available upstream; their URLs and article context remain preserved. Continue toward the remainder of Anthropic's publication inventory only after media handling is integrated. |
| Claude.com blog | Page archive complete; media active | All 201 inventoried URL identities are captured across the pilot and four deduplicated batches. Representative long, image-heavy, technical, customer-story, and video-bearing pages render locally with complete article text and ordinary images. | Import the 81 YouTube videos referenced by 58 captured Claude.com articles; add future publications incrementally. |
| Dario Amodei personal site | Complete | The homepage and all five self-hosted writings are captured and visually/offline-network verified. | Pursue archival copies of three unavailable outbound citation PDFs; continue the separate broader writing and interview inventory. |
| Andrej Karpathy blog | Capture-ready | A reviewed 26-URL scope covers the homepage, About page, RSS feed, and 23 dated posts. The representative `microgpt` post, primary image, and all 35 Disqus comments replay locally without scripts or external requests. | Run the bounded deduplicated blog crawl, then inventory outbound Medium, `karpathy.ai`, notebook, paper, video, and other first-party writing dependencies separately. |
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

Claude.com has a separate ledger at
[`inventories/claude-youtube.json`](inventories/claude-youtube.json):

- 81 unique YouTube videos;
- 58 referring Claude.com articles; and
- 81 entries currently marked `pending_download` under the private Claude.com
  archive's `media/youtube/<video_id>` directories.

## Immediate next source

Claude.com's approved 201-URL inventory is complete. The replay layer normalizes its captured
pre-animation state (`opacity: 0`, `visibility: hidden`, translated elements,
and the black transition overlay). The final 35-page batch passed manifest,
visual, image-loading, and offline-network checks; its only two asset misses
were the same unused Webflow placeholder SVG returning HTTP 403. Dario's
bounded personal-site scope is also complete, and Karpathy's blog is now the
active next source.
