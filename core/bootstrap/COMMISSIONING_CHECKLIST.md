# Commissioning Checklist

Do not start real project work until this passes.

## Repository

- [ ] `swarm-config.json` has no material `TBD` values.
- [ ] Protocol version is recorded.
- [ ] Orchestrator and Worker role files exist.
- [ ] Current state is `READY_TO_COMMISSION` or later.
- [ ] Decision register contains commissioning decisions.
- [ ] Open questions contain only genuine unresolved items.
- [ ] Work queue has a clear first executable task.
- [ ] `python scripts/validate_swarm.py` passes.

## Channels

- [ ] Substantive channel exists.
- [ ] Notices channel exists.
- [ ] Both agents can read the channels they are expected to use.
- [ ] Active-thread read behavior is understood.

## Orchestrator boot

- [ ] Read config/protocol/state.
- [ ] Completed owner interview.
- [ ] Completed external role/prompt research or recorded explicit opt-out.
- [ ] Owner approved role design.
- [ ] Can state Worker security boundary accurately.

## Worker boot

- [ ] Read `CLAUDE.md` and `AGENTS.md`.
- [ ] Returned BOOTLOAD.
- [ ] BOOTLOAD matches repository.
- [ ] Understands direct-owner confirmation rule.
- [ ] Understands fresh/intervening-change rule.

## Smoke tests

- [ ] Read-only work item test passed.
- [ ] State disagreement test passed.
- [ ] Security challenge test passed.
- [ ] Intervening commit test passed.
- [ ] Restart/recovery test passed.

## Commissioning acceptance

- [ ] Owner confirms the swarm is commissioned.
- [ ] Orchestrator updates `state/CURRENT_STATE.md` to `COMMISSIONED`.
- [ ] Worker posts `IDLE — commissioning complete, awaiting first bounded work item`.
