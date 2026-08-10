# AI Futures Model reconnaissance

Investigated through browser-backed deep research and independently checked in
Chromium on 2026-08-10. This is a distinct, bounded AI Futures Project release,
not an AI 2027 subpage or an AI 2040 alias.

## Identity and date

The canonical site is `https://www.aifuturesmodel.com/`. Its About page calls
it the December 2025 AI Futures Model and describes it as the project's improved
timelines and takeoff model. The first-party launch article at
`https://blog.aifutures.org/p/ai-futures-model-dec-2025-update` and the AI 2027
changelog both identify 2025-12-31 as its publication date.

Use `published_at=2025-12-31` for the release. The current About changelog ends
at 2026-04-02, when model parameters, all-things-considered distributions, and
METR data were updated; keep that as `updated_at`, not a replacement publication
date.

## Reviewed web-app scope

The five same-host identities in `sources/ai-futures-model.txt` cover the main
interactive explanation, About/changelog, behavior analysis, forecast selector,
and the historical `/results` route linked by the launch material. The current
navigation uses `/analysis`; preserve `/results` until capture proves whether it
is an alias or a distinct historical route.

The forecast selector exposes eight dated Eli/Daniel parameter states from
2025-12-29 through 2026-04-02. Treat them as versioned model states, not eight
independent publications. Preserve their exact serialized parameters and enough
representative share states to reconstruct the application without recursively
crawling the combinatorial query space.

Several launch links point to different tabs of one first-party Google document
containing supplementary material. Inventory and preserve that complete
multi-tab document as an external-hosted first-party dependency after recording
its exact document identity. No dedicated first-party PDF was found in current
bounded navigation.

Before a batch, validate one representative page through Chromium capture and
offline replay. Require the app shell, JavaScript/CSS, same-origin model data,
charts, and forecast definitions—not merely a screenshot or final canvas—to be
retained.

## Representative capture validation

A homepage, forecast, and analysis pilot completed at
`/mnt2/capsule/epitome/ai-futures-model/validation/1786383520-pilot`. All three
manifests are complete and tab-closed; 239 queued dependencies completed with
no failures, and both image audits are clean. Homepage replay retains the model
diagram, SVG charts, parameter sliders and values, and its 61,922 visible
characters. Forecast replay retains both charts, milestone controls, and all
eight Eli/Daniel dated parameter states.

The first analysis capture serialized a complete Next.js streamed response
before its boundary swap, leaving the article hidden behind `Loading results`
in script-free replay. The live route takes roughly ten seconds to materialize.
A targeted 15-second-settle retry at
`/mnt2/capsule/epitome/ai-futures-model/validation/1786384586-analysis-retry`
captures the post-swap DOM, with no hidden streaming boundary. Its replay shows
10,165 visible characters, all seven analysis section headings, and eight plot
images. A fresh reload made sixteen requests, all to loopback.

Use at least a 15-second settle for the remaining app routes. The bounded
five-route scope is approved for completion; retain the first analysis attempt
as evidence of the timing failure, but serve the newer complete identity.

The final `/about` and `/results` requests completed at
`/mnt2/capsule/epitome/ai-futures-model/crawls/1786385455`, with complete,
tab-closed manifests and no asset failures. About replay preserves the complete
changelog through 2026-04-02. `/results` resolves to `/analysis`; isolated replay
serves both requested identities from the same fully materialized analysis
capture. It is therefore a preserved historical alias, not a fifth canonical
publication.

The finished archive contains five requested identities, four canonical pages,
and no missing images. Catalog all four canonical pages with the 2025-12-31
release date and retain 2026-04-02 separately as their latest documented update.
The bounded AI Futures Model web-app scope is complete.
