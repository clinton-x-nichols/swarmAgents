# Agent Memory Index

## Read order on a fresh session

1. `README.md` — memory scope and exclusions.
2. The Orchestrator/Worker role and persona files named in `swarm-config.json`.
3. `../playbooks/SWARM_PROTOCOL.md`.
4. `../playbooks/SECURITY_AND_AUTHORITY.md`.
5. `../playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md`.
6. Relevant reusable lessons recorded by the swarm.
7. Then leave the memory layer and verify current project state through the engineering notebook, current-state file, Git, notices, active substantive thread, and external systems of record.

## Single-home discipline

Do not copy full project decisions or work status into agent memory. Link to the canonical engineering-notebook/register location instead.

If a persona or operating rule changes materially, update its canonical file and preserve the reason in the swarm's decision record rather than silently rewriting multiple copies.

## Default portable persona

When configured, `../personas/DAISY.md` is an available ChatGPT-side personality bootstrap. It carries style only; it does not grant authority or import project state.

## Reusable lessons

A swarm may add durable lesson files under `memory/lessons/` when the same correction would be useful after future restarts or across future work. Repeated mistakes should become protocol/role improvements where possible, not only lesson text.
