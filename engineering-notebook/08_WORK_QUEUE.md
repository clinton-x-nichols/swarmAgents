# Work Queue

This queue covers the `swarmAgents` parent project / Swarm Manager product, not any instantiated swarm.

| ID | Work item | Owner | Status | Depends on | Evidence / output |
|---|---|---|---|---|---|
| SM-W001 | Establish parent-project engineering notebook and capture charter/decisions. | Daisy | IMPLEMENTATION_COMPLETE | none | Root `engineering-notebook/` structure and records. |
| SM-W002 | Produce proposed Swarm Manager architecture and build-vs-buy landscape review. | Daisy | IN_PROGRESS | SM-W001 | Original proposal plus `10_ARCHITECTURE_REVIEW_2026_08_08.md`; deeper research underway after Owner feedback. |
| SM-W003 | Owner architecture review: accept, modify, reject, or defer proposed decisions SM-P001–SM-P013. | Owner | BLOCKED | SM-W002 refinement | Updated decision register / architecture direction. |
| SM-W004 | Inventory existing Cloud Configuration Manager interfaces and host constraints. | Daisy / Worker | READY | none | API/CLI capability map; closes or narrows host/provider questions. |
| SM-W005 | Technical proof-of-fit: Agyn, Agno, Microsoft Agent Framework, OpenAI Agents SDK, Hermes, and native runtime adapters. | Daisy / Worker | READY | none | Runtime capability/security/integration matrix. |
| SM-W006 | Define v1 `SwarmSpec`, blueprint schema, provider capability contract, resource ledger, and lifecycle state machine. | Daisy | READY_FOR_DESIGN | SM-W002 | Versioned schemas and examples; no implementation yet. |
| SM-W007 | Define persistent lifecycle-step model, idempotency rules, compensation semantics, and commissioning evidence model. | Daisy | READY_FOR_DESIGN | SM-W002 | Workflow/state schema and failure-recovery rules. |
| SM-W008 | Produce first executable headless vertical-slice plan for a two-agent Research & Decision swarm. | Daisy | BLOCKED | SM-W004, SM-W006, SM-W007 | Bounded API/CLI implementation work orders. |
| SM-W009 | Implement lifecycle core and first provider set: Cloud Configuration Manager, GitHub, Slack, Protocol Registry, Ansible Runner host automation. | Worker | BLOCKED | SM-W008 | Provider tests + resource ledger evidence. |
| SM-W010 | Implement ChatGPT/Claude runtime adapters, Boot Manifest compilation, and commissioning suite. | Worker + Daisy review | BLOCKED | SM-W005, SM-W009 | End-to-end commissioning evidence. |
| SM-W011 | Prove create→commission→reconcile→archive vertical slice without destructive deletion. | Worker + Daisy review | BLOCKED | SM-W010 | Verified lifecycle evidence. |
| SM-W012 | Implement minimal light UI on port 5015 as a client of stable lifecycle APIs. | Worker | BLOCKED | SM-W011 | Clean Google/Material-style fleet/create/plan/job/status workflow. |
| SM-W013 | Implement richer Blueprint Catalog, Swarm Builder, and optional per-swarm dashboard modules. | Worker + Daisy review | BLOCKED | SM-W012 | Modular catalog/builder/dashboard capabilities. |
| SM-W014 | Implement destructive retirement after archive with explicit Owner gate and residual-resource verification. | Worker + Daisy review | BLOCKED | SM-W011 | Verified archive + destroy evidence. |

## Current queue head

Independent work that should continue now:

1. **SM-W002** — finish architecture refinement and research.
2. **SM-W004** — inventory Cloud Configuration Manager and host integration surfaces.
3. **SM-W005** — runtime/provider proof-of-fit.
4. **SM-W006 / SM-W007** — design schemas and failure semantics; these are architecture work, not implementation authorization.

UI implementation is intentionally downstream of the proven headless lifecycle slice.

## Status rule

Do not mark `VERIFIED/CLOSED` merely because a document exists. Architecture becomes accepted only after Owner review; implementation becomes verified only after independent evidence review.
