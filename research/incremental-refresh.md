# Incremental source refresh

The first all-source update check ran on 2026-08-10 with
`util/refresh_sources`. Discovery covered all 17 configured first-party source
families and separated newly listed URLs from reviewed but uncaptured historical
backlog. The reviewed plan contained exactly 25 new publications:

- 16 OpenAI `/index/` pages;
- two Anthropic pages;
- six Claude blog posts; and
- one SemiAnalysis newsletter post.

Every other configured source had zero newly listed URLs. The plan kept 162
Anthropic, 41 Claude, 77 Paul Graham, and 1,554 Slate Star Codex historical
identities out of the update capture. These remain explicit backlog rather than
being mistaken for new publications. YouTube and Twitter/X were not downloaded.

## Capture and audit

The captures are stored under the private archive's per-source `refresh/`
directories. OpenAI completed 15 pages in its first run; one page lost its
temporary CDP session and the source-scoped retry selected only that missing
identity. Anthropic completed 2/2, Claude 6/6, and SemiAnalysis 1/1. All 25 final
manifests are complete and tab-closed, with zero asset-completion failures.

Primary and all-rendered-image audits report zero missing images. Script-free
Chromium replay sampled OpenAI's Model ML page, Anthropic's Riemann-zeta
research post, Claude's production auto-mode post, and the new SemiAnalysis
article. The four pages retained 9,638–25,140 visible characters, rendered 1–22
images with zero broken images, and loaded no production-origin resources.
SemiAnalysis faithfully ends at its public paid-subscriber boundary.

Reviewed baselines are tracked under `sources/`, including the larger OpenAI,
Anthropic, and Claude lists, so a fresh checkout can reproduce the distinction
between old backlog and future live-listing additions. The normal workflow is:

```sh
util/refresh_sources
util/refresh_sources --capture
```

The first command is plan-only. The second must follow URL review and captures
only the newly listed delta. `--source SOURCE_ID` supports isolated retries
without repeating successful sources.
