# Situational Awareness source reconnaissance

Investigated through Chromium on CDP port 2103 at Unix timestamp `1786349229`.
No YouTube or Twitter/X content was opened or downloaded.

## Approved page scope

The rendered navigation at `https://situational-awareness.ai/` exposes the
introduction, eight numbered essay installments, Leopold Aschenbrenner's about
page, and the first-party full-series PDF. These eleven canonical identities are
tracked in `sources/situational-awareness.txt`. Fragment links and the external
Dwarkesh interview do not expand this bounded source.

The introduction is a 6,204-character overview with the complete series table
of contents. A representative long installment, *From GPT-4 to AGI*, retains
62,607 visible characters and 27 image elements. Neither inspected page contains
video, audio, or iframe elements.

## Preservation risk and pilot plan

The live representative essay currently leaves twenty of its twenty-seven
figures broken. Its WordPress markup retains original filenames, dimensions,
responsive variants, attachment IDs, and attachment permalinks, but both several
responsive variants and some original URLs fail to load in the rendered browser.
This is an upstream defect, not a local replay failure.

Capture the introduction as a small structural pilot, then capture *From GPT-4
to AGI* with generous asset completion before approving the remaining batch.
Classify which original-size images remain available and recover confirmed
missing figures from exact historical copies where practical. The first-party
PDF is especially important as a second representation of the full essay and
its figures; require the actual PDF body rather than a viewer shell.

## Validated pilots

The introduction pilot completed at:

`/mnt2/capsule/epitome/situational-awareness/validation/1786349398-home`

Its manifest is complete, the capture tab closed, and both image audits report
zero omissions. Asset completion recovered all seven missing references,
including the actual 21,371,840-byte full-series PDF. The document identifies as
a valid PDF 1.5 file with 165 pages.

The representative long-essay pilot completed at:

`/mnt2/capsule/epitome/situational-awareness/validation/1786349432-from-gpt-4-to-agi`

Its manifest is complete and the capture tab closed. The run retained 205
response bodies totaling 92,920,405 bytes. Asset completion attempted and
recovered all 181 discovered missing references with two-second spacing and zero
failures. Primary and all-rendered-image audits are both zero: the offline page
loads all 27 figures at natural size even though twenty were broken in the live
rendered page during reconnaissance.

A 1440x900 replay audit found exact introduction text metrics and 62,619 visible
characters in the long essay, with its complete figure-rich layout. The PDF
renders locally with all 165 pages. A strict network log recorded 81 requests to
the local replay server plus Chromium's internal PDF-viewer stylesheet and no
production-origin request. Audit tabs were closed afterward.

The two pilots establish a viable figure strategy: retain every responsive and
original WordPress asset discovered from the page markup rather than accepting
the live browser's selected broken variants. The remaining nine identities are
ready for one bounded batch with generous inter-page and per-asset delays.

## Completed bounded scope

The final nine identities completed with 45-second inter-page spacing and
two-second asset spacing at:

`/mnt2/capsule/epitome/situational-awareness/crawls/1786350214`

All nine manifests are complete, every capture tab closed, and the run reported
zero page failures. Across the increment it retained 306 network requests and
284,745,503 response-body bytes. Asset completion attempted 165 references and
recovered 163. The two misses were not rendered figures: they were a Deloitte
report whose live URL now returns 404 and a RAND report whose live URL returns
403. Repeated primary and all-rendered-image audits across all eleven approved
pages report zero omissions.

Exact Wayback PDF copies were found and retained at:

- `/mnt2/capsule/epitome/situational-awareness/dependencies/wayback-deloitte-green-energy-1786353070`
- `/mnt2/capsule/epitome/situational-awareness/dependencies/wayback-rand-rr1751-1786353071`

They are valid 27-page and PDF 1.3 documents. Reviewed resource aliases make the
two original citation URLs serve these historical bodies locally, eliminating
the substantive dependency gaps without changing the raw failed responses.

A final 1440x900 audit covered all seven remaining essay installments and the
author page. The essays retain 8,133–44,704 visible characters, all rendered
figures load at natural size, and the author page preserves its portrait and
text. A strict log recorded 93 requests, all to the local replay server. Both
recovered citation URLs return local PDF bodies, and audit tabs were closed.

Completed-URL selection now reports all eleven approved identities archived and
none remaining. The bounded *Situational Awareness* page scope is complete. No
YouTube or Twitter/X content was opened or downloaded.
