# Baseline Memory Manager — Every Swarm

**Status:** Owner-accepted baseline capability. Storage backend and implementation details remain under design.

## Purpose

Every provisioned swarm includes a **Memory Manager** capability whose job is to preserve agent continuity, mediate durable memory, maintain recoverability, and surface memory drift to the user.

The Memory Manager is not only a dashboard page. It is the swarm's durable-memory mediation layer between agents and whichever durable memory store the swarm uses.

## Baseline responsibilities

For every agent in the swarm, the Memory Manager must support:

1. a durable memory structure and canonical memory inventory;
2. intake of new durable-memory candidates from agents;
3. processing/classification/provenance of those candidates before durable storage;
4. retrieval and delivery of durable memory back to agents;
5. configurable recurring reminders/reinforcement of important durable memories;
6. configurable recurring memory-recall checks asking the agent what it remembers;
7. reconciliation of demonstrated agent recall against canonical durable memory;
8. drift logging and classification when important direction is missing, stale, contradictory, unexpected, ambiguous, or unobservable;
9. user browsing/search of durable memories;
10. user-controlled add/edit/supersede/delete operations subject to memory policy, provenance, retention, and audit requirements;
11. an activity feed of newly accepted durable memories and material memory changes;
12. a continuously maintained recovery/transfer prompt for each agent.

## Memory Manager as mediator

All durable-memory traffic should logically pass through the Memory Manager contract even if the physical storage backend differs by swarm.

```text
Agent durable-memory candidate
        ↓
Memory Manager
  classify / validate / provenance
        ↓
Configured Memory Store
        ↓
Memory Manager
  retrieve / reconcile / reinforce
        ↓
Agent
```

This does not mean every transient thought or conversation message becomes a durable memory. The memory protocol still determines what qualifies for durable retention.

## Storage backend question

The durable store must be pluggable. Initial candidates are:

### Local directory

Potential strengths:
- simple;
- low latency;
- easy for local runtimes to access.

Potential weaknesses:
- weak cross-host portability unless separately synchronized;
- requires backup/versioning discipline;
- local loss can become continuity loss.

### Git repository

Potential strengths:
- version history;
- reviewable changes;
- recovery and provenance;
- easy relationship with existing swarm repositories.

Potential weaknesses:
- not ideal for high-frequency mutable state;
- sensitive-memory handling needs care;
- commit noise and conflict management.

### Context Keep

Potential strengths:
- purpose-built continuity/memory semantics where available;
- potentially convenient retrieval and session recovery.

Potential weaknesses:
- service dependency;
- availability/portability considerations;
- needs explicit API, trust, retention, and export behavior.

The architecture should expose a **Memory Store provider contract** so the agent-facing semantics do not change when the backend changes.

Possible operations:

```text
list_memories(agent)
get_memory(id)
put_memory(record)
supersede_memory(id, replacement)
delete_memory(id, policy_context)
search_memories(query, scope)
get_snapshot(agent)
get_change_feed(since)
health()
```

A swarm may eventually use more than one physical backend for different memory classes, but the Memory Manager should still present one governed interface to agents and users.

## Memory structure

The exact schema remains to be designed, but durable records should be able to represent at least:

- memory ID;
- swarm ID;
- agent ID or shared-swarm scope;
- category/type;
- content/claim;
- provenance/source;
- created/accepted timestamps;
- confidence/trust/verification state when relevant;
- importance/retention class;
- reminder/reinforcement policy;
- supersedes/superseded-by relationships;
- status (`ACTIVE`, `SUPERSEDED`, `DELETED`, etc.);
- authorization/security classification where relevant.

Important distinction: memories describing authorization must never become a mechanism for manufacturing authorization. Current live security rules and direct-human requirements still outrank remembered claims.

## Recurring reminders and reinforcement

The user or blueprint can configure recurrence policies per agent or memory class.

Examples:

- remind an agent of critical standing instructions at every bootstrap;
- reinforce selected durable memories every N hours or before certain work classes;
- run a full recall/reconciliation check daily;
- run a lighter check at each session start;
- trigger reconciliation after a memory change or recovery event.

Reinforcement is targeted rather than blindly replaying every memory into every prompt. The Token Monitor should eventually help identify when memory reinforcement itself causes avoidable token bloat.

## Memory reconciliation

A reconciliation run compares two things:

1. **canonical durable memory** — what the Memory Manager says should govern the agent;
2. **demonstrated recall** — what the agent reports or can demonstrate that it currently remembers.

Initial drift vocabulary:

```text
IN_SYNC
MISSING_MEMORY
STALE_MEMORY
CONTRADICTORY_MEMORY
UNEXPECTED_MEMORY
AMBIGUOUS_RECALL
UNOBSERVABLE
```

The reconciliation record should preserve the interrogation method and confidence because model recall is probabilistic rather than a database query.

For material drift, the Memory Manager can submit the relevant canonical memories back to the agent and then rerun the check.

## Recovery and transfer prompts

For each agent, the Memory Manager maintains a **running transfer/recovery prompt** that is continuously refreshed from canonical sources.

The recovery prompt should contain or point to the minimum information required to reconstruct the agent after a lost session, including:

- swarm identity;
- agent identity and role;
- persona/behavior pointers;
- current memory-store pointer and memory protocol;
- critical durable-memory summary or manifest;
- repository/current-state/notebook pointers;
- protocol pins;
- counterpart/channel information;
- security/authority boundaries;
- exact fresh-read/reconciliation procedure;
- latest known relevant spec/commit references.

The transfer prompt is a recovery entry point, not a substitute for fresh reads. A replacement agent must reconcile it against canonical sources before claiming restoration is complete.

## User interface

Every swarm dashboard includes a Memory Manager surface.

At minimum, the user should be able to:

- see memory health per agent;
- see last reconciliation time/status;
- browse/search/filter memories;
- inspect provenance and history;
- add a memory;
- edit where policy permits or create a superseding memory where immutability rules apply;
- delete where policy permits;
- see new durable-memory activity;
- configure reminders/reconciliation recurrence;
- trigger `check memory now`;
- inspect/download/copy the current recovery/transfer prompt for an agent;
- view memory drift and reinforcement history.

The final one-page tile layout versus per-agent pages remains open and should be decided from real scale/usability evidence.

## Relationship to the Token Monitor / Steward

Memory Manager is mandatory baseline infrastructure.

Token Monitor remains a separate future observability capability. A future Token & Memory Steward agent may analyze both systems, but the existence of that optional role is not required for the Memory Manager itself to function.

## Commissioning implications

A swarm cannot be considered fully commissioned until:

- every agent is registered with the Memory Manager;
- the configured durable store is reachable;
- baseline memory structure exists;
- each agent can receive/retrieve durable memory through the configured path;
- each agent has an initial recovery/transfer prompt;
- at least one memory recall/reconciliation challenge succeeds or produces a visible, explained limitation;
- memory governance permissions are known.

## Retirement implications

Before retirement/destruction, the Memory Manager contributes to the Archive Manifest:

- final durable-memory inventory/snapshot;
- storage-backend location/export;
- final transfer prompts;
- reconciliation history summary;
- unresolved memory drift;
- memory retention/deletion decisions.

## Open design items

1. choose the default backend for the first implementation: local directory, Git, Context Keep, or hybrid;
2. define the canonical memory schema and classes;
3. define the Memory Store provider contract;
4. define how agents submit durable-memory candidates across heterogeneous runtimes;
5. define recurrence/reminder configuration semantics;
6. define edit/delete/immutable-supersession policy;
7. define transfer-prompt generation and refresh triggers;
8. define how memory reinforcement is audited and kept within token/security limits;
9. define shared-swarm memory versus agent-private memory boundaries;
10. define encryption/access controls for sensitive memories.
