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
