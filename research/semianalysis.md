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
