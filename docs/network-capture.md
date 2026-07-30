# CDP network capture

Epitome currently uses the workstation's `cdp network-log` as its acquisition
layer. WARC is an optional future export, not a prerequisite.

## Capture one URL

```sh
util/capture_url 'https://openai.com/index/example/'
```

The default CDP port is 2103. A capture is written below `data/captures/`, which
is ignored by Git. It contains:

- `network/*/metadata.json`: URL, method, status, and timestamp;
- request and response headers, with credential headers redacted;
- `response-body.bin` and JSON bodies where applicable;
- `page.html`: the final rendered DOM;
- `read.json`: the visibility-aware semantic view from `cdp read`;
- `interactive-media.json`: deferred video embeds found and activated;
- `asset-completion.json`: referenced assets that were already complete,
  recovered, failed, or skipped by a bound;
- `manifest.json`: limits and response/host/byte counts.

The logger is attached to an `about:blank` tab before navigation so it captures
the main document. The utility then performs bounded scrolling to trigger lazy
resources. After logging stops, a completion pass discovers resource URLs in
the rendered HTML and captured CSS, then explicitly downloads any whose complete
bodies are absent. A `206 Partial Content` response counts as complete only when
its range covers the entire declared entity. When a request cap applies,
audiovisual files are prioritized, followed by documents and images. Defaults
are deliberately finite:
40 scroll operations, 90 seconds, at most 50 recovery requests, and at most
500 MiB of recovered bodies. Recovery requests are spaced two seconds apart.

OpenAI's Vimeo component sometimes leaves iframe URLs blank until a visitor
interacts with it. During capture, Epitome reconstructs the ordered Vimeo URLs
from the page's embedded React data and hydrates those frames while logging is
active. The completion pass fetches each player configuration. It preserves the
highest-resolution progressive MP4 when Vimeo exposes one; otherwise it uses
the advertised HLS presentation and asks `ffmpeg` to losslessly remux its best
H.264/AAC rendition into a single MP4. This does not re-encode the media.
Derived MP4 records retain the source HLS URL, transform description, size, and
digest. The same asset byte and timeout limits apply, and over-budget temporary
remuxes are stopped and discarded.

When all capture and recovery work is finished, Epitome closes the exact CDP
target recorded in its session and disconnects. It does not close unrelated
browser tabs. `--keep-tab` is available for interactive debugging.

Useful smaller research run:

```sh
util/capture_url URL --max-scrolls 4 --max-seconds 30
```

Asset recovery can be tuned or disabled:

```sh
util/capture_url URL --max-assets 10 --max-asset-bytes 104857600 \
  --asset-delay-seconds 5
util/capture_url URL --no-complete-assets
```

## Capture a bounded URL list

```sh
util/capture_urls --url-file data/urls.txt
```

Batch capture is sequential and refuses more than 10 unique URLs unless
`--max-urls` is explicitly raised. Before starting, it scans complete captures
below `data/` and skips their requested and final URLs, treating fragments and
trailing-slash differences as the same page. Incomplete captures remain
eligible for retry. Use repeatable `--existing-root` options to scan other
archive roots, or the explicit `--allow-recapture` escape hatch when a fresh
copy is intentional.

The default pause grows with the post-deduplication batch size: 10 seconds for
up to 10 pages, 15 for 20, 20 for 40, 30 for 80, and 45 above 80. An explicit
`--delay-seconds` overrides it. Each run records the effective delay, selected
URLs, and skipped existing URLs in its `progress.jsonl` ledger.

Summarize a completed run with:

```sh
util/summarize_crawl data/crawls/RUN_TIMESTAMP
```

When a large crawl is approved, sitemap URLs can be prepared with the committed
research utility:

```sh
research/list_sitemap_urls https://openai.com/sitemap.xml \
  > data/openai-urls.txt
```

Listing and capturing are separate so the URL set can be inspected before it
causes browser traffic.

Prepare a bounded article-only batch while preserving sitemap order and
excluding every completed capture:

```sh
research/select_uncaptured_urls data/openai-sitemap-urls.txt \
  --url-prefix https://openai.com/index/ --max-urls 80 \
  --output data/next-openai-index-urls.txt
util/capture_urls --url-file data/next-openai-index-urls.txt --max-urls 80
```

The selector and the capture command independently enforce the completed-page
check, so a stale selection file cannot silently cause duplicate acquisition.

## Current limitations

- Resource completion follows rendered HTML and captured CSS references.
  Vimeo players have explicit completion support, but arbitrary nested iframe
  dependencies, unopened carousel states, and other interaction-only downloads
  may still be absent.
- The final DOM is captured after bounded scrolling, not exhaustive interaction.
- Captures remain response-oriented directories interpreted by the local replay
  server rather than a portable, pre-materialized static tree.
- Response bodies can contain site-generated identifiers or personalized
  experiment data even after credential headers are redacted. Captures remain
  ignored/private by default.

These are observable limitations we can address individually after the simple
pipeline encounters them.
