# Andrej Karpathy Bear and Medium reconnaissance

Investigated through browser-backed deep research and independently checked in
Chromium on 2026-08-10. These are distinct successors to the already-complete
`karpathy.github.io` blog; neither should be folded into that archive directory.

## First-party ownership

Karpathy's current `karpathy.ai` homepage calls the GitHub/Jekyll site his old
blog, `https://karpathy.medium.com/` his second blog, and
`https://karpathy.bearblog.dev/blog/` his current blog. The Bear homepage links
back to `karpathy.ai` and identifies itself as the Bear blog of Andrej Karpathy.
No second Karpathy-owned Bear property or separate Medium publication was found.

## Bear Blog scope

The rendered Bear index exposes thirteen posts plus the homepage, `/blog/`
index, and `/feed/` Atom feed. The reviewed 16-identity scope is tracked in
`sources/andrej-karpathy-bear.txt`. Capture only media requested by these pages;
do not recursively crawl Bear's shared platform/CDN.

The index supplies exact `<time datetime>` values for every post:

- 2026-04-30 — *Sequoia Ascent 2026 summary*;
- 2025-12-19 — *2025 LLM Year in Review*;
- 2025-12-18 — *Chemical hygiene*;
- 2025-12-10 — *Auto-grading decade-old Hacker News discussions with hindsight*;
- 2025-11-29 — *The space of minds*;
- 2025-11-17 — *Verifiability*;
- 2025-10-01 — *Animals vs Ghosts*;
- 2025-04-27 — *Vibe coding MenuGen*;
- 2025-04-07 — *Power to the people*;
- 2025-03-24 — *Finding the Best Sleep Tracker*;
- 2025-03-19 — *The append-and-review note*;
- 2025-03-17 — *Digital hygiene*; and
- 2024-09-08 — *I love calculator*.

The homepage separately says the Bear property started in March 2025. Preserve
that as a site-history event rather than overwriting the displayed 2024 post
date; the older post was likely imported or backdated, but that is an inference.

### Representative capture validation

A bounded homepage, index, and image-bearing long-post pilot completed at
`/mnt2/capsule/epitome/andrej-karpathy-bear/validation/1786378012-pilot`.
All three manifests are complete and tab-closed, with no capture or image-audit
failures. The index replay preserves all thirteen exact displayed dates. The
2025 year-review replay retains 10,703 visible characters and both CDN images
at their captured 1024 by 559 and 1200 by 340 dimensions.

Desktop replay matches the live site's narrow dark layout. A fresh network-log
reload requested only the local replay document and two local resource routes;
it made no production-origin requests. The reviewed sixteen-identity Bear scope
is approved for one bounded completion batch.

The remaining thirteen identities completed at
`/mnt2/capsule/epitome/andrej-karpathy-bear/crawls/1786378795`. All thirteen
manifests are complete and tab-closed, bringing the archive to all sixteen
reviewed identities. Primary and all-image audits are clean across the combined
archive. A second long post, *Animals vs Ghosts*, retains 10,650 visible
characters and its exact 2025-10-01 datetime; the Atom replay retains its full
143,501-character XML body. The Bear scope is complete.

## Medium scope

The canonical profile is `https://karpathy.medium.com/`; the historical
`https://medium.com/@karpathy` identity redirects there. The rendered profile
exposes eight authored posts dated from November 2015 through November 2017,
plus an About page and XML feed. The reviewed 11-identity scope is tracked in
`sources/andrej-karpathy-medium.txt`.

Medium adds tracking query strings to profile links. Capture only the clean,
queryless article identities, rendered DOM, original response, and media those
pages request. Exclude repost/activity/follower pages, recommendations, tags,
and platform-wide navigation. The eight canonical posts and publication dates
are:

- 2017-11-11 — *Software 2.0*;
- 2017-05-31 — *AlphaGo, in context* (explicitly updated 2017-10-18);
- 2017-05-24 — *ICML accepted papers institution stats*;
- 2017-04-07 — *A Peek at Trends in Machine Learning*;
- 2017-03-14 — *ICLR 2017 vs arxiv-sanity*;
- 2017-01-17 — *Virtual Reality: still not quite there, again.*;
- 2016-12-19 — *Yes you should understand backprop*; and
- 2015-11-15 — *CS183c Assignment #3*.

Before capture approval, compare normalized article bodies against the completed
Jekyll corpus for mirrors. No title-level duplicate was identified, but body
similarity is a stronger archival check.

### Representative capture validation

A profile plus two-article pilot completed at
`/mnt2/capsule/epitome/andrej-karpathy-medium/validation/1786379902-pilot`.
All three manifests are complete and tab-closed. The only asset failures are
three identical requests for Medium's nonexistent `/sitemap/sitemap.xml`, which
returns HTTP 404; primary and all-image audits are otherwise clean.

Script-free desktop replay preserves Medium's layout and full readable bodies,
without a paywall truncation. *Software 2.0* retains 13,961 visible characters;
*AlphaGo, in context* retains 7,589 and its visible 2017-10-18 update notice. A
fresh Software 2.0 reload made 23 requests, all to the loopback replay server.

Normalized seven-word-shingle comparisons against every page in the completed
Jekyll archive found no substantive duplicate: AlphaGo had zero overlap and
Software 2.0's maximum containment was 0.04%, against an unrelated post. The
reviewed eleven-identity Medium scope is approved for one bounded completion
batch.

The remaining eight identities completed at
`/mnt2/capsule/epitome/andrej-karpathy-medium/crawls/1786380982`. Every manifest
is complete and tab-closed, bringing the archive to all eleven reviewed
identities. The only seven asset failures are repeated HTTP 404 responses from
the nonexistent sitemap; both image audits are clean across the combined
archive.

Final replays preserve the About profile, the full 95,213-character RSS XML,
and a third complete article: *Yes you should understand backprop* retains
9,992 visible characters and its 2016-12-19 date. The feed's sole visually
broken image is an inert Medium `post.clientViewed` 1 by 1 tracking pixel inside
the XML content, not publication media. The Medium scope is complete.
