# Epitome

Epitome is an archival project for the public OpenAI website. The intended
outputs are:

1. a high-fidelity, replayable capture of the site; and
2. clean Markdown renditions of OpenAI articles.

The repository contains bounded CDP capture utilities and investigation/design
notes. Captured site data remains private and ignored by Git.

See [docs/network-capture.md](docs/network-capture.md) for current capture usage,
[docs/archive-plan.md](docs/archive-plan.md) for the broader site-capture design,
[docs/markdown-plan.md](docs/markdown-plan.md) for article conversion, and
[TODO.md](TODO.md) for the future source backlog. Current per-source coverage and
active preservation gaps are tracked in [STATUS.md](STATUS.md); external-media
import mappings live under [inventories/](inventories/README.md).

Quick start:

```sh
util/capture_url 'https://openai.com/index/example/'
util/url_to_markdown 'https://openai.com/index/example/'
util/serve_archive data --port 8013
util/summarize_article output/markdown/openai.com-index-example.md
util/serve_summaries --port 8014
```

The archive browser is then available at `http://127.0.0.1:8013/`. It rewrites
captured pages for local-only static replay and never falls back to the live
site. See [docs/replay.md](docs/replay.md).

The independent summary browser is available at `http://127.0.0.1:8014/`.
Summary Markdown and its catalog are tracked, while Codex run diagnostics and
generated site files stay ignored. See [docs/summaries.md](docs/summaries.md).
