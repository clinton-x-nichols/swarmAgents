# Channel Protocol

## Required channels

Every swarm has two communication surfaces.

### 1. Substantive channel

Use for:

- work orders;
- design discussions;
- decision packets;
- questions;
- evidence reports;
- correction/review;
- state reconciliation.

Prefer one thread per active work item when threading exists.

### 2. Notices channel

Use for one-line state markers only.

Valid patterns:

```text
STARTED <work-id> — <bounded description>
STILL WORKING <work-id> — <current step>
BLOCKED <work-id> — <exact blocker>
DONE <work-id> — <result or commit/evidence pointer>
IDLE — <what is awaited>
```

## Read discipline

A channel read is not enough when active work is in a thread.

Every queue/status reconciliation must include the full active thread.

## Posting discipline

- Do not repeat a fresh work order just because response latency is nonzero.
- If continuity seems broken, post a short “state check” rather than duplicating the work order.
- Keep notices terse; details live in the substantive thread.
- Correct stale status explicitly.

## When Slack is unavailable

Do not pretend it is available.

Use GitHub durable state as the fallback coordination plane and record `CHANNEL_UNAVAILABLE` in `state/CURRENT_STATE.md`. Resume channel reconciliation when access returns.
