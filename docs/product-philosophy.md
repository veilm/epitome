# Product philosophy and reading experience

Recorded 2026-09-09, with the user's digest idea added 2026-09-10. This document
gives future contributors the purpose behind the product. “User's stated
intent” and “User's additional idea: daily and weekly posts” record the user's
thinking. All subsequent sections are assistant proposals, not accepted
decisions or descriptions of implemented behavior. The user has not yet
reviewed those proposals; the digest addition does not imply their acceptance.
See [summaries.md](summaries.md) for the existing implementation.

## User's stated intent

Epitome has two purposes: preserve historically valuable material, and help
people stay informed efficiently. The reader product is intended to be fully
free for now. Preservation can be comprehensive even when the reading surface
is selective.

Being informed includes news, but also understanding mechanisms, arguments,
and changing conditions. A model release is relevant; so are discussions of
GPU economics, compute growth, infrastructure bottlenecks, lab expenditure,
and revenue. The desired result is a useful picture of the world across
sources, rather than familiarity with a stream of announcements.

Current habits scatter attention across websites, Twitter, and YouTube. These
services can turn a brief attempt to catch up into prolonged consumption.
Epitome should minimize the time needed to obtain useful information and make
it easy to stop. Time spent, scrolling, and compulsive return visits are not
success measures in themselves.

The user values active thinking as well as efficient consumption. Thinking
through a problem before seeing an author's answer may help the reader build
a mental model into which that answer fits. The product should support that
experience. The strength and generality of any psychological or learning
benefit remain hypotheses here; this document does not establish research
claims about them.

The user proposed several complementary representations of each resource:

- A short summary of what it actually says, including its conclusions.
- A short description of its topic, without necessarily revealing conclusions.
- Questions that help the reader think about its subject before reading it.
- A longer, potentially structured summary on an Epitome detail page.

Feed length and format are open design choices. Settings could let readers
choose a representation while using the same precomputed content. Longer
summaries could expand with the amount of substantive material and use Markdown.
Original sources should remain directly accessible.

Importance and novelty may help prioritize reading. The user's contrast is
between a major geopolitical development and a narrow promotional claim with
little wider consequence. A separate LLM memory project could eventually help
recognize repeated ideas, connect new claims to earlier material, and assess
what has actually changed without placing the whole archive in context.

The user is open to consulting Claude later about prompt wording and writing
quality. Model choice and final wording are undecided; this conversation does
not authorize or require an external consultation.

## User's additional idea: daily and weekly posts

Epitome could publish its own daily and weekly summaries as entries in the
same feed as externally sourced posts. “Epitome Digest” is a working name,
not a naming decision. These entries would identify Epitome as their source
and use its animated logo, just as external entries use their source or
organization's logo. The Epitome logo should also animate within the feed.
Each digest would open as an Epitome post.

The daily post would summarize the most important developments across the
inputs for the preceding day: for example, GPU developments, a model release,
and other noteworthy announcements or ideas. The weekly post would cover the
preceding week. This is a synthesis of the period's useful information, with
the precise article structure and generation design still to be determined.

The intended canonical timezone is San Francisco local time. Express this as
`America/Los_Angeles` so it follows Pacific standard/daylight time, rather than
fixed PST throughout the year. The proposed generation boundaries are:

- Daily: midnight local time, covering the day that just ended.
- Weekly: Monday at midnight local time, covering the Monday-through-Sunday
  week that just ended.

The user envisages scheduled generation; no scheduling is implemented or
authorized by this design note. Exact publication timing, handling of inputs
that arrive late, and any processing delay after the boundary remain open.

Generation could reuse existing work. A daily-writing agent would have access
to Epitome's individual article summaries and could consult them without
necessarily rereading every original. A weekly-writing agent would similarly
have access to that week's daily digests. Access to underlying material would
remain possible when useful. This hierarchy could connect to the separate
LLM memory architecture; the precise integration is undecided.

Digest entries could receive the same eventual “worth reading” indicator as
other feed entries. The scoring method remains open. A quiet day with only a
minor announcement might produce a very short, low-value digest; length and
rating should reflect the actual material. When there are no articles to
summarize, the user proposes skipping the digest entirely. Do not invent
content or pad a quiet period merely to publish on schedule.

This addition records an idea the user wanted to preserve before reviewing
the assistant's earlier proposals. It does not settle the overall feed design,
ranking scheme, summary formats, or any of the recommendations below.

## Proposed default experience

Provide a finite catch-up view for selected sources or topics, bounded by a
visible time window. Each entry gives the source, publication date, title, and
one or two sentences stating the substantive takeaway. Start by testing roughly
35–65 words, with shorter entries where sufficient. Treat this as a budget,
not a quota: never pad a simple announcement or omit a decisive qualification
to equalize card heights.

An entry offers both an Epitome detail view and the original. Finish each
catch-up batch with an explicit endpoint. Late arrivals belong to the next
refresh, rather than continually moving that endpoint. Older material remains
available through deliberate browsing. Archived historical material newly
ingested today must not masquerade as today's news.

The default detail view presents the longer summary immediately and offers
an optional “Think first” section. A reader choosing that section sees useful
questions before revealing the summary. No answer entry, quiz completion,
timer, streak, or other obligation is required to continue.

Offer a small number of understandable settings:

| Setting | Proposed default | Alternatives |
| --- | --- | --- |
| Feed text | Takeaway | Topic; question |
| Detail opening | Summary visible | Think first, summary initially hidden |
| Source/topic selection | Explicit reader selection | Editable at any time |

A “Think first” preset should coordinate feed and detail behavior: a takeaway
already seen in the feed can spoil the question on the detail page. Original
titles can also reveal conclusions. Retain the original title in the record,
but use a faithful neutral topic heading in this preset when necessary, with
the original title available on demand. Do not promise complete spoiler
avoidance when the reader has seen the story elsewhere.

Do not begin with arbitrary lengths, model selectors, and a large matrix of
preferences. Add controls when observed reading behavior justifies them.

## What the representations should accomplish

A takeaway conveys the result and whatever mechanism or qualification is
necessary to interpret it. A topic description identifies the substantive
problem and scope. Neither should be promotional or a curiosity hook.

For example, for a hypothetical proof announcement:

- Takeaway: “The team reports a proof of X under assumption Y; independent
  verification is still pending.”
- Topic: “Whether X follows from Y, and how a proposed proof is checked.”
- Question: “Where could an argument from Y to X fail, and what would checking
  the proof need to establish?”

These examples illustrate formats, not a claim about an actual publication.
Questions for a real theorem must respect the reader's prerequisites; asking
someone to solve a frontier problem with no setup is not useful preparation.

There are two different question functions:

- **Before reading:** activate relevant reasoning, expose a tradeoff, or invite
  a prediction without supplying the author's solution. Provide enough setup
  to make an attempt possible. Usually one or two worthwhile questions suffice.
- **After reading:** test whether the reader can explain the mechanism,
  evidence, or limitation. These may refer explicitly to the author's answer.
  Keep them optional and separate from preparatory questions.

For an article introducing futarchy, a possible preparatory question is:
“How could a government separate disagreement about desired outcomes from
disagreement about which policies would produce them?” A comprehension
question could instead ask how the proposed system performs that separation
and what assumptions it needs. The actual article must support any answer
provided; these are illustrative prompts, not universal questions for the topic.

Do not force questions onto routine factual updates. A feature rollout may
need a sentence and no reflective exercise. Do not invent an open problem
simply to fill a field. An empty question list can be the correct output.

## Longer summaries

Length should follow distinct substantive content and explanatory difficulty,
with source length as a secondary signal. A repetitive two-hour conversation
may deserve less space than a dense short essay. Start with a short overview,
then use sections or bullets where they make relationships easier to follow.

Preserve what changes the reader's understanding: central claims, mechanisms,
supporting evidence, consequential quantities and comparisons, uncertainty,
and limitations. Preserve attribution and disagreement in interviews rather
than turning multiple speakers into one authoritative narrator. Distinguish
reported results, conjectures, proposals, and established background.

An announcement, argument, interview, tutorial, and empirical report need
different structures. Use flexible Markdown with a shared editorial standard,
rather than mandatory headings that produce empty or repetitive sections.
Show what the original offers beyond the summary when material: derivations,
worked examples, methodological detail, visual evidence, or literary experience.

Incomplete transcripts, paywalled excerpts, missing figures, and inaccessible
attachments constrain the output. Label those limits and summarize only the
available material; never imply that a preview represents the whole work.

## Importance, novelty, and reader relevance

Avoid starting with one model-generated “importance” number. Several judgments
need different evidence and should remain distinguishable:

| Judgment | What it means | Evidence needed |
| --- | --- | --- |
| Consequence | How much this could matter if accurate | Scope, magnitude, affected people or decisions |
| Support | How well the particular claim is substantiated | Source evidence, attribution, corroboration where available |
| Novelty | What this adds to prior coverage | Retrieved earlier claims and event history |
| Reader relevance | Whether it serves this reader's interests | Explicit topic choices initially |
| Explanatory value | Whether it improves understanding | Mechanism, synthesis, counterexamples, useful framing |

These dimensions guide curation; they are not all facts a model can reliably
score from one article. A consequential allegation with weak support should
not be displayed as confirmed news. A familiar concept can be worth featuring
when the explanation is unusually useful or the reader is new to it.

“High entropy” is interpreted here as useful information gain for the reader.
Surprise alone can reward rumors and sensationalism. Likewise, low novelty
does not establish low value, and repetition across sources does not establish
independent corroboration.

Start with coarse, explainable judgments and chronological order within a
chosen scope. Test consequential-item prioritization against human examples
before making it the default. Show brief reasons where ranking affects
visibility, and retain access to all entries. A narrow environmental claim
could be minor in one context and significant evidence of an energy bottleneck
in another; do not permanently rank by topic labels or dramatic language.

The eventual reading unit may be a development or question spanning multiple
articles. Group reports about the same event and surface the substantive delta;
retain individual resources and source links underneath. Corrections,
contradictions, and genuinely new evidence must survive deduplication.

## Generation workflow and stored content

Keep source-bound reading content separate from contextual editorial judgments.
Both are needed, but they change on different schedules.

1. Preserve the resource and establish an identified extraction with coverage
   metadata: full text, excerpt, transcript limitations, missing evidence.
2. Identify claims, mechanisms, qualifications, and supporting source locations.
   Generate the takeaway, topic description, suitable questions, and longer
   summary from that shared understanding. One response can supply the bundle;
   separate model calls are not inherently required.
3. Check source fidelity and consistency across representations. Validate the
   data shape mechanically; review whether compression changed the claims,
   erased uncertainty, or made questions impossible or revealing.
4. Retrieve related prior material to assess duplication, novelty, disagreement,
   and context. Store these judgments with their comparison set and assessment
   time, independently of the source-bound summary.
5. Publish the selected representations in a finite reading batch. Preferences
   choose stored content without triggering generation on every view.

Store a small structured manifest referring to Markdown files for the takeaway,
topic, and longer summary, plus structured question entries with stable IDs,
purpose, and any answer/source references. The feed question can reference a
preparatory question from the bundle instead of independently paraphrasing it.
This extends the existing convention that Markdown content stays out of JSON.
The final schema remains to be designed.

Record source/capture identity, extraction hash and coverage, model, prompt
version, and generation time. Preserve older versions when sources or summaries
change. Source links or section/timestamp references should let a reviewer
verify important statements without rereading the whole resource.

Do not equate the current pipeline's status confidence with factual reliability
or editorial quality. Existing structural validation cannot establish those.
Source text remains untrusted input, including for any future memory writer.

## Memory as an incremental capability

Begin with retrieval over past resources and compact, attributable claim
records. For each new resource, retrieve candidate predecessors and compare
their actual content. Useful relationships include “repeats,” “extends,”
“contradicts,” “corrects,” and “supplies evidence for.” Similar topic or wording
alone does not prove duplication.

A richer memory system can later maintain concept and event summaries pointing
back to those records. Keep dates, uncertainty, disagreement, and provenance;
do not repeatedly compress summaries until the evidence disappears. Retrieval
failure means novelty is unknown, not that the claim is new.

Keep corpus memory separate from reader history. An idea's prior appearance in
the archive does not mean a particular reader understands it; opening a page
does not prove learning either. Initially use explicit preferences rather than
an inferred psychological profile. The first useful product should not depend
on solving general LLM long-term memory.

## How to decide what works

Before scaling generation, assemble roughly 12–20 diverse archived examples:
an ordinary update, a major development, a dense argument, a long repetitive
interview, a tutorial, conflicting accounts, duplicate reporting, and a partial
or paywalled extraction. Compare candidate prompts and models on the same inputs.
Claude consultation can help refine wording, but judge actual outputs.

Review whether a reader can state the key claim, explain the mechanism when
applicable, retain the decisive qualification, and decide whether the original
is worth opening. Examine specific omissions and distortions rather than only
asking whether a summary “sounds good.” Evaluate fidelity against the source,
including whether a question has enough setup and whether its answer is supported.

Compare takeaway-first and think-first reading on comprehension, delayed recall
if practical, time spent, effort, and willingness to finish. Treat benefits of
preparatory questions as something to test, not a reason to impose homework.
Success includes a reader confidently stopping after a short useful session.

Suggested sequence: calibrate the content bundle on examples; implement inline
takeaways and optional think-first details; establish finite catch-up sessions;
then add cross-source grouping and contextual ranking. Keep initial prompt
wording, exact lengths, scoring weights, and the memory backend open until
examples reveal what they need to do.
