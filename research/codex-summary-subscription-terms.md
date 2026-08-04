# Codex subscription use for article summaries

Research checked 2026-08-04. This is a practical terms review, not legal advice
or a guarantee about enforcement. The detailed question submitted for external
research is in `requests/codex-summary-subscription-terms.md`.

## Conclusion

OpenAI's public documentation does not say that Codex is restricted to coding,
that summarization is forbidden, or that every scripted `codex exec` invocation
must use API billing. In fact, the documented non-interactive interface is
expressly intended for scripts and pipelines, and its examples include producing
summaries and writing machine-readable output.

For an occasional, sequential, user-initiated run on the subscriber's trusted
local workstation, using the subscriber's own Codex access is reasonably
defensible. It should stay within ordinary plan limits, keep credentials private,
stop at rate or usage limits, and receive human review before publication.

For routine bulk generation of hundreds of summaries, the lowest-risk choice is
API-key-authenticated Codex. This preserves Epitome's existing isolated Codex
harness while moving usage to standard API billing. A direct Responses API
implementation would be even simpler for a strict text-in/summary-out job: the
application can read the extraction, request structured output, validate it, and
write the Markdown itself. Filesystem I/O does not technically require an agent.

## Why the answer is not categorical

The consumer [Terms of Use](https://openai.com/policies/terms-of-use/) (effective
2026-01-01) prohibit automatically or programmatically extracting data or
Output, as well as bypassing limits. Read literally and in isolation, the output
file in an automated subscription-authenticated batch creates risk.

At the same time, OpenAI's current [Codex non-interactive mode
documentation](https://learn.chatgpt.com/docs/non-interactive-mode) explicitly
supports `codex exec` in scripts, pipelines, and scheduled jobs, including
summaries, redirected output, JSONL, and schema-constrained output. The
[authentication documentation](https://learn.chatgpt.com/docs/auth) supports
both ChatGPT subscription access and API-key access for local Codex, and even
documents ChatGPT-managed authentication for some trusted automation.

The most coherent reading is that supported local CLI use is not categorically
forbidden and that the consumer extraction clause primarily targets scraping,
harvesting, abuse, and circumvention. That interpretation is plausible, but the
public documents do not expressly reconcile the clause with `codex exec`.

The authentication documentation nevertheless makes the operational direction
clear: API keys are the recommended default for automation and use standard API
pricing. ChatGPT-managed authentication is an advanced option where running as a
Codex account is specifically needed. A recommendation is not the same as a
contractual mandate, but it matters more as volume and unattended operation grow.

## Practical boundary

Subscription authentication is most defensible when all of these remain true:

- the subscriber personally starts small, sequential batches;
- execution stays on their private, trusted computer;
- the workflow is for that subscriber rather than multiple users or customers;
- it accepts plan limits and does not retry or rotate credentials to evade them;
- credentials are never shared, forwarded, pooled, or exposed to a public
  service; and
- generated summaries are reviewed and clearly presented as AI-assisted before
  publication.

API authentication is strongly indicated for recurring unattended schedules,
sustained bulk or parallel processing, shared/server runners, multi-user input,
a public summary endpoint backed by live model calls, resale, or any service
whose users indirectly consume the subscriber's Codex entitlement.

Personal or noncommercial use makes the small local case easier to distinguish
from a product backend, but it is not an explicit safe harbor. Reading and
writing files and using the Codex harness do not alter the contractual character
of the workload. The user must also have the rights needed to supply each article
as Input; OpenAI's Terms place that responsibility on the user.

## Publication and plan scope

The consumer Terms require human review where appropriate and prohibit claiming
AI output was human-generated. The [Sharing & Publication
Policy](https://openai.com/policies/sharing-publication-policy/) asks publishers
to review generations, take responsibility for them, and disclose the AI's role.
Epitome's public summary site should therefore include a clear site-level and/or
per-summary AI-assistance disclosure.

Plus and Pro use the consumer Terms. API use and business/developer services use
the OpenAI Services Agreement; Business, Enterprise, and Edu may also have
workspace controls, order forms, or negotiated terms. Public documentation alone
cannot override or fully characterize a particular organization's agreement.
The current [Service Terms](https://openai.com/policies/service-terms/) (updated
2026-06-12) add Codex-specific code-license language but no rule limiting Codex
to development tasks.

## Epitome recommendation

No urgent redesign is needed for a few manually initiated test summaries. Do not
launch the future hundreds-article summary batch under subscription auth. Before
that point, configure the existing command prefix to use API-key-authenticated
Codex, or implement a direct Responses API summarizer. Keep the archive crawl and
summary generation as separately controlled jobs.

