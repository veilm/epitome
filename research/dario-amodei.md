# Dario Amodei source reconnaissance

Checked on 2026-08-04 through Chromium/CDP, primary publication pages, and
search-engine discovery. This is an inventory aid, not a claim that every page
mentioning Dario was written by or is an interview with him.

## The personal site is only a seed

`https://darioamodei.com/` currently lists five self-hosted writings:

- `https://darioamodei.com/essay/the-adolescence-of-technology`
- `https://darioamodei.com/essay/machines-of-loving-grace`
- `https://darioamodei.com/post/policy-on-the-ai-exponential`
- `https://darioamodei.com/post/the-urgency-of-interpretability`
- `https://darioamodei.com/post/on-deepseek-and-export-controls`

The site's `sitemap.xml` contains those same five content pages and no hidden
essay archive. The `Archive` navigation link currently returns 404. A long
essay is cleanly contained by `article`, with its title, subtitle, visible date,
main body, acknowledgements, and footnotes; it should work with the generic
capture and extraction pipeline.

The homepage also links two 2025 op-eds and nine interviews. That interview
list is demonstrably stale: it includes the August 2023 Dwarkesh conversation,
but not the February 2026 follow-up.

## Obvious writing gaps

The personal homepage omits at least this primary-source testimony:

- `https://www.judiciary.senate.gov/imo/media/doc/2023-07-26_-_testimony_-_amodei.pdf`
  — written testimony before the Senate Judiciary Subcommittee on Privacy,
  Technology, and the Law, 2023-07-25.

It also does not serve as an index of Dario-attributed Anthropic statements and
prepared remarks. First-party examples include:

- `https://www.anthropic.com/news/statement-dario-amodei-american-ai-leadership`
- `https://www.anthropic.com/news/statement-department-of-war`
- `https://www.anthropic.com/news/where-stand-department-war`
- `https://www.anthropic.com/news/paris-ai-summit`
- `https://www.anthropic.com/news/uk-ai-safety-summit`

These should be discovered from actual title/byline metadata and newsroom
search, not from body-text mentions of Dario. They belong in both the Anthropic
company archive and a derived Dario-author inventory.

## Interview gap audit

The personal homepage lists nine interviews. The independent
`https://dariosaid.ai/interviews` index lists 13 substantive interviews and was
last updated 2026-06-22. Comparing them produces eight clear additions absent
from Dario's homepage:

- Hard Fork, February 2025 — `https://www.youtube.com/watch?v=YhGUSIvsn_Y`
- Council on Foreign Relations, March 2025 —
  `https://www.youtube.com/watch?v=esCSpbDPJik`
- Logan Bartlett, October 2023 —
  `https://www.youtube.com/watch?v=gAaCqj6j5sQ`
- Dwarkesh Patel follow-up, February 2026 —
  `https://www.dwarkesh.com/p/dario-amodei-2`
- Wall Street Journal at Davos, January 2026 —
  `https://www.youtube.com/watch?v=K7F6ohcBJus`
- Nikhil Kamath, February 2026 —
  `https://www.youtube.com/watch?v=68ylaeBbdsg`
- Databricks with Ali Ghodsi, March 2026 —
  `https://www.youtube.com/watch?v=MTsoRWPS46o`
- Bloomberg *The Circuit*, June 2026 —
  `https://www.youtube.com/watch?v=x2VHFgyawPE`

Conversely, the personal homepage has four interviews that this independent
index omits: Zanny Minton Beddoes, Econ 102 with Noah Smith, TIME, and Ezra
Klein. The union is therefore at least 17 interviews, and neither index should
be treated as exhaustive.

Search also found substantive candidates absent from both lists, including the
May 2025 Axios interview about white-collar jobs, the September 2025 Axios AI+
appearance, and CBS's full February 2026 Pentagon interview transcript. These
need a reviewed inventory rather than an unbounded search crawl:

- `https://www.axios.com/2025/05/28/ai-jobs-white-collar-unemployment-anthropic`
- `https://www.axios.com/2025/09/17/anthropic-amodei-ai`
- `https://www.cbsnews.com/news/anthropic-ceo-dario-amodei-full-transcript/`

## Discovery and capture plan

1. Use the personal sitemap as the canonical five-page self-hosted inventory.
2. Preserve all outbound items on the personal homepage, including op-eds and
   the four interviews absent from the independent index.
3. Use independent indices only for discovery, then retain the primary video,
   transcript, publication page, and metadata as the archival source.
4. Generate Dario-attributed Anthropic candidates from title/byline metadata and
   manually review them before capture.
5. Keep an incremental interview ledger because the personal site's listing is
   not maintained promptly. Preserve video, audio, captions/transcripts,
   thumbnail, description, chapters, and the publisher's surrounding page.

No Dario crawl was started during this reconnaissance.
