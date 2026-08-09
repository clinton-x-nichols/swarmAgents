# Program Charter and Principles

## Working product name

**Swarm Manager**

## Outcome

Create an open-source, local-first **swarm lifecycle control plane** that lets a human start with an intended outcome, select or design an agent swarm, and have the system provision, commission, operate, evolve, archive, and safely deprovision the resources required by that swarm.

The human should not need to manually create Linux identities, Slack channels, GitHub repositories, agent bootstrap files, permissions, protocol configuration, or commissioning tests for each new swarm.

## Primary user experience

The Swarm Manager UI listens on **port 5015** and presents a clean, white, Google/Material-style interface.

A normal create flow is:

1. describe what the swarm must accomplish;
2. choose a suitable existing swarm blueprint or invoke the Swarm Builder;
3. review/customize roles, personalities, responsibilities, relationships, platforms, identities, tools, permissions, dashboard modules, and protocol versions;
4. preview a provisioning plan;
5. apply the plan;
6. watch automated provisioning and commissioning checks;
7. receive a commissioned swarm ready for direct human work.

A normal retirement flow archives the durable record and resources first, then revokes/deprovisions them under explicit destructive-action controls.

## First-class requirements accepted by the Owner

### Modularity

Modularity is architectural, not cosmetic. The system must support extension without broad rewrites at three visible levels:

1. **Control-plane modules** — Slack, GitHub, local identity/configuration management, protocol registry, agent runtime platforms, secrets/policy, workflow execution, observability.
2. **Swarm modules** — optional dashboard capabilities such as engineering notebook, project management, evidence views, decision views, protocol status, or future modules.
3. **Agent modules** — role/persona, runtime/platform, tool access, skills, MCP servers, command policy, memory behavior, protocol subscriptions, and security controls.

The design should permit deeper modularity where useful.

### Declarative lifecycle

The system should model **what a swarm should be** separately from the procedural commands required to create it. The durable swarm specification is the desired state; provider modules reconcile real systems toward that state.

### Blueprint library + builder

Provide both:

- a library of understandable, reusable swarm blueprints such as research, software development, documentation, training, or mixed decision-support swarms; and
- a **Swarm Builder** for designing a new blueprint from first principles when the library does not fit.

Blueprints should explain their roles, relationships, evidence model, expected tools, and use cases before selection.

### External-system provisioning

The control plane must be able to coordinate creation/configuration of at least:

- Ubuntu/Linux user identities through the existing Cloud Configuration Manager;
- GitHub repositories and permissions;
- Slack substantive/status channels and access;
- agent bootstrap/configuration material;
- agent runtime sessions/processes where the target platform permits it;
- per-swarm dashboards and selected dashboard modules.

### Universal protocols

Some operating rules are universal platform assets rather than copied, hand-edited project files. Initial examples are:

- Slack/agent communication protocol;
- memory protocol.

These should be published through versioned APIs. A newly provisioned swarm retrieves the current approved version during commissioning and records the exact version/hash it loaded. Later upgrades should be deliberate and auditable rather than silently changing behavior underneath a running swarm.

### Durable engineering record

This root engineering notebook is the parent project's durable design/history layer. Each provisioned swarm receives its own separate notebook through Swarm OS.

### Automated commissioning

Provisioning is not complete merely because resources were created. A swarm must pass automated commissioning checks, including as applicable:

- agents can read the correct GitHub repo;
- authorized writes work and unauthorized writes do not;
- agents can reach the required Slack channels;
- agent-to-agent test messages succeed;
- protocol APIs are reachable and loaded versions/hashes match the requested specification;
- each agent can report its identity, role, counterpart relationships, security boundaries, and current swarm state;
- durable state/notebook paths exist;
- required integrations are healthy.

### Archive before destroy

Retirement must separate **archive** from **destruction**. Capture enough information to reconstruct or audit the swarm before deleting/revoking resources. Destructive actions remain Owner-gated.

### Open-source constraint

If an existing open-source product already satisfies the complete outcome, prefer adopting it to building a duplicate. If no single product fits, reuse strong open-source components and patterns where they reduce risk without forcing the product away from its outcome.

## Architectural principles

1. **Core orchestrates; providers provide behavior.**
2. **Desired state is data.** Blueprints/specifications must not require hard-coded provisioning flows.
3. **Plan before apply.** Show exactly which external resources and permissions will change.
4. **Idempotent where possible.** Re-running reconciliation should converge rather than duplicate resources.
5. **Provider-neutral contracts.** ChatGPT/Claude are initial adapters, not permanent assumptions.
6. **Protocol versions are immutable artifacts.** “Latest” is a selection operation, not a hidden runtime dependency.
7. **Least privilege by default.** Agent capability and command policy are explicit configuration.
8. **Secrets stay out of prompts, Git, and agent-readable config whenever possible.**
9. **Commission before handoff.** Created is not ready.
10. **Retire before destroy.** Revocation/deletion is the final phase, not the first.
11. **Every lifecycle transition is auditable.**
12. **UI and API are peers.** Every meaningful UI operation should map to a stable API/service operation so automation does not depend on the UI.

## Definition of done — product-level draft

The project is not finished until a user can, from the Swarm Manager UI, create a useful swarm from a blueprint or Builder, have all required resources provisioned and commissioned automatically, use the resulting swarm, then archive and deprovision it safely — while adding a new provider/module without rewriting core lifecycle logic.

This definition will be refined into release milestones after the proposed architecture is reviewed.
