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

## Careers N+1i result

The `next-15i` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788809225-next-15i` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 357 requests,
356 response bodies, one response-body/status boundary record, and 33,289,097
response bytes. The status ledger contained 356 HTTP 200 responses and one
HTTP 302 for job `5399221008`; that listing redirected to the public
Greenhouse board error/index shell (`?error=true`) rather than an application
or authenticated route. The resulting page was still captured completely as
public Greenhouse content, and no application route was opened.

The asset ledger contained 341 discovered assets, 176 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,514,706 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images. The
only response-level boundary record was the ordinary Greenhouse routing event
above; the other pages had complete 23/23 or 24/24 response-body coverage.

Local-only early/middle/late replays of `5416016008`, `5399160008`, and
`5240422008` preserved 17,178, 18,339, and 17,983 body-text characters and
one intact 2000px logo image per page, with no broken images, frames, video,
or audio. The replay logger recorded 18 loopback-only requests (15 HTTP 200
and three pending), with no production-origin or excluded-host result. The
replay tab and server were closed after validation.

The archived index has 430 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15j.txt`; application links remain references
only and the four held-out Fellows/application-form-heavy listings remain
outside the ordinary lane.

## Careers N+1j result

The `next-15j` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788815149-next-15j` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 359 requests,
359 response bodies, no response-body errors, and 33,571,075 response bytes;
every recorded response was HTTP 200. Application links remained references
only, and no application or authenticated route was opened.

The asset ledger contained 344 discovered assets, 179 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,700,889 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5197529008`, `5383596008`, and
`5287926008` preserved 18,576, 19,164, and 17,845 body-text characters and
one intact 2000px logo image per page, with no broken images, frames, video,
or audio. The replay logger recorded 18 loopback-only requests (15 HTTP 200
and three pending), with no production-origin or excluded-host result. The
replay tab and server were closed after validation.

The archived index has 415 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15k.txt`; application links remain references
only and the four held-out Fellows/application-form-heavy listings remain
outside the ordinary lane.

## Careers N+1k result

The `next-15k` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788820951-next-15k` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 360 requests,
360 response bodies, no response-body errors, and 33,668,486 response bytes;
every recorded response was HTTP 200. Application links remained references
only, and no application or authenticated route was opened.

The asset ledger contained 345 discovered assets, 180 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,762,950 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5098025008`, `5229345008`, and
`5305402008` preserved 18,494, 20,062, and 17,812 body-text characters and
one intact 2000px logo image per page, with no broken images, frames, video,
or audio. The replay logger recorded 18 loopback-only requests (15 HTTP 200
and three pending), with no production-origin or excluded-host result. The
replay tab and server were closed after validation.

The archived index has 400 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15l.txt`; application links remain references
only and the four held-out Fellows/application-form-heavy listings remain
outside the ordinary lane.

## Careers N+1l result

The `next-15l` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788826659-next-15l` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 353 requests,
353 response bodies, no response-body errors, and 33,046,178 response bytes;
every recorded response was HTTP 200. Application links remained references
only, and no application or authenticated route was opened.

The asset ledger contained 338 discovered assets, 173 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,328,523 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5385217008`, `5288742008`, and
`5392335008` preserved 17,687, 17,515, and 12,525 body-text characters and
one intact 2000px logo image per page, with no broken images, frames, video,
or audio. The replay logger recorded 18 loopback-only requests (15 HTTP 200
and three pending), with no production-origin or excluded-host result. The
replay tab and server were closed after validation.

The archived index has 385 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15m.txt`; application links remain references
only and the four held-out Fellows/application-form-heavy listings remain
outside the ordinary lane.

## Careers N+1m result

The `next-15m` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788832409-next-15m` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 358 requests,
355 response bodies, three response-body/status boundary records, and
33,156,521 response bytes. The status ledger contained 355 HTTP 200
responses and three HTTP 302 redirects for jobs `5358112008`,
`5358130008`, and `5358144008`; each resolved to the public Greenhouse
`?error=true` board shell because the listing was unavailable. No application or
authenticated route was opened.

The asset ledger contained 340 discovered assets, 175 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,452,645 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5397131008`, `5358130008`, and
`5318977008` preserved 13,112, 4,664, and 19,572 body-text characters and
one intact 2000px logo image per page, with no broken images, frames, video,
or audio. The middle replay reproduced the public `Jobs at Anthropic` shell
for the retired listing. The replay logger recorded 18 loopback-only
requests (15 HTTP 200 and three pending), with no production-origin or
excluded-host result. The replay tab and server were closed after validation.

The archived index has 385 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15n.txt`; 370 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1n result

The `next-15n` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788838389-next-15n` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 359 requests,
357 response bodies, two response-body/status boundary records, and
33,323,811 response bytes. The status ledger contained 357 HTTP 200
responses and two HTTP 302 redirects for jobs `5393268008` and
`5409108008`; each resolved to the public Greenhouse `?error=true` board shell
because the listing was unavailable. No application or authenticated route was
opened.

The asset ledger contained 342 discovered assets, 177 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,576,767 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5345466008`, `5393268008`, and
`5357943008` preserved 18,592, 4,664, and 16,224 body-text characters and
one intact 2000px logo image per page, with no broken images, frames, video,
or audio. The early and late replays retained the public application form
surface without opening an application link; the middle replay reproduced the
public `Jobs at Anthropic` shell for the retired listing. The replay logger
recorded 18 loopback-only requests (15 HTTP 200 and three pending), with no
production-origin or excluded-host result. The replay tab and server were
closed after validation.

The archived index has 370 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15o.txt`; 355 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1o result

The `next-15o` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788844186-next-15o` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 357 requests,
355 response bodies, two response-body/status boundary records, and
33,187,097 response bytes. The status ledger contained 355 HTTP 200 responses
and two HTTP 302 redirects for jobs `5197551008` and `5115051008`; each
resolved to the public Greenhouse `?error=true` board shell because the listing
was unavailable. No application or authenticated route was opened.

The asset ledger contained 340 discovered assets, 175 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,452,645 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5358100008`, `5197551008`, and
`5248494008` preserved 11,242, 4,664, and 18,251 body-text characters and
one intact 2000px logo image per page, with no broken images, frames, video,
or audio. The early and late replays retained the public application form
surface with an Apply button without opening an application link; the middle
replay reproduced the public `Jobs at Anthropic` shell for the retired listing.
The replay logger recorded 18 loopback-only requests (15 HTTP 200 and three
pending), with no production-origin or excluded-host result. The replay tab and
server were closed after validation.

The archived index has 355 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15p.txt`; 340 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1p result

The `next-15p` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788849998-next-15p` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 377 requests,
373 response bodies, three response-body error records, and 35,377,802
response bytes. The status ledger contained 373 HTTP 200 responses, one HTTP
302 redirect for job `5358142008`, one HTTP 401 from the optional
`my.greenhouse.io/users/self?job_post_id=5358114008` check, and two pending
font responses. The 302 resolved to the public Greenhouse `?error=true` board
shell because the listing was unavailable; the 401 and pending records were
optional application-surface dependencies. No application or authenticated
route was opened.

The asset ledger contained 345 discovered assets, 178 attempted and completed
downloads, 167 already-complete entries, 0 failures, 0 exclusions, and
7,638,828 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5358116008`, `5358142008`, and
`5074052008` preserved 15,328, 4,664, and 17,570 body-text characters and
one intact 2000x2001 logo image per page, with no broken images, frames, video,
or audio. The early and late replays retained the public application form
surface with an Apply button without opening an application link; the middle
replay reproduced the public `Jobs at Anthropic` shell for the retired listing.
Fresh performance-resource checks showed only loopback `127.0.0.1:8056`
resources for all three replays, with no production-origin or excluded-host
result. The replay tabs and server were closed after validation.

The archived index has 340 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15q.txt`; 325 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1q result

The `next-15q` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788855894-next-15q` completed
15/15 public Greenhouse detail routes with `finish.failures=0`, no
capture-level failures, and all capture tabs closed. It recorded 358 requests,
358 response bodies, no response-body errors, and 33,475,681 response bytes;
all 358 responses were HTTP 200. No application or authenticated route was
opened.

The asset ledger contained 343 discovered assets, 178 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,638,828 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5275765008`, `5398360008`, and
`5398641008` preserved 17,721, 18,465, and 19,865 body-text characters and
one intact 2000x2001 logo image per page, with no broken images, frames, video,
or audio. All three replays retained the public application form surface with
an Apply button without opening an application link. Fresh performance-resource
checks showed only loopback `127.0.0.1:8057` resources for all three replays,
with no production-origin or excluded-host result. The replay tabs and server
were closed after validation.

The archived index has 325 uncaptured public job identities after this batch.
The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15r.txt`; 310 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1r result

The `next-15r` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788861605-next-15r` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Fourteen routes preserved public
Greenhouse job-detail pages. Job `5324841008` returned one public 302 boundary
record and resolved to the public Anthropic Greenhouse index at `?error=true`
with the visible 587-job board shell; its one response-body error is classified
as the retired-listing/status boundary, not a page-capture failure. The batch
recorded 358 requests, 357 response bodies, one response-body error, and
33,388,734 response bytes: 357 HTTP 200 responses and one HTTP 302. No
application or authenticated route was opened.

The asset ledger contained 342 discovered assets, 177 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,576,767 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images. Result
URLs contained none of the excluded YouTube, Twitter, or X hosts.

Local-only early/middle/late replays of `5398653008`, `5393720008`, and
`4977027008` preserved 11,144, 17,482, and 18,412 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. The retired `5324841008` replay preserved the public 587-job index shell
with 4,664 body-text characters and the same intact logo. All fresh replay
resource hosts were loopback-only. The detail replays preserved the public
Apply/application surface without activating it; the late replay recorded the
visible careers, mailto, Greenhouse, Apply, and Submit application references
without opening an application route. The replay tab and server were closed
after validation.

The archived index has 310 uncaptured public job identities before the next
selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15s.txt`; 295 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1s result

The `next-15s` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788867537-next-15s` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Fourteen routes preserved public
Greenhouse job-detail pages. Job `4778843008` returned one public 302 boundary
record and resolved to the public Anthropic Greenhouse index at `?error=true`
with the visible 587-job board shell; its one response-body error is classified
as the retired-listing/status boundary, not a page-capture failure. The batch
recorded 360 requests, 359 response bodies, one response-body error, and
33,592,514 response bytes: 359 HTTP 200 responses and one HTTP 302. No
application or authenticated route was opened.

The asset ledger contained 344 discovered assets, 179 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,700,889 downloaded bytes. Interactive media was zero. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images. Result
URLs contained none of the excluded YouTube, Twitter, or X hosts.

Local-only early/middle/late replays of `4423394008`, `4935314008`, and
`4982193008` preserved 17,789, 17,599, and 17,709 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. The retired `4778843008` replay preserved the public 587-job index shell
with 4,664 body-text characters and the same intact logo. All fresh replay
resource hosts were loopback-only. The detail replays preserved the public
Apply/application surface without activating it; the late replay recorded the
visible careers, mailto, Greenhouse, Apply, and Submit application references
without opening an application route. The replay tab and server were closed
after validation.

The archived index has 295 uncaptured public job identities before the next
selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15t.txt`; 280 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1t result

The `next-15t` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788873307-next-15t` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. All 15 routes preserved public
Greenhouse job-detail pages with HTTP 200 responses and no response-body
errors. The batch recorded 359 requests, 359 response bodies, 0 response-body
errors, and 39,563,506 response bytes. No application or authenticated route
was opened.

The asset ledger contained 344 discovered assets, 179 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
13,721,863 downloaded bytes. One detail page, job `5018472008`, preserved the
public first-party `Economic_Tasks_AI_Paper.pdf` dependency from
`assets.anthropic.com`, along with its ordinary Greenhouse assets. Interactive
media was zero. Both the primary and all-rendered-image audits reported 15/15
pages with no missing images. Result URLs contained none of the excluded
YouTube, Twitter, or X hosts.

Local-only early/middle/late replays of `4986159008`, `5018472008`, and
`5068570008` preserved 19,582, 19,348, and 19,585 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. The middle replay covered the PDF/reference-bearing role; the captured
PDF remained a non-activated public reference. All fresh replay resource hosts
were loopback-only. The detail replays preserved the public Apply/application
surface without activating it, and visible careers, mailto, and Greenhouse
references were recorded without opening an application route. The replay tab
and server were closed after validation.

The archived index has 280 uncaptured public job identities before the next
selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15u.txt`; 265 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1u result

The `next-15u` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788879051-next-15u` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. All 15 routes preserved public job-detail
pages with HTTP 200 responses and no response-body errors. The batch recorded
356 requests, 356 response bodies, 0 response-body errors, and 33,237,515
response bytes. No application or authenticated route was opened.

The asset ledger contained 341 discovered assets, 176 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and 7,514,706
downloaded bytes. Interactive media was zero. Result URLs contained none of the
excluded YouTube, Twitter, or X hosts. Both the primary and all-rendered-image
audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5073998008`, `5079916008`, and
`5097742008` preserved 8,615, 17,160, and 9,448 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. All fresh replay resource hosts were loopback-only. The late replay
recorded the visible Apply, Submit application, `anthropic.com/careers`, and
Greenhouse references without activating an application route; the unavailable
references were retained as references only.

The archived index has 265 uncaptured public job identities before the next
selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15v.txt`; 250 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1v result

The `next-15v` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788884903-next-15v` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. All 15 routes preserved public job-detail
pages with HTTP 200 responses and no response-body errors. The batch recorded
356 requests, 356 response bodies, 0 response-body errors, and 33,230,923
response bytes. No application or authenticated route was opened.

The asset ledger contained 341 discovered assets, 176 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and 7,514,706
downloaded bytes. Interactive media was zero. Result URLs contained none of the
excluded YouTube, Twitter, or X hosts. Both the primary and all-rendered-image
audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5098092008`, `5110511008`, and
`5123039008` preserved 19,062, 18,565, and 17,237 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. All fresh replay resource hosts were loopback-only. The late replay
recorded the visible Apply, Submit application, `anthropic.com/careers`, and
Greenhouse references without activating an application route.

The archived index has 250 uncaptured public job identities before the next
selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15w.txt`; 235 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1w result

The `next-15w` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788890723-next-15w` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. All 15 routes preserved public job-detail
pages with HTTP 200 responses and no response-body errors. The batch recorded
359 requests, 359 response bodies, 0 response-body errors, and 33,579,878
response bytes. No application or authenticated route was opened.

The asset ledger contained 344 discovered assets, 179 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and 7,700,889
downloaded bytes. Interactive media was zero. Result URLs contained none of the
excluded YouTube, Twitter, or X hosts. Both the primary and all-rendered-image
audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5368476008`, `5409026008`, and
`5139628008` preserved 18,166, 17,525, and 18,373 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. All fresh replay resource hosts were loopback-only. The replays exposed
the public Apply/Submit application surface and careers/Greenhouse references
without activating an application route.

The archived index has 235 uncaptured public job identities before the next
selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15x.txt`; 220 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1x result

The `next-15x` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788896295-next-15x` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. All 15 routes preserved public job-detail
pages with HTTP 200 responses and no response-body errors. The batch recorded
359 requests, 359 response bodies, 0 response-body errors, and 33,540,124
response bytes. No application or authenticated route was opened.

The asset ledger contained 344 discovered assets, 179 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and 7,700,889
downloaded bytes. Interactive media was zero. Result URLs contained none of the
excluded YouTube, Twitter, or X hosts. Both the primary and all-rendered-image
audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5207565008`, `5406106008`, and
`5179891008` preserved 17,480, 16,557, and 19,037 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. All fresh replay resource hosts were loopback-only. The replays exposed
the public Apply/Submit application surface and careers/Greenhouse references
without activating an application route.

The archived index has 220 uncaptured public job identities before the next
selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15y.txt`; 205 public identities remain after that
prepared batch. Application links remain references only and the four held-out
Fellows/application-form-heavy listings remain outside the ordinary lane.

## Careers N+1y result

The `next-15y` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788901876-next-15y` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Fourteen routes preserved public
Greenhouse job-detail pages. Job `5247407008` returned one public HTTP 302
boundary record and resolved to the Greenhouse `?error=true` index shell; its
single response-body error is classified as a retired/removed public listing,
not a page-capture failure. The batch recorded 358 requests, 357 response
bodies, one response-body error, and 51,325,310 response bytes: 357 HTTP 200
responses and one HTTP 302. No application or authenticated route was opened.

The asset ledger contained 342 discovered assets, 177 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
25,639,689 downloaded bytes. Interactive media was zero. Result URLs contained
none of the excluded YouTube, Twitter, or X hosts. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5138042008`, `5149802008`, and
`5397699008` preserved 9,194, 19,199, and 17,414 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. The middle captured page retains a public `assets.anthropic.com` PDF
reference (`Economic_Tasks_AI_Paper.pdf`); the replay kept that reference on
the local archive boundary and made no production-origin request. All fresh
replay resource hosts were loopback-only. The replays exposed the public
Apply/Submit application surface and careers/Greenhouse references without
activating an application route.

The archived index has 205 uncaptured ordinary public job identities before the
next selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15z.txt`; 190 ordinary public identities remain
after that prepared batch. Application links remain references only and the
four held-out Fellows/application-form-heavy listings remain outside the
ordinary lane.

## Careers N+1z result

The `next-15z` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788907840-next-15z` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Fourteen routes preserved public
Greenhouse job-detail pages. Job `5319592008` returned one public HTTP 302
boundary record and resolved to the Greenhouse `?error=true` index shell; its
single response-body error is classified as a retired/removed public listing,
not a page-capture failure. The batch recorded 360 requests, 359 response
bodies, one response-body error, and 33,571,906 response bytes: 359 HTTP 200
responses and one HTTP 302. No application or authenticated route was opened.

The asset ledger contained 344 discovered assets, 179 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,700,889 downloaded bytes. Interactive media was zero. Result URLs contained
none of the excluded YouTube, Twitter, or X hosts. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5392184008`, `5311234008`, and
`5311149008` preserved 18,499, 19,064, and 18,981 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. The structurally unusual replay of retired `5319592008` preserved the
public Greenhouse index shell with 4,702 body-text characters and the same
intact logo. All fresh replay resource hosts were loopback-only. The normal
replays exposed the public Apply/Submit application surface and
careers/Greenhouse references without activating an application route; the
retired route exposed only the public Greenhouse reference.

The archived index has 190 uncaptured ordinary public job identities before the
next selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15aa.txt`; 175 ordinary public identities remain
after that prepared batch. Application links remain references only and the
four held-out Fellows/application-form-heavy listings remain outside the
ordinary lane.

## Careers N+1aa result

The `next-15aa` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788913655-next-15aa` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Fourteen routes preserved public
Greenhouse job-detail pages. Job `5230394008` returned one public HTTP 302
boundary record and resolved to the Greenhouse `?error=true` index shell; its
single response-body error is classified as a retired/removed public listing,
not a page-capture failure. The other four response-level records were two
optional `my.greenhouse.io` application-session probes returning HTTP 401 and
two optional Greenhouse font responses still pending; the public job pages
rendered completely. The batch recorded 396 requests, 389 response bodies,
five response-level records, and 37,403,970 response bytes: 389 HTTP 200
responses, one HTTP 302, two HTTP 401 responses, and four pending records. No
application or authenticated route was opened.

The asset ledger contained 344 discovered assets, 179 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,700,889 downloaded bytes. Interactive media was zero. Result URLs contained
none of the excluded YouTube, Twitter, or X hosts. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5137183008`, `5397708008`, and
`5305476008` preserved 19,039, 17,496, and 19,418 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, video, or audio.
The early application-surface replay exposed three captured reCAPTCHA/Google
frames, all rewritten to loopback resources; the normal detail replays had no
frames. The structurally unusual replay of retired `5230394008` preserved the
public Greenhouse index shell with 4,702 body-text characters and the same
intact logo. All fresh replay resource hosts were loopback-only. The normal
replays exposed the public application surface without activating an
application route; the retired route exposed only the public Greenhouse
reference.

The archived index has 175 uncaptured ordinary public job identities before the
next selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15ab.txt`; 160 ordinary public identities remain
after that prepared batch. Application links remain references only and the
four held-out Fellows/application-form-heavy listings remain outside the
ordinary lane.

## Careers N+1ab result

The `next-15ab` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788919439-next-15ab` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Thirteen routes preserved public
Greenhouse job-detail pages. Jobs `5129961008` and `5391219008` each returned a
public HTTP 302 boundary record and resolved to the Greenhouse `?error=true`
index shell; their response-body errors are classified as retired/removed
public listings, not page-capture failures. The batch recorded 356 requests,
354 response bodies, two response-body errors, and 33,008,366 response bytes:
354 HTTP 200 responses and two HTTP 302 responses. No application or
authenticated route was opened.

The asset ledger contained 339 discovered assets, 174 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,390,584 downloaded bytes. Interactive media was zero. Result URLs contained
none of the excluded YouTube, Twitter, or X hosts. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5391376008`, `5391184008`, and
`5391257008` preserved 9,607, 15,461, and 11,402 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. The structurally unusual replay of retired `5129961008` preserved the
public Greenhouse index shell with 4,702 body-text characters and the same
intact logo. All fresh replay resource hosts were loopback-only. The normal
replays exposed the public application surface without activating an
application route; the retired route exposed only the public Greenhouse
reference.

The archived index has 160 uncaptured ordinary public job identities before the
next selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15ac.txt`; 145 ordinary public identities remain
after that prepared batch. Application links remain references only and the
four held-out Fellows/application-form-heavy listings remain outside the
ordinary lane.

## Careers N+1ac result

The `next-15ac` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788925139-next-15ac` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Thirteen routes preserved public
Greenhouse job-detail pages. Jobs `5129961008` and `5391219008` each returned a
public HTTP 302 boundary record and resolved to the Greenhouse `?error=true`
index shell; their response-body errors are classified as retired/removed
public listings, not page-capture failures. The batch recorded 356 requests,
354 response bodies, two response-body errors, and 33,008,366 response bytes:
354 HTTP 200 responses and two HTTP 302 responses. No application or
authenticated route was opened.

The asset ledger contained 339 discovered assets, 174 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,390,584 downloaded bytes. Interactive media was zero. Result URLs contained
none of the excluded YouTube, Twitter, or X hosts. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5391376008`, `5391184008`, and
`5391257008` preserved 9,607, 15,461, and 11,402 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. The structurally unusual replay of retired `5129961008` preserved the
public Greenhouse index shell with 4,702 body-text characters and the same
intact logo. All fresh replay resource hosts were loopback-only. The normal
replays exposed the public application surface without activating an
application route; the retired route exposed only the public Greenhouse
reference.

The archived index has 145 uncaptured ordinary public job identities before the
next selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15ad.txt`; 130 ordinary public identities remain
after that prepared batch. Application links remain references only and the
four held-out Fellows/application-form-heavy listings remain outside the
ordinary lane.

## Careers N+1ad result

The `next-15ad` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788930914-next-15ad` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Fourteen routes preserved public
Greenhouse job-detail pages. Job `5227904008` returned a public HTTP 302
boundary record and resolved to the Greenhouse `?error=true` index shell; its
response-body error is classified as a retired/removed public listing, not a
page-capture failure. The batch recorded 351 requests, 350 response bodies,
one response-body error, and 32,626,537 response bytes: 350 HTTP 200 responses
and one HTTP 302 response. No application or authenticated route was opened.

The asset ledger contained 335 discovered assets, 170 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,142,340 downloaded bytes. Interactive media was zero. Result URLs contained
none of the excluded YouTube, Twitter, or X hosts. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5218573008`, `5196014008`, and
`5391309008` preserved 9,715, 17,395, and 9,627 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. The structurally unusual replay of retired `5227904008` preserved the
public Greenhouse index shell with 4,702 body-text characters and the same
intact logo. All fresh replay resource hosts were loopback-only. The normal
replays exposed the captured public application surface without activating an
application route; the retired route exposed only the public Greenhouse
reference.

The archived index has 130 uncaptured ordinary public job identities before the
next selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15ae.txt`; 115 ordinary public identities remain
after that prepared batch. Application links remain references only and the
four held-out Fellows/application-form-heavy listings remain outside the
ordinary lane.

## Careers N+1ae result

The `next-15ae` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788936686-next-15ae` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. All 15 routes preserved public
Greenhouse job-detail pages. The batch recorded 358 requests, 358 response
bodies, zero response-body errors, and 33,440,569 response bytes; every
response was HTTP 200. No application or authenticated route was opened.

The asset ledger contained 343 discovered assets, 178 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,390,584 downloaded bytes. Interactive media was zero. Result URLs contained
none of the excluded YouTube, Twitter, or X hosts. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5390980008`, `5391195008`, and
`5412584008` preserved 16,506, 19,160, and 9,195 body-text characters and one
intact 2000x2001 logo image per page, with no broken images, frames, video, or
audio. The structurally unusual replay of retired `5227904008` from the
preceding continuation preserved the public Greenhouse index shell with 4,702
body-text characters and the same intact logo. All fresh replay resource hosts
were loopback-only. The normal replays exposed the captured public application
surface without activating an application route; the retired route exposed
only the public Greenhouse reference.

The archived index has 115 uncaptured ordinary public job identities before the
next selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15af.txt`; 100 ordinary public identities remain
after that prepared batch. Application links remain references only and the
four held-out Fellows/application-form-heavy listings remain outside the
ordinary lane.

## Careers N+1af result

The `next-15af` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788942471-next-15af` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Fourteen routes preserved public
Greenhouse job-detail pages. Job `5229558008` returned a public HTTP 302
boundary record and resolved to the Greenhouse `?error=true` index shell; its
response-body error is classified as a retired/removed public listing, not a
page-capture failure. The batch recorded 355 requests, 354 response bodies,
one response-body error, and 33,096,861 response bytes: 354 HTTP 200 responses
and one HTTP 302 response. No application or authenticated route was opened.

The asset ledger contained 339 discovered assets, 174 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,638,828 downloaded bytes. Interactive media was zero. Result URLs contained
none of the excluded YouTube, Twitter, or X hosts. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5170628008`, `5407938008`, and
`5390972008` preserved 19,029, 19,039, and 15,824 body-text characters and
one intact 2000x2001 logo image per page, with no broken images, frames, video,
or audio. The structurally unusual replay of retired `5229558008` preserved
the public Greenhouse index shell with 4,702 body-text characters and the same
intact logo. All fresh replay resource hosts were loopback-only. The normal
replays exposed the captured public application surface without activating an
application route; the retired route exposed only the public Greenhouse
reference.

The archived index has 100 uncaptured ordinary public job identities before the
next selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15ag.txt`; 85 ordinary public identities remain
after that prepared batch. Application links remain references only and the
four held-out Fellows/application-form-heavy listings remain outside the
ordinary lane.

## Careers N+1ag result

The `next-15ag` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788948179-next-15ag` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Fourteen routes preserved public
Greenhouse job-detail pages. Job `5391233008` returned a public HTTP 302
boundary record and resolved to the Greenhouse `?error=true` index shell; its
response-body error is classified as a retired/removed public listing, not a
page-capture failure. The batch recorded 357 requests, 356 response bodies,
one response-body error, and 33,314,276 response bytes: 356 HTTP 200 responses
and one HTTP 302 response. No application or authenticated route was opened.

The asset ledger contained 341 discovered assets, 176 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,514,706 downloaded bytes. Interactive media was zero. Result URLs contained
none of the excluded YouTube, Twitter, or X hosts. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5221916008`, `5235692008`, and
`5385588008` preserved 12,465, 17,743, and 19,727 body-text characters and
one intact 2000x2001 logo image per page, with no broken images, frames, video,
or audio. The structurally unusual replay of retired `5391233008` preserved
the public Greenhouse index shell with 4,702 body-text characters and the same
intact logo. All fresh replay resource hosts were loopback-only. The normal
replays exposed the captured public application surface without activating an
application route; the retired route exposed only the public Greenhouse
reference.

The archived index has 85 uncaptured ordinary public job identities before the
next selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15ah.txt`; 70 ordinary public identities remain
after that prepared batch. Application links remain references only and the
four held-out Fellows/application-form-heavy listings remain outside the
ordinary lane.

## Careers N+1ah result

The `next-15ah` continuation at
`/mnt2/capsule/epitome/anthropic-careers/crawls/1788954007-next-15ah` completed
15/15 public Greenhouse route pages with `finish.failures=0`, no capture-level
failures, and all capture tabs closed. Fourteen routes preserved public
Greenhouse job-detail pages. Job `5396282008` returned a public HTTP 302
boundary record and resolved to the Greenhouse `?error=true` index shell; its
response-body error is classified as a retired/removed public listing, not a
page-capture failure. The batch recorded 358 requests, 357 response bodies,
one response-body error, and 33,471,490 response bytes: 357 HTTP 200 responses
and one HTTP 302 response. No application or authenticated route was opened.

The asset ledger contained 342 discovered assets, 177 attempted and completed
downloads, 165 already-complete entries, 0 failures, 0 exclusions, and
7,576,767 downloaded bytes. Interactive media was zero. Result URLs contained
none of the excluded YouTube, Twitter, or X hosts. Both the primary and
all-rendered-image audits reported 15/15 pages with no missing images.

Local-only early/middle/late replays of `5385590008`, `5391787008`, and
`5386949008` preserved 16,232, 19,838, and 19,383 body-text characters and
one intact 2000x2001 logo image per page, with no broken images, frames, video,
or audio. The structurally unusual replay of retired `5396282008` preserved
the public Greenhouse index shell with 4,702 body-text characters and the same
intact logo. All fresh replay resource hosts were loopback-only. The normal
replays exposed the captured public application surface without activating an
application route; the retired route exposed only the public Greenhouse
reference.

The archived index has 70 uncaptured ordinary public job identities before the
next selection. The next deduplicated public-only batch is prepared in ignored
`data/anthropic-careers-next-15ai.txt`; 55 ordinary public identities remain
after that prepared batch. Application links remain references only and the
four held-out Fellows/application-form-heavy listings remain outside the
ordinary lane.

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
