# Low-risk source capture workflow

This is the operating queue for sources the user has explicitly classified as
low risk. Until every source below is complete, keep one bounded capture batch
running whenever the public CDP browser and archive storage are healthy.

Low risk means that the source has ordinary public pages and a scraper failure
is unlikely to cause harm. It does not waive Epitome's completeness, offline
replay, deduplication, pacing, or source-boundary validation requirements.

## Pipeline rule

Maintain two positions:

1. **N — active:** one capture batch is running.
2. **N+1 — ready:** the next batch has a reviewed canonical URL list, known
   output and existing-root paths, capture arguments, expected URL count, and
   a brief validation plan. Starting it must require no new reconnaissance.

When N finishes, validate it promptly and start N+1. Research and prepare the
new N+1 while the new N runs. Do not leave the capture lane empty merely to do
documentation, catalog rebuilding, recovery of dead outbound dependencies, or
research that can happen alongside a healthy batch.

Use one capture batch at a time by default. This avoids competing for the same
CDP browser, saturating archive storage, and confusing tab or process failures.
Catalog and unified archive-server rebuilds are not capture batches and do not
satisfy the active-lane rule.

## Readiness gate

Before a batch becomes N+1-ready, record or verify:

- canonical identities and displayed ordering where ordering is meaningful;
- deduplication against the source's full existing archive root;
- exclusions for aliases, feeds, login/account pages, and out-of-scope media;
- a bounded first batch for a new source, followed by progressively larger
  batches only after representative replay passes;
- exact command, CDP port, output root convention, pacing, and asset budget;
- expected manifest count after known deduplication;
- representative image, text, comment, PDF, redirect, and offline-network
  checks appropriate to the source.

Never download YouTube or Twitter/X as an incidental dependency of these page
batches. Inventory those identities for a separately approved media workflow.

## Alarm policy

Every long-running capture uses the Codex alarm workflow. Choose the checkpoint
from observed survival and throughput rather than a fixed ritual:

- For a new or recently failing source, check after the first one or two pages,
  commonly in 5–15 minutes.
- After several clean pages, estimate completion from actual completed manifests
  and page spacing, then set the alarm near the source or batch boundary with a
  modest buffer.
- A stable 160-page batch averaging one minute per page warrants roughly a
  170–180 minute checkpoint.
- If failures recur after about five minutes, continue with approximately
  five-minute checkpoints until the cause is fixed and survival improves.
- Do not overshoot a plausible early failure window. A dead batch plus a long
  alarm leaves the capture lane unnecessarily idle.

Each alarm message must include the PID/session, exact output root, expected and
completed counts, active URL if any, pacing, known failure pattern, checks to
perform on return, N+1's prepared command/list, and the prohibition on
YouTube/Twitter/X downloads.

## Low-risk queue and current status

| Queue item | Current status | N+1 readiness / next action |
| --- | --- | --- |
| LessWrong | **Partial.** Taxonomy and the 1,384-post core/curated inventory are complete. The seven-page pilot, all 51 rendered Highlights identities, all 19 Janus identities, the nine-route priority pilot, and all deduplicated priority sequence members (29 Fun Theory, 12 6BF, and 16 Highly Advanced Epistemology) pass capture/image checks; 13 rendered-only historical/external image gaps are classified and the priority queue is complete. | No further priority batch is queued; preserve the existing LessWrong public archive and deduplication records. |
| Yudkowsky fiction and writing | **Complete: 15/15; explicitly low risk.** The rendered public inventory found the Sword of Good page, a writing index, and 13 canonical linked writing pages. The seven-route varied pilot and eight-route continuation completed with zero page or asset failures, classified Tumblr telemetry/monetization redirects, clean primary/all-image audits, and local-only representative replays after the compression-dictionary fix. | Public fiction/writing scope is complete; preserve the 15-route archive and wait for a future reviewed source refresh. |
| Paul Graham essays | **Baseline plus incremental refresh complete: 233/233 approved identities.** The approved index-and-essay scope is captured and offline-verified; the newly listed public *How Universities Should Prepare Founders* route completed with `finish.failures=0`, clean image audits, and a substantive loopback replay. | Preserve the completed public archive and refresh history; await a future reviewed source snapshot. |
| George Hotz blog | **Complete: 146/146 reviewed routes.** The 143 canonical Jekyll posts plus home/about/feed structural routes are captured across the clean seven-route pilot and 139-route completion batch. Both runs have `finish.failures=0`, all manifests are complete/tab-closed, image audits report zero missing images, five optional external PDF/reference failures are classified, no interactive media or prohibited-host results occurred, and combined local replays preserved substantive content with no live-origin fallback. | Preserve the public Jekyll archive and refresh from the rendered homepage when a future reviewed snapshot is requested; social links remain references only. |
| Greg Brockman blog | **Complete: 20/20 reviewed routes.** The seven-route pilot and 13-route deduplicated completion run have `finish.failures=0`, complete/tab-closed manifests, clean primary/all-rendered-image audits, zero interactive media, zero prohibited-host result URLs, and local-only structural/early/middle/reference/image/late replays with no live-origin fallback. Two optional external-reference records are classified: one unavailable CloudFront PDF and one 301/response-body record. | Preserve the public SVBTLE archive and refresh from both rendered listing pages when a future reviewed snapshot is requested; the X link remains a reference only. |
| Sam Altman blog | **Complete: 136/136 reviewed public routes.** The seven-route pilot plus 129-route deduplicated completion run have `finish.failures=0` and complete/tab-closed manifests. All page, asset, response, and incidental telemetry outcomes are classified: 129 repeated optional `loading128.gif` 404s, two unavailable PDF references, two unavailable legacy Google-image references, two Box-viewer asset failures, one font timeout, two pending duplicate image-status records, and two incidental `syndication.twitter.com` share GIF records. There are zero interactive media captures, zero exact prohibited-host result URLs, and no downloader use. Primary/all-rendered-image audits identify only the same two source-side missing Google images on `?page=5` and `/affordable-care`; 12 representative local-only replays preserved substantive content with 362 loopback-only requests and no live-origin fallback. | Preserve the complete public archive; future refreshes should re-review the home/archive/Atom and 13 listing views, deduplicate canonical posts, and capture only new public posts. Keep Posthaven administrative/authentication paths out of scope. |
| Slate Star Codex | **Complete: 1,562/1,562.** The reviewed canonical publication scope and five representative variants are captured and offline-verified. Comment text and substantive images are preserved; Gravatar completion remains intentionally excluded. | Only separately scoped dependency recovery or newly published material remains. |
| Astral Codex Ten | **Fourteen bounded production batches complete: 1,449 pages, plus a five-page pilot.** The 1,452-identity source snapshot is fully covered; the union of working lists also contains two historical list-only URLs (`/archive` and `/mistakes`) outside that snapshot. The batches preserve long articles, images, comments, media references, and the paid-preview boundary. The final 84-page batch is complete and tab-closed with zero capture-level page failures; its 215 response-body errors and 209 incomplete asset results were classified. Primary/all-rendered-image audits classified one primary and three rendered missing images, including one intentionally excluded Twitter-host avatar variant. Paid-preview, comment-heavy, media/reference, and known-missing-image local-only replays completed with no production-origin requests. Exact YouTube/Twitter/X asset exclusions recorded five decisions with no excluded-host asset result; no YouTube or Twitter/X downloader was invoked. | Source-backed queue exhausted; monitor for a new intentional source snapshot before preparing another bounded batch. Preserve the port-2103-only workflow, access boundary, bounded asset policy, and exact host exclusions. |
| Import AI by Jack Clark | **Complete pilot: 5/5; explicitly low risk.** The public Substack routes completed with zero capture failures; preview, platform-frame, reporting, and challenge records were classified, both image audits were clean, prohibited-host result URLs were absent, and five local-only replays made no production-origin requests. Article replays preserve the available preview without crossing the paywall. | Preserve the public-preview boundary while expanding only through a separately reviewed archive or outbound-link scope. |
| Gwern.net | **Bounded families complete: 19/19 routes; explicitly low risk.** The seven-route public-shape pilot and twelve-route major-essay family are complete and tab-closed with `finish.failures=0`. The major family’s 287 response-body errors and 275 optional-asset failures are classified, including the `/face` completion-budget boundary, public-reference 403/404/DNS/TLS/no-route/timeout results, 42 known missing images, zero interactive media, zero excluded-host asset results, and zero downloader use. Both image audits and representative early/middle/late, reference-heavy, media-heavy, and loopback replays passed the substantive-content/public-boundary checks; `/embryo-selection` remains separately deferred direct-video scope. | Preserve the bounded archive and wait for a future reviewed Gwern source snapshot; keep direct-video and broader unbounded graph scope out of the ordinary page lane. |
| Cyborgism Wiki | **Complete: 7/7; explicitly low risk.** The public pilot completed with zero page failures, classified the repeated missing favicon 404 and three linked public PDF references, passed both image audits, and passed five local-only structural/image replays. | Preserve the bounded public pilot and wait for a future reviewed source snapshot. |
| Generative Ink | **Complete: 7/7; explicitly low risk.** The public pilot completed with zero page failures, classified the 28 repeated favicon 404s, one unavailable CloudFront PDF, external reference assets, and pending/redirect body records, passed both image audits, and passed six local-only content/image/media replays. | Preserve the bounded public pilot and wait for a future reviewed source snapshot. |
| alien.v01d.zone | **Complete: 1/1; explicitly low risk.** The canonical public page completed with zero page, response, or asset failures, passed both image audits, preserved all 15 images and 220,166 characters in three local-only long-form/fragment replays, and had no excluded-host results or interactive media. | Preserve the bounded public pilot and wait for a future reviewed source snapshot. |
| Michael Burry article | **Complete: 1/1; explicitly low risk.** The validated public Substack article completed with zero capture/asset failures, zero response-body errors, clean primary/all-image audits, and a local-only replay preserving 35 images and the article text. | Preserve the one-page public archive and wait for a future reviewed source snapshot. |
| Citrini Research article | **Complete: 1/1; explicitly low risk.** The validated public Substack article completed with zero capture/asset failures, zero response-body errors, clean primary/all-image audits, and a local-only replay preserving 26 images and the article text. | Preserve the one-page public archive and wait for a future reviewed source snapshot. |
| near.blog and its link graph | **Complete pilot: 7/7; explicitly low risk.** The bounded WordPress routes completed with zero capture failures; repeated Matomo HTTP 403 telemetry and seven response-body errors were classified, both image audits were clean, prohibited-host result URLs were absent, and seven local-only replays made no production-origin requests. The direct-video `/this-anime-does-not-exist/` route remains deferred to a separate media scope. | Inventory outbound provenance from the links page and bound recursive discovery; keep the direct-video route out of the ordinary page lane. |
| OpenAI careers and jobs | **Incremental refresh complete: 18/18 new public `/index/` identities; explicitly low risk.** All manifests are complete/tab-closed with `finish.failures=0`, clean primary/all-rendered-image audits, zero excluded-host result URLs, two optional same-origin font 403s, six hydrated Vimeo references, and local-only representative replays. | Preserve the completed refresh at `/mnt2/capsule/epitome/openai/refresh/1789621253`; the Claude delta is complete and the prepared four-route SemiAnalysis delta is next. |
| Anthropic careers and jobs | **Baseline plus incremental refresh complete: 610/610 public route pages, explicitly low risk.** The baseline public careers inventory remains 592/592 after the four-route repair; the reviewed 15-identity public news/research refresh and three-page reconciliation completed with all manifests tab-closed, `finish.failures=0`, clean primary/all-rendered-image audits, seven policy-excluded YouTube requests plus zero result URLs, one classified pending response record in the reconciliation, and loopback-only representative replays. No application or authenticated route was opened. | Preserve the completed public-only archive; no new Anthropic identity remains in the reconciled source snapshot. |
| Claude blog and research | **Incremental refresh complete: 8/8 new public routes; explicitly low risk.** The reviewed 37-line public list skipped 29 already-complete URLs and captured eight genuinely new routes with `finish.failures=0`, complete/tab-closed manifests, clean primary/all-rendered-image audits, 221 completed assets with zero failures, and five representative loopback replays. Nine incidental media requests were policy-excluded, including four YouTube iframe dependencies found in browser metadata; no excluded asset-result URL or asset bytes were written. | Preserve `/mnt2/capsule/epitome/claude/refresh/1789621253`; the prepared four-route SemiAnalysis delta is now active as the sole lane. |
| Dwarkesh Substack research | **Incremental refresh complete: 7/7 public posts, explicitly low risk.** The six-page delta and one-page reconciliation completed with `finish.failures=0`, all manifests tab-closed, clean primary/all-rendered-image audits, 18 classified response-level records, five optional oversized video failures, five YouTube-nocookie policy exclusions with zero excluded result URLs, and hydration-aware early/middle/late/media loopback replays with no production-origin requests. | Preserve the public-preview/paywall boundary and recorded Mux/Substack media references; no new Dwarkesh identity remains in the reconciled source snapshot. |
| SemiAnalysis newsletter | **Incremental refresh complete: 4/4 new public routes; explicitly low risk.** All manifests are complete/tab-closed with `finish.failures=0`, both image audits are clean, 842 assets completed with zero failures, four optional HTTP-401 provider/telemetry records classified, zero prohibited-host result URLs, zero interactive-media results, and four local-only long-form/image/paywall replays with the public paid boundary intact. | Preserve `/mnt2/capsule/epitome/semianalysis/refresh/1789621253`; start the prepared one-route Paul Graham delta as the sole next lane. |
| AI-2040 | **Incremental refresh complete: 1/1 public route, explicitly low risk.** The new `/summary` route completed with `finish.failures=0`, its manifest tab-closed, four assets with zero failures, clean primary/all-rendered-image audits, two classified pending response records, zero prohibited-host result URLs, and a substantive local-only replay with no production-origin requests. | Preserve the Plan A summary and public boundary; no new AI-2040 identity remains in refresh plan 1789091412. |

The queue order may change to keep the lane occupied: a later ready batch should
run instead of leaving the lane idle while an earlier source is still being
prepared. Do not bypass the bounded pilot for a brand-new source solely to
preserve queue order.

## Completion handoff

At each batch boundary:

1. Require the expected number of complete, tab-closed manifests and classify
   every page and asset failure.
2. Run primary and all-image audits.
3. Replay representative early, middle, late, and structurally unusual pages
   from an isolated loopback server; require visible substantive content and no
   production-origin resource requests.
4. Document and commit the logical result.
5. Start the prepared N+1 batch before doing work that can safely wait.
6. Update this table whenever N, N+1, coverage, or readiness changes.
