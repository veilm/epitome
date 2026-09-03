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
