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
- `manifest.json`: limits and response/host/byte counts.

The logger is attached to an `about:blank` tab before navigation so it captures
the main document. The utility then performs bounded scrolling to trigger lazy
resources. Defaults are deliberately finite: 40 scroll operations and 90
seconds.

Useful smaller research run:

```sh
util/capture_url URL --max-scrolls 4 --max-seconds 30
```

## Capture a bounded URL list

```sh
util/capture_urls --url-file data/urls.txt
```

Batch capture is sequential and refuses more than 10 unique URLs unless
`--max-urls` is explicitly raised. It pauses 10 seconds between pages by
default; use `--delay-seconds` to increase that interval. Each run has a
`progress.jsonl` ledger.

When a large crawl is approved, sitemap URLs can be prepared with the committed
research utility:

```sh
research/list_sitemap_urls https://openai.com/sitemap.xml \
  > data/openai-urls.txt
```

Listing and capturing are separate so the URL set can be inspected before it
causes browser traffic.

## Current limitations

- Only resources actually requested by the browser are captured. Unopened tabs,
  carousel states, downloads, and deep iframe interactions may be absent.
- The final DOM is captured after bounded scrolling, not exhaustive interaction.
- Captures are response-oriented directories, not yet a directly servable tree.
- A static materializer/replay server still needs to map complete URLs (including
  query strings and methods) to captured responses and rewrite external URLs.
- Response bodies can contain site-generated identifiers or personalized
  experiment data even after credential headers are redacted. Captures remain
  ignored/private by default.

These are observable limitations we can address individually after the simple
pipeline encounters them.
