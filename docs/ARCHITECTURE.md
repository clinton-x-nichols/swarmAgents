# Architecture

## Parent library versus live swarm

`swarmAgents` is a **factory/library**. Each live swarm gets its own repository.

Why separate them:

- the parent can evolve without mutating active swarm state;
- each swarm has an independent decision register, work queue, evidence history, and current-state file;
- security and repository permissions can differ by swarm;
- one swarm cannot accidentally overwrite another swarm's durable coordination state;
- upgrading an existing swarm can be explicit and reviewed instead of implicit.

## Stable layers

1. **Human Owner** — mission, genuine decisions, direct security approvals.
2. **Conversational Orchestrator** — owner-facing reasoning, architecture, bounded dispatch, synthesis, independent review.
3. **Execution Worker** — implementation/research/document work, evidence, repository operations, exact blockers.
4. **Durable coordination plane** — GitHub protocol, current state, decisions, questions, queue, evidence.
5. **Live coordination plane** — substantive channel plus notices channel.

## Swarm type profiles

A swarm type changes defaults, specialized roles, commissioning questions, and workflow-specific QA. It does not replace the stable coordination architecture.

Profiles included initially:

- `general` — neutral starting point for mixed work;
- `research` — evidence acquisition, source evaluation, synthesis, citation QA;
- `documentation` — source-grounded drafting, information architecture, editorial and publication QA;
- `software-development` — design, implementation, tests, code review, CI, and release boundaries.

Profiles are deliberately small overlays. The shared protocol remains in `core/`.
