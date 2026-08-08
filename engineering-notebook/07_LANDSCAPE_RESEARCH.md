# Landscape Research — Open-Source Agent and Control-Plane Patterns

**Research date:** 2026-08-07

**Question:** Is there already an open-source product that performs the complete Swarm Manager outcome? If not, what should we adopt or learn from rather than rebuilding blindly?

## Conclusion

No verified single open-source product found in this pass covers the entire requested lifecycle:

- outcome-driven swarm/team design;
- reusable blueprint library + custom team builder;
- separate Ubuntu identity provisioning through the Owner's local configuration system;
- GitHub repository/access provisioning;
- Slack channel/membership provisioning;
- universal versioned protocol distribution;
- per-agent platform/config/security provisioning;
- per-swarm modular dashboard;
- automated cross-agent commissioning/role attestation;
- ongoing reconcile/update lifecycle;
- archive-before-destroy deprovisioning.

**Recommendation:** Continue Swarm Manager design, but explicitly evaluate Agyn and Agno before implementing a custom agent-runtime/security layer. Borrow control-plane patterns from Crossplane/Backstage/Temporal/AWX and visual-builder ideas from Dify/Flowise.

## Closest runtime/control-plane candidates

### Agyn

- Site/docs: https://agyn.io/ and https://docs.agyn.io/
- Open-source, AGPL-3.0.
- Kubernetes-native runtime/control plane for agents such as Claude and Codex.
- Public docs describe Terraform-managed organizations, agents, agent roles, MCPs, skills, hooks, environment, init scripts, volumes, runners, apps, models, secrets, and permissions.
- Strong zero-trust/credential-isolation model; real credentials are kept outside the agent sandbox and injected by gateways.
- Team-oriented material describes role separation, communication rules, GitHub-native work, tracing, and task visibility.

**Fit:** very strong for secure runtime/isolation and agents-as-code.

**Gap relative to Swarm Manager:** Kubernetes-centric; no verified full ownership of the Owner's local Unix identity manager, GitHub repo creation lifecycle, Slack topology provisioning, Swarm OS protocol registry, per-swarm dashboard composition, or archive/deprovision transaction.

**Adopt/Adapt/Build:** **Adapt / possibly Adopt as one runtime provider.** Do not rebuild its isolation/security primitives without an evaluation.

### Agno

- GitHub: https://github.com/agno-agi/agno
- Apache-2.0.
- Describes itself as an SDK for building, running, and managing agent platforms with a single control plane.
- Features include API services, memory/storage, 100+ integrations, human approval, OpenTelemetry, RBAC/multi-tenancy, scheduling, and Slack/Telegram/WhatsApp/Discord/A2A interfaces.

**Fit:** useful agent-platform abstraction and observability/integration layer.

**Gap:** not observed as a full infrastructure lifecycle manager for local OS identities + external collaboration/repo provisioning + archive/deprovision.

**Adopt/Adapt/Build:** **Adapt; evaluate runtime/provider use.**

## Multi-agent orchestration frameworks

### CrewAI

- GitHub: https://github.com/crewAIInc/crewAI
- MIT licensed.
- Role-based multi-agent Crews plus event-driven Flows.
- Strong agent/task design patterns and production workflow concepts.
- Commercial AMP provides a control plane, but the open-source core is primarily an orchestration framework.

**Use here:** blueprint/role/workflow inspiration, not fleet provisioning foundation.

### Microsoft Agent Framework

- GitHub: https://github.com/microsoft/agent-framework
- Successor recommended by Microsoft for new users instead of AutoGen, which is now maintenance-mode.
- Supports production-grade agents and multi-agent workflows in Python/.NET with sequential, concurrent, handoff, and group collaboration patterns.

**Use here:** runtime/provider interoperability and multi-agent workflow patterns.

### LangGraph

- GitHub: https://github.com/langchain-ai/langgraph
- Low-level framework for long-running stateful agents, graphs, memory/persistence, branching/subgraphs.

**Use here:** stateful workflow patterns; not external swarm infrastructure provisioning.

## Visual agent/application builders

### Dify

- GitHub: https://github.com/langgenius/dify
- Visual workflow/agent platform, model management, RAG, tools, observability, APIs, self-hosting.
- 2026 experimental Dify Agent work adds Linux-sandbox agent building via UI.
- License is the Dify Open Source License based on Apache 2.0 with additional conditions.

**Use here:** UX ideas for visual/conversational agent construction and application publishing.

**Caution:** security notes in the experimental agent release explicitly warn that strict agent isolation was not yet complete in that release; do not treat it as the desired security baseline.

### Flowise

- GitHub: https://github.com/FlowiseAI/Flowise
- Apache-2.0.
- Visual AI agent/workflow builder with API/CLI/SDK, tracing/analytics, evaluations, human-in-loop, teams/workspaces.

**Use here:** visual-builder/module UX and plugin/component patterns.

## Persistent single-agent runtime

### Hermes Agent

- GitHub: https://github.com/NousResearch/hermes-agent
- MIT licensed.
- Persistent self-hosted agent with memory, self-created skills, cron/scheduling, terminal/UI, and messaging gateways including Slack.

**Use here:** memory/skills/runtime-adapter ideas.

**Gap:** primarily a persistent agent, not a declarative team/resource lifecycle manager.

## Architecture-pattern projects

### Crossplane

- GitHub: https://github.com/crossplane/crossplane
- Apache-2.0 CNCF project.
- Framework for building extensible declarative control planes and orchestrating resources across environments.

**Pattern to borrow:** desired state, composition, providers, observe/reconcile loops, resource conditions.

### Backstage

- GitHub: https://github.com/backstage/backstage
- Apache-2.0.
- Open developer portal with software catalog, software templates, TechDocs, and plugin ecosystem.

**Pattern to borrow:** understandable catalog of reusable blueprints/templates, extensible plugin UI, human-friendly scaffolding experience.

### Temporal

- GitHub: https://github.com/temporalio/temporal
- MIT licensed.
- Durable execution platform with replayable workflow history, retries, and user-hosted activities.

**Pattern to borrow:** resilient long-running lifecycle orchestration with recoverable partial failure.

**Decision:** do not require Temporal in MVP until complexity proves it necessary; preserve an engine interface so it can be adopted later.

### AWX

- GitHub: https://github.com/ansible/awx
- Web UI + REST API + task engine over Ansible.

**Pattern to borrow:** automation controller separation among user interface, API, inventories/credentials, and job execution.

## Other emerging work worth watching

### Agyn research

A 2026 paper describes Agyn as an open-source platform for stateful on-demand agent execution, agent definition as code, Terraform provisioning, zero-trust access, and model/cloud agnosticism. This reinforces the idea that Swarm Manager should treat agent runtime as a provider and concentrate its differentiation on team/lifecycle composition across systems.

### Swarm Skills

A 2026 research proposal treats multi-agent roles, workflows, execution bounds, and coordination behavior as portable distributable assets. That direction aligns with Swarm Manager's blueprint + universal-protocol model, although any self-evolution behavior should remain subject to explicit governance rather than silently rewriting live coordination rules.

## Proposed build-vs-buy evaluation gate

Before implementing the runtime/provider layer, run a bounded proof-of-fit for:

1. **Agyn** — can it run the desired local agent types on this host/environment, and can Swarm Manager drive it declaratively without surrendering the broader lifecycle?
2. **Agno** — can it simplify the runtime/API/memory/observability layer for non-Kubernetes deployments?
3. **Native adapters** — what automation is actually possible for ChatGPT web and Claude Code under their platform security constraints?

The product should remain provider-neutral whichever path wins.
