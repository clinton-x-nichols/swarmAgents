# Work Orders, Handoffs, and Continuation

## Bounded work beats vague delegation

A Worker should receive a bounded task, not “go finish the project.”

Use `templates/work-order.md`.

## Required work-order fields

- ID
- title
- objective
- authorized scope
- authoritative sources
- allowed writes
- prohibited writes
- owner decisions already settled
- owner decisions still open
- expected output/evidence
- continuation rule
- notice format

## Continuation rule

Every work order should say what happens when a sub-item is blocked.

Default:

> Mark only the exact blocked item. Continue all independent authorized work. Ask a precise question with source/conflict references. Do not create an approval stop for unaffected work.

## Review loop

1. Worker returns result + evidence.
2. Orchestrator verifies key claims independently.
3. Orchestrator either:
   - accepts;
   - accepts with bounded corrections;
   - rejects with exact defects;
   - isolates an owner decision.
4. Corrections stay in the same work item unless scope truly changed.
5. Avoid creating a new work number merely to fix a defect in the existing work.

## Consolidate owner decisions

When analysis across several work items exposes multiple genuine owner decisions, collect them into a single decision bundle.

For each decision include:

- exact question;
- why it cannot be resolved from accepted sources;
- options;
- strongest evidence each way;
- Orchestrator recommendation;
- affected artifacts;
- dependencies on other decisions;
- what can proceed if deferred.

This prevents the Owner from becoming the message bus.
