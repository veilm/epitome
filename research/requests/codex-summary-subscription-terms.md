# Research request: Codex subscription use for Epitome article summaries

## Context

Epitome is a personal archival project. It captures public articles, extracts a
compact model-readable Markdown rendition, and can ask a locally installed
Codex CLI to create a neutral Markdown summary. The summaries may eventually be
published on a small static website, while the full archives remain private.

The current summarizer is a local, sequential, human-controlled workflow—not a
public API, multi-user service, resale product, or background fleet. For each
article it:

1. creates a fresh temporary directory;
2. copies one extracted article to `input.md`;
3. invokes `codex exec` with an ephemeral session, ignored user configuration
   and rules, a workspace-write sandbox, no approvals, a named Codex model, and
   medium reasoning;
4. prompts Codex to read only `input.md`, assess whether it is complete enough,
   and write `output.md` with validated front matter plus a prose summary;
5. validates the output programmatically and stores the Markdown summary and a
   small catalog entry.

The task's primary semantic operation is summarization, not software
development. However, it intentionally uses the Codex agent harness for isolated
filesystem input/output, status assessment, validation-friendly output, and
fail-closed handling. It could be redesigned as one Responses API or Chat
Completions request whose application code supplies the article and writes the
result, but that is not the current implementation.

Codex is authenticated through the user's paid ChatGPT subscription rather than
an OpenAI Platform API key. The intended future volume may be hundreds of
articles, run sequentially and with explicit user initiation. We want to know
whether this is permitted or whether OpenAI expects usage-based API billing.

Relevant current public documentation already observed:

- The Codex manual's non-interactive-mode page explicitly presents `codex exec`
  as a scripting/pipeline interface and gives examples including summaries,
  piped data, and writing output files.
- The authentication page says Codex CLI supports both ChatGPT subscription
  access and API-key usage-based access.
- The same page recommends API-key authentication for programmatic Codex CLI
  workflows such as CI/CD, while also documenting ChatGPT-managed Codex auth for
  trusted automation in some contexts.

## Questions

Research current, official OpenAI sources and give a careful answer to these:

1. Does running the described local `codex exec` summarization workflow under a
   paid ChatGPT/Codex subscription violate any binding OpenAI Terms of Use,
   Service Terms, Codex-specific terms, usage policies, plan restrictions, or
   anti-abuse rules?
2. Is API-key authentication merely a security/billing recommendation for
   programmatic automation, or is it mandatory for this use case? Clearly
   distinguish binding requirements from documentation recommendations and
   examples.
3. Do task category (summarization versus coding), filesystem reads/writes, use
   of the Codex harness, sequential batch size, eventual publication of derived
   summaries, or personal/noncommercial status materially change the answer?
4. Where is the likely boundary between ordinary subscribed Codex use and an
   API/service workload that should use the OpenAI Platform—for example:
   unattended schedules, high throughput, multiple users, a public endpoint,
   resale, account sharing, credential forwarding, or attempts to evade limits?
5. Does the answer differ across ChatGPT Plus/Pro, Business, Enterprise, or Edu?
   If plan-specific contract documents are required, say exactly what cannot be
   concluded from public terms.
6. What is the lowest-risk practical recommendation for Epitome now? Consider
   staying with local subscribed Codex for small user-initiated batches,
   migrating bulk summaries to API-key-authenticated Codex, or replacing Codex
   with a direct Responses API implementation.

## Research requirements

- Prioritize primary, current official OpenAI sources and link directly to each
  relevant provision.
- Quote only short decisive phrases and otherwise paraphrase.
- Record page titles and effective/update dates where available.
- Do not infer that a recommendation is a contractual prohibition.
- Explicitly flag ambiguity and avoid presenting legal advice as certainty.
- If official documents conflict or distinguish consumer and business plans,
  explain the hierarchy and scope.

