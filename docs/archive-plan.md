# OpenAI site archive investigation

Investigated on 2026-07-22 through Chrome DevTools on port 2103. This was a
bounded exploration: the homepage, two article pages, `robots.txt`, the root
sitemap, RSS, and five child sitemaps. It was not a crawl.

## What the site looks like

- `openai.com` is a Next.js/React site. Pages are server-rendered and then
  hydrated. Raw article responses already contain the semantic article text.
- The root sitemap is an index with 34 content-type sitemaps. The sampled child
  maps contain overlapping URLs, so discovery must deduplicate canonical URLs.
- The five sampled maps contained 445 `page`, 165 `product`, 43 `research`, 234
  `company`, and 192 `publication` entries. These counts must not be summed.
- `robots.txt` currently allows `/` except `/microsoft-for-startups/` and names
  `https://openai.com/sitemap.xml` as the sitemap.
- `/news/rss.xml` is useful for rapid discovery and metadata, but it contains
  descriptions rather than full article bodies.
- Primary resource hosts seen in the samples were:
  - `openai.com` for HTML, Next.js JS/CSS, gates, and article TTS;
  - `images.ctfassets.net` and `assets.ctfassets.net` for Contentful media;
  - `cdn.openai.com` for video, data, and self-contained interactive sites;
  - `chatgpt.com` and `ab.chatgpt.com` for client configuration and experiments;
  - Cloudflare endpoints for telemetry.
- Some article content is not a simple image/text tree. The current model post
  includes audio, video, tables, canvases, charts, and an embedded interactive
  site. An older article uses a simpler but different component mixture.
- Sample raw HTML sizes differed substantially: roughly 1.88 MB for a current,
  complex model post and 408 KB for a 2023 article. Both included `<article>`
  and React Flight (`self.__next_f`) data.
- Responses use `Vary` headers for RSC/router state. Query strings on Next.js
  assets include a deployment identifier and must not be discarded casually.

## What “1:1 clone” should mean

A recursive folder of rewritten HTML may be enough for the first visual clone,
but the capture store must retain the original request URL, timestamp, status,
redirects, headers, and response bytes. The current CDP network-log directories
do that directly. WARC can be exported later if interoperability with existing
web-archive replay tools becomes useful.

There are two fidelity levels:

1. **Archival fidelity:** the exact public HTTP responses can be replayed and
   audited, including historical versions of a URL.
2. **Behavioral fidelity:** a browser renders the same page without consulting
   the live site. This additionally needs dynamically requested resources,
   embedded sites, and deterministic substitutes for analytics, experiments,
   and other non-content services.

Start with archival fidelity plus a generated static mirror. Add behavioral
replay only for concrete features that the static result fails to reproduce.

## Proposed capture architecture

### 1. Discovery

- Fetch `robots.txt` and the root sitemap once per run.
- Fetch each child sitemap with a low concurrency limit and record its body.
- Normalize only for the crawl frontier: strip fragments, resolve relative
  URLs, retain meaningful query strings, and deduplicate by canonical URL.
- Supplement discovery from RSS and same-origin links found in captured HTML.
- Keep excluded, external, malformed, and redirected URLs in an audit log.
- Incremental runs prioritize new URLs and changed `lastmod` values, but do not
  treat `lastmod` as proof that unchanged pages are byte-identical.

### 2. Network capture

- Attach `cdp network-log` before navigation and store every observed request
  and response, including redirects and failures.
- Store crawl frontier/state and a URL lookup index separately.
- Record capture timestamp, source sitemap(s), referrer, canonical URL, content
  hash, MIME type, response size, and retry history.
- Capture HTML before its dependencies, then parse resource URLs from HTML,
  CSS, React Flight data, `srcset`, media tags, and preload directives.
- Preserve response headers and original URL spelling. Content-addressed
  deduplication may save space, but replay metadata must remain per request.

### 3. Browser completion

Raw HTML parsing cannot discover every lazy or computed request. Run a real
browser against a controlled subset first, then expand only if missing-resource
tests justify it:

- record browser network traffic into the capture directories;
- scroll pages to trigger lazy images and media metadata;
- enumerate same-origin iframes and archive them recursively;
- exercise non-destructive presentation controls such as tabs and carousels;
- capture the final DOM and a screenshot as diagnostic artifacts;
- never archive authenticated state or personal cookies.

The browser pass should initially cover one page per template/component family,
not every URL. If raw capture plus dependency parsing proves complete for a
family, avoid paying the browser cost for every page.

### 4. Static materialization, then replay if needed

- First generate a static tree by mapping captured GET responses to local paths
  and rewriting HTML/CSS resource references.
- Preserve the original URL and timestamp in the capture index.
- Block live-network fallback during fidelity testing; missing requests must be
  visible errors, not silently fetched from production.
- Stub analytics and experimentation calls when they do not affect content.
  Archive content-bearing gates, TTS, downloadable files, and embedded sites.
- If runtime requests or interactions fail in practice, add a lookup server
  keyed by method plus complete URL. WARC/`pywb` remains an available export and
  replay option rather than an initial dependency.

## Candidate implementation

The first capture worker is implemented in Python around the installed `cdp`
CLI, with no third-party dependency. It provides:

- response bodies and request/response metadata from `cdp network-log`;
- final rendered HTML and a semantic `cdp read` snapshot;
- sequential bounded batch capture with a JSONL progress ledger;
- a bounded sitemap-listing research utility;
- CLI limits such as `--max-urls`, `--max-scrolls`, and `--max-seconds` that
  default to conservative values.

Concurrency, retries, stronger resumption, and a database catalog should be
added only when observed crawl size or failures justify them.

## Fidelity verification

- Validate capture manifests and ensure every recorded response is indexable.
- Replay with outbound networking disabled and collect every failed request.
- Compare live and replay DOM structure, text, canonical metadata, link targets,
  and screenshots at desktop and mobile widths.
- Test video/audio URLs, downloadable files, `srcset`, CSS fonts/backgrounds,
  iframes, tables, code, footnotes, and interactive components explicitly.
- Produce per-page manifests so a failure can be traced to a missing or changed
  response.

## Before a full crawl

1. Review current site terms/policy and settle the intended private/public use
   of the archive.
2. Define host scope: only `openai.com`, or also the content-bearing external
   hosts listed above.
3. Implement a 5–10 page spike with hard request/byte/time limits.
4. Replay that spike offline and quantify missing requests.
5. Estimate total URL count and bytes from sitemap metadata plus sampled pages.
6. Only then approve a complete initial capture.
