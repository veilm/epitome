# Import AI by Jack Clark

## Public validation and N+1 pilot

The first-party newsletter is `https://importai.substack.com/`. Its public
Substack home rendered the Import AI description and subscription boundary in
approximately 310 visible characters. A representative public article,
`/p/import-ai-471-why-hugging-face-worries`, rendered a substantive preview in
approximately 16,895 visible characters with 15 image elements, one platform
frame, and no video or audio. The home and article include Substack CDN assets,
subscription/telemetry frames, and some optional broken preview images; these
are boundary-classification items rather than permission to cross the paywall.

The prepared bounded pilot is in ignored `data/import-ai-pilot.txt`. It covers
the public home, archive and about routes, and two public article previews. It
uses the standard public settings: CDP port 2103 only, 15-second settle,
120-second page limit, 400-asset limit, two-second asset pacing, 90-second
asset timeout, and 30 seconds between pages. The exact YouTube/Twitter/X asset
exclusions remain in force. At the pilot boundary, require public-preview
classification, substantive available text, image/optional-missing-image and
platform-frame classification, no live-origin fallback in replay, and no
account or paywall bypass.
