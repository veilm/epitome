# Paul Graham

## Reviewed essay scope

The rendered `https://paulgraham.com/articles.html` index was inspected through
Chromium/CDP on 2026-08-10. It currently exposes 238 links: 233 distinct
`paulgraham.com` URLs and two text chapters hosted on the site's historical
Turbify CDN. Three essay links are duplicated in the index.

The bounded page inventory in `sources/paul-graham-essays.txt` contains the
essay index itself plus its 231 distinct same-host essay links, preserving the
index's newest-to-oldest document order. The site homepage and `rss.html` are
structural pages and are excluded from this essay batch. The two *ANSI Common
Lisp* chapter text files are book excerpts rather than essays; keep them as a
separate dependency/future book scope instead of silently folding them into the
essay catalog.

The site is old-style static HTML, but much of its visual chrome and some essay
figures are served from `s.turbifycdn.com` and `sep.turbifycdn.com`. A pilot must
therefore verify CDN image capture and local replay before a larger batch.
YouTube and Twitter/X identities are not part of this scope; an essay whose
filename is `twitter.html` is ordinary first-party prose and does not authorize
crawling Twitter itself.

## Validation plan

1. Capture the essay index and verify its image-heavy table layout locally.
2. Capture varied new, old, and figure-bearing essays, including a page with
   footnotes and one Lisp-era page.
3. Require complete manifests, closed tabs, zero missing rendered images, and
   no production-origin requests during replay before starting a bounded page
   batch.

## Pilot results

The essay index completed at:

`/mnt2/capsule/epitome/paul-graham/validation/1786353509-index`

Four varied essays were then exercised across:

- `/mnt2/capsule/epitome/paul-graham/validation/1786353572-varied`
- `/mnt2/capsule/epitome/paul-graham/validation/1786353899-avg-retry`

The index and *How to Do Great Work*, *What I Worked On*, *The Roots of Lisp*,
and *Beating the Averages* all have complete page captures and closed tabs.
They retain 2,246–75,005 visible characters. Primary-image audits are clean.

Two early-web preservation cases required explicit handling:

- *Beating the Averages* remains stuck at `document.readyState=interactive`
  on the live site because the former Virtumundo host no longer serves four
  layout spacer GIFs. Capture now accepts a substantially parsed HTTP document
  after the bounded full-load timeout while still rejecting blank/loading
  documents. The dead spacer is reviewed as equivalent to the site's captured
  1x1 transparent GIF and resolves through that local alias.
- Paul Graham's pages use the deprecated HTML `background` attribute for the
  tiled page texture. Replay now localizes this fetch-bearing attribute in the
  same way as CSS backgrounds, preventing a quiet production-CDN request.

The corrected desktop replay has zero broken images and zero production-origin
requests across all five pages. *The Roots of Lisp* links to an unavailable
`www.ciul.ul.pt` PDF; the complete essay and its rendered figures are present,
but the outbound paper is a later dependency-recovery task rather than a reason
to reject the first-party page. The reviewed scope is ready for a small bounded
batch.

## First bounded batch

The first 15-page batch completed at:

`/mnt2/capsule/epitome/paul-graham/crawls/1786354191`

All 15 manifests are complete and tab-closed. The run recorded 151 requests and
717,296 response-body bytes with zero capture or asset failures. Primary and
all-rendered-image audits both report zero omissions. Desktop replay checks of
five varied pages retained 3,801–36,771 visible characters and 4–11 images per
page, with no broken images or production-origin requests. The visual layout
matches the intentionally narrow, image-chrome early-web source design.

Together with the pilot, 20/232 approved identities are complete. The public
catalog excludes the structural essay index and includes the other 19 pages.
Because this corpus usually provides publication dates only to the month, the
catalog stores and displays month precision explicitly (`YYYY-MM`) rather than
inventing a day. The revised *Beating the Averages* byline is correctly treated
as April 2001, not its April 2003 revision date.

## Second bounded batch

The next 30 deduplicated essays completed at:

`/mnt2/capsule/epitome/paul-graham/crawls/1786356129`

All 30 manifests are complete and tab-closed. The run retained 310 responses
and 1,345,732 response-body bytes with zero page or asset failures. Primary and
all-rendered-image audits report zero omissions. Five desktop replay checks
spanning illustrated, short, long, political, and technical essays retained
1,480–24,993 visible characters and 4–15 images, with no broken images or
production-origin requests. Coverage is now 50/232 approved identities; the
public catalog contains the 49 non-structural essays.

## Third bounded batch

The next 45 deduplicated essays completed at:

`/mnt2/capsule/epitome/paul-graham/crawls/1786358665`

All 45 manifests are complete and tab-closed. Primary-image audits report zero
omissions. The only eleven asset failures are repeated requests for the same
dead Virtumundo 1x1 layout spacer already reviewed in the pilot; the replay
alias substitutes the captured transparent GIF, so affected pages have zero
broken rendered images. Five desktop checks spanning short, long, illustrated,
and obsolete-layout variants retained their article text and source styling
with zero production-origin requests. Coverage is now 95/232 approved
identities.

## Fourth bounded batch

The next 60 deduplicated essays completed at:

`/mnt2/capsule/epitome/paul-graham/crawls/1786364735`

All 60 manifests are complete and tab-closed. The run retained 703 responses
and 3,197,147 response-body bytes with zero page failures. Primary-image audit
across all 155 completed identities reports no omissions. Twenty-three of the
28 raw asset misses are the already-reviewed dead Virtumundo spacer and replay
continues to substitute the captured transparent GIF.

The other five misses came from the retired `ycombinator.com/images` path: four
pages use the same 18x18 Hacker News comment badge, while *Two Years of Hacker
News* links its historical traffic chart. Exact 200-status Wayback bodies from
2007 and 2009 are preserved under the private Paul Graham dependency tree, and
reviewed aliases restore the original URLs only when no captured live body is
available. Five desktop replays spanning short, long, illustrated, obsolete-
layout, and restored-YC-asset variants retain their source styling and make no
production-origin requests. Coverage is now 155/232 approved identities, with
the next 60-page deduplicated input selected from the 77 remaining essays.

## Fifth bounded batch

The next 60 deduplicated essays completed at:

`/mnt2/capsule/epitome/paul-graham/crawls/1786472698-next-60`

All 60 manifests are complete and tab-closed with no page errors. The
primary-image audit is clean. Twenty-five all-image misses are the already
reviewed obsolete Virtumundo layout spacer and two are the retired Hacker News
badge; replay aliases cover those decorative assets. The other misses are dead
outbound Tipjoy and Boss Talks dependencies rather than article content.

Representative early, middle, and late replays retain 2,841–24,441 visible
characters in the source's narrow legacy layout, have no substantive broken
images, and make no production-origin requests. Coverage is now 215/232. The
final 17 uncaptured identities are prepared in `data/paul-graham-final-17.txt`.

## Final batch

The final 17 essays completed at:

`/mnt2/capsule/epitome/paul-graham/crawls/1786488163-final-17`

All manifests are complete and tab-closed with no page errors. Primary-image
audit is clean. Four all-image misses are the already-reviewed obsolete
Virtumundo spacer; two additional failures are unavailable outbound programming
papers and do not affect article content. Representative replays retain
25,000–32,000 visible characters, the original narrow legacy layout, no
substantive broken images, and no production-origin requests.

All 232 approved index-and-essay identities are now captured and offline-
verified. The unavailable outbound *Roots of Lisp* paper and deferred books,
RSS, and language-history material remain separate from this completed page
scope.
