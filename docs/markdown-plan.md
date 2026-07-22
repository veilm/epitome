# OpenAI article-to-Markdown investigation

This is a separate derivative pipeline from archival capture. WARC/raw HTML is
the source of truth; Markdown is a normalized reading and analysis format.

The investigation compared:

- `https://openai.com/index/gpt-5-6/`, a current, complex article; and
- `https://openai.com/index/chatgpt-can-now-see-hear-and-speak/`, an older
  article with audio, images, and legacy content components.

## Findings

- Both pages have a semantic `<main>` and `<article>`, exactly one `<h1>`, a
  canonical link, description/social metadata, and server-rendered body text.
- Useful hero regions have explicit attributes:
  `data-article-hero-copy-region="meta|headline|subhead"`.
- Citations use `data-testid="citations"`; author lists use
  `data-testid="author-list"`. These are better initial hooks than generated
  utility classes.
- The article element also contains page UI and recommendations: table-of-
  contents navigation, listen/share controls, author/footnote cards, and “Keep
  reading” cards. Converting the entire `<article>` blindly produces noise and
  duplicates.
- Older body blocks often have a `.prose` class. Current ordinary paragraphs do
  not, so `.prose` is not a valid universal body selector.
- A current complex article contained 57 paragraphs, 46 list items, 20 block
  quotes, 30 figures, 11 real HTML tables, code, video, audio, canvas, and three
  iframes. The older sample had a different structure and no `<figure>` tags.
- Current charts expose accessible table/text content in the DOM. A converter
  should prefer that over screenshots, while retaining an associated visual or
  embed URL where useful.
- Some images are lazy and had an empty `currentSrc` in the sampled viewport.
  Their original `src`, `srcset`, `<source>`, or React/SSR representation must
  be read rather than relying only on loaded browser state.
- Superscript links, captions, “opens in a new window” helper text, duplicated
  responsive markup, audio timers, loading placeholders, and hidden carousel
  slides require explicit normalization.
- No JSON-LD was present in the two inspected pages. Metadata extraction cannot
  depend on it.

## Output contract

Each article should produce deterministic UTF-8 Markdown with YAML frontmatter:

```yaml
---
title: ...
canonical_url: https://openai.com/index/...
description: ...
published_at: 1695600000
updated_at: null
authors: []
categories: []
language: en-US
captured_at: 1784760000
source_sha256: ...
---
```

Use Unix seconds for timestamps. Frontmatter should distinguish publication,
source modification, and capture time rather than collapsing them.

The Markdown body should retain, in document order:

- headings and stable heading anchors;
- paragraphs and inline emphasis/code;
- ordered and unordered lists;
- block quotes and attributions;
- links resolved to absolute canonical URLs;
- images with alt text and a selected archival/original URL;
- captions immediately after their media;
- audio/video/download links with captions or transcripts when present;
- fenced code blocks with language when discoverable;
- tables, using Markdown tables only when rectangular and readable, otherwise
  embedded HTML tables;
- footnote references and definitions;
- a marked placeholder for interactive embeds that cannot be represented.

Authors, acknowledgments, and footnotes belong in the output. “Keep reading,”
global navigation, cookie UI, listen/share controls, carousel controls, and
analytics do not.

## Conversion pipeline

### 1. Choose the source representation

Keep both of these in the ignored capture area:

1. original response bytes and headers from the archive;
2. an optional post-hydration DOM snapshot from the browser completion pass.

Default to original server-rendered HTML. Use the rendered snapshot only for a
component whose meaningful content is absent from the original DOM. Record the
choice in the conversion manifest.

### 2. Extract metadata

In priority order:

- canonical URL from `link[rel=canonical]`;
- title from the hero headline, then `<h1>`, then `og:title`;
- subhead from the hero subhead, then the description meta tag;
- displayed publication time from the hero meta region and `<time datetime>`;
- author list from `[data-testid=author-list]`;
- category/type from hero metadata and article navigation;
- language from `<html lang>`;
- hero media from the hero/backdrop component and social-image metadata.

Store the unparsed displayed date as diagnostic metadata when parsing fails.

### 3. Isolate content

- Start at `<article>`.
- Extract hero metadata separately so it is not duplicated in the body.
- Drop `nav`, form controls, share/listen UI, cookie UI, loading placeholders,
  and nodes marked `data-nosnippet` when they are presentational duplicates.
- Stop ordinary body extraction before the citations/author container, then
  extract its semantic author, acknowledgment, and footnote subsections with
  dedicated handlers.
- Exclude the trailing related/“Keep reading” collection.
- Do not key the boundary only to English heading text. Prefer structural/test
  attributes and use heading text as a checked fallback.

### 4. Convert with a custom block walker

A generic HTML-to-Markdown package can handle inline markup, but component
boundaries require project-specific rules. Walk the cleaned tree in document
order and emit typed intermediate blocks before rendering Markdown:

```text
Heading | Paragraph | List | Quote | Code | Table | Media | Embed | Footnote
```

The intermediate representation prevents nested responsive wrappers from
creating duplicate text and makes it possible to unit-test extraction
separately from Markdown formatting.

Important custom rules:

- collapse exact duplicate blocks caused by responsive variants, but never
  deduplicate merely similar prose;
- remove accessibility helper text such as “opens in a new window” from link
  labels while preserving the destination;
- select the highest-quality original image candidate, retaining all candidates
  in a sidecar manifest;
- represent chart/table components from accessible DOM data;
- retain iframe source, title, fallback text, and archived screenshot;
- map linked superscripts to Markdown footnotes;
- turn `<br>` into a hard break only where it is semantically meaningful;
- normalize non-breaking spaces but preserve significant Unicode punctuation.

### 5. Validate

For every conversion, emit a small JSON manifest (also generated/ignored) with
source hash, extraction warnings, counts by block type, skipped embeds, selected
media, and converter version.

Automated checks should reject or warn on:

- missing title, canonical URL, publication date, or body;
- body word count far below visible article text;
- duplicate consecutive paragraphs/headings;
- empty links or media without both a URL and fallback description;
- malformed tables or unresolved relative URLs;
- visible body text present in the source but absent from all emitted blocks.

## Implementation recommendation

Build a Python CLI with two stages:

```text
epitome-md extract SOURCE_HTML > intermediate.json
epitome-md render intermediate.json > article.md
```

Use a mature HTML5 parser with CSS selectors (for example `selectolax` or
`lxml`) and a small custom Markdown renderer. The standard-library HTML parser
is too forgiving in the wrong ways for this component-heavy HTML. Dependency
selection should happen when implementation begins; no package was installed
as part of this investigation.

Suggested initial corpus, capped at 8–10 pages:

1. a simple company announcement;
2. the inspected 2023 voice/image article;
3. a complex current model launch with tables and interactive media;
4. a research publication with equations/code;
5. a system card;
6. a customer story;
7. an article with an embedded site or video;
8. a page with extensive footnotes/acknowledgments.

Hand-review expected Markdown for this corpus and commit only small, authored
fixtures or structural assertions—not copied full articles. Full source pages,
Markdown exports, manifests, screenshots, and media remain under ignored data
or output directories.

## Definition of done for the spike

- All corpus pages convert without an exception.
- Metadata matches the visible/source values.
- No article paragraph, list, table, quote, code block, or footnote is silently
  omitted.
- Global/related UI does not leak into the body.
- Media and embeds have useful archival references and fallback text.
- A second run over identical input is byte-for-byte deterministic.
- The converter never fetches the network; capture and conversion remain
  separate operations.

