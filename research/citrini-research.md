# Citrini Research article

## Public validation and N+1 pilot

The canonical first-party page is
`https://www.citriniresearch.com/p/2028gic`. It rendered as
`THE 2028 GLOBAL INTELLIGENCE CRISIS` in a real browser and exposed
approximately 48,761 visible body characters, the article headings, 26 images,
and the ordinary public Substack subscribe/sign-in frame. No tracking
parameters were used. The page was inspected without logging in, bypassing a
paywall, or using a media downloader; the public preview boundary remains in
force.

The one-page pilot is prepared in ignored
`data/citrini-research-pilot.txt`. It uses the standard public settings: CDP
port 2103 only, 15-second settle, 120-second page limit, 400-asset limit,
two-second asset pacing, 90-second asset timeout, and 30 seconds between pages.
The exact YouTube/Twitter/X asset exclusions remain in force. At its boundary,
require complete tab-closed manifests, dependency/media and exclusion
classification, both image audits, and local-only replay of the article and
image path.

The next low-risk scope is prepared while this pilot runs: a seven-route
Cyborgism Wiki pilot covering the public home, representative hypha, glossary,
categories, profiles, all-hyphae list, and bibliography routes. Login and
random routes remain out of scope.

## Pilot result

The pilot completed at
`/mnt2/capsule/epitome/citrini-research/crawls/1788440179-article-pilot`.
The one manifest is complete and tab-closed; `finish` reports `failures=0`.
The capture recorded 368 requests, 361 response bodies, 20,773,519 response
bytes, and zero response-body errors. Statuses were 362×200, 5×204, and one
401 from the site's reporting API; it did not affect the public article.
The saved page contains one substantive article element and 48,761 visible
body characters.

The capture discovered 341 asset references and attempted and completed 215;
there were zero asset failures and zero exclusion decisions. The interactive
media ledger reports zero discovered, embedded, activated, or result-level
media. No YouTube or Twitter/X downloader was invoked, and no excluded-host
URL appears in an asset or media result. Both primary-image and all-rendered-
image audits report zero missing images, repairs, or repair failures.

A local replay preserved the article title and headings, 48,761 visible
characters, 26 complete images, 19 content images, and one article element.
Its 57 logged requests were loopback-only: 52 local 200s, two local optional-
resource 404s, and three terminal pending body reads for local Spectral-font
resources when the logger stopped. There were no production-origin requests;
the optional local observations did not affect substantive text or images.

The one-page pilot is complete and the next prepared low-risk scope is the
seven-route public Cyborgism Wiki pilot in
`data/cyborgism-wiki-pilot.txt`.
