# Research request: durable alarms that resume a Codex conversation

## Problem

We frequently run local operations that take from minutes to hours: polite web
crawls, builds, downloads, batch processing, deployment observation, and other
jobs whose next step requires some agent judgment. A Codex turn can launch the
background work, but the particular harness may not expose a heartbeat or alarm
capability that wakes the same conversation later. Keeping the turn alive with
frequent polling wastes resources and is brittle.

We want a general mechanism resembling:

1. Codex calls `alarm.set` with either a duration or absolute timestamp, a
   reason, and perhaps a small continuation instruction.
2. The tool durably records the alarm and immediately acknowledges it, allowing
   Codex to finish its turn instead of blocking.
3. At the due time, a local supervisor resumes the same Codex conversation and
   submits a generated follow-up such as: “Your alarm is due. It is now X; Y
   elapsed. Recheck operation Z and continue or schedule another alarm.”
4. Codex inspects current state, acts, reports, and may schedule another alarm.

This should work for both an interactive TUI that remains open and a thread
whose TUI process/window has since closed. It should survive restarts and avoid
duplicate wakeups.

## Existing local architecture

The workstation already has most of the lifecycle plumbing:

- A local launcher selects a configured Codex home, enables structured TUI
  session recording, creates a per-process JSONL session log, and starts a
  Slate monitor alongside Codex.
- Slate tails that JSONL. It interprets `task_started` as active and
  `task_complete`/`turn_aborted` as idle, writes an atomic sidecar containing
  the tmux pane/window, log path, instance ID, task ID, and state, and tracks
  task state.
- A Codex `notify` hook receives `agent-turn-complete` JSON containing thread
  and turn IDs. It atomically spools those completion records to a state
  directory and produces user notifications.
- Semaphore is a local web/mobile wrapper around Codex conversations. It has a
  durable task record, filesystem locking, pane ownership via a tmux option,
  thread discovery from the session/rollout logs, and a reply operation.
- Semaphore can safely bracket-paste a follow-up into an idle or active TUI.
  If the pane is closed, it launches the configured Codex frontend with
  `resume THREAD_ID`, re-establishes ownership, and supplies the follow-up.
- Semaphore already recovers durable voice-input delivery jobs after its server
  restarts, so there is a precedent for persisted queued work and retries.

Simplified existing lifecycle:

```text
launcher
  -> Codex TUI + structured session JSONL
  -> Slate monitor -> active/idle sidecar

Codex completion notify
  -> durable {thread_id, turn_id, received_at, final_message} record

Semaphore task
  -> durable task/profile/thread/pane metadata
  -> reply(task_id, prompt)
       idle TUI: bracketed paste + Enter
       closed TUI: launch `resume THREAD_ID` + prompt
```

Codex's current public manual also describes first-party Scheduled tasks,
including scheduled tasks inside an existing chat for checking long-running
operations. But the Codex CLI and IDE do not expose the Scheduled management
interface, and not every harness/session supplies a callable scheduling tool.
We need to understand whether that feature can be integrated locally or whether
our mechanism should be independent.

## Proposed design to evaluate

The likely design is a small MCP server plus a durable scheduler integrated
with Semaphore:

```text
Codex -> MCP alarm.set
          validate owner/thread/task and due time
          persist alarm with idempotency key
          return alarm ID and due time immediately

durable alarm store (probably SQLite)
  -> scheduler claims due alarm transactionally
  -> confirms target task is not currently active
  -> Semaphore reply/resume with a structured wake message
  -> marks delivery attempt/result
  -> completion hook correlates the resulting turn
```

The MCP tool should probably offer `set`, `list`, `cancel`, and possibly
`reschedule`. It must not sleep inside the MCP request. Relative durations
should be converted to an absolute UTC/Unix due timestamp at creation, while
retaining the originally requested duration for auditability.

A reusable Codex skill could explain when to set an alarm, how to write a
durable continuation instruction, when to schedule another alarm, when to stop,
and how to avoid wake loops.

## Questions for research

Please perform browser-backed research across current official Codex/OpenAI
documentation, the Codex open-source repository and issue tracker, MCP
documentation/SDKs, and relevant credible community projects or discussions.
Clearly distinguish supported public behavior, experimental behavior,
community workarounds, and your architectural recommendations.

1. Is “sleep now and resume this same agent/thread later” a recognized Codex or
   coding-agent problem? Find relevant Codex issues/discussions and established
   solutions, including scheduled tasks, polling agents, hooks, supervisors,
   App Server clients, or CLI resume automation.
2. Is there a supported way for a local integration to create a first-party
   Codex/ChatGPT scheduled task, especially one attached to the current chat?
   Is there an API, App Server method, deep link, plugin/app mechanism, or only
   desktop/web UI? Note authentication and product-surface limitations.
3. Compare reliable mechanisms for waking the same local Codex context:
   interactive TUI input, `codex resume`, `codex exec resume`, Codex App Server,
   Codex SDK, and any thread/follow-up API. Which is most stable and intended for
   automation? What identifiers and lifecycle records are available?
4. Does an MCP alarm tool fit MCP semantics? Can it return immediately after
   persisting the alarm, and what context can it reliably know about the
   calling Codex thread/task? Should the alarm target be supplied explicitly,
   injected through environment/config, or resolved by the wrapper?
5. Would it be better for the MCP server to own scheduling, for Semaphore to
   own it, or to use a system scheduler such as systemd timers? Evaluate
   restart survival, atomicity, observability, portability, and complexity.
6. Recommend a concrete minimal architecture for this workstation, followed by
   a production-hardening path. Include data model, state transitions, APIs,
   wake-message envelope, process boundaries, and how the completion hook should
   correlate an alarm with the resumed turn.
7. Analyze failure modes: duplicate delivery, missed alarms, clock jumps,
   workstation sleep/offline time, target already active, target closed or
   archived, stale instructions, thread/profile unavailable, rate limits,
   permission prompts, MCP process restart, concurrent alarms, cancellation
   races, and an agent repeatedly scheduling itself forever.
8. Recommend safety policy and defaults: minimum/maximum duration, maximum
   alarms per task, retry/backoff, expiry, approval rules, allowed operations,
   wake budget, loop detection, and when the system must ask the user instead.
9. Suggest an MCP tool schema and a concise skill workflow. Prefer absolute Unix
   seconds for durable timestamps. Avoid designs that keep a model turn or MCP
   request blocked for the duration.
10. Identify what parts of our existing local infrastructure can be reused
    directly and what should remain separate. Point out any fragile reliance on
    terminal scraping or undocumented log formats, and suggest supported
    replacements where available.

Please end with a recommended implementation sequence that can be tested in
small increments without initially granting an autonomous agent permission to
run indefinitely.
