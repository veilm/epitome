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

## Five-route public pilot validation

The bounded pilot completed on 2026-09-03 at
`/mnt2/capsule/epitome/import-ai/crawls/1788455496-pilot`. All five manifests
are complete and tab-closed; the terminal `finish` record reports
`failures=0`. The capture recorded 1,048 requests, 1,023 response bodies,
41,361,855 response bytes, and two response-body errors. Statuses were 1,029
HTTP 200 responses, twelve HTTP 204 telemetry records, two HTTP 302 Cloudflare
challenge-script responses whose bodies could not be retrieved after headers,
and five HTTP 401 public reporting-endpoint responses. The 401s are
`/api/v1/reporting/flows` attempts and are not paywall access; no account or
access-control bypass was attempted.

Asset completion discovered 900 references and attempted 315 after 585 were
already complete; all 315 attempted assets completed, with zero failures and
zero exclusions, totaling 2,227,607 downloaded bytes. The attempted result
URLs are all on `substackcdn.com`. The five interactive-media ledgers contain
zero discovered, embedded, activated, or result-level media. Exact checks
found zero result URLs on the prohibited YouTube/Twitter/X hosts.

Both primary-image and all-rendered-image audits report five pages, zero
missing images, zero repair attempts, and zero repair failures. Local-only
loopback replays covered the home, archive, about page, and both public article
previews. They retained 310–27,561 visible characters and 5–26 rendered
images; all images decoded, the Substack attribution/platform frames were
rewritten to loopback, and no replay contained video or audio. A CDP network
logger recorded 156 requests, all to `127.0.0.1:8035` (149 HTTP 200 and seven
pending body records), with zero production-origin requests. The article
replays therefore preserve the available public preview only; the paywall
boundary remains intact.
