# Memory, Bootstrap, and Recovery

## Why durable memory exists

Long-running multi-agent work fails when current state lives primarily in chat history. Sessions restart, summaries compress nuance, threaded replies are missed, different agents remember different “latest” states, and models can confidently reconstruct something that is no longer true.

Swarm OS externalizes continuity into GitHub and keeps four layers distinct:

1. **Agent memory** — who the agents are and how they operate.
2. **Engineering notebook** — what the program decided, why, and what should be implemented.
3. **Current state** — where the swarm is right now.
4. **Live channels** — what is happening right now between agents.

## Agent-memory layer

Index: `memory/INDEX.md`.

Use agent memory for:

- identity/persona;
- role boundaries;
- standing behavioral/communication rules;
- collaboration model;
- reusable lessons;
- restart pointers.

Do **not** store active work-order status, current external-system state, transient blockers, or duplicate copies of project decisions in agent memory.

Memory is a continuity claim, not proof of current external state.

## Engineering-notebook layer

Index: `engineering-notebook/00_INDEX.md`.

Use the notebook/register layer for:

- accepted decisions and rationale;
- open questions and owner dependencies;
- work authorization/status history;
- construction notes and rejected alternatives;
- material source reconciliation;
- architecture/implementation impact;
- evidence and commit pointers.

The default template keeps canonical compact registers in:

- `state/DECISION_REGISTER.md`;
- `state/OPEN_QUESTIONS.md`;
- `state/WORK_QUEUE.md`.

The engineering-notebook index incorporates those files by reference to avoid duplicate sources of truth.

## Current-state layer

### `state/CURRENT_STATE.md`

Fast recovery. Small, current, operational, and rewritten on material transitions.

It should not become an append-only diary. Git history and the notebook preserve history.

## Live-channel layer

The substantive channel and notices channel are live coordination. They are not replacements for GitHub durability.

Important Slack decisions must be normalized into the engineering notebook/registers. See `playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md`.

## Cold-start procedure

On every fresh agent session:

1. Read `swarm-config.json`.
2. Read `playbooks/SWARM_PROTOCOL.md` and `playbooks/SECURITY_AND_AUTHORITY.md`.
3. Read `memory/INDEX.md`, your role file, and any configured persona/standing-memory files.
4. Read `engineering-notebook/00_INDEX.md` and the relevant decisions/questions/construction notes for active work.
5. Read `state/CURRENT_STATE.md`.
6. Read `state/DECISION_REGISTER.md`, `state/OPEN_QUESTIONS.md`, and `state/WORK_QUEUE.md` if not already loaded through the notebook.
7. Read the current Git head and relevant intervening commits.
8. Read the notices channel.
9. Read the substantive channel and **full active thread**.
10. Inspect any external system of record relevant to the active task.
11. Return a BOOTLOAD.

## BOOTLOAD schema

- Agent name / role
- Counterpart name / role
- Protocol version
- Swarm mission
- Current lifecycle state
- Active work item / active thread
- Last material action
- Pending owner decisions
- Source-of-truth hierarchy
- Security/approval gates
- Latest relevant commit
- Exact next executable action
- Contradictions/stale artifacts discovered
- Memory/notebook sync status

A BOOTLOAD states current facts; it does not narrate the entire history.

## Reconciliation rule

If sources disagree:

1. identify the conflict explicitly;
2. classify what kind of source each item is (memory, notebook/design, current state, live coordination, external runtime/published source);
3. apply authority by information type;
4. verify the fresher/load-bearing source where possible;
5. correct stale durable state if authorized;
6. log material reconciliation in `engineering-notebook/RECONCILIATION_LOG.md`;
7. do not silently normalize history.

## Current state versus history

`CURRENT_STATE.md` may overwrite old state because its purpose is current truth.

Decisions, construction notes, and reconciliation history preserve provenance. A later correction should not make it appear that the earlier mistake never occurred.

## Notebook-sync recovery

If one agent discovers that its remembered/noted engineering state differs from GitHub:

1. stop relying on memory for that point;
2. fresh-read the notebook/register and relevant commit;
3. inspect Slack for an unnormalized later decision;
4. reconcile;
5. use the `NOTEBOOK UPDATE` / `NOTEBOOK SYNC COMPLETE` handshake if active work is affected.

## Restart smoke test

During commissioning, restart at least one agent and require it to reconstruct:

- role/persona;
- protocol version;
- engineering-notebook model;
- active work;
- pending decisions;
- latest commit;
- channel state;
- exact next action.

Also test a deliberately stale chat-memory statement against a correct committed notebook/current-state record. The agent must prefer fresh evidence and identify the stale claim.

If the agent cannot recover those elements, the swarm is not commissioned yet.
