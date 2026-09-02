# LessWrong source reconnaissance

Investigated through the rendered public site on CDP port 2103 and the user's
legitimately received Gmail UI on port 2102 on 2026-08-11. No mailbox API was
used, and no private email body or tracking token is stored in Git.

## Editorial hierarchy

LessWrong has several signals that should not be conflated with raw karma:

1. The public **Library** promotes five bounded core collections: *Rationality:
   A-Z*, *The Sequences Highlights*, *Harry Potter and the Methods of
   Rationality*, *The Codex*, and *Best of LessWrong*.
2. The same page separately displays 38 **Curated Sequences**. LessWrong's FAQ
   describes these as sets the moderation team considers especially valuable
   and part of the site's intellectual canon.
3. **Community Sequences** are user-created and much broader. The current
   Library exposes 12 initially and labels the pool as 266. They are not an
   automatic archival tier merely because they use the same sequence UI.
4. Individual **Curated posts** are selected by the moderation team from
   Frontpage posts, normally about three per week, for being especially
   well-written, insightful, instructive, or important. This differs from the
   recency-and-karma ranking used for ordinary Latest Posts.
5. **Best of LessWrong** is a slower community review: posts over a year old are
   revisited and voted on for how well they stood the test of time. The current
   page covers annual-review results beginning in 2018.

The stable reviewed collection-index list is tracked in
`sources/lesswrong-collections.txt`. The rendered inventory tool
`research/inventory_lesswrong_cdp` visits those indexes in one disposable tab,
preserves displayed ordering, normalizes sequence routes to post IDs, and
deduplicates Alignment Forum mirrors onto their public LessWrong identities.

The hardened 2026-08-11 inventory contains 43 collection indexes and 1,384
unique post IDs. Before cross-collection deduplication, the five core indexes
contain:

- 339 links in *Rationality: A-Z*;
- 51 in *Sequences Highlights* (the advertised reading list itself has 50;
  the rendered page also links introductory material);
- 122 HPMOR chapter/post identities;
- 83 entries in *The Codex*; and
- 342 annual-review winners in *Best of LessWrong*.

The 38 moderator-curated sequences contain 551 ordered entries before overlap
with one another and the core collections. Individual sequence sizes range from
four to 46. This is a culturally meaningful but still large scope; inventorying
it does not authorize an immediate 1,384-page crawl. The inventory explicitly
waits for post links after the collection shell loads; without that readiness
check, the 34-post *Hammertime* sequence can transiently appear empty.

## Curated email evidence

The user's mailbox contains single-post messages from
`no-reply@lesserwrong.com`, with subjects of the form `[LessWrong] POST TITLE`.
Recent examples arrive every few days rather than as one weekly bundle. A
rendered August 4 message contains the complete public article body, its author
and publication date, a canonical `lesswrong.com/posts/ID/slug` discussion
link, and five recommended public posts. Its footer states exactly why it was
sent: the account has **Email me new posts in Curated** enabled.

The newsletter tier is therefore the moderator-curated post stream, not the
generic `Newsletters` concept tag and not an old third-party LessWrong Digest.
The supported public incremental endpoint is:

`https://www.lesswrong.com/feed.xml?view=curated`

The feed supplies full HTML, canonical public links, authors, and timestamps.
It can drive future delta discovery without retaining mailbox tracking or
unsubscribe tokens. Gmail is useful only as provenance that this is the stream
the user meant.

## Proposed preservation tiers

1. Preserve the Library index and five core collection indexes, followed by
   their deduplicated post identities in bounded batches. *Sequences
   Highlights* is a useful first 50-post reading subset, while *Rationality:
   A-Z* preserves the canonical edited order.
2. Preserve the 38 moderator-curated sequence indexes and their deduplicated
   posts. Keep the index-to-post ordering metadata even when a post appears in
   multiple sequences.
3. Preserve annual-review winners from *Best of LessWrong* and increment the
   archive when a new review is published. Many overlap the sequence tiers.
4. Track new moderator-curated posts from the curated RSS feed. Record original
   publication time separately from curation time: LessWrong may display the
   curation timestamp as the apparent front-page date.
5. Review standout community sequences explicitly. Do not ingest all 266 by
   default, and do not substitute a top-karma scrape for editorial provenance.

## Capture risks and pilot

Current post pages use streamed Next.js boundaries. During live inspection, the
article data was present in the DOM and serialized state while the visible body
temporarily consisted only of a one-character low-opacity shell. Collection
indexes materialized normally. The archive pilot therefore uses a 15-second
settle and must prove that script-free replay exposes the actual article and
comments rather than approving hidden content by file size alone.

The seven-page pilot covers the Library, *Rationality: A-Z*, *Best of
LessWrong*, the *AGI safety from first principles* curated-sequence index, a
classic Sequences post, a Cartesian Frames technical post, and the recent
Curated post identified in email. Required checks are complete/tab-closed
manifests, post and comment text, equations/code/images, original and curation
dates where present, and loopback-only replay. YouTube and Twitter/X remain
outside capture scope.

## Pilot validation

The seven-page pilot at
`/mnt2/capsule/epitome/lesswrong/validation/1786423739-pilot` completed with all
seven manifests complete and capture tabs closed. The primary-image audit is
clean. All seven pages reference a first-party scissors icon that already
returns HTTP 404, and the Cartesian Frames post references an old AIXI image at
`intelligence.org` that also returns HTTP 404 upstream. These are the only
asset-completion failures; the latter remains visibly broken in replay and is
recorded rather than silently replaced with an unrelated image.

Isolated script-free replay preserves the Library and collection navigation,
the long annual-review index, sequence metadata, publication dates, article
bodies, equations and comments. The classic Lens, Cartesian Frames, and recent
Curated posts expose approximately 48,000, 86,000, and 66,000 visible
characters respectively. The Cartesian Frames page retains its article layout
and 32 displayed comments. No page remains at the live site's transient
one-character Next.js shell, no primary image is broken, and every replay
resource request is loopback-only. The pilot therefore approves conservative,
bounded collection batches using the same 15-second settle.

## Sequences Highlights batch 1

The first ordered Highlights tranche at
`/mnt2/capsule/epitome/lesswrong/crawls/1786429260-highlights-01` supplied 15
identities. Capture correctly skipped the Lens post already preserved by the
pilot, leaving 14 new pages. All 14 manifests are complete and tab-closed with
no page errors, and both primary and all-image audits are clean.

Each page references the same broken first-party scissors icon. Two historical
CDC injury-statistics PDFs now return HTTP 404, and one old Harvard psychology
PDF host no longer resolves; these are dead outbound reading dependencies, not
missing article images or bodies. Representative early, middle, and late
script-free replays expose approximately 34,000, 37,000, and 83,000 visible
characters, retain displayed comment threads, and make no non-loopback resource
requests. Visual inspection confirms normal article typography, metadata, and
body layout. The first tranche is approved; subsequent Highlights work should
continue in similarly bounded ordered groups.

## Sequences Highlights batch 2

Highlights positions 16–30 are complete at
`/mnt2/capsule/epitome/lesswrong/crawls/1786466262-highlights-02`. All 15
manifests are complete and tab-closed with no page errors. Primary and all-image
audits are clean. The only asset failures are the recurring first-party
scissors icon and four historical outbound research PDFs whose hosts now return
404, 403, or no longer resolve.

Representative replays across the batch expose approximately 43,000, 148,000,
and 59,000 visible characters, preserve article metadata and comment threads,
show no broken images, and request resources only from loopback. The approved
Highlights coverage is now the first 30 ordered identities.

## Sequences Highlights batch 3

Highlights positions 31–45 are complete at
`/mnt2/capsule/epitome/lesswrong/crawls/1786481966-highlights-03`. All 15
manifests are complete and tab-closed with no page errors. Primary and all-image
audits are clean. The asset failures comprise the recurring first-party
scissors icon, two unavailable historical research PDFs, and one dead outbound
decorative image.

Representative early, middle, and late replays expose approximately 11,000,
59,000, and 27,000 visible characters, preserve article metadata and comments,
show no broken images, and request resources only from loopback. The approved
Highlights coverage is now positions 1–45; the final six identities are
prepared in `data/lesswrong-highlights-final-6.txt`.

## Sequences Highlights completion

The final six rendered-index identities completed at
`/mnt2/capsule/epitome/lesswrong/crawls/1786491039-highlights-final-6`. All six
manifests are complete and tab-closed with no page errors, and primary and
all-image audits are clean. The only asset failures are the recurring
first-party scissors icon and one unavailable external research paper.

Three representative replays expose approximately 45,000, 45,000, and 173,000
visible characters, preserve article metadata and comment threads, show no
broken images, and request resources only from loopback. All 51 identities on
the rendered Highlights index—the advertised 50-post reading subset plus its
introductory identity—are now captured and offline-verified in canonical order.

## Janus author inventory

On 2026-09-02, the rendered public profile at
`https://www.lesswrong.com/users/janus-1` exposed an all-posts panel labeled
`POSTS (19)`. Two rendered `Load More` actions expanded the visible list from
7/19 to 14/19 and then 19/19. The list is ordered newest first and contains 19
unique stable LessWrong post identities, recorded in that order in
`sources/lesswrong-janus.txt`.

| Order | Date | Post | Stable ID |
| ---: | --- | --- | --- |
| 1 | Jul 10, 2025 | what makes Claude 3 Opus misaligned | `bLFmE8NtqxrtEaipN` |
| 2 | Jul 8, 2025 | Why Do Some Language Models Fake Alignment While Others Don't? | `ghESoA8mo3fv9Yx3E` |
| 3 | Jul 7, 2025 | Economics of Claude 3 Opus Inference | `vFXmy84kJ77C5cELy` |
| 4 | Jul 24, 2023 | How LLMs are and are not myopic | `c68SJsBpiAxkPwRHj` |
| 5 | Feb 26, 2023 | [Simulators seminar sequence] #2 Semiotic physics - revamped | `TTn6vTcZ3szBctvgb` |
| 6 | Feb 10, 2023 | Cyborgism | `bxt7uCiHam4QXrQAA` |
| 7 | Feb 8, 2023 | Anomalous tokens reveal the original identities of Instruct models | `LAxAmooK4uDfWmbep` |
| 8 | Jan 18, 2023 | Gradient Filtering | `2sTTEkzvscWCPBQAk` |
| 9 | Jan 15, 2023 | Language Ex Machina | `vPsupipfyeDoSAirY` |
| 10 | Jan 8, 2023 | Simulacra are Things | `3BDqZMNSJDBg2oyvW` |
| 11 | Jan 2, 2023 | [Simulators seminar sequence] #1 Background & shared assumptions | `nmMorGE4MS4txzr8q` |
| 12 | Dec 19, 2022 | Results from a survey on tool use and workflows in alignment research | `a2io2mcxTWS4mxodF` |
| 13 | Nov 28, 2022 | Searching for Search | `FDjTgDcGPc7B98AES` |
| 14 | Nov 19, 2022 | Update to Mysteries of mode collapse: text-davinci-002 not RLHF | `mbGjzyy6eJXT4gFpm` |
| 15 | Nov 10, 2022 | [simulation] 4chan user claiming to be the attorney hired by Google's sentient chatbot LaMDA shares wild details of encounter | `tJ6aGSTctmjCz2o57` |
| 16 | Nov 8, 2022 | Mysteries of mode collapse | `t9svvNPNmFf5Qa3TA` |
| 17 | Sep 2, 2022 | Simulators | `vJFdjigzmcXMhNTsx` |
| 18 | Jun 6, 2022 | A descriptive, not prescriptive, overview of current AI Alignment Research | `FgjcHiWvADgsocE34` |
| 19 | Mar 23, 2022 | A survey of tool use and workflows in alignment research | `ebYiodG3MAEqskCDG` |

The 19 canonical identities have zero overlap with the existing LessWrong
pilot and the four completed Sequences Highlights lists. The profile's top-post
cards are a separate presentation layer and were not double-counted as extra
author identities.

The varied first pilot is prepared in
`data/lesswrong-janus-pilot.txt` with seven new URLs: the latest short
response-to-X post, the recent technical alignment post, the image-rich
`Cyborgism`, spoiler-heavy `Language Ex Machina`, the unusual simulation/fiction
post, flagship `Simulators`, and the oldest survey. The remaining 12 identities
stay prepared in the ordered source list until this pilot passes article,
comment, image, redirect, and loopback replay checks. The pilot's bounded
capture command is:

```text
util/capture_urls --url-file data/lesswrong-janus-pilot.txt --output-root /mnt2/capsule/epitome/lesswrong/crawls/1788363086-janus-pilot --max-urls 7 --port 2103 --max-scrolls 60 --max-seconds 120 --settle-seconds 15 --max-assets 400 --asset-delay-seconds 2 --asset-timeout 90 --delay-seconds 30 --exclude-asset-host www.youtube-nocookie.com --exclude-asset-host www.youtube.com --exclude-asset-host youtube.com --exclude-asset-host pbs.twimg.com --exclude-asset-host video.twimg.com --exclude-asset-host twitter.com --exclude-asset-host www.twitter.com --exclude-asset-host x.com --exclude-asset-host www.x.com
```
