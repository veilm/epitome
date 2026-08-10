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
