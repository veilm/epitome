# LLM-ready article extraction

The Markdown output is an intermediate representation for language models, not
a user-facing republication of the source page. Its job is to retain the useful
article context while discarding JavaScript, CSS, navigation, cookie UI,
recommendations, and other page chrome.

Exact visual or media fidelity belongs to the separate network capture. For
model input, it is acceptable to reduce an interactive chart to its accessible
table, omit playback controls, or leave out decorative media.

## Usage

```sh
util/url_to_markdown 'https://openai.com/index/example/'
```

The default output is:

```text
output/markdown/HOST-PATH.md
```

The command also writes ignored research artifacts below `data/extractions/`:

- `page.html`: the complete rendered DOM, available when extraction looks
  incomplete;
- `content.html`: the selected and cleaned content subtree;
- `read.json`: the visibility-aware semantic view produced by `cdp read`;
- `metadata.json`: extracted title, canonical URL, date, author, and language;
- `report.json`: text coverage, input/output sizes, media observations, and
  warnings.

Use `--selector` to override automatic selection for a one-off page. Use
`--strict` when a pipeline should return nonzero for quality warnings.

## How it works

1. Open the URL in a fresh tab through CDP.
2. Choose the largest useful `article`, `main`, or `[role=main]` subtree.
3. Apply small matching rules from `research/site_rules.json`.
4. Remove scripts, styles, navigation, forms, controls, and known trailing
   recommendation sections.
5. Convert semantic HTML into compact Markdown using the dependency-free
   renderer in `util/epitome_lib/html_to_markdown.py`.
6. Compare words in the cleaned source against words in the result and emit a
   report.

The converter preserves the structures most useful to an LLM:

- title, canonical URL, description, date, author, and language;
- headings and paragraphs;
- links and basic emphasis;
- lists and quotes;
- code blocks;
- accessible tables;
- image alt text/URLs and sourced media links when readily available;
- author, acknowledgment, and footnote text.

It does not attempt to preserve page layout, animations, client state, visual
chart styling, playback controls, or every decorative image.

## Generalization

The generic extractor is intentionally the default. Site-specific behavior is
data-driven where possible:

```json
{
  "host_suffix": "example.com",
  "root_selectors": ["article"],
  "exclude_selectors": [".newsletter-prompt"],
  "exclude_text_exact": ["Loading..."],
  "cut_at_headings": ["Related articles"]
}
```

OpenAI currently needs only a preferred article root, a few UI text exclusions,
and a cutoff before recommendation cards. Generated CSS classes are avoided.

## Review and future LLM repair

The report is the first automatic review layer. A suspiciously short body,
missing title, or low word coverage produces a warning. Media without source
URLs is recorded as an observation rather than a failure because the output is
text-oriented.

A future LLM reviewer can receive:

1. the Markdown;
2. `report.json`;
3. `read.json`; and, only if necessary,
4. the cleaned or complete HTML.

It can then decide whether important article text is missing or page chrome
leaked in. The preferred repair order is:

1. adjust `research/site_rules.json`;
2. add a small, named site hook for a genuinely unusual component;
3. improve the generic renderer when the issue applies across sites.

Generated patches should be reviewed and tested against saved artifacts before
being used for a crawl. The crawler itself should not silently rewrite its own
extractor during a production run.

## Current observed results

The bounded test corpus currently includes an older OpenAI product article and
a large current model launch. Both produced readable article text with tables,
footnotes, headings, and metadata. The complex page had an approximately 1.88
MB raw server response during investigation and produced about 35 thousand
Markdown characters while retaining about 95% of the words in the cleaned
content subtree.

This percentage is a diagnostic, not a requirement for textual identity. Manual
review remains important when adding a new site or component family.
