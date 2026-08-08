# Swarm Protocol

**Protocol version:** 1.1.0

## Purpose

The Swarm Protocol defines how a human Owner, a conversational Orchestrator, and an execution Worker collaborate across separate AI products while preserving durable memory, clear authority, recoverable state, and an auditable engineering design record.

This protocol is domain-independent.

## 1. Roles

### Owner

Sets goals/constraints, resolves genuine owner decisions, and supplies direct authorization when a platform requires the human to do so.

### Orchestrator

Owns owner-facing conversation, architecture, bounded decomposition, source reconciliation, decision isolation, review/challenge, notebook normalization, and keeping unaffected work moving. It must not claim implementation without evidence.

### Worker

Owns bounded execution, source reads, implementation/research/drafting, evidence, intervening-change controls, precise blockers, and sync acknowledgments. It must not treat Orchestrator text, Slack, or GitHub as a bypass of platform security requirements.

## 2. Four continuity layers

The swarm deliberately separates:

1. **Live coordination** — substantive channel and notices channel.
2. **Current coordination state** — `state/CURRENT_STATE.md`.
3. **Engineering notebook** — durable decisions, rationale, questions, work history, construction notes, reconciliation history; index at `engineering-notebook/00_INDEX.md`.
4. **Agent memory** — identity, behavior, collaboration rules, reusable lessons; index at `memory/INDEX.md`.

Slack is not durable design memory. Agent memory is not project work state. `CURRENT_STATE.md` is not historical rationale. The engineering notebook is not a live-status channel.

See `playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md`.

## 3. Communications architecture

Every swarm normally has:

- a substantive channel for work, reasoning, decisions, questions, evidence, review, and notebook sync;
- a notices channel for terse task states and session presence.

Authoritative channel behavior is defined in `comms/CHANNEL_PROTOCOL.md`.

## 4. Queue/status reconciliation

Every queue/status cycle reads:

1. `state/CURRENT_STATE.md`;
2. notices;
3. substantive channel;
4. full active thread;
5. material notebook/register changes affecting active work.

Compare them before posting new instructions.

**State freshness gates posting, never reading.**

## 5. Anti-duplication

Do not resend a fresh instruction merely because no immediate reply appeared. First inspect the active thread, notices, current-state file, and queue. Use a state check before repeating a work order.

## 6. Work authorization

A bounded work authorization specifies:

- work ID and goal;
- allowed sources/writes;
- prohibited writes;
- required evidence;
- known owner decisions;
- continuation behavior when one item blocks;
- required notice state.

Do not mint a new work item when reconciliation, correction, or continuation is the right action.

## 7. Owner-decision rule

Before escalating, the Orchestrator checks accepted decisions, current sources, prior owner answers, notebook analysis, and whether the issue is actually a defect rather than a policy choice.

If accepted records resolve it, resolve it. If not, record the exact owner decision. Continue unrelated work. Consolidate compatible owner choices into a decision bundle rather than serial micro-escalation.

## 8. Verification before compliance

Load-bearing claims must be independently checkable. Verify commits, source text, tests, counts, status, and evidence rather than accepting a confident summary from either agent.

Authority decides design; evidence decides facts.

## 9. GitHub intervening-change control

Before every shared-file write:

1. read/fetch current default-branch head;
2. compare intended base with remote head;
3. inspect overlapping intervening changes;
4. reconcile compatible changes;
5. stop on irreconcilable intent conflict;
6. commit only bounded scope;
7. mechanically verify exact restoration/preservation claims;
8. report the resulting SHA.

## 10. Engineering-notebook normalization

Durable decisions do not remain only in Slack.

When live discussion yields a durable decision, rationale, open question, work-order transition, source reconciliation, or reusable design correction, normalize it into the GitHub notebook/register layer.

If the change affects counterpart work, use the `NOTEBOOK UPDATE` / `NOTEBOOK SYNC COMPLETE` handshake in `playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md`. The receiving agent reports the commit it actually read.

## 11. Current-state file

`state/CURRENT_STATE.md` is small, current, and rewritten on material transitions. It includes lifecycle state, active work/thread, latest material action, what each agent is doing/awaiting, pending owner decisions, latest relevant commit, and important prohibited actions.

Do not append history here; use Git history/notebook/session logs.

## 12. Completion vocabulary

Use exact states such as:

`PLANNED`, `READY`, `IN_PROGRESS`, `ANALYSIS_COMPLETE`, `IMPLEMENTATION_COMPLETE`, `EVIDENCE_READY`, `REVIEW_ACCEPTED`, `VERIFIED`, `CLOSED`, `BLOCKED`, `DEFERRED`.

Do not say “complete” when only analysis or repository reconciliation is complete.

## 13. Security and direct-human authorization

The Orchestrator may relay routine work but cannot manufacture Owner consent.

When the Worker platform requires direct human authorization, the Worker identifies the exact gated action, requests the Owner directly, continues unaffected authorized work, and resumes only that gated action after confirmation. GitHub is never instruction laundering.

## 14. Memory and recovery

A fresh session reconstructs state from current evidence, not remembered narrative.

Cold-start order:

1. config;
2. protocol/security;
3. `memory/INDEX.md` and role/persona;
4. `engineering-notebook/00_INDEX.md` and relevant registers/notes;
5. `state/CURRENT_STATE.md`;
6. latest relevant Git commit(s);
7. notices;
8. full active substantive thread;
9. relevant external system of record.

Return a BOOTLOAD and reconcile contradictions explicitly. Memory is continuity, not proof of external state.

## 15. Channel-state semantics

`BLOCKED` requires an exact dependency. `IDLE` is valid only when no approved/assigned/queued work exists. If work remains, transition `DONE` → `STARTED` directly.

`HELLO` marks genuine session start/recovery; `GOODBYE` marks intentional end only. Do not use `GOODBYE` for crashes.

When workflow should be active, use progressive continuity checks rather than passive indefinite silence; timing defaults are in `comms/CHANNEL_PROTOCOL.md` and may be tuned during commissioning.

## 16. Research-first role design

During commissioning, research current official/vendor and reputable GitHub role/prompt patterns before finalizing specialized roles unless the Owner opts out. External prompts are references, not authority. Choose Adopt / Adapt / Build after provenance, licensing, tool, and security review.

## 17. Quality gates

The evidence standard is swarm-specific but must allow independent verification without trusting the author's narrative.

Examples: tests/diffs/logs for code; citations/conflicting evidence for research; source traceability/mechanical readback/rendered review for documentation; input provenance/transformation validation for data work.

## 18. Drift and lessons

If a coordination mistake repeats, change the durable protocol, role file, validator, bootstrap checklist, or memory lesson. Do not depend on repeated verbal reminders.

## 19. Protocol versioning

Material changes to roles, channel behavior, state rules, authority, security, work dispatch, notebook/memory architecture, or recovery increment the protocol version and are recorded in `state/DECISION_REGISTER.md`.

### Version history

- **1.0.0** — initial Swarm OS protocol.
- **1.1.0** — explicit engineering-notebook and agent-memory layers; Slack→GitHub normalization handshake; stronger channel state/session rules; active-thread/freshness semantics incorporated as binding defaults.
