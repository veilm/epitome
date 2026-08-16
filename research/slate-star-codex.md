# Slate Star Codex

## Canonical scope

The historical WordPress site at `https://slatestarcodex.com/` was inspected
through Chromium/CDP on 2026-08-10 while the Paul Graham crawl was active. The
homepage is still a rendered first-party archive with about 75,000 visible
characters and links to the archive, about/top-posts material, monthly indexes,
RSS, and the successor site.

`https://slatestarcodex.com/archives/` is the authoritative post inventory. Its
rendered page contains 1,906 links, including 1,558 distinct canonical post
URLs matching the site's dated `/YYYY/MM/DD/slug/` structure. The reviewed
source list in `sources/slate-star-codex.txt` contains those posts in the
archive's newest-to-oldest order plus four structural identities:

- homepage;
- about page;
- complete archives page; and
- curated top-posts page.

This yields 1,562 approved identities. Monthly/category/tag listings, RSS and
comments feeds, WordPress service endpoints, and the separate Astral Codex Ten
Substack are not duplicated into this scope. Comments embedded on individual
post pages remain part of each historical page and need explicit pilot review;
they are not equivalent to crawling the global comments feed.

## Validation plan

Before any page batch begins:

1. capture and locally replay the complete archives page;
2. validate a short ordinary post, an image-bearing post, a very long top post,
   and a comment-heavy/open-thread page;
3. measure whether server-rendered comments, pagination, MathJax/code, images,
   and outbound embeds survive script-free replay;
4. inventory external media without downloading YouTube or Twitter/X; and
5. require complete manifests, closed capture tabs, clean rendered-image
   audits, and zero production-origin requests during local replay.

The successor `astralcodexten.com` remains a separate source because its
Substack structure and free/paywalled/email variants require their own scope.

## Archives-page pilot

The complete structural archive was captured at:

`/mnt2/capsule/epitome/slate-star-codex/validation/1786356305-archives`

Its manifest is complete and tab-closed. The capture retains a 562,635-byte
final DOM, 84,297 visible characters, 1,906 links, 59 rendered images, and 46
server-rendered historical comments. Asset completion recovered 88 of 90
initially missing references with two-second spacing. The only failures are two
obsolete Gravatar share-button sprites that return HTTP 404 upstream and are
not rendered `<img>` content; both primary and all-image audits are clean.

Desktop replay preserves the full three-column WordPress layout, archive list,
sidebars, advertising/book images, avatars, and comments. Its 41,774-pixel page
has zero broken rendered images and made zero production-origin requests. The
structural path is therefore capture-ready, but representative ordinary,
image-heavy, long, and open-thread post pilots still precede any large crawl.

## Representative post validation

Four varied posts were captured at:

`/mnt2/capsule/epitome/slate-star-codex/validation/1786358714-varied`

They cover the short *Introducing Astral Codex Ten* post, the long-form
*Meditations on Moloch*, the political-spectrum quiz, and comment-heavy *Open
Thread 156*. A redundant post-navigation ready-state wait marked the first
Moloch attempt incomplete despite preserving its 1.55 MB final DOM and 410
response bodies. Capture now reads the already-parsed DOM without repeating
that full-load wait; the bounded retry at
`/mnt2/capsule/epitome/slate-star-codex/validation/1786362856-moloch-retry`
is complete and tab-closed.

All five representative identities—including the archive pilot—retain the
three-column WordPress layout, article bodies, sidebars, ads, avatars, and
server-rendered comments. The long Moloch replay contains about 504,000 visible
characters and 726 comments; the quiz contains about 209,000 characters and
439 matched comment nodes; the open thread contains about 444,000 characters
and 1,208 displayed comments. The quiz questions and choices are preserved,
but JavaScript scoring is intentionally inert in script-free replay.

Primary-image audits are clean. The only remaining Moloch misses are two
zero-size Amazon tracking pixels, two obsolete Gravatar share sprites, and one
external event image already returning HTTP 404 upstream. The open thread also
references two dead outbound PDFs; those are dependency-recovery tasks rather
than missing first-party post content. Desktop replays show zero substantive
broken images and make zero production-origin requests. This representative
scope is ready for bounded page batches after the active Paul Graham scope is
complete.

## First bounded batch

The first 15 identities not already completed by representative validation are
captured at:

`/mnt2/capsule/epitome/slate-star-codex/crawls/1786493569-first-15`

All 15 manifests are complete and tab-closed with no page errors. The
primary-image audit is clean. Two pages exposed more rendered avatars than the
500-asset capture budget: a targeted all-image repair recovered all 52 omitted
Gravatars (79,814 bytes), after which the repeated all-image audit was clean.
The remaining failures are obsolete Gravatar share sprites plus dead or blocked
outbound documents and images, not missing first-party article content.

Isolated replay samples preserve the homepage and indexes, ordinary posts, and
large comment-heavy threads. The largest checked open thread exposes about
1.79 million visible characters, 2,996 comment nodes, and 3,014 images with no
broken images. Every checked replay resource is loopback-only. The approved
batch pattern retains the bounded 500-asset page capture, followed by targeted
all-image repair at the batch boundary when a page has more rendered avatars.

## Second bounded batch and avatar policy

The next 30 identities are complete across:

- `/mnt2/capsule/epitome/slate-star-codex/crawls/1786503032-next-30` (first 15);
- `/mnt2/capsule/epitome/slate-star-codex/crawls/1786520508-next-30-no-gravatars`
  (remaining 15).

All 30 manifests are complete and tab-closed with no page errors, and both
halves have clean primary-image audits. The original half showed that hundreds
of unique 40-pixel Gravatars dominated runtime at two-second request spacing,
despite being incidental to the preserved discussion. Capture now supports an
exact-host asset-completion exclusion; the continuation skipped 5,244 missing
`secure.gravatar.com` avatar downloads while still attempting 433 non-avatar
assets. It completed about six to seven times faster.

The exclusion does not remove the server-rendered comment DOM, authors,
timestamps, or text, nor does it block avatars received during the initial
browser load. Representative combined replays retain 314,000–770,000 visible
characters and 464–1,464 comments. They have no substantive broken images and
make no production-origin requests. Subsequent Slate Star Codex batches should
use `--exclude-asset-host secure.gravatar.com`; missing small avatars are an
accepted presentation loss, while primary article images remain required.

## Third bounded batch

The next 45 identities are complete at
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786523829-next-45-no-gravatars`.
All 45 manifests are complete and tab-closed with no page errors. Asset
completion attempted 1,189 non-avatar dependencies, excluded 14,144
`secure.gravatar.com` URLs, and recorded 92 failures from dead, blocked,
rate-limited, or timed-out outbound sites. The primary-image audit is clean on
all 45 pages.

Early, middle, and late isolated replays retain 65,000–616,000 visible
characters and 102–863 comment nodes, including comment text and authors. The
only broken rendered images in those samples are 40-pixel comment avatars;
there are no substantive broken images and every loaded resource is
loopback-only. The optimized policy is therefore approved for the active
60-page continuation.

## Fourth bounded batch

The next 60 identities are complete across
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786534399-next-60-no-gravatars`
and the one-page retry at
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786546288-next-60-retry`.
The main run preserved 59 pages and closed all 60 tabs; one article lost its
temporary CDP session before completion and passed on the focused retry. The
combined scope is therefore 60/60 complete and tab-closed.

The main run attempted 1,488 non-avatar dependencies and excluded 14,684
Gravatar URLs. Its 87 asset failures are dead, blocked, rate-limited, or timed
out outbound dependencies, while the primary-image audit is clean. Three
isolated replays retain 359,000–795,000 visible characters and 554–1,152
comments with substantial comment text. Their only broken images are 40-pixel
avatars, and all loaded resources are loopback-only. The same policy is
approved for the active 75-page continuation.

## Fifth bounded batch

The next 75 identities are complete at
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786546385-next-75-no-gravatars`.
All 75 manifests are complete and tab-closed with no page errors. Asset
completion attempted 1,826 non-avatar dependencies, excluded 17,746 Gravatar
URLs, and recorded 116 dead, blocked, rate-limited, or timed-out outbound
failures. The primary-image audit is clean on every page.

Early, middle, and late isolated replays retain 88,000–796,000 visible
characters and 101–1,228 comments with substantial comment text. Their only
broken images are 40-pixel avatars, and every loaded resource is loopback-only.
The optimized policy is approved for the active 90-page continuation.

## Sixth bounded batch

The next 90 identities are complete at
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786563033-next-90-no-gravatars`.
All 90 manifests are complete and tab-closed with no page errors. Asset
completion attempted 2,299 non-avatar dependencies, excluded 22,834 Gravatar
URLs, and recorded 186 dead, blocked, rate-limited, or timed-out outbound
failures. The primary-image audit is clean on every page.

Early, middle, and late isolated replays retain 133,000–696,000 visible
characters and 155–978 comments with substantial comment text. Their only
broken images are 40-pixel avatars, and every loaded resource is loopback-only.
The optimized policy is approved for the active 105-page continuation.

## Seventh bounded batch

The next 105 identities are complete across
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786579580-next-105-no-gravatars`
and the focused continuation at
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786603084-next-105-retry`.
The original run preserved 91 complete pages before a comment-linked MP3 from
`vivalapanda.moe` streamed indefinitely at playback speed. Capture now applies
its asset timeout as a wall-clock deadline rather than only a socket-inactivity
timeout. The retry excluded that incidental stream and completed the remaining
14 identities. The combined scope has 105 unique URLs, all complete and
tab-closed with no final page errors.

Primary-image audits are clean across both runs. Early, middle, and late
isolated replays retain 160,000–283,000 visible characters and 260–402 comments
with substantial comment text. Their only broken images are 40-pixel avatars,
and every loaded resource is loopback-only. One malformed bracketed historical
link also prompted replay normalization to leave invalid URLs inert instead of
aborting an entire audit. The hardened policy is approved for the active
120-page continuation.

## Eighth and ninth bounded batches

The next 120 identities are complete across
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786605860-next-120-no-gravatars`
and `/mnt2/capsule/epitome/slate-star-codex/crawls/1786636339-next-120-retry`.
The main run preserved 96 complete pages before its long-lived CDP context
began timing out consistently; a fresh browser check remained healthy and the
focused retry completed all 24 missing identities. The combined scope has 120
unique complete URLs; superseded failed manifests remain as provenance.

The following 135 identities are complete across
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786641864-next-135-no-gravatars`
and `/mnt2/capsule/epitome/slate-star-codex/crawls/1786669098-next-135-retry`.
The main run preserved 133 pages. One page lost its temporary CDP session and
another contained a malformed comment dependency URL; asset completion now
records `InvalidURL` as a nonfatal failed dependency. Both pages passed on the
focused retry, yielding 135/135 complete and tab-closed identities.

Primary-image audits are clean across all 135 successful captures. Early,
middle, and late isolated replays retain 173,000–624,000 visible characters and
183–856 comments with substantial comment text. Their only broken images are
40-pixel avatars, and every loaded resource is loopback-only. The current
policy is approved unchanged for the active 150-page continuation.

## Tenth bounded batch

The next 150 identities are complete at
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786669793-next-150-no-gravatars`.
All 150 manifests are complete and tab-closed with no page errors. Asset
completion attempted 4,128 non-avatar dependencies, excluded 37,230 Gravatar
URLs, and recorded 486 dead, blocked, rate-limited, malformed, or timed-out
outbound failures. Primary-image audits split into two 75-page views are clean
on every page.

Early, middle, and late isolated replays retain 154,000–517,000 visible
characters and 243–642 comments with substantial comment text. Their only
broken images are 40-pixel avatars, and every loaded resource is loopback-only.
The current policy is approved unchanged for the active 165-page continuation.

## Eleventh bounded batch

The next 165 identities are complete across
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786700179-next-165-no-gravatars`,
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786734763-next-165-retry`,
and `/mnt2/capsule/epitome/slate-star-codex/crawls/1786735842-next-165-retry-2`.
The main run preserved 161 complete pages; four late pages lost temporary CDP
sessions. The first focused retry recovered two, and the second recovered the
remaining two. The combined scope is 165/165 complete and tab-closed.

Split primary-image audits are clean across all 165 successful identities.
Early, middle, and late isolated replays retain 267,000–502,000 visible
characters and 426–684 comments with substantial comment text. Their only
broken images are 40-pixel avatars, and every loaded resource is loopback-only.
The current policy is approved unchanged for the active 180-page continuation.

## Twelfth bounded batch

The next 180 identities are complete across
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786736538-next-180-no-gravatars`,
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786737496-next-180-diagnostic`,
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786738417-session-lock-validation`,
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786738534-next-180-session-lock-fixed`,
and
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786746271-next-180-post-reboot`.
The first attempts exposed a shared CDP session-registry race; after the
registry was made safe for concurrent writers, 21 identities completed before
a workstation reboot and the remaining 154 resumed without recapture. The
combined scope is 180/180 complete and tab-closed. Successful pages attempted
5,019 non-avatar dependencies, excluded 59,860 Gravatar URLs, and recorded 731
dead, blocked, rate-limited, or timed-out outbound failures.

Primary-image audits are clean across the first 26 recovered identities. The
bulk audit process could not finish the 154-page root, so early, middle, and
late local replays were checked directly instead. They retain
135,000–872,000 visible characters and 212–892 comments, load no non-loopback
resources, and preserve substantive images. Their broken image elements are
the accepted 40-pixel Gravatars plus two 1-pixel Amazon tracking images in the
middle sample. The current policy is approved unchanged for the active
195-page continuation.

## Thirteenth bounded batch

The next 195 identities are complete at
`/mnt2/capsule/epitome/slate-star-codex/crawls/1786786220-next-195-no-gravatars`.
All 195 manifests are complete and tab-closed with no page or CDP-session
errors. Asset completion attempted 4,571 non-avatar dependencies, excluded
29,162 Gravatar URLs, and recorded 474 dead, blocked, rate-limited, or timed-out
outbound failures.

Primary-image audits of the first, middle, and final identities are clean.
Their isolated replays retain 117,000–384,000 visible characters and 177–579
comments. Broken image elements are limited to the accepted small avatars and
tracking pixels; there are no substantive broken images and every loaded
resource is loopback-only. The current policy is approved unchanged for the
final 193 canonical identities.
