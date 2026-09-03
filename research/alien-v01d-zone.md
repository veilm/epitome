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
