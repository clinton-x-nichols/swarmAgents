# Swarm Manager Engineering Notebook Index

This is the durable engineering/design record for the **`swarmAgents` parent project itself**, including the planned Swarm Manager control plane.

It is deliberately separate from `core/engineering-notebook/`. The `core/` notebook is a reusable template copied into each live swarm; this root notebook records how the parent library, factory, protocols, and Swarm Manager product evolve.

## Read order

1. `01_PROGRAM_CHARTER_AND_PRINCIPLES.md` — outcome, boundaries, design principles, and definition of done.
2. `02_ENGINEERING_NARRATIVE.md` — chronological explanation of how the design evolved and why.
3. `03_DECISION_REGISTER.md` — accepted, proposed, superseded, rejected, and deferred decisions.
4. `04_CONSTRUCTION_NOTES.md` — detailed technical reasoning, alternatives, experiments, failures, and evidence.
5. `05_OPEN_QUESTIONS.md` — genuine unresolved dependencies and Owner decisions.
6. `06_PROPOSED_ARCHITECTURE.md` — first full architecture proposal; retained as design history.
7. `07_LANDSCAPE_RESEARCH.md` — external-product and architecture-pattern research.
8. `08_WORK_QUEUE.md` — bounded project work and sequencing.
9. `09_RECONCILIATION_LOG.md` — material source/state contradictions and how they were resolved.
10. `10_ARCHITECTURE_REVIEW_2026_08_08.md` — architecture/functionality-first control-plane refinement after Owner feedback.
11. `11_TOKEN_AND_MEMORY_STEWARD.md` — accepted future Token Monitor, Memory Manager, and Token & Memory Steward capability; detailed implementation remains evolvable.
12. `12_PROVISIONING_AND_AUTHORING_REFINEMENT_2026_08_08.md` — controlling separation between library-first provisioning and the separate Swarm Creation Tool; per-swarm UI/port direction; Cloud Configuration Manager API dependency; Explainer Swarm POC.

## Information ownership

- **Charter/principles** own stable project intent and design principles.
- **Decision register** owns durable decisions and their status.
- **Engineering narrative** explains the story; it must not silently replace decisions.
- **Construction notes** own detailed reasoning, experiments, alternatives, and failure/success records.
- **Open questions** contain only genuine unresolved items.
- **Work queue** owns current bounded engineering work and sequencing.
- **Architecture review/refinement documents** may supersede earlier proposals but never silently rewrite accepted Owner decisions.
- **Capability/module design documents** capture accepted future direction and proposed implementation boundaries without prematurely freezing unresolved UX or algorithm choices.
- **Git history** proves exactly what changed.

## Write rules

1. Every durable fact has one canonical home; other files link or summarize.
2. Accepted decisions are never silently rewritten. If the conclusion changes, mark the old decision superseded and add a new decision.
3. Record failed approaches as well as successful ones when they could prevent repeat work.
4. Distinguish **Owner-accepted** design from **Daisy-proposed** architecture.
5. Do not import DDCRM risk-management content into this notebook. The notebook structure was adapted from that project because it worked; the domain content is unrelated and excluded.
6. Fresh evidence outranks remembered conversation summaries.
7. Material architectural changes should update the narrative, decision register, and affected construction notes together.

## Current status

The project is in **architecture / rules-of-the-road formation**. The Owner has established the product outcome and first-class requirements.

The controlling provisioning/product boundary is now:

> **Swarm Creation Tool authors reusable organizations. Blueprint Library publishes them. Provisioning instantiates them.**

Normal provisioning is library-first rather than prompt-first. Provisioning configures runtime/deployment choices and optional modules for a known blueprint; role/relationship/transaction logic is edited in the separate Swarm Creation Tool. `12_PROVISIONING_AND_AUTHORING_REFINEMENT_2026_08_08.md` records this direction.

The existing Cloud Configuration Manager replaces the previously proposed Ansible role in the assumed architecture, but it requires a future API interface before Swarm Manager can use it as a provider.

Every provisioned swarm receives its own UI/dashboard, with an available port selected during provisioning from the 6000–7000 range.

The **Explainer Swarm** is the standing proof-of-concept blueprint and should evolve continuously as Swarm Manager grows.

Token Monitor, Memory Manager, and Token & Memory Steward remain accepted future capabilities, with their implementation intentionally downstream of core lifecycle/provider functionality.
