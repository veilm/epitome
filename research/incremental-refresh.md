# Incremental source refresh

## Refresh plan 1789091412

On 2026-09-11, the reviewed all-source plan found 130 newly listed canonical
identities after deduplicating against each source's full existing archive.
The bounded capture order is OpenAI 70, Anthropic 15, Claude 28, Dwarkesh 6,
SemiAnalysis 9, AI 2040 1, and Paul Graham 1. All other configured source
families had zero new identities in this snapshot. Known historical but
uncaptured backlogs—especially Anthropic and Claude—remain excluded from this
refresh and are not silently treated as new work.

The OpenAI 70-identity delta is complete at
`/mnt2/capsule/epitome/openai/refresh/1789091412`: 70/70 manifests are
complete and tab-closed, `finish.failures=0`, both image audits are clean, and
excluded-host result URLs are absent. Its optional same-origin 403 asset
failures, response-level status/dependency records, 44 hydrated Vimeo
references, and representative loopback replay results are documented in
`research/openai-careers.md`. The 15-identity public Anthropic delta is now
complete at `/mnt2/capsule/epitome/anthropic/refresh/1789091412`: all manifests
are complete/tab-closed, `finish.failures=0`, both image audits are clean, and
excluded-host result URLs are absent; its seven policy exclusions and six
response-level partial/pending records are documented in `research/anthropic.md`.
The 28-identity public Claude delta is now complete at
`/mnt2/capsule/epitome/claude/refresh/1789091412`: all manifests are
complete/tab-closed, `finish.failures=0`, both image audits are clean, and
excluded-host result URLs are absent; its 32 redirect/pending response records,
three policy exclusions, and offline replays are documented in
`research/anthropic.md`. The six-identity public Dwarkesh delta is now complete
at `/mnt2/capsule/epitome/dwarkesh/refresh/1789091412`: all manifests are
complete/tab-closed, `finish.failures=0`, both image audits are clean, the four
optional oversized video failures and four YouTube-nocookie exclusions are
classified, and the audited replays stayed on the loopback archive server.
The nine-identity public SemiAnalysis delta is also complete at
`/mnt2/capsule/epitome/semianalysis/refresh/1789091412`: all manifests are
complete/tab-closed, `finish.failures=0`, both image audits are clean, four
response-level records are classified, no asset failed, and the audited
replays stayed on the loopback archive server with the paid boundary intact.
The one-identity public AI-2040 delta is also complete at
`/mnt2/capsule/epitome/ai-2040/refresh/1789091412`: its manifest is
complete/tab-closed, `finish.failures=0`, both image audits are clean, two
pending response records are classified, and the replay stayed on the
loopback archive server. The one-identity public Paul Graham delta is now also
complete at `/mnt2/capsule/epitome/paul-graham/refresh/1789091412`: its
manifest is complete/tab-closed, `finish.failures=0`, both image audits are
clean, all ten responses returned HTTP 200, the one attempted asset completed,
and the local replay stayed on the loopback archive server with substantive
text and images intact. No prohibited-host result URL was recorded.

All 130 identities in refresh plan 1789091412 have now been captured or
confirmed complete in their source-scoped output roots. A final plan-only
all-source discovery check remains the handoff gate for newly listed pages;
historical uncaptured backlogs remain out of scope.

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
