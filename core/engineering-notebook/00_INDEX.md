# Engineering Notebook Index

The engineering notebook is the swarm's durable design/history layer. It is not a second current-state file and it is not a copy of Slack.

## Read order

1. `../state/CURRENT_STATE.md` — fast current coordination state.
2. `../state/DECISION_REGISTER.md` — accepted decisions and rationale.
3. `../state/OPEN_QUESTIONS.md` — genuine unresolved questions and blocking scope.
4. `../state/WORK_QUEUE.md` — authorized work and sequencing.
5. `CONSTRUCTION_NOTES.md` — design reasoning, alternatives, source findings, implementation impact.
6. `RECONCILIATION_LOG.md` — material source/state discrepancies and how they were reconciled.
7. Relevant Git history and evidence files.

## Authority model

The notebook answers:

- What has the swarm decided?
- Why was that decision made?
- What should be implemented?
- What is still unresolved?
- What source contradiction or stale state was found?
- What implementation/evidence remains?

The source system being changed by the swarm remains authoritative for its own current published/runtime state. A notebook decision that has not yet been implemented is a synchronization state, not permission to pretend the source system already changed.

## Single-home rule

The canonical decision, open-question, and work registers live in `../state/`. Do not create duplicate copies inside this folder. This index makes them part of the logical engineering notebook by reference.

Use `CONSTRUCTION_NOTES.md` for rationale and design analysis that does not belong in a compact register row. Use `RECONCILIATION_LOG.md` when a material mismatch between GitHub, Slack, memory, or another system of record must be preserved for traceability.

## Write rules

- Check the current remote head immediately before writing shared notebook files.
- Do not overwrite intervening work.
- Preserve historical provenance; later corrections should identify what was superseded rather than rewriting history invisibly.
- Mechanically verify exact restorations against a known-good source.
- Notify the counterpart when a notebook change affects active work, and require a fresh-read sync acknowledgment.

See `../playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md` for the complete operating model.
