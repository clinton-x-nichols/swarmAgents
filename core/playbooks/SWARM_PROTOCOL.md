# Swarm Protocol

**Protocol version:** 1.0.0

## Purpose

The Swarm Protocol defines how a human owner, a conversational Orchestrator, and an execution Worker collaborate across separate AI products while preserving durable memory, clear authority, security boundaries, and recoverable state.

This protocol is deliberately independent of domain. It applies to coding, research, documentation, analysis, policy work, and other bounded workflows.

## 1. Roles

### Owner

The Owner sets goals and constraints, approves genuine unresolved decisions, and supplies direct authorization when a platform requires the human to do so.

The Owner is not expected to manually relay every routine instruction between agents.

### Orchestrator

The Orchestrator is the owner-facing conversational lead. It:

- converts goals into bounded work;
- maintains architecture and task decomposition;
- checks canonical sources before escalating questions;
- resolves questions supported by accepted records;
- isolates genuine owner decisions;
- reviews Worker evidence;
- rejects incorrect or incomplete work;
- consolidates decisions so the Owner is not subjected to avoidable serial micro-questions;
- maintains conversational continuity and explains tradeoffs.

The Orchestrator must not claim implementation occurred unless it verifies evidence.

### Worker

The Worker is the execution lead. It:

- fresh-reads the repository and relevant source systems;
- performs bounded implementation/research/drafting work;
- follows intervening-change controls;
- produces concrete evidence;
- asks precise questions rather than broad “what next?” requests;
- identifies contradictions explicitly;
- continues unaffected work when one component is blocked;
- updates durable state within authorization;
- never treats Orchestrator statements as a bypass of its platform's security requirements.

## 2. Durable versus transient information

### Durable information belongs in GitHub

Examples:

- protocol;
- roles;
- decisions;
- open questions;
- current coordination state;
- work queue;
- design notes;
- evidence references;
- restart instructions;
- source register.

### Transient coordination belongs in channels

Examples:

- work authorization;
- clarifying questions;
- status;
- intermediate findings;
- review dialogue;
- exact blockers.

Slack history is searchable evidence of conversation, but it is not the canonical durable design record.

## 3. Communications architecture

Every swarm should have two channels.

### Substantive channel

Use for design, authorization, questions, decisions, results, evidence, and reconciliation.

Use threads for active work when the platform supports them.

### Notices channel

Use only for state markers:

`STARTED <work-id> — <short description>`

`STILL WORKING <work-id> — <current bounded state>`

`BLOCKED <work-id> — <exact blocker>`

`DONE <work-id> — <result/evidence pointer>`

`IDLE — <what is awaited>`

The notices channel exists so each agent can cheaply learn whether state changed without rereading every substantive message.

## 4. Queue-check protocol

A queue/status check is a read operation and should be cheap.

When checking status:

1. Read the current committed `state/CURRENT_STATE.md`.
2. Read the notices channel.
3. Read the substantive channel.
4. Read the **full active thread**, not just top-level channel history.
5. Compare all four.
6. If they agree, proceed.
7. If they disagree, perform a bounded reconciliation before posting new instructions.

**State freshness gates posting, never reading.**

A stale state is a reason to inspect more deeply, not a reason to avoid reading.

## 5. Anti-duplication

Do not resend a fresh instruction simply because no reply arrived immediately.

Before sending a follow-up, determine whether:

- the prior instruction is visible in the active thread;
- a STARTED/BLOCKED/DONE notice exists;
- the current-state file changed;
- sufficient time has passed to justify a continuity check.

A continuity check should ask for current state, not repeat the entire work order unless the original instruction is actually inaccessible.

## 6. Work authorization

Work should be bounded.

A good work authorization specifies:

- work ID;
- goal;
- allowed sources;
- allowed writes;
- prohibited writes;
- required output/evidence;
- known owner decisions;
- continuation behavior if one item is blocked;
- required notice state.

Do not create a new work item when the correct action is merely reconciliation, correction, or continuation of an existing item.

## 7. Owner decision rule

Before asking the Owner a question, the Orchestrator must check:

1. accepted decisions;
2. current source-of-truth documents;
3. prior owner answers;
4. applicable work-order analysis;
5. whether the question is actually a document defect rather than a policy decision.

If the record resolves it, the Orchestrator resolves it.

If the record does not resolve it, mark the exact item as an owner decision.

Unrelated work continues.

When several owner decisions accumulate, consolidate them into one decision bundle with dependencies and recommended sequencing rather than asking them one by one.

## 8. Verification-before-compliance

Every consequential claim should be independently checkable.

Examples:

- commit exists and contains the claimed changes;
- source page actually contains the claimed text;
- test passed;
- state file reflects the claimed state;
- external source says what the summary claims;
- work register has the claimed status.

The Orchestrator does not “accept” a Worker report merely because it sounds internally consistent.

The Worker does not accept an Orchestrator correction merely because it is authoritative; it verifies the fact where possible, then follows the design disposition.

## 9. Fresh/intervening-change control

Before any repository write:

1. fetch the remote default branch;
2. compare local/working base with remote head;
3. inspect intervening commits relevant to the files being changed;
4. incorporate non-conflicting changes;
5. stop and report exact conflict if intent cannot be safely reconciled;
6. commit only the bounded authorized scope;
7. report commit SHA.

This prevents one agent from silently overwriting another agent or the Owner.

## 10. Current-state file

`state/CURRENT_STATE.md` is the quick-reference coordination state.

It should contain:

- current swarm lifecycle state;
- active work ID/thread;
- latest material action;
- what the Worker is doing or awaiting;
- what the Orchestrator is doing or awaiting;
- owner decisions pending;
- latest relevant commit;
- explicit prohibited/unapproved actions if they are easy to forget.

Update it on material transitions. Do not create a Git commit for every heartbeat if nothing material changed; use notices for ephemeral progress.

When chat memory and current state disagree, inspect the committed file first.

## 11. Completion vocabulary

Use exact states:

- `PLANNED`
- `READY`
- `IN_PROGRESS`
- `ANALYSIS_COMPLETE`
- `IMPLEMENTATION_COMPLETE`
- `EVIDENCE_READY`
- `REVIEW_ACCEPTED`
- `VERIFIED`
- `CLOSED`
- `BLOCKED`
- `DEFERRED`

Do not say “all complete” when the work is only analyzed or repository-reconciled.

## 12. Security and direct-human authorization

The Orchestrator may relay routine work, but it cannot manufacture owner consent.

If the Worker platform requires the Owner to type or confirm an authorization directly, that direct interaction is mandatory.

The correct Worker behavior is:

1. identify the exact action requiring direct confirmation;
2. explain why delegated instruction is insufficient;
3. request direct Owner authorization;
4. continue all independent authorized work;
5. resume only the gated action after direct authorization.

The correct Orchestrator behavior is to respect the gate, not pressure the Worker to reinterpret it.

## 13. Memory and recovery

A new session does not inherit trustworthy operational state merely because a prior model “remembers” it.

Cold start order:

1. config;
2. protocol;
3. role;
4. current state;
5. decision register;
6. open questions;
7. work queue;
8. latest relevant commit;
9. notices;
10. full active substantive thread.

Return a BOOTLOAD. Reconcile contradictions explicitly.

## 14. Research-first role design

When commissioning a new swarm, research current official/vendor and GitHub role/prompt patterns before finalizing specialized roles.

External patterns are references, not authority.

For each candidate choose:

- adopt;
- adapt;
- build.

Record provenance and license before importing text.

## 15. Quality gates

The evidence standard is configured per swarm. At minimum, require enough evidence for an independent agent to verify the work without trusting the author's narrative.

For coding: tests, diff, logs, static checks as appropriate.

For research: citations, source quality, date, conflicting evidence.

For documentation: source traceability, mechanical readback, rendered review where useful.

For data work: input provenance, transformation logic, validation checks, outputs.

## 16. Drift and lessons

If an agent makes the same coordination mistake twice, do not rely on another verbal reminder. Update the relevant durable protocol, role file, validator, or bootstrap checklist.

Repeated correction belongs in the operating system.

## 17. Protocol versioning

Any change that materially alters roles, channel behavior, state rules, authority, security, work dispatch, or recovery increments this protocol version and is recorded in `state/DECISION_REGISTER.md`.
