# Anthropic source reconnaissance

Checked through Chromium/CDP on 2026-08-04. No direct HTTP client was used for
this investigation. The browser-only sitemap utility added during the research
is `research/list_sitemap_urls_cdp`.

## Publication surfaces

Anthropic has two distinct first-party publication systems worth preserving:

1. `https://www.anthropic.com/sitemap.xml` currently contains 509 URLs:
   - 254 under `/news` (the index plus 253 posts);
   - 150 under `/research` (the index plus 149 posts);
   - 26 under `/engineering` (the index plus 25 posts);
   - four feature stories, nine event pages, four learning pages, and smaller
     policy, governance, economic, model, legal, and institutional collections.
2. `https://claude.com/sitemap.xml` is a separate multilingual product-site
   sitemap. After excluding localized path prefixes, it currently contains 201
   individual `/blog/` posts. This is where many Claude Code, agent workflow,
   context engineering, security, and product-usage articles live.

The Anthropic homepage and newsroom expose company announcements and model
launches under `/news`. Research posts and engineering guidance have their own
collections. Some older `/engineering/` sitemap URLs now redirect to the
standalone Claude Code documentation site, so captures must retain both the
requested and final canonical URL rather than assuming every sitemap URL remains
an Anthropic article.

Developer documentation is a lower-priority, separately versioned source. It is
not required to preserve company news, policy, research, model announcements, or
the editorial technical guidance found in Anthropic Engineering and the Claude
blog.

## Discovery commands

These commands load the public sitemap in a disposable CDP tab, list only the
desired paths, and close the tab afterward:

```sh
research/list_sitemap_urls_cdp https://www.anthropic.com/sitemap.xml \
  --include-path-prefix /news/ \
  --include-path-prefix /research/ \
  --include-path-prefix /engineering/ \
  --include-path-prefix /features/ \
  --output data/inventories/anthropic-publications.txt

research/list_sitemap_urls_cdp https://claude.com/sitemap.xml \
  --include-path-prefix /blog/ \
  --output data/inventories/claude-blog.txt
```

`data/` is ignored. Before a real crawl, review and add the important singleton
pages that do not live below a post collection, including the constitution,
Responsible Scaling Policy and updates, transparency material, economic work,
system cards, and major policy initiatives.

The existing `util/capture_urls` engine already provides bounded batches,
inter-page delays, progress/error ledgers, completed-capture deduplication,
network-body preservation, offline replay inputs, and automatic tab cleanup.
It accepts Anthropic and Claude URLs without a site-specific crawler fork.

## Extraction validation

A three-page browser-only archive sample covered a model announcement, a long
research article, and a Claude Code technical article. All three captures
completed and closed their tabs. The model-readable extractor achieved 98.2%,
99.4%, and 98.7% word coverage with no quality warnings.

Anthropic article pages use `article` as their useful content root and end in a
“Related content” section. Claude blog posts use `main` and end in “Related
posts.” These rules are now recorded in `research/site_rules.json`. Publication
date recovery supports the visible Anthropic byline date and Claude's JSON-LD
`datePublished` value.

Media requires the same full network capture used for OpenAI. The tested Claude
Code post contained article images and a YouTube privacy-domain iframe. A future
offline review should specifically verify YouTube embeds, downloadable PDFs,
responsive Webflow images, and any video streams before approving a large
Anthropic batch.

## Dario Amodei writing

The newsroom's browser search finds direct Dario-attributed company statements,
including American AI leadership, the Paris AI Action Summit, the UK AI Safety
Summit, and the Department of War discussion. Longer Dario essays are not a
single reliable sitemap category and some are hosted outside the main Anthropic
post collection.

The personal-site and external-index gap audit is recorded in
`research/dario-amodei.md`. In brief, the personal sitemap has only five writing
pages, its `Archive` link currently returns 404, and its interview list is
stale. The reviewed union of the personal homepage and one independent index is
already at least 17 interviews, plus several additional primary-source
candidates found separately.

The eventual inventory should combine:

- explicit Dario matches from page author/byline metadata and newsroom search;
- a small reviewed list of standalone first-party Dario essay URLs;
- canonical redirects and publication dates; and
- outbound official links from Anthropic pages, without recursively crawling
  unrelated sites.

Do not infer authorship merely because a page mentions Dario in its body.

## Careers

`/careers/jobs` was revalidated through Chromium/CDP on 2026-09-04. It rendered
as `Jobs \\ Anthropic` with 53,335 body-text characters and 590 unique opening
links, each carrying a stable numeric `job-boards.greenhouse.io` job ID. The
index had no images, broken images, frames, video, or audio. The count is a
versioned observation and supersedes the earlier 254-opening observation; it
must not be treated as a permanently complete inventory. The main sitemap
contains only `/careers` and `/careers/jobs`, not those individual job pages.

The careers crawler therefore needs a second discovery step from the rendered
jobs index. Store the external job ID, title, department, locations,
first-seen/last-seen timestamps, and the full posting snapshot. Incremental runs
should preserve removed listings instead of deleting or overwriting their last
known content.

The first bounded public-only pilot is prepared in the ignored
`data/anthropic-careers-pilot.txt` and contains the index plus six distinct
Greenhouse detail pages:

1. `https://www.anthropic.com/careers/jobs` — current public job index.
2. `https://job-boards.greenhouse.io/anthropic/jobs/4980436008` — Research
   Manager, Interpretability; San Francisco.
3. `https://job-boards.greenhouse.io/anthropic/jobs/5076109008` — Applied AI
   Architect; Tokyo.
4. `https://job-boards.greenhouse.io/anthropic/jobs/5394887008` — Product
   Manager, Claude Science; San Francisco/New York/Seattle.
5. `https://job-boards.greenhouse.io/anthropic/jobs/5254582008` — Policy
   Communications; San Francisco/New York.
6. `https://job-boards.greenhouse.io/anthropic/jobs/5391293008` — Enterprise
   Account Executive, Automotive; Paris.
7. `https://job-boards.greenhouse.io/anthropic/jobs/5287327008` — Salesforce
   Developer, Partnerships; San Francisco/New York/Seattle.

The six details were live-validated as public Greenhouse job pages. They
rendered 21,332, 9,568, 21,398, 19,708, 15,302, and 18,054 body-text
characters respectively, each with one intact image and no broken images,
video, or audio. No application link was opened. The related Fellows page was
deliberately not selected for this first pilot because it exposes a visible
external application form reference and an embedded frame; that reference
remains outside the public archive lane.

This is an explicitly bounded job-board pilot, not a request to crawl every
current opening in one pass. Keep the Greenhouse detail URLs public-only,
record application links as references without following them, and retain the
same exact asset-host exclusions used by the other low-risk lanes.

## Careers N+1 preparation

The pilot’s archived index was used to prepare the ignored
`data/anthropic-careers-next-15.txt`. It contains the first 15 uncaptured
Greenhouse detail IDs in the captured display order, after removing the six
pilot detail IDs. The four immediately adjacent Fellows listings
(`5023394008`, `5183044008`, `5183051008`, and `5183053008`) are intentionally
held out because the live validation showed an embedded frame or visible
external application-form references; they remain public references for a
separate boundary review and were not opened. The N+1 list is therefore a
bounded 15-page detail-only continuation with no application URLs.

## Careers N+1 result

The continuation in `/mnt2/capsule/epitome/anthropic-careers/crawls/1788497343-next-15`
completed all 15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and every capture tab closed. The batch recorded 431
requests, 419 response bodies, 8 response-body error records, and 41,171,966
response bytes. Statuses were 419 HTTP 200 responses, four HTTP 401 records,
and eight pending records. The 401/pending records were optional Greenhouse
application scaffolding and asynchronous dependencies, not a failure to render
the public job descriptions.

Page 10 (`5357746008`, Life Sciences Operator, Lead) was the only unusual
route: it made 42 requests with 39 response bodies and two response-body error
records. Its public page rendered the job description and application-form
shell. The related `my.greenhouse.io` 401, Google Picker/identity,
reCAPTCHA, Dropbox Chooser, and Snowplow traffic was classified as optional
application-reference, anti-abuse, or telemetry behavior. No application form
was submitted and no application link was opened.

The asset ledger contained 351 discovered assets, 178 attempted and completed
downloads, 173 already-complete entries, 0 failures, 0 exclusions, and
7,638,828 downloaded bytes. Interactive media was zero across all 15 pages.
Both primary-image and all-rendered-image audits reported 15/15 pages with
zero missing images. A local-only archive replay of early page `4951814008`,
the page-10 form/reference case `5357746008`, and late page `5224564008`
preserved 16,927, 17,666, and 19,414 body-text characters respectively, with
one intact logo image on each and no broken images, video, or audio. The
middle replay exposed three local reCAPTCHA frames as expected; early and late
pages exposed no frames. Its 25 network records were loopback-only (19 HTTP
200, one intentionally unavailable captured reCAPTCHA stylesheet at HTTP 404,
and five pending), with no production-origin or excluded-host result.

The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15b.txt`. It contains the next 15 IDs in the
archived 590-ID index order after excluding the six pilot details, the four
held-out Fellows/application-form-heavy listings, and the completed
`next-15` continuation. This keeps application links as references only while
continuing the versioned public job-identity snapshots.

## Careers N+1b result

The `next-15b` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788499452-next-15b` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all tabs closed. It recorded 506 requests, 482
response bodies, 16 response-body error records, and 70,300,621 response
bytes. The status ledger contained 482 HTTP 200 responses, eight HTTP 401
session probes, and 16 pending asynchronous records. The eight error-bearing
pages were ordinary application-shell variants: their public descriptions
rendered while `my.greenhouse.io` session checks, Google Picker/identity,
reCAPTCHA, Dropbox Chooser, and telemetry remained optional boundary traffic.

Three public Anthropic PDF references were captured from
`www-cdn.anthropic.com`; they were treated as reference assets, not as
application routes. The asset ledger contained 362 discovered assets, 181
attempted and completed downloads, 181 already-complete entries, 0 failures,
0 exclusions, and 29,072,724 downloaded bytes. Interactive media was zero.
Both image audits reported 15/15 pages with zero missing images.

Local-only early/middle/late replays of `5367417008`, `5231612008`, and
`5198074008` preserved 17,776, 17,496, and 8,010 body-text characters, one
intact logo image per page, and no broken images, video, or audio. The middle
and late pages exposed three local application/anti-abuse frames each; no
application route was opened or submitted. The replay logger recorded 32
loopback-only requests (23 HTTP 200, two unavailable captured reCAPTCHA
stylesheet 404s, and seven pending), with no production-origin or
excluded-host result.

The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15c.txt`, continuing the archived index after the
pilot, held-out Fellows listings, `next-15`, and `next-15b`.

## Careers N+1c result

The `next-15c` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788505201-next-15c` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and no remaining capture tab. It recorded 482
requests, 461 response bodies, 14 response-body error records, and 46,753,580
response bytes. The status ledger contained 461 HTTP 200 responses, seven
HTTP 401 session probes, and 14 pending asynchronous records. These were the
same optional Greenhouse application-shell, anti-abuse, Google/Dropbox,
reCAPTCHA, and telemetry boundary dependencies seen in earlier batches; no
application or authenticated route was opened.

The asset ledger contained 355 discovered assets, 176 attempted and completed
downloads, 179 already-complete entries, 0 failures, 0 exclusions, and
7,514,706 downloaded bytes. Interactive media was zero. The primary and
all-rendered-image audits both reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5198108008`, `5160330008`, and
`5239733008` preserved 16,657, 17,023, and 18,857 body-text characters, one
intact logo image per page, and no broken images, frames, video, or audio.
The replay logger recorded 18 loopback-only requests (15 HTTP 200 and three
pending), with no production-origin or excluded-host result. The replay tabs
and server were closed after validation.

The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15d.txt`, continuing the archived index after the
pilot, held-out Fellows listings, `next-15`, `next-15b`, and `next-15c`.

## Careers N+1d result

The `next-15d` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788511006-next-15d` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 503
requests, 478 response bodies, 17 response-body error records, and 48,834,539
response bytes. The status ledger contained 478 HTTP 200 responses, eight
HTTP 401 session probes, and 17 pending asynchronous records. The error and
session traffic was classified as optional Greenhouse application-shell,
anti-abuse, Google/Dropbox, reCAPTCHA, and telemetry boundary traffic; no
application or authenticated route was opened.

The asset ledger contained 359 discovered assets, 178 attempted and completed
downloads, 181 already-complete entries, 0 failures, 0 exclusions, and
7,638,828 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5387564008`, `5370690008`, and
`5227672008` preserved 17,376, 13,510, and 9,422 body-text characters and one
intact logo image per page, with no broken images, video, or audio. The early
and late pages exposed three archived optional frames each; the middle page
exposed none. The replay logger recorded 32 loopback-only requests (23 HTTP
200, two unavailable captured Google reCAPTCHA stylesheet 404s, and seven
pending), with no production-origin or excluded-host result. The replay tab
and server were closed after validation.

The archived index still has 505 uncaptured public job identities after this
batch. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15e.txt`; application links remain references
only and the four held-out Fellows/application-form-heavy listings remain
outside the ordinary lane.

## Careers N+1e result

The `next-15e` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788516808-next-15e` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 532
requests, 500 response bodies, 22 response-body error records, and 51,933,465
response bytes. The status ledger contained 500 HTTP 200 responses, ten
HTTP 401 session probes, and 22 pending asynchronous records. These records
were classified as optional Greenhouse application-shell, anti-abuse,
Google/Dropbox, reCAPTCHA, and telemetry boundary traffic; no application or
authenticated route was opened.

The asset ledger contained 355 discovered assets, 170 attempted and completed
downloads, 185 already-complete entries, 0 failures, 0 exclusions, and
7,142,340 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5390735008`, `5383335008`, and
`5300430008` preserved 9,668, 18,472, and 17,837 body-text characters and one
intact logo image per page, with no broken images, video, or audio. The early
and middle pages exposed three archived optional frames each; the late page
exposed none. The replay logger recorded 32 loopback-only requests (23 HTTP
200, two unavailable captured Google reCAPTCHA stylesheet 404s, and seven
pending), with no production-origin or excluded-host result. The replay tab
and server were closed after validation.

The archived index has 490 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15f.txt`; application links remain references
only and the four held-out Fellows/application-form-heavy listings remain
outside the ordinary lane.

## Careers N+1f result

The `next-15f` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788792009-next-15f` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 426
requests, 413 response bodies, nine response-body error records, and
40,683,201 response bytes. The status ledger contained 413 HTTP 200
responses, four HTTP 401 session probes, and nine pending asynchronous
records. These were classified as optional Greenhouse application-shell,
anti-abuse, Google/Dropbox, reCAPTCHA, and telemetry boundary traffic; no
application or authenticated route was opened.

The asset ledger contained 346 discovered assets, 173 attempted and completed
downloads, 173 already-complete entries, 0 failures, 0 exclusions, and
7,328,523 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5390877008`, `5227641008`, and
`5390890008` preserved 18,561, 10,862, and 18,825 body-text characters and
one intact logo image per page, with no broken images, video, or audio. The
early page exposed three archived optional frames; the middle and late pages
exposed none. The replay logger recorded 25 loopback-only requests (19 HTTP
200, one unavailable captured Google reCAPTCHA stylesheet 404, and five
pending), with no production-origin or excluded-host result. The replay tab
and server were closed after validation.

The archived index has 475 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15g.txt`; application links remain references
only and the four held-out Fellows/application-form-heavy listings remain
outside the ordinary lane.

## Careers N+1g result

The `next-15g` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788797701-next-15g` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 356 requests,
356 response bodies, no response-body errors, and 33,307,746 response bytes;
all 356 responses were HTTP 200. The observed hosts were limited to the
Greenhouse job page and CDN hosts, with no application or authenticated route
opened.

The asset ledger contained 341 discovered assets, 176 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,514,706 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5390865008`, `5383388008`, and
`5240487008` preserved 20,671, 19,278, and 17,118 body-text characters and
one intact logo image per page, with no broken images, frames, video, or
audio. The replay logger recorded 18 loopback-only requests (15 HTTP 200 and
three pending), with no production-origin or excluded-host result. The replay
tab and server were closed after validation.

The archived index has 460 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15h.txt`; application links remain references
only and the four held-out Fellows/application-form-heavy listings remain
outside the ordinary lane.

## Careers N+1h result

The `next-15h` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788803485-next-15h` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 355
requests, 354 response bodies, one response-body/status boundary record, and
33,097,824 response bytes. The status ledger contained 354 HTTP 200
responses and one HTTP 302 redirect for job `5406245008`; the page remained
complete. This was classified as ordinary Greenhouse routing traffic, with
no application or authenticated route opened.

The asset ledger contained 339 discovered assets, 174 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,390,584 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5252781008`, `5405710008`, and
`5405748008` preserved 18,527, 11,159, and 23,052 body-text characters and
one intact logo image per page, with no broken images, frames, video, or
audio. The replay logger recorded 18 loopback-only requests (15 HTTP 200 and
three pending), with no production-origin or excluded-host result. The replay
tab and server were closed after validation.

The archived index has 445 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15i.txt`; application links remain references
only and the four held-out Fellows/application-form-heavy listings remain
outside the ordinary lane.

## Proposed first bounded batch

Before any large crawl, use roughly 10–15 deliberately varied pages:

- recent and old newsroom posts;
- short company statements and long model announcements;
- long research posts with footnotes, figures, and downloadable papers;
- several Engineering and Claude blog posts with code, images, and embeds;
- one feature story, policy page, system card/PDF, careers index, and external
  Greenhouse job page.

Inspect offline replay and extracted text for every sample. Only then generate
the larger deduplicated URL lists and choose a delay appropriate to their size.
