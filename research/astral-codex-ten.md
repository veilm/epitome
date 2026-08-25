# Astral Codex Ten

## Scope inventory

Astral Codex Ten is Scott Alexander's current Substack publication and remains
separate from the completed historical Slate Star Codex archive. On 2026-08-16,
the publication's first-party paginated archive API returned 1,452 unique
canonical `/p/` identities, ordered newest first, spanning 2020-08-30 through
2026-08-14. The reviewed capture list is tracked in
`sources/astral-codex-ten.txt`.

All 1,452 entries are newsletter posts. The API labels 1,170 for everyone and
282 as paid-only. Paid-only identities remain in the canonical inventory so the
archive preserves their public title, metadata, preview, and paywall boundary;
capture does not attempt to bypass access controls. Archive/listing, account,
authentication, and Substack platform routes are not publication identities.

## Representative validation

The five-page pilot at
`/mnt2/capsule/epitome/astral-codex-ten/validation/1786876733-pilot` covers the
archive, an ordinary article, a long book review, an image-rich article, and a
comment-heavy open thread. All five captures are complete and tab-closed, with
1,451 attempted assets and no page or asset failures. Primary and all-image
audits report no missing images.

Isolated replay retained roughly 33,000 visible characters for the ordinary
article, 89,000 for the image-rich caffeine article, and 466,000 for Open Thread
446. The latter two retained thousands of comment-related nodes, all checked
images loaded, and replay made no production-origin requests. No article was
reduced to a loading shell. The pilot did not contain an actual audio or video
post; its Substack frame resources are platform scaffolding, not substantive
media. Media ledgers therefore remain a batch-boundary audit requirement.

The pilot approves bounded capture batches. The first 15 uncaptured identities
are prepared in ignored working data as `data/astral-codex-ten-first-15.txt`;
it deliberately includes two paid-only posts to validate faithful public
preview/paywall replay without crossing the access boundary.

## First bounded batch

The prepared first 15 uncaptured identities completed at:

`/mnt2/capsule/epitome/astral-codex-ten/crawls/1786880775-first-15`

All 15 manifests are complete and tab-closed with zero page errors. Asset
completion attempted 5,262 dependencies. The only two failures are external
research PDFs returning HTTP 403 from `research.vu.nl` and ResearchGate; they
are outbound citation dependencies rather than missing Astral-hosted content.
Primary-image and all-rendered-image audits report zero missing images.

Isolated replay of an early ordinary article retained about 43,000 visible
characters, the middle Open Thread 444 retained about 429,000, and the late
Hugging Face article retained about 360,000. A hidden Open Thread 445.5
preserved its explicit paid-subscriber boundary and public preview. The
representative replays retained their article/comment content and made no
production-origin requests.

The first batch is therefore approved. The next 30 uncaptured identities are
prepared in ignored working data as `data/astral-codex-ten-next-30.txt`; the
next batch should retain the same access boundary, bounded asset policy, and
port-2103-only capture workflow.

## Second bounded batch

The prepared next 30 uncaptured identities completed at:

`/mnt2/capsule/epitome/astral-codex-ten/crawls/1786928623-next-30`

All 30 manifests are complete and tab-closed, with zero page errors and a
zero-failure batch finish. Asset completion attempted 10,271 dependencies;
the 13 failed assets are all attributable external or platform dependencies:
three cited PDFs (HTTP 403, an external TLS verification failure, and HTTP
503), one malformed Substack avatar fetch (HTTP 400), five stale Substack
profile-image variants (HTTP 404), one Flourish thumbnail (HTTP 403), and
three connection resets (one Berkeley icon and two Dialectical Imagination
image fetches). None is an Astral-hosted primary image.

The network ledger separately records 17 response-body errors across nine
pages. These are dependency/media responses: the Links and Book of Abraham
pages have citation or platform responses, Chip Off The Old Block and Never
Cross a River Four Feet Deep have Mux media responses, Open Thread 440 has a
400 avatar response, Should People Avoid Whole-Body Screening has five 404
profile-image responses, Berkeley Meetup has one unknown dependency response,
Open Thread 437 has one 403 response, and The Dialectical Imagination has one
503 plus two unknown responses. They did not become page failures.

Primary-image and all-rendered-image audits both report 30 pages with zero
missing images and no repair attempts. Loopback replay of an early links page,
Open Thread 440, paid-preview Hidden Open Thread 440.5, the Mux-bearing Chip
Off The Old Block, and the late Dialectical Imagination page rendered their
article content from the local archive with no production-origin requests.
The hidden page retained its explicit “This post is for paid subscribers”
boundary, and the media page retained one video element.

Together with the first bounded batch, 45 previously uncaptured identities
are now captured and audited. The next batch must begin with a deduplicated,
explicitly prepared list; this completed list should not be grown in place.

## Third bounded batch

The prepared next 45 uncaptured identities completed at:

`/mnt2/capsule/epitome/astral-codex-ten/crawls/1786978416-next-45`

All 45 manifests are complete and tab-closed, with zero page errors and a
zero-failure batch finish. Asset completion attempted 13,439 dependencies;
the four failures are a malformed Substack avatar fetch (HTTP 400), a
90-second timeout for an external `i.postimg.cc` image, an external TLS
handshake failure, and a transient DNS failure for a Substack avatar. None is
an Astral-hosted primary image.

The network ledger records six response-body errors across five pages: one
HTTP 400 on Use AI This Election, two media responses on The Types Of
Candidate You Find In The California Gubernatorial Race, one unknown response
on Open Thread 431, one redirect/dependency response on Links For April 2026,
and one unknown response on Open Thread 427. They did not become page
failures.

Generic asset completion also encountered two small YouTube embed documents
(about 127 KB and 129 KB) and one 229 KB `pbs.twimg.com` image from article
embeds. No YouTube video or Twitter/X post/media downloader was invoked, and
the Substack-hosted `twitter.white.svg` share icons are not Twitter-hosted
content. The next capture explicitly excludes the observed exact hosts so
these incidental dependencies are not fetched again.

Primary-image and all-rendered-image audits both report 45 pages with zero
missing images and no repair attempts. Loopback replay of paid-preview Hidden
Open Thread 435.5 retained its explicit subscriber boundary; Open Thread 435
retained about 99,500 visible characters and 215 images; the Mux-bearing
candidate article retained about 138,600 characters, 348 images, and one
video; Links For April 2026 retained about 250,700 characters and 416 images;
and the late paid-preview Lines Composed In A Fake Sequoia Forest retained
its public boundary. All five replays made no production-origin requests.

Together with the first two bounded batches, 90 previously uncaptured
identities are now captured and audited. The next 60 deduplicated identities
are prepared in ignored working data as
`data/astral-codex-ten-next-60.txt`; the next run must retain the same
port-2103-only workflow and pass `--exclude-asset-host
www.youtube-nocookie.com --exclude-asset-host pbs.twimg.com`.

## Fourth bounded batch

The prepared next 60 uncaptured identities completed at:

`/mnt2/capsule/epitome/astral-codex-ten/crawls/1787013682-next-60`

All 60 manifests are complete and tab-closed, with zero page errors and a
zero-failure batch finish. Asset completion attempted 19,325 dependencies;
19,308 completed, 17 failed, and seven were skipped by the exact-host
exclusions. The failed dependencies were eight HTTP 403 responses, five HTTP
404 responses, one HTTP 429 response, one connection reset, and two malformed
local-file references. They were external citations, stale linked media,
profile images, or a local-file reference from the source page; none was an
Astral-hosted primary image. The network ledger records 19 response-body
errors across 15 pages, consisting of two timed-out prediction embeds, the
same external citation/image/dependency failures, two missing Pledge assets,
one Facebook-hosted image denial, one Substack avatar reset, and three
missing or malformed references on Vibecession. They did not become page
failures.

The exact asset-completion exclusions were
`www.youtube-nocookie.com`, `www.youtube.com`, `youtube.com`,
`pbs.twimg.com`, `video.twimg.com`, `twitter.com`, `www.twitter.com`,
`x.com`, and `www.x.com`. The batch recorded no asset result or network
request from those hosts, and no YouTube or Twitter/X media downloader was
invoked. Pages containing YouTube embeds therefore retain the source
reference while avoiding incidental media downloads.

The primary-image audit reported 60 pages with zero missing images. The
all-rendered-image audit initially found one non-article cover variant on
The Dilbert Afterlife; a targeted repair recovered 11,677 bytes, and the
repeat audit reported 60 pages with zero missing images and no remaining
repair attempts. Loopback replay of paid-preview Hidden Open Thread 410.5
retained its explicit subscriber boundary, the December links page retained
326,153 visible characters and 647 images while rewriting its YouTube embeds
offline, and comment-heavy Open Thread 417 retained 621,362 visible
characters and 1,208 images. A replay of the Mux-bearing candidate page from
the preceding batch retained 138,625 visible characters, 348 images, and one
ready local video element. All four replays made no production-origin
requests; only expected local platform-CSS or unavailable-resource 404s were
observed.

Together with the first three production batches, 150 previously uncaptured
identities are now captured and audited, in addition to the five-page pilot.
The next 75 deduplicated identities are prepared in ignored working data as
`data/astral-codex-ten-next-75.txt`; the next run must retain the same
port-2103-only workflow, public/paywall boundary, bounded asset policy, and
exact YouTube/Twitter host exclusions.

## Fifth bounded batch

The prepared next 75 uncaptured identities completed at:

`/mnt2/capsule/epitome/astral-codex-ten/crawls/1787064294-next-75`

All 75 manifests are complete and tab-closed, with zero page failures and a
zero-failure batch finish. The aggregate contains 42,854 requests, 42,531
response bodies, 1,508,157,166 response bytes, and 17 response-body errors.
Asset completion attempted 22,190 dependencies: 22,173 completed, 17 failed,
and 14 were skipped by the exact-host exclusions. The 17 response/asset
failures are the same dependency failures and classify as follows:

* page 15 Liverpool repository PDF: read timeout;
* page 18 Saismaran PDF: HTTP 404;
* page 27 Wikimedia PDF: HTTP 429;
* page 31 IJMET PDF: TLS certificate validation failure, and BSWA PDF: HTTP
  403;
* page 40 Rutgers PDF: HTTP 404;
* page 41 UT Austin PDF: HTTP 404;
* page 47 Independent PDF: HTTP 403, and Independent.ie image: HTTP 404;
* page 49 MIT PDF: TLS certificate validation failure;
* page 55 Sheldrake PDF: HTTP 403;
* page 57 ResearchGate PDF: HTTP 403;
* page 60 RERO PDF: HTTP 410;
* page 61 Harvard PDF: HTTP 504;
* page 62 Alnylam PDF: HTTP 404;
* page 66 Harvard PDF: HTTP 504; and
* page 73 consc.net PDF: HTTP 522.

These are external citation PDFs or linked images, not Astral-hosted primary
content. The aggregate status counts were 200=42,609, 204=153, 401=75,
403=4, 404=5, 410=1, 429=1, 504=2, 522=1, and unknown=3. No page manifest
failed.

The exact asset-completion exclusions were
`www.youtube-nocookie.com`, `www.youtube.com`, `youtube.com`,
`pbs.twimg.com`, `video.twimg.com`, `twitter.com`, `www.twitter.com`,
`x.com`, and `www.x.com`. The batch recorded 14 exclusion decisions and no
network host or completed asset result from any excluded host. No YouTube or
Twitter/X downloader was invoked. This batch had no activated interactive
media (`discovered=0`, `embedded_urls=0`, `activated=0`); a media/reference
page retained its textual YouTube references and one Mux-hosted image
reference without fetching those services.

Primary and all-rendered-image audits both report 75 pages with zero missing
images and no repair attempts. Loopback replays included an early ordinary
page (180,188 visible characters and 300 loaded images), the
YouTube/Mux-reference page (184,591 characters and 287 loaded images), a
comment-heavy page (357,070 characters and 373 loaded images), a links-heavy
page (596,752 characters and 954 loaded images), and late and early
paid-preview pages (338 and 335 characters respectively, each retaining its
explicit subscriber boundary and 2 loaded images). The five-page combined
trace contained 695 requests: 682 local 200 responses and 13 local 404s, all
to `127.0.0.1:8018`; the separate early paid-preview trace was also entirely
loopback. No replay made a production-origin request.

Together with the first four production batches, 225 previously uncaptured
identities are now captured and audited, in addition to the five-page pilot.
The next 90 deduplicated identities are prepared in ignored working data as
`data/astral-codex-ten-next-90.txt`; the next run must retain the same
port-2103-only workflow, public/paywall boundary, bounded asset policy, and
exact YouTube/Twitter host exclusions.

## Sixth bounded batch

The prepared next 90 uncaptured identities completed at:

`/mnt2/capsule/epitome/astral-codex-ten/crawls/1787123812-next-90`

All 90 manifests are complete and tab-closed, with zero page failures and a
zero-failure batch finish. The aggregate contains 51,107 requests, 50,712
response bodies, 1,497,889,366 response bytes, and 32 response-body errors.
Asset completion discovered 76,450 dependencies, attempted 26,164, completed
26,134, failed 31, skipped 14 by exact-host exclusion, and downloaded
648,661,712 bytes. The 31 asset-completion failures classify as follows:

* page 10 Benning Army PDF: read timeout;
* pages 14 Discord PNG and imgcdn PNG, 15 ACA PDF, 22 ACLUM PDF, 25 UVA
  lactose PDF, 31 Core PDF and UN genocide-convention PDF, 41 Supreme Court
  transcript PDF, pages 44 CRS case-story, annual-report, and handbook PDFs,
  page 46 PVAL PDF, page 76 Democrats platform PDF, and page 77 NICJR PDF:
  HTTP 404 (14 total);
* page 17 RAND PDF, page 36 PhilPapers PDF, page 45 IMF PDF, page 47
  Tearfund PDF, page 50 Johns Hopkins PDF, page 65 Justia filing PDF, and
  page 70 ABA PDF: HTTP 403 (7 total);
* page 17 Syracuse PDF, page 25 BWH PDF, and page 51 Silverchair PDF: TLS
  hostname/certificate validation failures (3 total);
* page 24 Harvard PDF: HTTP 504;
* page 31 Wikimedia PDF and page 64 Wikimedia PDF: HTTP 429 (2 total);
* page 45 DrKnow PDF: HTTP 522;
* page 52 Evidencias en Pediatria PDF: HTTP 502; and
* page 88 Meetups Everywhere Spring 2025 Times: an internal
  `ValueError: Invalid IPv6 URL` while parsing a dependency URL, with zero
  asset attempts for that page.

These are external citation or linked-media dependencies, or one malformed
dependency URL; none is an Astral-hosted primary image. The network ledger
records 32 response-body errors across 23 pages. Its explicit error/status
classes are 14 HTTP 404, seven HTTP 403, two HTTP 429, one HTTP 504, one HTTP
522, one HTTP 502, and four unknown responses. The links-heavy Mux page also
has four 206 range responses and one 307 redirect in its network status ledger;
these are separate from the response-body error total. No page manifest
failed.

The exact asset-completion exclusions were
`www.youtube-nocookie.com`, `www.youtube.com`, `youtube.com`,
`pbs.twimg.com`, `video.twimg.com`, `twitter.com`, `www.twitter.com`,
`x.com`, and `www.x.com`. The batch recorded 14 exclusion decisions and no
asset-completion result from an excluded host. Three page-level network
requests used `www.youtube-nocookie.com` as incidental source-page
dependencies; no YouTube or Twitter/X downloader was invoked and no excluded
host was intentionally fetched as media. Interactive-media ledgers for all
90 pages report zero discovered, embedded, or activated interactive media.

Primary and all-rendered-image audits both report 90 pages with zero missing
images, zero repair attempts, and zero repair failures. Loopback replays used
the local archive server on port 8019 and included paid-preview Hidden Open
Thread 390.5 (336 visible characters, 2/2 images, explicit paywall), ordinary
My Heart Of Hearts (646,142 visible characters, 1,133/1,133 images),
comment-heavy Highlights From The Comments On Missing Heritability (143,101
characters, 149/149 images), links-heavy Links For July 2025 (325,077
characters, 617/617 images), and the Mux/media-reference Links For April 2025
(597,933 characters, 1,003/1,003 images, one local video element). The
combined trace contained 1,252 request records: 1,228 local 200 responses,
18 local 404s, and six local 206 range responses, all from `127.0.0.1:8019`;
no replay made a production-origin request.

Together with the first five production batches, 315 previously uncaptured
identities are now captured and audited, in addition to the five-page pilot.
The next 105 identities are prepared in ignored working data as
`data/astral-codex-ten-next-105.txt`, deduplicated against the pilot and all
six production batches. The next run must retain the same port-2103-only
workflow, public/paywall boundary, bounded asset policy, and exact
YouTube/Twitter host exclusions.

## Seventh bounded batch

The prepared next 105 uncaptured identities completed at:

`/mnt2/capsule/epitome/astral-codex-ten/crawls/1787194393-next-105`

All 105 manifests are complete and tab-closed, with zero page failures,
zero nonzero network-log return codes, and a zero-failure batch finish. The
aggregate contains 64,288 requests, 63,788 response bodies,
1,711,202,613 response bytes, and 74 response-body errors. Network status
counts are 200=63,900, 204=211, 308=24, 400=1, 401=105, 403=14, 404=14,
405=1, 429=3, 503=1, 504=1, and unknown=13. Asset completion discovered
101,369 dependencies, found 28,515 already-complete entries, attempted
33,215, completed 33,167, failed 48, skipped two by exact-host exclusion,
and downloaded 697,690,489 bytes. Interactive-media ledgers report zero
discovered, embedded, activated, or completed interactive media.

The 48 asset-completion failures classify as two connection resets, 14
HTTP 404s, 14 HTTP 403s, two TLS validation failures, one HTTP 400, eight
DNS/no-address failures, one timeout, three HTTP 429s, one HTTP 504, one
HTTP 503, and one HTTP 405. They are external citation PDFs, linked images
or media, or malformed external dependencies; no Astral-hosted primary
image failed. The exact per-page records remain in the bounded root. The
74 response-level records are distributed across pages 5, 6, 10, 12, 31,
32, 36, 38, 40, 44, 46, 52, 54, 56, 57, 58, 65, 66, 70, 72, 73, 74, 77,
81, 85, 86, 87, 88, 90, 92, 96, 101, and 104: 24 HTTP 308 redirect-body
records, 14 HTTP 403s, 14 HTTP 404s, three HTTP 429s, and one each of
HTTP 400, 405, 503, and 504, with the remainder statusless/unknown. No
page manifest failed.

The exact asset-completion exclusions were
`www.youtube-nocookie.com`, `www.youtube.com`, `youtube.com`,
`pbs.twimg.com`, `video.twimg.com`, `twitter.com`, `www.twitter.com`,
`x.com`, and `www.x.com`. There were two exclusion decisions and no
excluded-host asset result. One page-level request used
`www.youtube-nocookie.com` as an incidental source-page dependency; no
YouTube or Twitter/X downloader was invoked and no excluded host was
intentionally fetched as media.

Primary and all-rendered-image audits both report 105 pages with zero
missing images, zero repair attempts, and zero repair failures. Loopback
replays used the local archive server on port 8020 and included paid-preview
Hidden Open Thread 373.5 (337 visible characters, 2/2 images, explicit
paywall), ordinary Misophonia (195,062 characters, 286/286 images),
comment-heavy Highlights From The Comments On Tegmark (430,614 characters,
577/577 images), links-heavy Links For February 2025 (485,186 characters,
1,007/1,007 images), and the media/reference Model City Monday 2/3/25
(117,595 characters, 285/285 images, no activated video). The combined
trace contained 727 request records: 719 local 200 responses and eight
local 404s, all from `127.0.0.1:8020`; no replay made a production-origin
request and the replay tab was closed afterward.

Together with the first six production batches, 420 previously uncaptured
identities are now captured and audited, in addition to the five-page pilot.
The next 120 identities are prepared in ignored working data as
`data/astral-codex-ten-next-120.txt`, deduplicated against the pilot and all
seven production batches. The next run must retain the same port-2103-only
workflow, public/paywall boundary, bounded asset policy, and exact
YouTube/Twitter host exclusions.

## Eighth bounded batch

The prepared next 120 uncaptured identities completed at:

`/mnt2/capsule/epitome/astral-codex-ten/crawls/1787278704-next-120`

All 120 manifests are complete and tab-closed, with zero page failures and a
zero-failure batch finish. The aggregate contains 76,043 requests, 75,519
response bodies, 1,948,683,397 response bytes, and 39 response-body errors.
Asset completion discovered 111,258 dependencies, found 31,919
already-complete entries, attempted 41,162, completed 41,124, failed 38,
recorded 18 exact-host exclusions, and downloaded 784,005,253 bytes. The 38
asset-completion failures classify as 19 HTTP 404s, 10 HTTP 403s, one each
of HTTP 503, 500, 502, and 410, one read timeout, one DNS/no-address error,
one connection reset, one TLS hostname-validation failure, and one DNS
name-resolution error. They are external citation PDFs, linked images, or
other dependencies; no Astral-hosted primary image failed.

The response-level records are likewise dependency outcomes rather than page
failures. Their status counts include 19 HTTP 404s, 10 HTTP 403s, one each of
HTTP 410, 500, 502, and 503, and five statusless/unknown errors, alongside
the successful and ordinary platform responses. Interactive-media ledgers
for all 120 pages report zero discovered, embedded, activated, or completed
interactive media. The exact asset-completion exclusions were
`www.youtube-nocookie.com`, `www.youtube.com`, `youtube.com`,
`pbs.twimg.com`, `video.twimg.com`, `twitter.com`, `www.twitter.com`,
`x.com`, and `www.x.com`; no excluded-host URL appears in an asset result,
and no YouTube or Twitter/X downloader was invoked.

Primary and all-rendered-image audits both report 120 pages with zero
missing images, zero repair attempts, and zero repair failures. Loopback
replays used the local archive server on port 8021 and covered ordinary
Ballots Everywhere (17,519 visible characters, 49/49 images), comment-heavy
Open Thread 347 (639,359 characters, 1,103/1,103 images), links-heavy Links
For September 2024 (678,019 characters, 1,058/1,058 images), paid-preview
Hidden Open Thread 338.5 (338 characters, 2/2 images, explicit paywall), and
the YouTube-reference Your Book Review: Autobiography Of Yukichi Fukuzawa
(91,437 characters, 155/155 images). The combined trace contained 625
request records: 611 local 200 responses and 14 local 404s, all from
`127.0.0.1:8021`; no replay made a production-origin request.

Together with the first eight production batches, 540 bounded production
pages are now captured and audited, in addition to the five-page pilot. The
next 135 identities are prepared in ignored working data as
`data/astral-codex-ten-next-135.txt`, deduplicated against the pilot and all
eight production batches. The next run must retain the same port-2103-only
workflow, public/paywall boundary, bounded asset policy, and exact
YouTube/Twitter host exclusions.

## Ninth bounded batch

The prepared next 135 uncaptured identities completed at:

`/mnt2/capsule/epitome/astral-codex-ten/crawls/1787383071-next-135`

All 135 manifests are complete and tab-closed, with zero page failures and a
zero-failure batch finish. The aggregate contains 80,675 requests,
79,825 response bodies, 2,482,436,863 response bytes, and 285 response-body
errors. The status ledger includes 16 HTTP 403s, 17 HTTP 404s, three HTTP
429s, two HTTP 500s, and one each of HTTP 400, 418, 502, and 520, with 11
unknown-status records; the large body-error count includes 233
response-body-budget failures on Seen In The Bay. These are dependency or
response-body outcomes, not capture-level page failures.

Asset completion discovered 110,000 dependencies, found 33,350
already-complete entries, attempted 43,743, completed 43,459, failed 284,
skipped 32,897 already-accounted-for entries, recorded 10 exact-host
exclusions, and downloaded 1,205,112,090 bytes. The 284 asset-completion
failures classify as 233 response-body-budget errors on Seen In The Bay;
16 HTTP 403s; 15 HTTP 404s; three HTTP 429s; two HTTP 500s; one each of
HTTP 400, 418, 502, and 520; three TLS certificate failures; four connection
resets; three timeouts; and one DNS/URL-resolution failure. They are linked
external citations, images, or other dependencies; no Astral-hosted primary
image failed.

The exact asset-completion exclusions were
`www.youtube-nocookie.com`, `www.youtube.com`, `youtube.com`,
`pbs.twimg.com`, `video.twimg.com`, `twitter.com`, `www.twitter.com`,
`x.com`, and `www.x.com`. The 10 exclusion decisions occurred on five
pages; no excluded-host URL appears in an asset result. Interactive-media
ledgers for all 135 pages report zero discovered, embedded, activated, or
completed interactive media. No YouTube or Twitter/X downloader was invoked.

Primary and all-rendered-image audits both report 135 pages with zero missing
images, zero repair attempts, and zero repair failures. Loopback replays used
the local archive server on port 8022 and included public The Mystery Of
Internet Survey IQs (201,729 visible characters, 356/356 images),
comment-heavy Open Thread 320 (357,893 characters, 702/702 images),
links-heavy Links For February 2024 (302,097 characters, 585/585 images),
paid-preview Hidden Open Thread 321 (336 characters, 2/2 images), and the
YouTube-reference Book Review Contest Rules 2024 (29,570 characters,
110/110 images). The combined trace contained 657 request records: 647
local 200 responses and 10 local 404s, all from `127.0.0.1:8022`; no replay
made a production-origin request.

Together with the first nine production batches, 675 bounded production
pages are now captured and audited, in addition to the five-page pilot. The
next 150 identities are prepared in ignored working data as
`data/astral-codex-ten-next-150.txt`, deduplicated against the pilot and all
nine production batches. The next run must retain the same port-2103-only
workflow, public/paywall boundary, bounded asset policy, and exact
YouTube/Twitter host exclusions.

## Tenth bounded batch

The prepared next 150 uncaptured identities completed at:

`/mnt2/capsule/epitome/astral-codex-ten/crawls/1787494909-next-150`

All 150 manifests are complete and tab-closed, with zero page failures and a
zero-failure batch finish. The aggregate contains 89,073 requests,
88,372 response bodies, 2,309,212,019 response bytes, and 86 response-body
errors across 47 pages. Among error-bearing pages, the status ledger contains
47 HTTP 404s, 15 HTTP 403s, two HTTP 400s, one HTTP 500, one HTTP 503, and
14 unknown-status records; six additional response-body records have no
paired error status. These are dependency/body outcomes rather than page
capture failures.

Asset completion discovered 120,545 dependencies, found 36,850
already-complete entries, attempted 48,542, completed 48,465, failed 77,
skipped 35,142 already-accounted-for entries, recorded 11 exact-host
exclusions, and downloaded 911,157,927 bytes. The 77 asset-completion
failures classify as 44 HTTP 404s, 15 HTTP 403s, two HTTP 400s, one HTTP 500,
one HTTP 503, seven connection resets, one read timeout, and six DNS/name
resolution failures. The five primary-image repair attempts all returned
HTTP 404 with zero bytes, confirming that those historical image URLs are no
longer available.

The exact asset-completion exclusions were
`www.youtube-nocookie.com`, `www.youtube.com`, `youtube.com`,
`pbs.twimg.com`, `video.twimg.com`, `twitter.com`, `www.twitter.com`,
`x.com`, and `www.x.com`. The 11 exclusion decisions produced no excluded-host
asset result. The all-rendered-image audit additionally identified two
Twitter-host avatar variants as intentionally excluded dependencies; no
YouTube or Twitter/X downloader was invoked. Interactive-media ledgers for
all 150 pages report zero discovered, embedded, activated, or completed
interactive media.

The primary image audit found 150 pages with five missing images on three
pages. The all-rendered-image audit found seven missing images on five pages:
the same five unavailable HTTP-404 images plus two excluded Twitter-host
avatar variants. No repair succeeded or altered the public/paywall boundary.

Bounded loopback replays used the local archive server on port 8023 and
covered early Open Thread 290 (369,957 visible characters, 672/672 images),
paid-preview Hidden Open Thread 289.5 (338 visible characters, 2/2 images,
the preserved `.paywall` marker and paid-subscriber text), comment-heavy
Highlights From The Comments On Putin (268,965 characters, 298/298 images,
one offline media placeholder), links-heavy Links For August 2023 (433,058
characters, 801/801 images), media/reference Your Book Review: The Rise And
Fall Of The Third Reich (207,646 characters, 297/297 images), a middle
Hypergamy review preview (373 characters, 2/2 images), and late Berkeley
Meetup On Tuesday (37,915 characters, 96/96 images). The trace contained 890
request records, all from `127.0.0.1:8023` (870 local 200 responses, 19
intentional local 404s, and one local 400 route probe); no replay made a
production-origin request, and the replay tab was closed afterward.

Together with the first ten production batches, 825 bounded production pages
are now captured and audited, in addition to the five-page pilot. The next
165 identities are prepared in ignored working data as
`data/astral-codex-ten-next-165.txt`, with 165 unique URLs and zero overlap
against the pilot and all ten completed production batches. The next run must
retain the same port-2103-only workflow, public/paywall boundary, bounded
asset policy, and exact YouTube/Twitter host exclusions.
