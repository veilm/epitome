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
