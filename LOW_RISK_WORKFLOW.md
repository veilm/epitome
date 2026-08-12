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
| LessWrong | **Partial.** Taxonomy and the 1,384-post core/curated inventory are complete. The seven-page pilot and all 51 rendered Highlights identities pass offline replay. | Define the next bounded core/curated tier before the lane returns to LessWrong. |
| Paul Graham essays | **Complete: 232/232.** The approved index-and-essay scope is captured and offline-verified. | Only separately scoped dependency recovery and non-essay material remain. |
| Slate Star Codex | **Active.** The 1,562-identity canonical scope, five representative variants, first 15, next 30, and next 45 identities are approved. The following 60 are capturing with Gravatar completion excluded. | **Ready.** `data/slate-star-codex-next-75.txt` contains the following 75 identities. Continue using `--exclude-asset-host secure.gravatar.com`; require primary images and comment text, not complete avatar presentation. |
| Astral Codex Ten | **Not started as a capture scope.** It is intentionally separate from Slate Star Codex. | Inventory canonical archive/post identities and validate a small ordinary, long, comment-heavy, and media-bearing pilot. |
| Import AI by Jack Clark | **Not started.** First-party Substack home is identified. | Inventory archive/feed identities, email-only differences if any, attachments, and a varied pilot. |
| Gwern.net | **Not started.** Preliminary research identifies a large first-party site, so it must be divided into bounded families. | Inventory major essays, blog entries, and first-party documents; prepare a varied pilot rather than crawling the whole link graph at once. |
| near.blog and its link graph | **Not started.** Both Near's own pages and the specifically linked external corpus are in scope. | Inventory Near pages first. Preserve outbound-link provenance from the links post, prioritize linked sources, and bound recursive discovery before capture. |
| OpenAI careers and jobs | **Not started as a versioned job scope.** The general OpenAI public-site archive is complete. | Inventory careers indexes and individual job identities with stable job IDs plus first/last-seen and removal-history fields. |
| Anthropic careers and jobs | **Not started as a versioned job scope.** The general Anthropic public-site archive is page-complete. | Inventory the careers index and Greenhouse listings with the same first/last-seen and removal-history model. |

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
