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
