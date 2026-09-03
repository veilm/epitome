# Eliezer Yudkowsky fiction and writing

## Public inventory

The rendered public `https://www.yudkowsky.net/other/fiction/the-sword-of-good`
page resolves to the first-party Sword of Good fiction page. It contains a
long-form excerpt, a single visible WordPress comment, and an explicit
Creative Commons Attribution-No Derivative Works notice. Its navigation and
footer links are provenance or site navigation, not additional fiction
identities.

The rendered public `https://yudkowsky.tumblr.com/writing` page is titled
`Optimize Literally Everything | Intelligent Characters` and contains an
ordered list of 13 canonical writing pages:

1. Level 1 Intelligent characters
2. Intelligence via empathy and respect
3. Thoughtful responses and intelligent mistakes
4. True moral conflicts
5. Realistic villains and viewpoints
6. Originality
7. Genre savviness
8. Level 2 Intelligent characters
9. Inexploitability
10. Explaining other universes
11. Solvable mysteries
12. Real learning
13. Level 3 Intelligent characters

The local source records contain no matching canonical Yudkowsky fiction or
Tumblr writing URLs. The capture lists therefore use only the first-party
canonical page and linked writing identities, excluding the index's Facebook,
Amazon, HPMOR, Tumblr-navigation, and theme links. The scope is public-only;
no account or paywall route is required.

## Bounded pilot and continuation

The varied seven-route pilot is prepared in
`data/yudkowsky-fiction-writing-pilot.txt`: Sword of Good, the writing index,
and representative Level 1, thoughtful-response, Level 2, real-learning, and
Level 3 pages. The remaining eight canonical writing pages are prepared in
`data/yudkowsky-fiction-writing-next-8.txt` as N+1. Both lists use HTTPS
canonical URLs and contain no duplicate identities.

The pilot uses the standard public capture settings: port 2103 only, 15-second
settle, 120-second page limit, 400-asset limit, two-second asset pacing,
90-second asset timeout, and 30 seconds between pages. The exact
YouTube/Twitter/X asset exclusions remain in force, and no media downloader is
permitted. After the pilot, require complete tab-closed manifests, dependency
and asset classification, both image audits, and early/index/long-writing
loopback replays before starting the eight-page continuation.

## Seven-route pilot result

The pilot completed at
`/mnt2/capsule/epitome/yudkowsky/crawls/1788434170-fiction-writing-pilot`.
All seven manifests are complete and tab-closed; the terminal `finish` record
reports `failures=0`. The capture recorded 487 requests, 457 response bodies,
33,111,708 response bytes, and 14 response-body errors. The 14 errors are
bounded dependency outcomes: the Sword page's two errors are the 301/302
redirect chain for an old staging/header image, while each of the six Tumblr
pages contributes one ScorecardResearch telemetry redirect and one Tumblr
monetization-frame 303 redirect. No substantive article body or captured
asset depends on those responses.

Asset completion discovered 383 references and attempted and completed 299;
there were zero asset failures and zero exclusion decisions. The seven
interactive-media ledgers report zero discovered, embedded, activated, or
result-level media. No YouTube or Twitter/X downloader was invoked, and no
excluded-host URL appears in an asset result.

The primary-image and all-rendered-image audits both report seven pages with
zero missing images, repair attempts, or repair failures. Four patched replay
checks covered the early long-form Sword page (53,515 visible characters and
comment text), the Tumblr writing index (5,383 characters and 26 links), the
long Level 1 writing page (6,386 characters), and the comment-bearing Level 2
page (20,000 characters). Their combined network logs contain 38 requests,
all to `127.0.0.1:8031` (29 local 200s, seven local 404s, and two pending
observations), with no production-origin requests. The source has no
high-volume archived discussion in this pilot; the Sword page is the
comment-bearing structural check.

The first index replay exposed a Tumblr `rel="compression-dictionary"` hint
that Chromium followed to a live ad-support URL. The offline rewriter now
drops that non-content hint and localizes captured mask icons; the repeated
index replay had zero non-loopback requests. The replay fix is part of the
source handoff and applies before the eight-page continuation.

The pilot is approved for the prepared eight-route continuation in
`data/yudkowsky-fiction-writing-next-8.txt` under the same public-only and
exact-host-exclusion policy.
