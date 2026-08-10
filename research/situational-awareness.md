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
