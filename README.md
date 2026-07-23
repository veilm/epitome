# Epitome

Epitome is an archival project for the public OpenAI website. The intended
outputs are:

1. a high-fidelity, replayable capture of the site; and
2. clean Markdown renditions of OpenAI articles.

The repository contains bounded CDP capture utilities and investigation/design
notes. No bulk crawl has been started.

See [docs/network-capture.md](docs/network-capture.md) for current capture usage,
[docs/archive-plan.md](docs/archive-plan.md) for the broader site-capture design,
and [docs/markdown-plan.md](docs/markdown-plan.md) for article conversion.

Quick start:

```sh
util/capture_url 'https://openai.com/index/example/'
util/url_to_markdown 'https://openai.com/index/example/'
```
