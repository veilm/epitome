# Epitome archive status

Updated at Unix timestamp `1786299068` (2026-08-09 18:11 UTC).

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
| Dwarkesh Podcast | Page archive complete; media imports active | All 183 approved source identities are captured across structural validations and five bounded batches. Long transcripts, standalone essays, inline figures, ordinary images, and media posters replay locally without production requests. HLS playlist children fail closed through local replay. Seventy-two Substack audio assets, 128 YouTube videos, and 72 Substack videos are inventoried. | Import full audio/video through the external downloader. One cited 1989 UQ paper remains blocked by upstream verification and publisher authentication; its stable bibliographic landing page is preserved. Add future publication URLs incrementally. |
| SemiAnalysis newsletter | Page crawl active; media imports active | Two hundred twenty-eight of the reviewed 325 identities are complete across structural validations and five bounded batches. Paywalled and free articles, image-heavy technical posts, and the chronological archive replay locally without production requests. A total of 374 initially omitted article/listing images were repaired; ten Substack videos across five articles are inventoried. Free-subscriber emails end at the same paid boundary and are not a richer source. | Complete the selected final 97-page remainder. Import the ten videos separately. Inventory the corporate, careers, models, and public-tools site later; authenticated institutional data is out of public-crawl scope. |
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

- 128 YouTube videos referenced by 128 captured articles;
- 72 Substack-hosted videos referenced by 70 captured articles; and
- 72 Substack-hosted audio assets referenced by 72 captured articles.

All 272 entries are marked `pending_download` with stable private import paths.

## Immediate next source

Claude.com's approved 201-URL inventory is complete. The replay layer normalizes its captured
pre-animation state (`opacity: 0`, `visibility: hidden`, translated elements,
and the black transition overlay). The final 35-page batch passed manifest,
visual, image-loading, and offline-network checks; its only two asset misses
were the same unused Webflow placeholder SVG returning HTTP 403. Dario's
bounded personal-site scope and Karpathy's 26-page canonical blog scope are also
complete. Peter Steinberger's 116-identity core blog scope is now also complete
and replay-verified. Dwarkesh's approved 183-identity page scope is complete and
its external media imports remain active. SemiAnalysis is the active page crawl;
its first 228 identities passed data-level preservation review and the final
deduplicated 97-page remainder is selected.
