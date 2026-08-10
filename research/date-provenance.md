# Catalog date provenance

The public catalog had 2,266 pages on 2026-08-10: 2,074 with extracted
publication dates and 192 without them. The undated set was OpenAI 145, AI 2040
22, AI 2027 13, Anthropic 5, `karpathy.ai` 4, Situational Awareness 2, and Peter
Steinberger 1.

Every item should be chronologically sortable, but an evergreen homepage or
index should not acquire a fictitious `published_at`. Publication, update,
migration, source-build, and first-observed dates are different archival claims.

## Evidence order

Prefer explicit first-party visible/structured publication metadata, then a
first-party launch announcement, changelog/feed/index, explicit source front
matter, corroborated deployment history, contemporary independent evidence,
and finally the earliest reliable Wayback observation. Sitemap `lastmod`, HTTP
`Last-Modified`, filesystem mtimes, and Git commits are supporting evidence
unless the source's deployment model proves they correspond to publication.

An earliest Wayback snapshot establishes that a resource existed publicly by
that time. Store it as `first_observed_at` or an upper bound; do not silently
present the crawl timestamp as an exact publication date.

## Required model

Retain nullable semantic fields (`published_at`, `updated_at`) with precision,
plus provenance-bearing assertions for migration, redesign, rename, redirect,
artifact build, source commit, and first observation. Every item may have a
derived `sort_at`, accompanied by `sort_basis` and publication status
(`exact`, `partial`, `inferred`, `unknown`, or `not_applicable`).

Partial dates remain partial. For example, “June 2024” is a month interval; a
deterministic internal sort key must not display as an invented June 1 date.

## Source-specific next work

- OpenAI: add template-specific visible/metadata extraction before using
  sitemap or archive fallbacks. Policies and system cards often distinguish
  original publication from later versions in visible text.
- AI 2027: use the 2025-04-03 launch date for proven launch-set resources and
  retain month precision where forecast pages say only April 2025.
- AI 2040: use the 2026-07-09 public release, map later route additions through
  its changelog, and keep the 2026-04-20 site rewrite as a migration event.
- Anthropic: extract visible News/Research datelines and separate inline update
  notices.
- `karpathy.ai`: classify evergreen structural pages as not applicable and use
  first observation for sorting; inspect the slide PDF's cover/metadata.
- Situational Awareness: retain the displayed June 2024 month precision for the
  series and full PDF unless exact first-party evidence is found.
- Peter Steinberger: use the first-party repository's required `pubDatetime`
  and optional `modDatetime` front matter; structural pages remain distinct.
