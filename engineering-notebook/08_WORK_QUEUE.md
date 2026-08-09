# Work Queue

This queue covers the `swarmAgents` parent project / Swarm Manager product, not any instantiated swarm.

| ID | Work item | Owner | Status | Depends on | Evidence / output |
|---|---|---|---|---|---|
| SM-W001 | Establish parent-project engineering notebook and capture charter/decisions. | Daisy | IMPLEMENTATION_COMPLETE | none | Root `engineering-notebook/` structure and records. |
| SM-W002 | Produce proposed Swarm Manager architecture and build-vs-buy landscape review. | Daisy | IN_PROGRESS | SM-W001 | Current architecture refinements, research, and Owner feedback integrated. |
| SM-W003 | Owner architecture review: accept, modify, reject, or defer proposed decisions SM-P001–SM-P018. | Owner | BLOCKED | SM-W002 refinement | Updated decision register / architecture direction. |
| SM-W004 | Inventory the existing Cloud Configuration Manager object model and define the API contract Swarm Manager will require from it. | Daisy / Worker | READY | none | Capability map and API requirements; narrows identity/config provider design. |
| SM-W005 | Technical proof-of-fit: Agyn, Agno, Microsoft Agent Framework, OpenAI Agents SDK, Hermes, and native runtime adapters. | Daisy / Worker | READY | none | Runtime capability/security/integration matrix. |
| SM-W006 | Define v1 `SwarmSpec`, blueprint schema, provider capability contract, resource ledger, and lifecycle state machine. | Daisy | READY_FOR_DESIGN | SM-W002 | Versioned schemas and examples; no implementation yet. |
| SM-W007 | Define persistent lifecycle-step model, idempotency rules, compensation semantics, and commissioning evidence model. | Daisy | READY_FOR_DESIGN | SM-W002 | Workflow/state schema and failure-recovery rules. |
| SM-W008 | Produce the first executable headless vertical-slice plan using the evolving **Explainer Swarm** proof of concept. The first slice may use a reduced role set if needed, but must preserve the full blueprint evolution path. | Daisy | BLOCKED | SM-W004, SM-W006, SM-W007, SM-W019 | Bounded API/CLI implementation work orders. |
| SM-W009 | Implement lifecycle core and first provider set: Cloud Configuration Manager API provider, GitHub, Slack, and Protocol Registry. | Worker | BLOCKED | SM-W008, SM-W021 | Provider tests + resource ledger evidence. |
| SM-W010 | Implement ChatGPT/Claude runtime adapters, Boot Manifest compilation, and commissioning suite. | Worker + Daisy review | BLOCKED | SM-W005, SM-W009 | End-to-end commissioning evidence. |
| SM-W011 | Prove create→commission→reconcile→archive vertical slice with the Explainer Swarm without destructive deletion. | Worker + Daisy review | BLOCKED | SM-W010 | Verified lifecycle evidence. |
| SM-W012 | Implement minimal light Swarm Manager UI on port 5015 as a client of stable lifecycle APIs, with the Blueprint Library as the normal provisioning entry point. | Worker | BLOCKED | SM-W011 | Clean Google/Material-style library/select/configure/plan/job/status workflow. |
| SM-W013 | Implement the separate **Swarm Creation Tool** for editing roles, relationships, transaction logic, priorities, gates, defaults, and commissioning rules; save the result as a versioned blueprint in the library. | Worker + Daisy review | BLOCKED | SM-W012, SM-W020 | Modular authoring tool and versioned blueprint output. |
| SM-W014 | Implement destructive retirement after archive with explicit Owner gate and residual-resource verification. | Worker + Daisy review | BLOCKED | SM-W011 | Verified archive + destroy evidence. |
| SM-W015 | Define Token Monitor telemetry schema, runtime capability hooks, efficiency scoring methodology, capture/redaction levels, and report-card model. | Daisy / Worker | FUTURE_DESIGN | SM-W005, dashboard module framework | Versioned token-observability design and test fixtures. |
| SM-W016 | Define Memory Manager data model, durable-memory browser/governance rules, recurrence configuration, recall challenge protocol, and memory-drift classifications. | Daisy / Worker | FUTURE_DESIGN | memory protocol maturity, dashboard module framework | Versioned memory-reconciliation design and UI contract. |
| SM-W017 | Define and implement optional Token & Memory Steward swarm role/agent, including recommendation authority boundaries and operational handoffs. | Daisy / Worker | FUTURE | SM-W015, SM-W016 | Role specification, boot manifest requirements, evidence and review tests. |
| SM-W018 | Implement Token Monitor and Memory Manager dashboard modules, with swarm summary and per-agent drill-down; final one-page-vs-separate-page layout decided from usability evidence. | Worker + Daisy review | FUTURE | SM-W015, SM-W016, dashboard module framework | Working modules, telemetry/reconciliation tests, user-management flows. |
| SM-W019 | **Create and continuously evolve the Explainer Swarm blueprint as the principal product proof of concept.** Begin with the Presenter/SME/Researcher/Curriculum/Writer/Reviewer model and refine roles, interactions, optional modules, and commissioning as Swarm Manager matures. | Daisy + Owner review | READY | none | Versioned Explainer blueprint history and POC acceptance notes. |
| SM-W020 | Research and select an open-source visual graph/workflow authoring component for the Swarm Creation Tool. It must support editable connections, logic gates/conditions, priorities, and extensibility without becoming the lifecycle runtime itself. | Daisy / Worker | READY | none | OSS comparison, license/provenance, proof-of-fit, recommendation. |
| SM-W021 | Design and later build an API interface for the existing Cloud Configuration Manager so Swarm Manager can reserve/create/configure/inspect/retire agent identities and related runtime configuration through a stable provider contract. | Owner / Worker | PLANNED | SM-W004 | API contract, implementation, authentication model, tests. |
| SM-W022 | Design per-swarm UI deployment and port allocation: every provisioned swarm receives a UI, and provisioning selects/reserves an available port in the 6000–7000 range. | Daisy / Worker | READY_FOR_DESIGN | SM-W006 | Port-allocation model, UI deployment contract, lifecycle/retirement semantics. |
| SM-W023 | Define the dense-information UI interaction standard for Swarm Manager and swarm dashboards: small readable type, resizable panes/splitters, scrollbars, contextual popovers/tooltips, and efficient use of horizontal/vertical space. | Daisy / Worker | FUTURE_DESIGN | SM-W012 | UI design standard and component examples. |

## Current queue head

Independent work that should continue now:

1. **SM-W002** — finish architecture refinement and research.
2. **SM-W004** — define what the Cloud Configuration Manager API must expose.
3. **SM-W005** — runtime/provider proof-of-fit.
4. **SM-W006 / SM-W007** — design schemas and failure semantics; these are architecture work, not implementation authorization.
5. **SM-W019** — begin the Explainer Swarm blueprint and keep evolving it as the standing proof of concept.
6. **SM-W020** — evaluate reusable OSS workflow/graph editors for the Swarm Creation Tool.
7. **SM-W022** — design per-swarm UI deployment and 6000–7000 port allocation.

Normal provisioning is now **library-first**. Swarm authoring is a separate tool and workstream.

The Token Monitor, Memory Manager, and Token & Memory Steward are accepted future capabilities, but implementation is intentionally downstream of the stable lifecycle APIs, runtime observability capabilities, and dashboard module framework.

## Status rule

Do not mark `VERIFIED/CLOSED` merely because a document exists. Architecture becomes accepted only after Owner review; implementation becomes verified only after independent evidence review.
