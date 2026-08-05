# Durable Codex alarms: research synthesis

Research performed 2026-08-05 with RES2, then checked against current Codex
documentation, the Codex issue tracker, and the local launcher, Slate, notify,
and Semaphore implementations.

## Conclusion

Build the alarm mechanism locally. A thin MCP tool should validate and persist
an alarm, return immediately, and let the current turn end. Semaphore should own
the durable scheduler and later resume the same thread. A skill should teach the
agent when to use the tool and how to avoid stale or unbounded continuation
loops.

Do not try to keep a model turn or MCP request asleep. Do not initially depend
on first-party Codex Scheduled tasks: the product supports scheduling work in an
existing chat, but its management UI is currently in the app/web surfaces and
there is no documented App Server or CLI method for creating those schedules.

This is a recognized missing workflow rather than a workstation-specific oddity:

- [Codex issue 32993](https://github.com/openai/codex/issues/32993) asks for
  persistent same-thread future/event wakes for self-healing monitors, without
  continuous model polling.
- [Codex issue 32188](https://github.com/openai/codex/issues/32188) asks for an
  event-driven wake after a background command exits, with the current turn
  allowed to end in the meantime.
- [Codex issue 28144](https://github.com/openai/codex/issues/28144) asks for
  persisted wait/wake support without spending tokens while waiting.
- [Codex issue 24016](https://github.com/openai/codex/issues/24016) covers a
  nearby limitation in noninteractive session resumption.

## Recommended division of responsibility

```text
Codex turn
  -> alarm MCP: validate + persist + acknowledge
  -> turn ends

Semaphore
  -> durable SQLite queue
  -> claim due alarm
  -> verify target state and expiry
  -> submit one structured wake prompt to the original thread
  -> correlate the resulting turn/completion

Codex skill
  -> policy for deciding when to set another alarm or stop
```

The MCP process should be disposable and must never sleep until the due time.
Semaphore is the natural scheduler owner because it already owns durable task,
profile, thread, and pane mappings; locking; follow-up delivery; closed-thread
resumption; and restart-safe queued work. A service manager can supervise
Semaphore and optionally run a periodic safety sweep, but one OS timer per alarm
would fragment ownership and observability.

An MCP call cannot itself cause a future turn after it has returned. A live
supervisor must later submit new input. For the first version, reuse Semaphore's
existing reply/resume path and deliver only when the target is idle. For a
closed terminal, prefer a noninteractive same-thread resume rather than opening
and driving a terminal. Codex officially documents both
[`codex exec resume`](https://learn.chatgpt.com/docs/non-interactive-mode.md#resume-a-non-interactive-session)
and SDK thread resumption in the
[Codex SDK](https://learn.chatgpt.com/docs/codex-sdk.md).

The longer-term supported integration surface is
[Codex App Server](https://learn.chatgpt.com/docs/app-server.md): it exposes
thread and turn operations plus streamed lifecycle events. Its stdio protocol
is the safer pilot target. The WebSocket command and transport are explicitly
experimental, so isolate this behind a versioned adapter and retain the current
delivery fallback.

## Identity and delivery

The alarm tool should not let model-generated arguments select an arbitrary
thread or profile. Give each launched Codex task an opaque owner capability,
bound by the launcher/Semaphore configuration. The MCP server resolves that
capability to the durable Semaphore task and thread. A per-task MCP process is
another acceptable way to enforce the same boundary.

Each delivery needs a unique attempt ID embedded in the wake prompt. Record the
attempt before submitting it. The current completion hook includes thread ID,
turn ID, input messages, and the last assistant message, so it can correlate a
completion by the embedded attempt ID rather than by timing alone. App Server
would improve this by returning the new turn ID directly.

The wake message should contain:

- alarm, attempt, and continuation-chain IDs;
- due time, actual fire time, and lateness;
- a durable operation locator, not assumed process state;
- the reason for waking and a short checklist;
- the original authorization boundary and explicit stop conditions.

It should tell the resumed agent to inspect current reality first. Instructions
written hours earlier may be stale.

## Minimal data and semantics

An `alarms` table needs the alarm ID, owner task/profile/thread, chain ID,
status, Unix creation/due/expiry times, reason, continuation, operation
reference, idempotency key, attempt/wake counts, next attempt, lease owner/time,
wake turn ID, last error, and version. An immutable `alarm_attempts` table should
record every claim and delivery outcome.

Use transactional claims and at-least-once delivery. Exactly-once delivery is
not possible across a crash at the boundary where Codex accepts a prompt.
Before retrying after an ambiguous crash, reconcile the thread/completion spool
for the attempt ID. Useful states are `scheduled`, `claimed`, `deferred`,
`delivering`, `awaiting_completion`, `completed`, `expired`, and `dead_letter`.

Initial MCP methods:

- `alarm.set`: exactly one of `after_seconds` or `due_at_unix`, plus `reason`,
  `continuation`, `operation_ref`, `idempotency_key`, optional `chain_id`, and
  optional `expires_at_unix`;
- `alarm.get`, `alarm.list`, `alarm.cancel`, and `alarm.reschedule`.

Do not initially expose arbitrary target selection, fire-now, permission
changes, or wake-budget increases.

## Safety defaults for the pilot

- Observation/read-only work on automatic wakes; never auto-approve, escalate
  permissions, change accounts/profiles, or reinterpret an alarm as new
  authorization for an irreversible action.
- Minimum delay 60 seconds; maximum one-shot delay 24 hours.
- At most three live alarms per task and one per continuation chain.
- At most three model-generated wakes per chain, six per task per 24 hours, and
  a six-hour chain lifetime.
- Stop and report after two wakes with no measurable progress.
- Expire around two hours after the due time unless the chain has an earlier
  deadline.
- If the target is active, defer with 60--300 seconds of jitter. Never paste a
  wake prompt into an active turn.
- Use bounded infrastructure retry, for example 30 seconds, 2 minutes, 10
  minutes, 30 minutes, and 1 hour, then dead-letter.
- Missing profile/thread, archived target, required approval/credentials, or
  ambiguous unsafe state must stop for the user rather than silently changing
  configuration.

## Skill workflow

Before setting an alarm, confirm that the external operation actually started
and record a durable way to inspect it. Set one alarm with explicit success,
progress, failure, authorization, and stop checks, then end the turn. On wake,
inspect reality. If complete, validate and report. If clearly progressing,
schedule at most one successor. If failed, ambiguous, or unchanged twice, stop
and involve the user.

The skill is policy documentation, not the scheduler. Mechanical limits must
also be enforced in Semaphore so prompt injection or agent mistakes cannot
bypass them.

## Incremental implementation

1. Add the SQLite schema and MCP methods with a dry-run due-alarm scanner; no
   automatic delivery.
2. Show due alarms in Semaphore and add an explicit **Wake now** action.
3. Deliver to an idle, open terminal only, with attempt correlation and audit.
4. Add closed-thread noninteractive resumption, still requiring manual wake.
5. Enable automatic one-shot, read-only observation with strict expiry and
   budgets.
6. Pilot App Server behind an adapter and a test profile.
7. Add bounded self-rescheduling, progress fingerprints, coalescing, and loop
   detection.

This sequence produces useful durable reminders early without initially giving
an agent indefinite autonomous execution.
