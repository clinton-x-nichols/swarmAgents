# Construction Notes

Use this file for durable technical reasoning, experiments, alternatives, successes, and failures that are too detailed for the compact decision register.

## 2026-08-07 — Control-plane framing

**Problem:** How should a product that provisions many different agent teams avoid becoming a collection of hard-coded scripts?

**Supported facts / requirements:**

- external systems will expand beyond initial ChatGPT/Claude, Slack, GitHub, and local Ubuntu identities;
- swarm dashboards will gain modules over time;
- agent configuration will gain new tool/security/memory options;
- create and destroy are not enough; the product will eventually need modify/upgrade/reconcile behavior;
- external resources can partially fail, drift, or change independently.

**Alternatives considered:**

1. **Imperative wizard:** UI directly calls a fixed sequence of provisioning commands.
   - Simple first demo.
   - Becomes brittle as integrations/options multiply.
   - Hard to resume after partial failure or compare actual versus desired state.

2. **Template generator only:** expand the existing `create_swarm.py` approach.
   - Useful for files/repositories.
   - Insufficient for lifecycle of external resources and long-running reconciliation.

3. **Declarative control plane:** versioned `SwarmSpec` + planner + provider adapters + lifecycle engine + observed-state reconciliation.
   - More architecture up front.
   - Strongest fit for modularity, idempotence, preview/plan, drift detection, upgrades, and deprovisioning.

**Recommendation:** Option 3. Keep the existing Swarm OS/profile assets as blueprint inputs rather than discarding them.

## 2026-08-07 — Universal protocol version semantics

**Problem:** Owner wants swarms to fetch the latest universal Slack/memory protocol from APIs during boot. If running swarms always dereference “latest,” behavior can change without an auditable swarm change.

**Recommendation:** Separate **selection** from **execution**.

1. At create/upgrade time, Swarm Manager asks the protocol registry for `latest-approved` or a user-selected version.
2. Registry returns immutable version metadata and a content digest.
3. The exact version/digest is written into the swarm's desired-state spec and commissioning record.
4. Agents fetch that exact version during bootstrap and attest the digest.
5. A later protocol release creates an available-upgrade signal; it does not silently mutate running swarms.

This preserves the Owner's centralized universal-protocol goal while keeping each swarm reproducible.

## 2026-08-07 — External product landscape

### Agyn

Agyn is the closest current open-source match to the **agent runtime/security** portion of the desired platform. Public documentation describes Kubernetes-native agent deployment, Terraform resources for agents, roles, MCPs, skills, hooks, environment, volumes, runners/apps, zero-trust networking, and credential isolation.

**Potential reuse:** agent runtime provider, isolation/security, agents-as-code, GitOps patterns.

**Mismatch:** Kubernetes-centric and does not appear to own the full local Ubuntu-user + Slack-channel + GitHub-repo + Swarm OS/protocol + per-swarm dashboard + archive/deprovision lifecycle.

### Agno

Agno describes itself as a runtime/control-plane platform for building, running, and managing agents. Current documentation also emphasizes multi-framework serving, which is evidence that Swarm Manager should not bind its lifecycle core to one orchestration framework.

**Potential reuse:** runtime provider, agent-service API, memory/observability patterns.

**Mismatch:** not observed as an infrastructure lifecycle manager for the Owner's full host/identity/Slack/GitHub provisioning model.

### CrewAI / Microsoft Agent Framework / OpenAI Agents SDK / LangGraph

These provide strong agent runtime/orchestration concepts: roles and flows, graph/workflow execution, handoffs, guardrails, sessions, sandboxes, tracing, memory/persistence, and human-in-loop patterns.

**Architecture implication:** do not build a universal proprietary agent loop. Treat these as optional runtime implementations behind a capability contract.

### Hermes Agent

Hermes is a strong persistent open-source runtime with memory, self-created skills, multiple messaging surfaces, subagents, and several sandbox backends.

**Potential reuse:** persistent runtime provider and memory/skills patterns.

**Mismatch:** primarily an agent runtime, not the lifecycle manager for the whole external organization around a swarm.

### Dify / Flowise

Strong visual agent/workflow builders and application platforms. Useful builder UX inspiration, not evidence that the Swarm Manager lifecycle problem is already solved.

### Backstage / Crossplane / Temporal / AWX / Ansible Runner

These are not direct competitors but are the most important infrastructure references:

- **Backstage:** catalog + software templates + plugins; useful for Blueprint Catalog and later UI-module thinking.
- **Crossplane:** desired/observed state, providers, reconcile loops, conditions, safe external-resource ownership.
- **Temporal:** crash/retry-resistant durable workflows; possible later workflow backend.
- **AWX:** controller separation between UI/API, credentials/inventory, and execution jobs.
- **Ansible Runner:** embeddable Python/CLI execution backend with structured status/events and process-isolation options; a strong fit for general host/configuration operations.

**Current conclusion:** the Swarm Manager differentiator is lifecycle composition across systems, not another agent runtime.

## 2026-08-07 — Engineering notebook structure import

**Source inspected:** `clinton-x-nichols/ddcrm-risk-management/engineering-notebook/`.

The DDCRM notebook uses a strong pattern: explicit index, charter/principles, engineering narrative, decision register, construction notes, specialized registers, and durable work history.

**Portable pattern adopted:** index + charter + narrative + decision register + construction notes + open questions + architecture proposal + landscape research + work queue + reconciliation log.

**Explicitly excluded:** all DDCRM risk-management decisions, work-order content, risk terminology, Confluence state, and implementation history.

## 2026-08-08 — First architecture presentation failed the emphasis test

**Observed failure:** The first user-facing architecture output emphasized a dense dark dashboard/poster. Although it contained many potentially useful future windows, it violated the Owner's accepted clean-white Google-style UI direction and, more importantly, displaced the requested architecture/functionality discussion.

**Owner correction:** focus on architecture and functionality first. UI should remain simple and light until the lifecycle model is proven.

**Root cause:** presentation was treated as the deliverable rather than as a visualization of an already-settled design.

**Durable correction:**

1. UI implementation is now sequenced after a headless create→commission→reconcile→archive lifecycle proof.
2. Architecture review separates lifecycle semantics from runtime-framework choices.
3. Future architecture visuals must explain control/data flow, not maximize the number of dashboard panels.
4. The accepted Google/Material light visual direction remains unchanged.

## 2026-08-08 — Execution-layer refinement

A single generic provider abstraction is useful, but there are two importantly different execution cases:

1. **Purpose-built authoritative providers** — Cloud Configuration Manager, GitHub, Slack, agent runtimes. Swarm Manager calls their supported interfaces.
2. **General host automation** — files, services, packages, permissions, local configuration not owned by another system. Ansible Runner is a strong execution backend here.

Swarm Manager should coordinate privileged systems rather than accumulating their privileges. The service should run unprivileged whenever possible, with narrowly-scoped provider credentials/helpers.

## 2026-08-08 — Failure model refinement

Provisioning crosses APIs that cannot participate in one ACID transaction. Therefore "roll everything back on any error" is unsafe and often impossible.

Recommended model: persistent saga-like steps with idempotency keys, recorded external IDs, evidence, and explicit provider-declared compensation. On failure, preserve partial state visibly and reconcile from observed reality instead of blindly replaying or deleting resources.
