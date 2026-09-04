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
