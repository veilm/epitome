# alien.v01d.zone

## Public validation and N+1 pilot

The canonical first-party site is `https://alien.v01d.zone/`. Its public home
rendered as `How to Befriend an Alien Mind` with approximately 220,166 visible
body characters, 15 images, 149 links, and no iframe, video, or audio element.
The same-origin links are fragment anchors within this single long-form page;
the only observed outbound profile link is an excluded X URL. The page uses
first-party image assets, public Google Fonts, and PostHog telemetry. No login,
paywall, or access-control bypass is in scope.

The bounded N+1 pilot is prepared in ignored `data/alien-v01d-pilot.txt` as a
one-route capture because the site's canonical material is one long page rather
than a multi-route archive. It uses the standard public settings: CDP port 2103
only, 15-second settle, 120-second page limit, 400-asset limit, two-second
asset pacing, 90-second asset timeout, and 30 seconds between pages. The exact
YouTube/Twitter/X asset exclusions remain in force. At the boundary, require
the long-form text, all 15 image references, static/telemetry classification,
no live-origin fallback in replay, and no prohibited-host result URL.

## Pilot result

The one-route pilot completed at
`/mnt2/capsule/epitome/alien-v01d-zone/crawls/1788451389-pilot`. Its manifest
is complete and tab-closed; `finish` reports `failures=0`. The capture recorded
281 requests and 281 response bodies, all HTTP 200, with zero response-body
errors and 5,654,852 response bytes. The captured hosts were the first-party
site, Google Fonts, and PostHog telemetry; the telemetry and redacted-header
records are classified as non-content platform requests.

The page discovered 279 asset references: 249 were attempted in the bounded
asset pass and all 249 completed, with 30 already-complete references reused.
There were zero asset failures and zero exclusion decisions. The interactive
media ledger reports zero discovered, embedded, activated, or result-level
media. No YouTube or Twitter/X downloader was invoked, no excluded-host result
URL appears in the asset or media ledgers, and the public-only boundary was
preserved.

Both primary-image and all-rendered-image audits report one page with zero
missing images, repairs, or repair failures. Local-only replay covered the
full long-form document and its early `#chapter-1` and late `#chapter-9`
fragment views. Each view retained approximately 220,166 visible characters
and all 15 images with zero broken images, frames, video, or audio. The replay
loaded 26 local resource entries and made zero production-origin requests.

The bounded Alien pilot is complete; the active lane advances to the prepared
seven-route near.blog pilot.
