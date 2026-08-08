# Landscape Research — Open-Source Agent and Control-Plane Patterns

**Research dates:** 2026-08-07 through 2026-08-08

**Question:** Is there already an open-source product that performs the complete Swarm Manager outcome? If not, what should we adopt or learn from rather than rebuilding blindly?

## Conclusion

No single product in the reviewed open-source set was verified to cover the complete requested lifecycle:

- outcome-driven swarm/team design;
- reusable blueprint library + custom team builder;
- separate Ubuntu identity provisioning through the Owner's local configuration system;
- GitHub repository/access provisioning;
- Slack channel/membership provisioning;
- universal versioned protocol distribution;
- heterogeneous per-agent runtime/config/security provisioning;
- commissioning and role/protocol attestation;
- ongoing desired-vs-observed reconciliation;
- archive-before-destroy retirement.

**Recommendation:** Continue Swarm Manager, but build only the lifecycle/control-plane layer that is actually missing. Adopt runtime and infrastructure components behind provider contracts where they fit.

## Most important architecture references

### Ansible Runner

Official Runner documentation describes it as an interface intended for automation/tooling that needs to invoke Ansible and consume results. It supports Python and CLI integration, structured job events/artifacts/status, callbacks/plugins, and process-isolation/execution-environment options.

**Use here:** general host/configuration execution backend for operations not already owned by a purpose-built service.

**Do not use it to replace:** Cloud Configuration Manager identity provisioning or API-backed resources that already have authoritative providers.

### Crossplane

Current documentation centers on managed resources, providers, reconciliation, conditions/observability, and desired-state ownership of external resources.

**Use here:** desired/observed state model, provider ownership, conditions, safe reconciliation, external-resource IDs.

### Temporal

Temporal documents durable execution that resumes workflows after crashes, network failures, or infrastructure outages.

**Use here:** possible future lifecycle-workflow backend when a simple persistent local step engine becomes insufficient.

### Backstage

Backstage provides a software catalog, software templates/scaffolding, and a plugin architecture. Its catalog explicitly models entities and relationships and its templates support push-button creation workflows.

**Use here:** Blueprint Catalog, Builder/scaffolding mental model, later plugin/module UX.

## Agent runtime/control-plane candidates

### Agyn

Agyn is close to the **secure runtime / agents-as-code** portion of the desired platform. Current public material describes Kubernetes-native execution, Terraform-managed agents/resources, and zero-trust/least-privilege design.

**Fit:** strong possible runtime provider for isolated agent execution.

**Gap:** not verified as the full local identity + GitHub + Slack + protocol + commissioning + retirement lifecycle manager.

**Adopt/Adapt/Build:** Adapt or adopt behind runtime-provider contract after proof-of-fit.

### Agno AgentOS

Current Agno documentation describes AgentOS as runtime + control plane, with API endpoints, RBAC, memory/knowledge/session management, traces, approvals, schedules, and a management UI. It also explicitly documents multi-framework support, including serving agents built with other frameworks.

**Fit:** strong evidence that runtime/control-plane services can be reused without making one framework the Swarm Manager core.

**Gap:** not verified to manage the Owner's external organization lifecycle across Ubuntu identities, GitHub, Slack topology, protocol registry, and archive/deprovision.

### Microsoft Agent Framework

Microsoft's current open framework supports Python/.NET agents and graph/workflow patterns such as sequential, concurrent, handoff, and group collaboration. Documentation includes agents, tools, skills, memory/persistence, workflows, providers, A2A integration, and hosting.

**Fit:** runtime provider and workflow/orchestration option for swarms that choose it.

**Architecture implication:** another reason not to hard-wire lifecycle to CrewAI/AutoGen-era abstractions.

### OpenAI Agents SDK

Current official SDK documentation includes agents, tools, handoffs, guardrails, sessions, MCP integration, sandbox agents, human-in-loop, and tracing.

**Fit:** runtime provider for API-hosted OpenAI-oriented agents.

**Gap:** it intentionally focuses on agent execution/orchestration rather than provisioning the external organization around a swarm.

### CrewAI

Current CrewAI documentation covers agents, crews, flows, guardrails, memory/knowledge, state persistence, human-in-loop, and production automation concepts.

**Use here:** blueprint/role/process inspiration and optional runtime provider.

### Hermes Agent

Current Hermes material describes a persistent self-hosted agent with memory, self-created skills, messaging surfaces including Slack, isolated subagents, scheduling, and multiple sandbox backends.

**Use here:** persistent runtime option, memory/skills/sandbox ideas.

**Gap:** primarily an agent runtime, not the full swarm organization lifecycle manager.

## Visual builders

### Flowise

Official project documentation describes an open generative-AI platform with visual builders, tracing/analytics, evaluations, human-in-loop, APIs/CLI/SDK, and teams/workspaces.

**Use here:** later Swarm Builder UX inspiration.

### Dify

Dify remains relevant as a visual workflow/application platform and product-design reference.

**Use here:** later builder/product UX concepts, not the infrastructure lifecycle core.

## Architecture conclusion

The strongest design is deliberately compositional:

```text
Swarm Manager lifecycle core
  ├── Cloud Configuration Manager provider
  ├── Ansible Runner host-automation provider
  ├── GitHub provider
  ├── Slack provider
  ├── Protocol Registry
  └── Runtime providers
       ├── ChatGPT web/bootstrap
       ├── Claude Code
       ├── OpenAI Agents SDK
       ├── Microsoft Agent Framework
       ├── Agno
       ├── Agyn
       ├── Hermes
       └── future runtimes
```

Swarm Manager's defensible responsibility is composing and governing the whole lifecycle across these systems. It should not compete with every runtime framework by recreating their agent loops, sandboxes, tracing, memory engines, and orchestration primitives.

## Proof-of-fit gate before runtime implementation

Create a capability/security matrix for each candidate runtime:

- install/configure automation;
- launch/stop/resume automation;
- sandbox/isolation;
- tools/MCP support;
- memory semantics;
- bootstrap manifest support;
- attestation capability;
- Slack/communication capability;
- direct-human requirements;
- secret isolation;
- observability/tracing;
- licensing/deployment constraints.

The winning choice may differ by swarm blueprint; runtime plurality is an expected feature, not a temporary inconvenience.
