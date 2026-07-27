# Codex article summaries

Epitome summarizes clean article extractions with an isolated headless Codex
run. The source extraction remains separate from both the archive and the
summary.

## Summarize one extraction

```sh
util/summarize_article output/markdown/openai.com-index-example.md
```

The default invocation uses:

- the workstation's `cdx exec` wrapper in a newly created temporary directory;
- `gpt-5.6-terra` with medium reasoning;
- an ephemeral session;
- a temporary workspace containing only the input and requested output;
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

`cdx` selects and exports the workstation's stored `CODEX_HOME` before launching
Codex, so the pipeline uses the intended local authentication. The wrapper
currently also injects `--dangerously-bypass-approvals-and-sandbox`; therefore
the temporary directory and prompt constrain the job's intended scope, but this
is not an OS-enforced Codex sandbox.

The command prefix is configurable:

```sh
util/summarize_article INPUT --codex-command 'cdx now8pm'
EPITOME_CODEX_COMMAND='cdx ms2' util/summarize_article INPUT
```

This accepts a command prefix rather than only an executable path so account
selectors and future wrappers can be used. Each catalog entry records the exact
prefix.

## Build and view the summary site

```sh
util/build_summary_site
util/serve_summaries --port 8014
```

The generated static site is written to ignored `dist/summaries/`; its source
data and generator remain tracked. Open `http://127.0.0.1:8014/` to browse all
records. Complete summaries link to their original OpenAI article. Error
records remain visible so extractor regressions cannot disappear silently.

The first bounded validation exposed a real partial-DOM extraction: the GPT‑5.6
input ended during footnote 3 even though the article referenced eight
footnotes. After adding bounded scrolling and note-target validation, the
article was extracted again with all eight notes.

The current two records were both generated through `cdx`:

- the 2023 “ChatGPT can now see, hear, and speak” extraction summarized
  successfully with 95% status confidence;
- the repaired GPT‑5.6 extraction summarized successfully with 95% status
  confidence.
