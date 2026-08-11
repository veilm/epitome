# Epitome

Epitome is a general archival system for historically valuable public web
sources. It currently preserves company publications, independent writers, and
newsletters, with additional source families planned. The intended outputs are:

1. high-fidelity page and media captures that replay without contacting the
   original site;
2. clean, model-readable article renditions; and
3. linked summaries suitable for a small static reference site.

The repository contains source-agnostic bounded CDP capture, replay,
model-readable extraction, and summary utilities, plus per-source investigation
notes and inventories. Site-specific recovery rules are added only when an
observed page needs them. Large captured site data remains private and ignored
by Git; compact source lists, status records, media mappings, and summaries can
be tracked.

See [docs/network-capture.md](docs/network-capture.md) for current capture usage,
[docs/archive-plan.md](docs/archive-plan.md) for the broader site-capture design,
[docs/markdown-plan.md](docs/markdown-plan.md) for article conversion, and
[TODO.md](TODO.md) for the future source backlog. Current per-source coverage and
active preservation gaps are tracked in [STATUS.md](STATUS.md); external-media
import mappings live under [inventories/](inventories/README.md).

Quick start, using an OpenAI article as one example source:

```sh
util/capture_url 'https://openai.com/index/example/'
util/url_to_markdown 'https://openai.com/index/example/'
util/serve_archive data --port 8013
util/summarize_article output/markdown/openai.com-index-example.md
util/serve_summaries --port 8014
```

Incremental refreshes use one command. Its safe default discovers each
first-party listing in Chromium, compares both reviewed inventories and complete
capture manifests, and writes a durable plan without downloading articles:

```sh
util/refresh_sources
```

Review the reported `plan.json` and per-source URL files. To capture only the
newly discovered delta with source-specific pacing and settle settings, run:

```sh
util/refresh_sources --capture
```

Use `--source SOURCE_ID` to limit either operation. Known inventory backlog is
reported separately from URLs newly appearing in a live listing, so an update
check does not accidentally turn an unfinished historical scope into an
unbounded crawl.

The reviewed baselines used for this comparison live in `sources/`, including
the larger OpenAI, Anthropic, and Claude inventories. After a captured delta
passes replay and image audits, append its URLs to the applicable baseline so a
fresh checkout preserves the same reviewed state.

The archive browser is then available at `http://127.0.0.1:8013/`. It rewrites
captured pages for local-only static replay and never falls back to the live
site. See [docs/replay.md](docs/replay.md).

The independent public catalog is available at `http://127.0.0.1:8014/`. It
interleaves preserved pages from every source by publication date, supports
source/search/summary filters, links to upstream originals, and exposes the
tracked summaries when available. The compact page catalog and summary Markdown
are tracked, while private captures, Codex diagnostics, and generated site files
stay ignored. See [docs/summaries.md](docs/summaries.md).
