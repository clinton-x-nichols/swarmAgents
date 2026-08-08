# Architecture

## Parent library versus live swarm

`swarmAgents` is a **factory/library**. Each live swarm gets its own repository.

Why separate them:

- the parent can evolve without mutating active swarm state;
- each swarm has independent decisions, work queue, notebook history, evidence, memory, and current state;
- security and repository permissions can differ by swarm;
- one swarm cannot overwrite another swarm's durable coordination state;
- upgrading an existing swarm can be explicit and reviewed.

## Stable layers

1. **Human Owner** — mission, genuine decisions, direct security approvals.
2. **Conversational Orchestrator** — owner-facing reasoning, architecture, bounded dispatch, synthesis, independent review, notebook normalization.
3. **Execution Worker** — implementation/research/document work, evidence, repository operations, exact blockers, sync acknowledgments.
4. **Agent memory layer** — identity/persona, role behavior, collaboration conventions, reusable lessons. Indexed by `memory/INDEX.md`.
5. **Engineering notebook layer** — durable decisions, rationale, open questions, work history, construction notes, reconciliation history. Indexed by `engineering-notebook/00_INDEX.md`.
6. **Current coordination state** — concise `state/CURRENT_STATE.md` plus compact registers.
7. **Live coordination plane** — substantive channel plus notices channel.
8. **External systems of record** — domain-specific runtime/published sources authoritative for their own content.

## Why memory, notebook, and state are separate

They answer different questions:

- **Memory:** Who are we and how do we operate?
- **Engineering notebook:** What did we decide, why, and what should be implemented?
- **Current state:** Where are we right now?
- **Slack:** What are we discussing/doing right now?
- **External system:** What is actually published/running right now?

Collapsing those categories causes stale-state and false-memory errors.

## Communication-to-durability loop

Substantive work happens in Slack threads. Status lives in notices. Durable decisions and material state transitions are normalized into GitHub. When a notebook change affects active counterpart work, the receiving agent fresh-reads the real commit and acknowledges the SHA actually read.

See `core/playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md` and `core/comms/CHANNEL_PROTOCOL.md`.

## Swarm type profiles

A swarm type changes defaults, specialized roles, commissioning questions, and workflow-specific QA. It does not replace the stable coordination architecture.

Profiles included initially:

- `general` — neutral starting point for mixed work;
- `research` — evidence acquisition, source evaluation, synthesis, citation QA;
- `documentation` — source-grounded drafting, information architecture, editorial and publication QA;
- `software-development` — design, implementation, tests, code review, CI, and release boundaries.

Profiles are deliberately small overlays. The shared protocol remains in `core/`.
