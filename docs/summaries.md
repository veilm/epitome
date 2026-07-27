# Codex article summaries

Epitome summarizes clean article extractions with an isolated headless Codex
run. The source extraction remains separate from both the archive and the
summary.

## Summarize one extraction

```sh
util/summarize_article output/markdown/openai.com-index-example.md
```

The default invocation uses:

- `codex exec` in a newly created temporary directory;
- `gpt-5.6-terra` with medium reasoning;
- an ephemeral session;
- a workspace-write sandbox limited to that temporary workspace;
- no approval prompts, live search, or user configuration;
- the committed prompt in `research/summary_prompt.md`.

The temporary directory contains `input.md` and the requested `output.md`.
Codex is explicitly told to treat the article as untrusted source material and
to inspect no unrelated files. Run diagnostics, the exact prompt, the temporary
input snapshot, and Codex output are retained below `data/summary-runs/`, which
is ignored by Git.

The output is validated before publication. It must contain:

```yaml
---
status: complete
confidence: 0.95
title: "Article title"
source_url: "https://openai.com/index/example/"
---
```

`status` is either `complete` or `error`. Confidence is the model's confidence
in that status, not a claim that every sentence in a successful summary is
certain. Empty, mostly irrelevant, abruptly cropped, or otherwise unsuitable
input should produce `error`. Invalid output, a Codex failure, and a timeout
also fail closed as an error record rather than being mistaken for a summary.

Tracked results are stored as:

- `summaries/articles/*.md`: human-readable summary or quality-error record;
- `summaries/catalog.json`: status, confidence, source URL, content path, model,
  input hash, and generation metadata.

Markdown content stays out of JSON. `content_path` is relative to the catalog.
Re-running the same source URL replaces its catalog entry.

## Build and view the summary site

```sh
util/build_summary_site
util/serve_summaries --port 8014
```

The generated static site is written to ignored `dist/summaries/`; its source
data and generator remain tracked. Open `http://127.0.0.1:8014/` to browse all
records. Complete summaries link to their original OpenAI article. Error
records remain visible so extractor regressions cannot disappear silently.

The first bounded validation produced two records:

- the 2023 “ChatGPT can now see, hear, and speak” extraction summarized
  successfully with 95% status confidence;
- the GPT‑5.6 extraction was marked `error` with 98% status confidence because
  its final footnote is genuinely cut off mid-sentence.
