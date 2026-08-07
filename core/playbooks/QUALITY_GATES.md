# Quality Gates

## Gate 1 — Commissioning quality

Before real work:

- roles are distinct;
- owner authority is explicit;
- systems of record are ordered;
- channels are accessible;
- Worker security constraints are known;
- current-state file exists;
- bootstrap/restart test passes.

## Gate 2 — Work-order quality

Before dispatch:

- objective is observable;
- scope and prohibited writes are explicit;
- authoritative sources are named;
- open decisions are isolated;
- continuation rule is present;
- expected evidence is specified.

## Gate 3 — Worker result quality

Before Orchestrator acceptance:

- result addresses the objective;
- evidence exists;
- claims are traceable;
- repository base was fresh before write;
- unrelated changes are absent;
- blockers are precise;
- status language is accurate.

## Gate 4 — Independent verification

For consequential work, the Orchestrator or Reviewer independently checks the most load-bearing claims.

Examples:

- fetch the commit rather than trust its SHA/summary;
- read the modified source rather than trust “updated successfully”;
- rerun a test or inspect test output;
- verify citations against primary sources;
- compare artifact output against acceptance criteria.

## Gate 5 — Closure

Do not mark VERIFIED/CLOSED until:

- implementation is complete;
- required evidence is complete;
- independent review is accepted;
- bounded defects are corrected or explicitly deferred by the correct authority;
- durable state reflects the final disposition.
