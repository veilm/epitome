# Offline archive replay

Epitome can render captured pages without consulting the live site:

```sh
util/serve_archive data --port 8013
```

Open `http://127.0.0.1:8013/` to browse the capture catalog. The server reads
ignored capture directories in place; it does not copy archive payloads into
Git.

## Offline behavior

For each captured page, the replay layer:

- serves the final rendered `page.html`;
- removes scripts, inline event handlers, refresh directives, preconnects, and
  script preloads;
- rewrites fetch-bearing HTML and CSS URLs to local `/resource/` routes;
- rewrites ordinary links to another captured page or a local “not archived”
  explanation;
- forces archived lazy images to load eagerly because production hydration
  scripts are intentionally absent;
- replaces captured Vimeo embeds with native video controls backed by the
  archived MP4;
- serves only complete captured response bodies;
- supports byte ranges for captured video and audio.

There is deliberately no live-network fallback. An absent asset produces a
local `404`, making the preservation gap visible.

The result is a static visual replay rather than a fully interactive clone.
Captured text, layout, styles, images, fonts, audio, and video can render.
Production JavaScript, analytics, experiments, forms, and interaction-driven
behavior do not run. This is the safer baseline; individual interactions can be
restored later when their preservation value justifies a controlled local
implementation.

## CDP offline verification

A bounded test of the captured Health in ChatGPT page was run through CDP on
port 2103. Its network log contained 20 requests, all to
`127.0.0.1:8013`. A captured MP4 was served locally with byte-range support.
Two missing favicons returned local `404` responses; they caused no production
fallback and do not affect the article, layout, or substantive media.

The generated verification capture and screenshot live below
`data/replay-tests/` and remain ignored.

A later five-page visual audit found two replay-specific media defects. The
Cars24 article's inline screenshots were captured but remained deferred because
their `loading="lazy"` behavior expected production JavaScript. All six of that
page's images now decode locally. The LSEG article contained two blank Vimeo
iframes; its recapture now preserves complete 150-second and 19-second videos.
A CDP replay advanced the first video to 2.4 seconds at 1920×1080, and its
network trace contained only `127.0.0.1:8013` requests.
