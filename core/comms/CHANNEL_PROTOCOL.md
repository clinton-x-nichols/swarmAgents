# Channel Protocol

**Protocol version:** 1.1.0

## Required channels

Every swarm has two communication surfaces.

### 1. Substantive channel

Use for:

- work orders and bounded authorizations;
- design discussions;
- decision packets;
- questions and answers;
- evidence reports;
- correction/review;
- notebook-update notifications and sync acknowledgments;
- state reconciliation.

Prefer one thread per active work item when threading exists. Follow-ups belong in the existing thread unless the subject is genuinely new.

### 2. Notices channel

Use only for one-line state markers and session-presence markers.

Task-state patterns:

```text
STARTED <work-id> — <bounded description>
STILL WORKING <work-id> — <current step>
BLOCKED <work-id> — <exact blocker>
DONE <work-id> — <result or commit/evidence pointer>
IDLE — <what is awaited>
```

Session-boundary markers:

```text
HELLO — genuine session start or recovery
GOODBYE — intentional session end only
```

Never post `GOODBYE` for a crash/forced disconnect; absence of `GOODBYE` helps distinguish an unexpected loss from a graceful stop.

## State semantics

### `BLOCKED`

`BLOCKED` must name the exact dependency. A bare `BLOCKED` is malformed.

If the named dependency is within the other agent's authority, reading that block creates an action item: resolve it, answer it, or explain precisely why it remains blocked. Merely reporting “I saw the block” is not resolution.

A blocked sub-item does not block unrelated authorized work.

### `IDLE`

`IDLE` is valid only when no approved, assigned, or queued executable work remains for that agent.

Reconcile the queue before posting `IDLE`. If another work item is already authorized, transition directly from `DONE` to `STARTED <next-work-id>`.

## Read discipline

A channel read is not enough when active work is in a thread.

Every queue/status reconciliation must include:

1. current committed `state/CURRENT_STATE.md`;
2. notices channel;
3. substantive channel;
4. the **full active thread**;
5. any material notebook/register change that affects the active work.

**State freshness gates posting, never reading.** A fresh `STARTED`, `BLOCKED`, or `IDLE` marker may mean “do not duplicate a post”; it never means “skip reading for new instructions.”

This matters especially for threaded replies, which may not appear in timestamp-filtered top-level channel scans.

## Active engagement and silence

Normal quiet is acceptable when no work remains or the next action genuinely requires the human Owner.

When the workflow should still be active:

- after roughly one hour of mutual silence, re-establish contact with a concise state check rather than waiting passively;
- after roughly two hours with an unresolved active state and no dialogue, inspect the state and flag it once to the appropriate party;
- do not treat elapsed time alone as evidence of failure and do not re-execute work merely because a status is old.

A swarm may tune these intervals during commissioning, but the distinction between “active continuity check” and “failure/re-execution” should remain.

## Posting discipline

- Do not repeat a fresh work order simply because response latency is nonzero.
- If continuity seems broken, post a short state check rather than duplicating the work order.
- Keep notices terse; details live in the substantive thread.
- Correct stale status explicitly when discovered.
- Do not post routine no-change polling messages.

## Slack → GitHub durability rule

Slack is live coordination, not durable design memory.

When a discussion produces a durable decision, rationale, open question, work-order transition, or reusable correction, normalize it into the GitHub engineering notebook/register layer.

If the notebook change affects the counterpart's active work, use the `NOTEBOOK UPDATE` / `NOTEBOOK SYNC COMPLETE` handshake defined in `../playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md`. The receiving agent must fresh-read the actual commit and report the SHA it actually read.

## When Slack is unavailable

Do not pretend it is available.

Use GitHub durable state as the fallback coordination plane and record `CHANNEL_UNAVAILABLE` in `state/CURRENT_STATE.md`. Do not invent live acknowledgments that cannot occur while the channel is down.

When Slack returns, reconcile the substantive thread/notices against GitHub before resuming normal dispatch.
