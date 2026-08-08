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

Agno describes itself as an SDK/control plane for building, running, and managing agent platforms, with RBAC, memory/storage, 100+ integrations, human approval, scheduling, observability, and multiple interfaces.

**Potential reuse:** agent service/runtime abstractions, integrations, memory/observability ideas.

**Mismatch:** not observed to be an infrastructure lifecycle manager for the Owner's full host/identity/Slack/GitHub provisioning model.

### CrewAI / Microsoft Agent Framework / LangGraph

Strong multi-agent orchestration and workflow frameworks. They solve agent collaboration/execution patterns, not the complete fleet provisioning and retirement lifecycle being designed here.

### Dify / Flowise

Strong visual agent/workflow builders and application platforms. Useful UX inspiration. Dify also exposes broad APIs and model/tool management. Neither was found to cover the complete external resource lifecycle; Dify also uses a source license with additional conditions rather than a plain permissive OSS license.

### Hermes Agent

Strong open-source persistent single-agent runtime with memory, skills, scheduling, messaging gateways, and self-hosting. Useful agent-runtime/memory inspiration, not a team lifecycle provisioner.

### Backstage / Crossplane / Temporal / AWX

Not direct competitors, but highly relevant architecture references:

- **Backstage:** catalog + software templates + plugin-based developer portal.
- **Crossplane:** declarative control plane and reconciliation model.
- **Temporal:** durable, replayable long-running workflows and activity retries.
- **AWX:** UI/API/task-engine separation around automation jobs.

**Current conclusion:** Do not abandon Swarm Manager. No verified single open-source product currently covers the full stated lifecycle. Before building a custom agent runtime, evaluate whether Agyn or Agno can sit behind the runtime-provider contract.

## 2026-08-07 — Engineering notebook structure import

**Source inspected:** `clinton-x-nichols/ddcrm-risk-management/engineering-notebook/`.

The DDCRM notebook uses a strong pattern: explicit index, charter/principles, engineering narrative, decision register, construction notes, specialized registers, and durable work history.

**Portable pattern adopted:** index + charter + narrative + decision register + construction notes + open questions + architecture proposal + landscape research + work queue + reconciliation log.

**Explicitly excluded:** all DDCRM risk-management decisions, work-order content, risk terminology, Confluence state, and implementation history.
