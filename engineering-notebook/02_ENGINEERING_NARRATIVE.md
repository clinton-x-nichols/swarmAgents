# Engineering Narrative

## 2026-08-07 — From reusable Swarm OS to Swarm Manager control plane

The `swarmAgents` repository began as a reusable Swarm Operating System and factory: stable `core/` behavior plus small swarm-type overlays, instantiated into separate live repositories.

During the 2026-08-07 design session, the Owner clarified that the desired product is broader than a file/template factory. The long-term target is **Swarm Manager**: an Ansible-like lifecycle control plane for AI swarms, with a web UI on port 5015 and automated integration with the surrounding Ubuntu host and external services.

The key shift is from **copy a template** to **declare an organization and reconcile it into existence**.

### Owner-described lifecycle

A human begins with an outcome, for example needing a team to research a technical question and produce a security recommendation. The system should help identify an existing swarm blueprint or construct a new one. The blueprint defines roles, personalities, responsibilities, relationships, evidence expectations, and required capabilities.

Once customized, Swarm Manager should perform the infrastructure work underneath the design:

- allocate/provision separate local identities through the existing Cloud Configuration Manager;
- create the swarm's GitHub repository and access model;
- create fit-for-purpose Slack channels and membership;
- apply role/persona/tool/configuration files to each agent identity;
- connect required universal protocol APIs such as Slack coordination and memory rules;
- create the swarm-specific dashboard with selected modules;
- launch or prepare each agent runtime where technically possible;
- run automated commissioning tests;
- hand the commissioned swarm to the Owner.

At end of life, Swarm Manager performs the inverse process deliberately: capture/archive the durable record, revoke access, archive communication/resources where possible, and only then delete/deprovision under explicit Owner confirmation.

### Why modularity became the dominant architectural concern

The Owner repeatedly generated new module ideas while describing the product: different LLM platforms, different swarm types, different per-swarm dashboard modules, and increasingly granular per-agent controls. That is evidence that a monolithic provisioning script would age badly.

The architecture therefore needs stable contracts at multiple layers so that a new provider or feature becomes an added module rather than a cross-cutting rewrite.

### Engineering notebook requirement

The Owner explicitly required a durable engineering notebook containing decisions, successful and abandoned approaches, failures, experiments, rationale, and current design intent. The structure in `ddcrm-risk-management/engineering-notebook/` was reviewed as a proven pattern. Its **structure and operating discipline** were adapted here; DDCRM risk-management content was not imported.

### External landscape check

A current open-source landscape pass found several strong adjacent products but no verified single product that performs the full described lifecycle.

The most important discovery is **Agyn**, an open-source Kubernetes-native agent management runtime with Terraform-managed agents, skills, MCPs, runners, security/isolation, and agent-team concepts. It is materially closer to Swarm Manager's runtime/security layer than CrewAI-style orchestration libraries. **Agno** is also relevant as a framework/control plane for building, running, and managing agent platforms with RBAC, memory, integrations, and scheduling.

However, based on current public documentation, neither product appears to own the complete local identity + Slack topology + GitHub repository + universal protocol + per-swarm dashboard + commissioning + archive/deprovision lifecycle described by the Owner. They should therefore be evaluated as provider/runtime candidates rather than assumed replacements for Swarm Manager.

### Current design stance

Daisy proposes treating Swarm Manager as a **declarative lifecycle control plane**:

- a versioned `SwarmSpec` captures desired state;
- a planner expands the spec into resource changes;
- lifecycle workflows execute provider operations;
- reconcilers compare desired and observed state;
- provider adapters own external-system specifics;
- commissioning proves that the resulting swarm works;
- archive/deprovision handles retirement safely.

This proposal is detailed in `06_PROPOSED_ARCHITECTURE.md` and remains pending Owner review.
