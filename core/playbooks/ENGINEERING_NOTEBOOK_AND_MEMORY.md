# Engineering Notebook and Memory Model

## Purpose

Every swarm maintains four distinct continuity layers. They are intentionally separate because each answers a different question.

1. **Live coordination** — Slack substantive channel and notices channel. Answers: what are the agents saying and doing right now?
2. **Current coordination state** — `state/CURRENT_STATE.md`. Answers: where is the swarm right now?
3. **Engineering notebook** — durable GitHub design record. Answers: what has been decided, why, what should be implemented, and what remains unresolved?
4. **Agent memory** — durable identity, rules, collaboration conventions, and reusable lessons. Answers: who are the agents, how do they work together, and what operating lessons should survive a restart?

Do not collapse these layers into one file and do not let chat history become the only source for any of them.

## Information ownership

### Slack substantive channel

Use for:
- work authorization;
- questions and answers;
- design discussion;
- evidence reports;
- review/correction;
- decision packets;
- notebook-update notifications.

Slack is live coordination, not durable design memory.

### Slack notices channel

Use only for terse state markers and session-presence markers. It is non-authoritative status telemetry.

### `state/CURRENT_STATE.md`

Small, rewritten current-state snapshot. It should be fast enough to read on every queue check or restart.

Do not append history here. Old state belongs in Git history, the engineering notebook, or session logs.

### Engineering notebook

The notebook is the durable design record. Its index is `engineering-notebook/00_INDEX.md`.

The notebook includes or points to:
- accepted decisions and rationale;
- open questions and owner dependencies;
- work-order/register state;
- construction notes and rejected alternatives;
- source reconciliation and contradiction findings;
- change/reconciliation history;
- evidence pointers;
- architecture and implementation impact.

To avoid duplicate sources of truth, the default template keeps the live canonical registers in `state/DECISION_REGISTER.md`, `state/OPEN_QUESTIONS.md`, and `state/WORK_QUEUE.md`; the engineering-notebook index incorporates those registers by reference rather than copying them.

### Agent memory

The memory layer is indexed by `memory/INDEX.md` and governed by `memory/README.md`.

Agent memory is for:
- identity/persona;
- role boundaries;
- standing behavioral rules;
- communication rituals and conventions;
- collaboration model;
- reusable verified lessons;
- restart/bootstrap pointers.

Agent memory is **not** project work state. Do not put active work-order status, current document versions, transient blockers, or project-specific decisions there when those already belong in the engineering notebook/state layer.

## Single-home rule

Every durable fact should have one canonical home.

Other files may link to or summarize the canonical fact, but should not reproduce full competing copies. If the summary becomes stale, correct the summary; do not silently reinterpret the canonical record.

## Slack → GitHub normalization loop

A durable decision made in Slack is not complete merely because both agents saw it.

The normal sequence is:

1. Orchestrator and Worker discuss the issue in the substantive thread.
2. Orchestrator resolves anything supported by accepted sources; genuine owner decisions go to the Owner.
3. Worker performs bounded work and returns evidence.
4. Orchestrator reviews/challenges the evidence.
5. Any durable accepted decision, rationale, open question, work-order transition, or reusable correction is normalized into GitHub.
6. The Orchestrator sends a concise `NOTEBOOK UPDATE` in the substantive thread.
7. The Worker fresh-reads the actual GitHub commit/files and returns `NOTEBOOK SYNC COMPLETE` using the SHA actually read.
8. `state/CURRENT_STATE.md` is updated if the material current state changed.
9. The notices channel reflects only the resulting execution state.

## Notebook update handshake

### Orchestrator → Worker

```text
NOTEBOOK UPDATE
Repository: <owner/repo>
Commit: <claimed SHA>
Files updated:
- <path>
Decisions added/changed/superseded:
- <id>: <summary>
Affected work items:
- <work-id>
Required Worker action:
- fresh-read the changed files;
- reconcile with active work;
- report any discrepancy;
Timing: <now / before next write / before related work>
Known implementation impact: <summary>
Questions requiring Worker analysis: <list or none>
```

### Worker → Orchestrator

```text
NOTEBOOK SYNC COMPLETE
Commit actually read: <SHA>
Files loaded:
- <path>
Active work affected: <summary>
Implementation impact: <summary>
Discrepancies: <none or exact mismatch>
```

The Worker must report the SHA actually read, not simply echo the Orchestrator's claimed SHA.

## GitHub write discipline

Before every shared-file write:

1. fetch/read the current default-branch head;
2. compare the intended base with remote head;
3. inspect intervening commits affecting the same files or intent;
4. reconcile compatible changes;
5. stop with an exact conflict if intent cannot be safely merged;
6. write only the bounded authorized scope;
7. mechanically verify the result where the claim is about exact preservation or restoration;
8. report the resulting commit.

Do not restore from memory when an actual known-good commit can be diffed.

## Memory refresh discipline

Memory is a continuity claim, not proof of current external state.

At restart:

1. read config and protocol;
2. read `memory/INDEX.md` and relevant identity/rule files;
3. read `engineering-notebook/00_INDEX.md` and relevant notebook/register files;
4. read `state/CURRENT_STATE.md`;
5. read the current Git head/commits relevant to active work;
6. read notices;
7. read the full active substantive thread;
8. inspect any external system of record relevant to the work;
9. reconcile discrepancies before issuing new work.

Do not claim a prior tool call, commit, channel state, or source-system state has been verified unless it was independently checked in the current session.

## What happens when sources disagree

Do not silently choose.

Classify the difference:
- stale current-state snapshot;
- unnormalized Slack decision;
- engineering design not yet implemented in a source system;
- genuine contradiction;
- superseded record;
- unverifiable memory claim.

Then apply the swarm's source hierarchy and record the reconciliation in `engineering-notebook/RECONCILIATION_LOG.md` when material.

## Operating principle

**Conversation reasons. Slack coordinates. Notices signal. Current state orients. The engineering notebook remembers the program. Agent memory remembers how the agents operate. Git history proves what changed.**
