# Epitome archive status

Updated at Unix timestamp `1786195175` (2026-08-08 13:19 UTC).

“Complete” below means complete for the currently discovered and approved source
scope. Incremental recrawls and newly published pages remain ongoing archival
work.

| Source | Status | Current coverage | Remaining work |
| --- | --- | --- | --- |
| OpenAI public site | Complete | The approved public-site inventory has been captured to the private raw archive, deduplicated across crawl runs, and validated through offline replay. | Add future publications incrementally. Careers and job-history snapshots remain a separately scoped source. |
| Anthropic public site | Page archive complete; media active | The approved 160-URL batch has 160 complete page captures. HTML, article text, styles, and ordinary images replay locally. | Import 34 YouTube videos referenced by 22 articles. Two Claude 2 Vimeo embeds are no longer available upstream; their URLs and article context remain preserved. Continue toward the remainder of Anthropic's publication inventory only after media handling is integrated. |
| Claude.com blog | Page archive complete; media active | All 201 inventoried URL identities are captured across the pilot and four deduplicated batches. Representative long, image-heavy, technical, customer-story, and video-bearing pages render locally with complete article text and ordinary images. | Import the 81 YouTube videos referenced by 58 captured Claude.com articles; add future publications incrementally. |
| Dario Amodei personal site | Complete | The homepage and all five self-hosted writings are captured and visually/offline-network verified. | Pursue archival copies of three unavailable outbound citation PDFs; continue the separate broader writing and interview inventory. |
| Andrej Karpathy blog | Complete | All 26 reviewed URL identities are captured and offline-verified. Recent, historical, image-heavy, and long code-heavy pages replay locally; captured Disqus threads render statically, including 35 comments on `microgpt` and 37 on the RNN article. | Recover archival copies of five unavailable outbound research PDFs, then inventory Medium, `karpathy.ai`, notebooks, papers, videos, and other first-party writing separately. |
| Peter Steinberger blog | Core page archive complete; media active | All 116 reviewed core URL identities are archived across validation and four bounded batches. Twenty desktop replays spanning 2012–2026 passed visual and offline-network checks. Five lost inline images are restored from reviewed canonical or Wayback copies, preserved tweets render statically, and two captured Vimeo videos play locally—including a 3h28m, 2.2 GB recording. | Import four inventoried YouTube videos. Two 2020 inline images are unavailable at the live origin, public source repository, and checked exact historical locations; another Vimeo player returns HTTP 403, and four dead outbound citations remain recovery tasks. Preserve deferred pagination/tag indexes later and evaluate the official Markdown mirror as a model-readable supplement. |
| Dwarkesh Podcast | Page crawl active; media imports active | 48 of the 183 approved source identities are captured across structural validations and two bounded batches. Long transcripts, essays, inline figures, and ordinary images replay locally without production requests. The second batch's 17 initially omitted primary images were repaired, and future completion prioritizes original article images. Three Substack audio assets, 22 YouTube videos, and 28 Substack videos are inventoried. | Continue with the selected deduplicated 45-page batch. Import full audio/video through the external downloader. One cited 1989 UQ paper remains blocked by upstream verification and publisher authentication; its stable bibliographic landing page is preserved. |
| SemiAnalysis newsletter | Page capture ready | A reviewed 325-identity scope contains the publication home, archive, feed, and 322 sitemap posts. Current and historical paywalled articles plus a free 2020 article are captured and offline-verified. Public subscription boundaries replay explicitly, and the validation pages contain no embedded audio/video imports. | Begin bounded batches only after the active Dwarkesh page scope completes. Inventory the separate corporate, careers, models, and public-tools site later; authenticated institutional data is out of public-crawl scope. |
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

Peter Steinberger's blog has a separate ledger at
[`inventories/peter-steinberger-youtube.json`](inventories/peter-steinberger-youtube.json):

- four unique YouTube videos referenced by four captured articles; and
- four entries marked `pending_download` under the private Peter archive's
  `media/youtube/<video_id>` directories.

Dwarkesh Podcast has three provider-specific ledgers:

- 22 YouTube videos referenced by 22 captured articles;
- 28 Substack-hosted videos referenced by 28 captured articles; and
- three Substack-hosted audio assets referenced by three captured articles.

All 53 entries are marked `pending_download` with stable private import paths.

## Immediate next source

Claude.com's approved 201-URL inventory is complete. The replay layer normalizes its captured
pre-animation state (`opacity: 0`, `visibility: hidden`, translated elements,
and the black transition overlay). The final 35-page batch passed manifest,
visual, image-loading, and offline-network checks; its only two asset misses
were the same unused Webflow placeholder SVG returning HTTP 403. Dario's
bounded personal-site scope and Karpathy's 26-page canonical blog scope are also
complete. Peter Steinberger's 116-identity core blog scope is now also complete
and replay-verified. Dwarkesh is the active page crawl; its first 48 source
identities passed preservation review and the next deduplicated 45-page batch is
selected.
