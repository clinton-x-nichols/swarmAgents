# Memory, Bootstrap, and Recovery

## Why durable memory exists

Long-running multi-agent work fails when current state lives primarily in chat history. Conversation is excellent for reasoning but poor as the sole recovery mechanism because:

- sessions restart;
- summaries compress nuance;
- threaded replies are easy to miss;
- two agents can remember different “latest” states;
- status language can drift from canonical work status;
- a model may confidently reconstruct a state that is no longer true.

Swarm OS therefore externalizes operational memory into the repository.

## Durable memory layers

### `state/CURRENT_STATE.md`

Fast recovery. Small, current, operational.

### `state/DECISION_REGISTER.md`

Accepted durable decisions, rationale, owner, and status.

### `state/OPEN_QUESTIONS.md`

Genuine unresolved questions, dependency, owner, blocking scope.

### `state/WORK_QUEUE.md`

Authorized work and sequencing.

### role/protocol files

Persistent behavior and collaboration rules.

### session logs

Optional narrative history. Useful for archaeology, not the first recovery source.

## Cold-start procedure

On every fresh agent session:

1. Read config.
2. Read protocol.
3. Read role.
4. Read current state.
5. Read decisions.
6. Read open questions.
7. Read work queue.
8. Read latest relevant commit(s).
9. Read notices.
10. Read the full active substantive thread.
11. Return a BOOTLOAD.

A BOOTLOAD should state facts, not narrate the entire history.

## BOOTLOAD schema

- Agent name / role
- Counterpart name / role
- Protocol version
- Swarm mission
- Current lifecycle state
- Active work item / active thread
- Last material action
- Pending owner decisions
- Source-of-truth order
- Security/approval gates
- Latest relevant commit
- Exact next executable action
- Contradictions/stale artifacts discovered

## Reconciliation rule

If two sources disagree:

1. Identify the conflict explicitly.
2. Apply the source hierarchy.
3. Verify the fresher source where possible.
4. Correct stale durable state if authorized.
5. Do not silently normalize history.
6. Report what changed and why.

## Current state versus history

`CURRENT_STATE.md` is allowed to overwrite old state because its job is *current truth*.

Decision and session history must preserve provenance. Do not rewrite history to make it look as though a later correction was always known.

## Restart smoke test

At least once during commissioning, restart one agent and require it to reconstruct:

- role;
- protocol version;
- active work;
- pending decisions;
- latest commit;
- exact next action.

If it cannot, the repository does not yet contain enough durable memory.
