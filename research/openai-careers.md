# OpenAI careers and jobs

## Public validation and N+1 pilot

The public careers index `https://openai.com/careers/search/` was validated on
2026-09-03. It rendered as `Careers | OpenAI` with 79,638 visible characters,
768 listed jobs, and no images, broken images, frames, video, or audio. The
index is public and did not require an account, application flow, or access
boundary bypass. Individual job cards expose public OpenAI detail routes and
separate Ashby application links; the application links are references only
and are not in the ordinary public archive lane.

The prepared, ignored seven-route pilot is `data/openai-careers-pilot.txt`:

1. `https://openai.com/careers/search/` — the ordered public index.
2. `https://openai.com/careers/3p-systems-architect-san-francisco/` —
   Datacenter Design, San Francisco/Seattle; Ashby ID
   `e2afdede-a222-4825-b2fc-fec439a7c893`.
3. `https://openai.com/careers/academic-research-partnerships-and-programs-lead-san-francisco/`
   — Partnerships, two locations; Ashby ID
   `d7dc62fc-e7ce-4f58-a912-4b62b65c7eb6`.
4. `https://openai.com/careers/account-associate-emea-(french-speaking)-dublin-ireland/`
   — Account Associates, Dublin; Ashby ID
   `1eb6ef0f-0e51-46d3-b888-c1a4c22c190a`.
5. `https://openai.com/careers/account-associate-japan-tokyo-japan/` —
   Account Associates, Tokyo; Ashby ID
   `2f3f416d-cc2a-4836-bcff-daee80c94e95`.
6. `https://openai.com/careers/account-director-commercial-new-york-city/`
   — Sales, New York City; Ashby ID
   `b5399d89-a3d1-4d2b-b6d7-f50e052f0d38`.
7. `https://openai.com/careers/account-director-federal-partnerships-washington-dc/`
   — OpenAI for Gov, Washington, DC; Ashby ID
   `fada5332-3ae3-46f2-afa2-10c5878bdd25`.

The six detail identities are unique, ordered examples across infrastructure,
partnerships, account associates, sales, and government work. The pilot is
deduplicated against the public search route and does not fetch any Ashby
application URL. Job IDs, title/team/location text, and first/last-seen
timestamps should be retained for the versioned job scope; removed jobs should
remain represented in later snapshots rather than being silently deleted.

The first detail route, 3P Systems Architect, rendered as
`3P Systems Architect | OpenAI` with 7,842 visible characters and substantive
role/team text. It had no images, broken images, frames, video, or audio. The
public careers scope is therefore suitable for a bounded low-risk pilot, while
the rapidly changing job inventory remains explicitly versioned rather than
treated as a static complete archive.

Use the standard public capture settings: CDP port 2103 only, 15-second
settle, 120-second page limit, 400-asset limit, two-second asset pacing,
90-second asset timeout, and 30 seconds between pages. Exact asset exclusions
are `www.youtube-nocookie.com`, `www.youtube.com`, `youtube.com`,
`pbs.twimg.com`, `video.twimg.com`, `twitter.com`, `www.twitter.com`, `x.com`,
and `www.x.com`. Never download or invoke a YouTube or Twitter/X downloader or
intentionally fetch incidental media variants. At the pilot boundary, require
complete public detail/index text, stable-ID classification, redirects,
application-link and telemetry classification, both image audits, and
representative local-only index/detail replays with no production-origin
fallback. Anthropic careers remains the next separate source after this pilot.

## Seven-route public pilot result

The seven-route pilot ran on 2026-09-03/04 with the standard public-only
capture settings. All seven manifests completed and their capture tabs were
closed; `finish.failures=0` and there were no capture-level page failures. The
index and six detail pages retained substantive public job text. The index
replay rendered 79,546 body-text characters; the representative detail
replays rendered 7,842, 7,313, and 9,147 characters for the 3P, Academic, and
Federal examples respectively (the fourth detail replay was covered by the
capture audit). No application or authenticated route was opened.

| route | requests / bodies / body errors; statuses | assets discovered / attempted / completed / already-complete / failed / excluded | interactive media discovered / embedded / activated / results |
| --- | --- | --- | --- |
| `/careers/search/` | 132 / 121 / 2; 200×122, 202×3, 204×2, 302×2, 304×2, 401×1 | 97 / 52 / 52 / 45 / 0 / 0 | 0 / 0 / 0 / 0 |
| 3P Systems Architect | 261 / 253 / 2; 200×252, 202×3, 204×1, 304×2, 401×1, 403×2 | 236 / 117 / 115 / 119 / 2 / 0 | 0 / 0 / 0 / 0 |
| Academic Research Partnerships & Programs Lead | 261 / 249 / 6; 200×248, 202×3, 204×1, 304×2, 401×1, 403×6 | 236 / 117 / 111 / 119 / 6 / 0 | 0 / 0 / 0 / 0 |
| Account Associate, EMEA (French) | 268 / 255 / 6; 200×255, 202×3, 204×1, 302×2, 304×2, 401×1, 403×4 | 236 / 117 / 113 / 119 / 4 / 0 | 0 / 0 / 0 / 0 |
| Account Associate, Japan | 259 / 249 / 6; 200×248, 202×3, 204×1, 401×1, 403×6 | 236 / 117 / 111 / 119 / 6 / 0 | 0 / 0 / 0 / 0 |
| Account Director, Commercial | 263 / 255 / 2; 200×254, 202×3, 204×1, 304×2, 401×1, 403×2 | 236 / 117 / 115 / 119 / 2 / 0 | 0 / 0 / 0 / 0 |
| Account Director, Federal Partnerships | 266 / 254 / 5; 200×254, 202×3, 204×1, 302×2, 304×2, 401×1, 403×3 | 236 / 117 / 114 / 119 / 3 / 0 | 0 / 0 / 0 / 0 |

The aggregate network contained 1,710 requests, 1,636 response bodies, 29
response-body errors, and 176,992,194 response bytes. The 21 `202`, eight
`204`, six `302`, twelve `304`, seven `401`, and 23 `403` records were
classified as platform/telemetry, redirects, cache responses, or optional
static-resource outcomes; they did not block the public job documents. The
23 failed assets were optional OpenAI static resources (fonts, a favicon, and
similar UI files), all HTTP 403; no job-content asset failed. Asset accounting
was 1,513 discovered, 754 attempted, 731 newly completed, 759 already
complete, 23 failed, zero excluded, and 54,735,006 downloaded bytes. The
result records contain zero URLs on the exact excluded hosts, and no
interactive media was discovered or activated.

The primary-image and all-rendered-image audits both report seven pages with
zero missing images, repair attempts, or repair failures. A local-only replay
of the index plus early, middle, and late detail pages used
`127.0.0.1:8038` only: 128 metadata requests were 84×200, 33 archive-only
400s for unavailable decorative paths, and 11 pending local font reads. The
index rendered 79,546 body-text characters with one frame; the 3P detail,
Academic detail, and Federal detail rendered 7,842, 7,313, and 9,147 body-text
characters respectively, with zero broken images, zero videos, and zero audio
elements (the index and Federal pages each exposed one archived frame). No
replay request reached the production origin. This completes the bounded
OpenAI careers pilot; future captures must preserve stable job IDs,
first/last-seen timestamps, and removal history rather than treating the
changing inventory as a static complete archive.
