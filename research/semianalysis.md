# SemiAnalysis source reconnaissance

Investigated through Chromium on CDP port 2103 at Unix timestamp `1786187951`.
This preparation separates the public publication archive from the company's
institutional products before any page batch begins.

## Site split

SemiAnalysis currently has two materially different first-party surfaces:

- `https://semianalysis.com/` is a WordPress corporate front end for company
  information, careers, events, models, tools, subscriptions, and institutional
  login. Its homepage mirrors a small set of recent publication cards but sends
  readers to the newsletter host for the articles.
- `https://newsletter.semianalysis.com/` is the custom-domain Substack
  publication. Its `/archive` page is the canonical chronological article
  index and exposes latest, top, and discussion views.

The public article archive is the first approved preservation scope. Corporate
pages, careers, model descriptions, and public tools should become a separate
second scope; authenticated institutional dashboards and paid model data are
not implied by this public crawl.

## Article inventory

The newsletter sitemap at
`https://newsletter.semianalysis.com/sitemap.xml` contained 322 `/p/...` post
identities at the investigation timestamp. It was loaded through the reusable
CDP sitemap utility, not a direct HTTP client. The tracked source file
`sources/semianalysis-newsletter.txt` adds the publication homepage, archive,
and feed for 325 total URL identities.

The archive ranges from current multi-author AI infrastructure analysis to the
earliest semiconductor posts. It mixes free and subscription-oriented entries,
so the first validation set needs at least one current long article, one older
article, and one page whose public view is paywalled or excerpted. The archive
must preserve exactly what the public browser receives rather than treating a
legitimate subscription boundary as an extractor failure.

## Capture readiness

The publication uses the same Substack page family already validated for
Dwarkesh, including responsive image proxies, embedded media, comments, and
custom-domain routes. Epitome's existing Substack replay and media-inventory
support should therefore be the baseline. Before a batch starts, complete these
bounded checks:

1. Capture and offline-network audit the homepage/archive plus varied free and
   paywalled article pages.
2. Confirm whether articles expose YouTube, Substack video, Substack audio, or
   downloadable attachments and create the corresponding tracked ledgers.
3. Verify long diagrams and image-heavy technical posts do not exceed the
   ordinary 50-asset completion ceiling; raise it only for observed substantive
   omissions.
4. Keep the 325-identity newsletter scope separate from a later reviewed
   `semianalysis.com` corporate/careers/models scope.

No SemiAnalysis batch has been started during this reconnaissance.

## Structural validations

Three article variants were captured under
`/mnt2/capsule/epitome/semianalysis/validation/`:

- the current `SpaceX 10GW in 2027` article;
- the widely linked 2023 `Google "We Have No Moat, And Neither Does OpenAI"`
  article; and
- the free 2020 `Moore's Law is Dead for DRAM` article.

All three manifests are complete and all capture tabs closed. The first two
currently declare `isAccessibleForFree: false` and render an explicit paid-
subscriber boundary. That is the complete public representation, not a cropped
capture error. The 2020 article declares `isAccessibleForFree: true` and
retains its full short article body and seven inline images.

Six direct legacy S3 originals returned HTTP 403, but preserved Substack proxy
variants covered all but one rendered image. The generic replay-image audit
identified that exact omission and repaired its 65,305-byte proxy resource. A
second audit reports zero missing primary images across all three validations.
Chromium checks at 1440×900 confirmed the two paywalls, the complete free
article, and zero broken article images. An attached network log recorded 171
requests, all to the local replay server.

The three provider inventories currently contain zero YouTube, Substack-video,
or Substack-audio entries. They remain tracked so later page batches can append
newly encountered media without changing the workflow. With public paywall and
legacy structures now distinguished and replay-tested, the newsletter scraper
is ready for a first bounded batch after Dwarkesh completes.

## Subscriber-email comparison

An authenticated mailbox was inspected through the ordinary rendered Gmail UI
on CDP port 2102; no mailbox APIs or direct HTTP clients were used. The search
found 44 SemiAnalysis messages spanning late 2024 through August 2026. Two
current paid issues were opened, including the same `SpaceX 10GW in 2027`
article used in the browser validation.

The email does not provide a hidden copy of the paid article. The SpaceX email
contains the same introduction, related-story card, final public paragraphs,
`Beyond the paywall` transition, and subscription boundary as the public web
page. It then offers an upgrade link. A second current issue likewise labels
itself `PREVIEW` and ends with `Subscribe to SemiAnalysis to unlock the rest`.
Gmail may visually clip a long message behind its own `View entire message`
control, but that is separate from—and does not bypass—the publication's paid
boundary.

Consequently, the public newsletter page remains the canonical crawl input.
Email is not a richer substitute for paid issues under the presently available
free subscription. If a future account legitimately receives full issues by
email, those messages should be treated as a separate private, authenticated
source rather than mixed into the public-web archive. No message body or
account-specific data is stored in Git.
