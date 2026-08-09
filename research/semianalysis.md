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

The checks below were completed before the first bounded batch started.

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

## First bounded page batch

The selected 15-page batch completed at:

`/mnt2/capsule/epitome/semianalysis/crawls/1786241060`

All 15 manifests are complete, all capture tabs closed, and the run reported
zero page or asset-completion failures. Together with the three structural
validations, 18 of the 325 approved source identities are complete.

The ordinary article-image audit found one concrete budget edge case. `The Wild
Wild West of LEGO Datacenters` contains 74 rendered images and exceeded the
50-asset completion ceiling, leaving 21 primary figures absent. Those exact 21
resources were recovered with three-second request delays. The structural
homepage and archive listing then exposed 22 additional missing card and
thumbnail images, so `research/audit_capture_images` gained an explicit
`--all-images` mode and recovered those resources as well. The three repairs
added 3,598,746 bytes; repeated article and structural audits report zero
missing rendered images.

The custom-domain homepage's public server HTML is a subscription welcome gate.
Its `No thanks` action depends on removed client scripts, and there is no
server-rendered homepage body behind the gate. Replay therefore preserves that
faithful gate state rather than hiding it into a blank page; `/archive` is the
complete, usable chronological index. Chromium checks also covered that index,
two extremely image-heavy paid previews, and a long architecture article. Text,
figures, subscription boundaries, and layouts were intact. The final strict
network check recorded 103 requests, all to the local replay server.

The refreshed provider inventories contain four Substack-hosted videos across
two articles and no YouTube or Substack-audio entries. These videos are explicit
external-downloader imports. The next deduplicated 30-page batch can proceed
with a longer inter-page delay.

## Second bounded page batch

The next 30 deduplicated article identities completed at:

`/mnt2/capsule/epitome/semianalysis/crawls/1786244832`

All 30 manifests are complete, all capture tabs closed, and the crawl reported
zero page or asset-completion failures. Together with the structural
validations and first batch, 48 of the 325 approved source identities are now
complete.

Five unusually image-heavy articles exceeded the ordinary 50-asset completion
budget, leaving 106 primary figures absent. Two other pages had six missing
listing/card images. The all-image repair recovered exactly those 112 resources
with three-second request spacing: 22,246,923 bytes with zero failures. Repeated
primary and all-rendered-image audits now report zero omissions across the 30
pages.

The refreshed archive index was then checked at 1440×900 in Chromium. Five
varied pages included the three heaviest repaired articles, a long CPU analysis,
and a four-video article. Each retained its article text, figures, paid boundary
where applicable, and 39–104 rendered images with zero broken or pending
images. All six video/frame sources on the video-bearing page were rewritten to
local archive resources. A strict network log across the sequence recorded 552
of 552 requests to `127.0.0.1:8013` and no production-origin traffic.

The refreshed provider inventories contain nine Substack-hosted videos across
four articles and no YouTube or Substack-audio entries. All nine videos remain
explicit external-downloader imports. The next 45 deduplicated articles are
selected in the ignored working list `data/semianalysis-next-45.txt` for a
longer-delay batch after local replay verification passes.
