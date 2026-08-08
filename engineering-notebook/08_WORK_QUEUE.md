# Work Queue

This queue covers the `swarmAgents` parent project / Swarm Manager product, not any instantiated swarm.

| ID | Work item | Owner | Status | Depends on | Evidence / output |
|---|---|---|---|---|---|
| SM-W001 | Establish parent-project engineering notebook and capture 2026-08-07 charter/decisions. | Daisy | IMPLEMENTATION_COMPLETE | none | Root `engineering-notebook/` structure and records. |
| SM-W002 | Produce proposed Swarm Manager architecture and build-vs-buy landscape review. | Daisy | EVIDENCE_READY | SM-W001 | `06_PROPOSED_ARCHITECTURE.md`, `07_LANDSCAPE_RESEARCH.md`, architecture/UI visuals. |
| SM-W003 | Owner architecture review: accept, modify, reject, or defer proposed decisions SM-P001–SM-P007. | Owner | READY | SM-W002 | Updated decision register / architecture direction. |
| SM-W004 | Inventory existing Cloud Configuration Manager interfaces and host constraints. | Daisy / Worker | READY | none | API/CLI capability map; closes or narrows SM-Q001, Q005, Q014. |
| SM-W005 | Technical proof-of-fit: Agyn versus Agno versus native runtime adapters. | Daisy / Worker | READY | Owner guidance on Kubernetes useful but not required for research | Comparison with install/runtime/security/integration implications. |
| SM-W006 | Define v1 `SwarmSpec`, blueprint schema, provider capability contract, and lifecycle state machine. | Daisy | BLOCKED | SM-W003 architecture acceptance | Versioned schemas and acceptance examples. |
| SM-W007 | Produce first executable vertical-slice plan for two-agent Research & Decision swarm. | Daisy | BLOCKED | SM-W003, SM-W004, SM-W006 | Bounded implementation work orders. |
| SM-W008 | Implement Swarm Manager shell on port 5015 with Swarms/Blueprints/Builder/Protocols/Integrations/Jobs/Settings navigation. | Worker | BLOCKED | SM-W007 | Running UI + tests. |
| SM-W009 | Implement first provider set: identity, GitHub, Slack, protocol registry, ChatGPT/Claude runtime bootstrap. | Worker | BLOCKED | SM-W004, SM-W006, SM-W007 | Provider tests + commissioning evidence. |
| SM-W010 | Implement commissioning suite and READY gate. | Worker + Daisy review | BLOCKED | SM-W009 | End-to-end commissioning evidence. |
| SM-W011 | Implement archive/retirement manifest and non-destructive retirement flow. | Worker + Daisy review | BLOCKED | SM-W006 | Verified archive evidence; destructive deletion still Owner-gated. |

## Current queue head

The next Owner-facing action is **SM-W003: architecture review**. In parallel, SM-W004 and SM-W005 are independent research tasks and do not need to wait for every architecture decision.

## Status rule

Do not mark `VERIFIED/CLOSED` merely because a document exists. Architecture becomes accepted only after Owner review; implementation becomes verified only after independent evidence review.
