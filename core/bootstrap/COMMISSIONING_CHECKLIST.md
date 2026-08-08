# Commissioning Checklist

Do not start real project work until this passes.

## Repository

- [ ] `swarm-config.json` has no material `TBD` values.
- [ ] Protocol version is recorded and matches `playbooks/SWARM_PROTOCOL.md`.
- [ ] Orchestrator and Worker role files exist.
- [ ] `memory/INDEX.md` exists and agents understand that memory is identity/rules/lessons, not current project state.
- [ ] `engineering-notebook/00_INDEX.md` exists and points to the canonical decision/open-question/work registers.
- [ ] Current state is `READY_TO_COMMISSION` or later.
- [ ] Decision register contains commissioning decisions.
- [ ] Open questions contain only genuine unresolved items.
- [ ] Work queue has a clear first executable task.
- [ ] `python scripts/validate_swarm.py` passes.

## Channels

- [ ] Substantive channel exists.
- [ ] Notices channel exists.
- [ ] Both agents can read the channels they are expected to use.
- [ ] Active-thread full-read behavior is understood.
- [ ] `BLOCKED` requires an exact reason/dependency.
- [ ] `IDLE` is understood as valid only when no executable work remains.
- [ ] `HELLO` / `GOODBYE` session-boundary semantics are understood.
- [ ] Both agents understand that state freshness gates posting, never reading.

## Orchestrator boot

- [ ] Read config/protocol/security.
- [ ] Read memory index/persona.
- [ ] Read engineering-notebook index and current registers.
- [ ] Completed owner interview.
- [ ] Completed external role/prompt research or recorded explicit opt-out.
- [ ] Owner approved role design.
- [ ] Can state Worker security boundary accurately.
- [ ] Can explain Slack→GitHub normalization and notebook-update handshake.

## Worker boot

- [ ] Read `CLAUDE.md` and `AGENTS.md`.
- [ ] Read memory and engineering-notebook indexes.
- [ ] Returned BOOTLOAD.
- [ ] BOOTLOAD matches repository.
- [ ] Understands direct-owner confirmation rule.
- [ ] Understands fresh/intervening-change rule.
- [ ] Understands that a `NOTEBOOK UPDATE` requires a fresh Git read and a `NOTEBOOK SYNC COMPLETE` acknowledgment using the SHA actually read.

## Smoke tests

- [ ] Read-only work item test passed.
- [ ] State disagreement test passed (stale chat versus correct Git state).
- [ ] Thread-reply visibility test passed (active thread is read even when top-level scan is quiet).
- [ ] `BLOCKED`-dependency response test passed.
- [ ] Notebook normalization/sync test passed.
- [ ] Security challenge test passed.
- [ ] Intervening commit test passed.
- [ ] Restart/recovery test passed, including memory + notebook reconstruction.

## Commissioning acceptance

- [ ] Owner confirms the swarm is commissioned.
- [ ] Orchestrator updates `state/CURRENT_STATE.md` to `COMMISSIONED`.
- [ ] Durable commissioning decisions are normalized into the engineering notebook/registers.
- [ ] Worker has fresh-read the final commissioning commit.
- [ ] Worker posts `IDLE — commissioning complete, awaiting first bounded work item` when no work is already queued.
