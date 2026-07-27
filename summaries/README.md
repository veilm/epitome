# Article summaries

`articles/` contains tracked Markdown summaries. Each file has front matter with
the summarizer's `status`, status confidence, title, and original source URL.

`catalog.json` is the machine-readable index. Its `content_path` values are
relative to this directory. The static summary site is generated from these
two sources rather than storing Markdown inside JSON.
