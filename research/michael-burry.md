# Michael Burry article

## Public validation and bounded pilot

The canonical first-party page is
`https://post.substack.com/p/the-ai-revolution-is-here-will-the`. It rendered
as `The AI revolution is here. Will the economy survive the transition?` in a
real browser and exposed approximately 41,717 visible body characters, the
article headings, 35 images, and the ordinary public Substack subscribe/sign-in
frame. The page was inspected without logging in, bypassing a paywall, or
using any media downloader; the public preview boundary remains in force.

The one-page pilot is prepared in ignored
`data/michael-burry-article-pilot.txt` and runs with the standard public
settings: CDP port 2103 only, 15-second settle, 120-second page limit,
400-asset limit, two-second asset pacing, 90-second asset timeout, and
30-second inter-page delay. The exact YouTube/Twitter/X asset exclusions remain
in force. At the pilot boundary, require complete tab-closed manifests,
dependency/media and exclusion classification, both image audits, and local
loopback replay of the article and its image/media path before moving on.

## Pilot result

The pilot completed at
`/mnt2/capsule/epitome/michael-burry/crawls/1788438718-article-pilot`.
The one manifest is complete and tab-closed; `finish` reports `failures=0`.
The capture recorded 431 requests, 427 response bodies, 15,170,056 response
bytes, and zero response-body errors. Statuses were 428×200, 2×204, and one
401 from Substack's reporting API; the reporting response did not affect the
public article. The page contains one substantive article element and 41,717
visible body characters.

The capture discovered 398 asset references and attempted and completed 270;
there were zero asset failures and zero exclusion decisions. The interactive
media ledger reports zero discovered, embedded, activated, or result-level
media. No YouTube or Twitter/X downloader was invoked, and no excluded-host
URL appears in an asset or media result. Both primary-image and all-rendered-
image audits report zero missing images, repairs, or repair failures.

A patched local replay preserved the article title and headings, 41,717 visible
characters, 35 images (all complete), and one article element. Its 62 logged
requests were loopback-only: 60 local 200s and two terminal pending body reads
for local Google-font resources when the logger stopped. There were no
production-origin requests; the pending font observations did not affect
article or image content.

The one-page pilot is complete and the next prepared low-risk pilot is the
public Citrini Research page at `https://www.citriniresearch.com/p/2028gic`.
