# Architecture Review and Functional Refinement — 2026-08-08

**Status:** Daisy architecture refinement for Owner review. This document responds to the Owner's feedback that the first architecture pass over-emphasized UI presentation and did not go deep enough on control-plane functionality.

## Owner feedback that controls this refinement

1. The dashboard concept was visually overbuilt and incorrectly dark; the accepted visual direction remains a clean white Google/Material-style interface.
2. Architecture and functionality come before elaborate UI work.
3. The project needs a serious control-plane design, current open-source research, and explicit architectural feedback—not merely a dashboard mockup.

## Architectural conclusion

Swarm Manager should be designed as a **declarative lifecycle control plane for agent organizations**, not as an agent framework and not as an Ansible GUI.

The architectural center is:

```text
Owner intent
    ↓
Blueprint + customization
    ↓
Versioned SwarmSpec (desired state)
    ↓
Planner + policy/approval gates
    ↓
Durable lifecycle workflow
    ↓
Provider operations
    ↓
Observed resource ledger
    ↓
Commissioning / reconciliation
    ↓
READY swarm
```

Agent frameworks and runtimes sit below this control plane as replaceable providers.

## 1. Product boundary

Swarm Manager owns the lifecycle of the **organization** around agents:

- team design and reusable blueprints;
- identity allocation and creation;
- repositories and access;
- communications topology;
- protocol selection and pinning;
- runtime/bootstrap configuration;
- tools, skills, MCPs, and policy references;
- commissioning and health evidence;
- modification and drift reconciliation;
- archive and deprovisioning.

Swarm Manager does **not** need to invent a universal agent loop. CrewAI, Microsoft Agent Framework, OpenAI Agents SDK, Agno, Agyn, Hermes, Claude Code, and future systems may all implement agent execution differently. Swarm Manager manages them through runtime capability contracts.

## 2. Control-plane functional components

### 2.1 Northbound API

The web UI, CLI, automation, and future external systems all use the same API.

Core operations:

```text
POST   /swarms                 create draft
POST   /swarms/{id}/plan       produce deterministic plan
POST   /swarms/{id}/apply      execute approved plan
POST   /swarms/{id}/commission run readiness suite
POST   /swarms/{id}/reconcile  compare desired vs observed
POST   /swarms/{id}/retire     freeze/archive
DELETE /swarms/{id}            destructive retirement after explicit gate
GET    /swarms/{id}
GET    /swarms/{id}/resources
GET    /swarms/{id}/jobs
GET    /swarms/{id}/evidence
```

The API should exist before a rich UI. The UI is a client of stable lifecycle semantics.

### 2.2 Blueprint Catalog

A blueprint is a reusable organization design, not an installed swarm.

It contains:

- intended outcome classes and anti-use-cases;
- roles, responsibilities, and relationships;
- default runtime/platform recommendations;
- required provider capabilities;
- default universal protocols;
- evidence and review model;
- security assumptions;
- commissioning tests;
- optional swarm-dashboard modules;
- customization questions.

Blueprints are versioned data artifacts. The existing `swarm-types/` profiles are seeds for this catalog.

### 2.3 Swarm Builder

The Builder creates a new blueprint or one-off swarm specification when no catalog item fits.

The Builder's output is explicit structured data. An LLM may propose roles and relationships, but the Owner reviews the resulting blueprint before provisioning.

### 2.4 SwarmSpec compiler

A `SwarmSpec` is the desired state for one swarm instance.

Configuration is layered:

```text
platform defaults
  < blueprint defaults
    < swarm overrides
      < agent-specific overrides
```

The compiled spec records provenance for every important value so the operator can answer "why does this agent have this setting?"

### 2.5 Planner

The planner compares desired state with current observed state and produces an ordered set of operations.

Each operation includes:

- provider;
- resource kind;
- desired change;
- external resource ID if known;
- idempotency key;
- consequential/destructive classification;
- approval requirement;
- dependencies;
- expected evidence;
- whether compensation is possible.

Planning is non-destructive and repeatable.

### 2.6 Policy and approval gate

Before apply, operations are evaluated against policy.

Examples:

- creating a local user may be routine if pre-authorized;
- granting admin repository access may require review;
- storing a secret must use an approved secret provider;
- external publishing/deployment may require direct Owner authorization;
- deletion always enters the retirement gate.

The plan shown to the Owner should clearly distinguish routine operations from gated operations.

### 2.7 Durable lifecycle engine

Provisioning is a distributed transaction across systems that do not share a database. A blind database-style rollback model is inappropriate.

Use a **saga-like persistent step ledger**:

1. persist job and step state before execution;
2. execute one idempotent provider operation;
3. record external ID, evidence, and result;
4. resume from the last verified step after interruption;
5. compensate only when a provider explicitly supports safe compensation;
6. otherwise leave the resource visible as partial state and require reconciliation.

Initial implementation can be a local persistent workflow engine. Preserve an interface that could later use Temporal if workflow complexity warrants it.

### 2.8 Resource/observed-state ledger

The control-plane database—not GitHub chat history—tracks operational state.

For every managed external resource store at least:

- swarm ID;
- logical resource ID;
- provider;
- resource kind;
- external ID;
- desired revision;
- last observed state;
- health/conditions;
- creation/update timestamps;
- last verification evidence;
- ownership/retirement policy.

GitHub remains durable design/history for each swarm; it should not be abused as the transactional job database.

### 2.9 Provider registry

Providers own system-specific knowledge. The lifecycle core must not know Slack endpoints, GitHub payloads, Claude configuration paths, or Cloud Configuration Manager internals.

Common contract:

```text
capabilities()
validate(binding, desired)
plan(desired, observed)
apply(operation)
observe(resource)
verify(resource)
archive(resource)
destroy(resource)
health()
```

Provider operations must be idempotent where possible and return structured evidence.

## 3. Provider families

### 3.1 Identity provider — Cloud Configuration Manager

The existing Cloud Configuration Manager remains authoritative for Ubuntu-user creation and its supported runtime/configuration provisioning.

Swarm Manager should call it, not duplicate it.

Required capability discovery includes:

- list/reserve available identities;
- create user;
- configure shell/runtime assets;
- apply skills/MCP/configuration selections;
- inspect current user configuration;
- disable/archive/delete according to policy.

Swarm Manager itself should not need root merely because an identity provider performs privileged work.

### 3.2 Host automation provider — Ansible Runner

Use Ansible Runner as a general host/configuration execution backend where no purpose-built provider exists.

Good fits:

- directories/files/permissions;
- systemd services;
- package prerequisites;
- local application configuration;
- repeatable health/cleanup tasks.

Do not use Ansible when a dedicated API-backed system is already authoritative (for example Cloud Configuration Manager identity creation).

Runner's event stream becomes evidence in the lifecycle job ledger.

### 3.3 Git provider — GitHub first

Owns:

- repository creation;
- branch/settings policy;
- collaborator/team permissions;
- initial Swarm OS/blueprint commit;
- tags/releases/archive markers;
- final archive evidence;
- optional archive/delete operation after retirement approval.

### 3.4 Communication provider — Slack first

Owns:

- substantive and notices channels;
- membership/access;
- test messages and readback;
- channel IDs in resource ledger;
- archive/retirement behavior.

Universal Slack protocol content is **not** owned by this provider; it is owned by the Protocol Registry.

### 3.5 Runtime providers

Runtime providers describe what can actually be automated for each agent platform.

Capability matrix fields should include:

```text
can_install
can_configure_files
can_launch
can_stop
can_resume
can_receive_boot_manifest
can_fetch_protocols
can_attest_bootload
can_post_slack
supports_tools
supports_mcp
supports_sandbox
supports_memory
requires_direct_human_boot
requires_direct_human_approval
```

This prevents the core from pretending ChatGPT web, Claude Code, an API-hosted OpenAI agent, Hermes, Agno, and Agyn have identical lifecycle semantics.

### 3.6 Secret provider

The spec stores **secret references**, never raw secrets.

A secret provider resolves credentials only at the execution/runtime boundary. Future backends may include system keyrings, Vault-compatible services, cloud secret stores, or platform-native credential brokers.

### 3.7 Dashboard-module provider

Dashboard modules are later-stage optional capabilities. They should register routes, data requirements, and authorization requirements without modifying lifecycle core code.

## 4. Protocol plane

The Protocol Registry serves **behavioral contracts**, not project state and not the memories themselves.

Examples:

- Slack coordination protocol;
- memory management protocol;
- notebook synchronization protocol;
- work-order/handoff protocol;
- recovery protocol;
- evidence/verification protocol;
- baseline capability/security protocol.

Protocol releases are immutable and content-addressed.

Provisioning behavior:

1. Blueprint asks for `latest-approved` or a fixed version.
2. Planner resolves it to exact version + digest.
3. Compiled SwarmSpec records the pin.
4. Boot Manifest contains registry endpoint + version + digest.
5. Agent retrieves exact artifact and attests the digest.
6. Later releases appear as upgrade opportunities rather than silently changing a running swarm.

## 5. Agent configuration and Boot Manifest

Every agent is compiled from reusable modules:

- identity;
- role/responsibility;
- persona;
- runtime/platform;
- relationships;
- repo/channel bindings;
- universal protocol pins;
- tools and MCPs;
- shell/runtime configuration;
- command/security policy;
- secret references;
- memory configuration;
- evidence obligations;
- current spec revision.

The runtime provider translates the generic Boot Manifest into platform-specific boot/configuration steps.

The agent returns a BOOTLOAD/attestation containing the exact spec revision, Git commit, and protocol digests it actually read.

## 6. Commissioning engine

`READY` is an evidence state, not "provisioning commands returned zero."

Required gate categories:

### Resource gate
- expected users/repos/channels exist;
- resource IDs match the ledger;
- provider health passes.

### Permission gate
- required access works;
- prohibited access is absent where testable;
- no unexpected local privilege.

### Protocol gate
- exact pinned protocol versions retrieved;
- digest attestation matches.

### Agent identity/role gate
Each agent reports:
- swarm and agent identity;
- role and counterpart relationships;
- allowed/prohibited scope;
- source hierarchy;
- repo commit;
- protocol pins;
- security gates.

### Communication gate
- each agent can access expected communication surface;
- cross-agent ping/reply succeeds;
- substantive/notices semantics are understood.

### Recovery gate
Restart or re-bootstrap at least one agent and prove it reconstructs the expected state from durable sources.

Commissioning results are first-class evidence records.

## 7. Reconciliation and evolution

Creation is only the first lifecycle.

The reconciler detects:

- missing/disabled identities;
- repository permission drift;
- missing Slack channels;
- stale agent boot manifests;
- protocol upgrades available;
- runtime/configuration drift;
- broken dashboard modules;
- failed commissioning conditions.

Drift classes:

```text
IN_SYNC
DRIFT_SAFE_TO_REPAIR
DRIFT_REQUIRES_APPROVAL
EXTERNAL_CHANGE_CONFLICT
UNOBSERVABLE
```

Safe automatic repair is policy-controlled. Destructive or authority-sensitive drift never causes silent repair.

## 8. Retirement model

Retirement is intentionally asymmetric with creation because deletion loses evidence.

```text
READY
  → FREEZING
  → ARCHIVING
  → RETIRED
  → AWAITING_DESTROY_APPROVAL
  → DESTROYING
  → DESTROYED
```

Archive Manifest captures:

- final spec/blueprint revisions;
- external resource IDs;
- final Git commit/archive;
- protocol pins;
- agent configuration manifests;
- notebook/current-state pointers;
- commissioning and health history;
- channel archive state;
- identity retirement state;
- residual resources;
- secret references only.

Destroy is independently approved and mechanically verified.

## 9. Data model

Core entities:

```text
Blueprint
BlueprintVersion
Swarm
SwarmSpecRevision
AgentSpec
ProviderBinding
Protocol
ProtocolRelease
ProtocolPin
Plan
PlanOperation
LifecycleJob
JobStep
ManagedResource
CommissioningRun
CommissioningCheck
ApprovalGate
ArchiveManifest
AuditEvent
```

This is a relational domain. PostgreSQL is the preferred long-term operational store; a SQLite implementation is acceptable for an early single-host prototype only if the persistence interface and migration path remain explicit.

## 10. Security architecture

1. Swarm Manager service runs unprivileged.
2. Privileged work is delegated to narrowly-scoped providers/helpers.
3. No secrets in GitHub, protocol artifacts, or agent prompts.
4. Provider credentials are isolated by provider and least privilege.
5. Every operation carries actor, reason, plan revision, and approval context.
6. Destructive operations are separate lifecycle phases.
7. Provider responses are treated as evidence but critical conditions are independently verified where possible.
8. Skills/MCPs/prompts are supply-chain artifacts: version, source, digest, and trust status should eventually be tracked.
9. Agent-to-agent messages never elevate authorization.
10. Runtime-specific direct-human confirmation requirements remain binding.

## 11. Open-source research implications

### Adopt patterns, not monoliths

- **Crossplane:** desired state, providers, observation/reconciliation, resource conditions.
- **Ansible Runner/AWX:** application-embedded automation jobs, structured events, isolated execution, UI/API/job separation.
- **Backstage:** catalog + templates + plugin extensibility.
- **Temporal:** durable workflow recovery if/when the local workflow engine becomes insufficient.

### Runtime/provider candidates

- **Agyn:** strong candidate for secure Kubernetes-based runtime/isolation and agents-as-code.
- **Agno:** useful multi-framework runtime/control-plane candidate; explicitly supports running agents built with multiple frameworks.
- **Microsoft Agent Framework:** strong open orchestration/workflow runtime provider for .NET/Python ecosystems.
- **OpenAI Agents SDK:** lightweight runtime option with handoffs, guardrails, sessions, sandbox agents, MCP integration, human-in-loop, and tracing.
- **CrewAI:** role/crew/flow runtime and blueprint-design inspiration.
- **Hermes:** persistent/self-improving runtime with messaging, memory, skills, and sandboxing.
- **Flowise/Dify:** visual-builder inspiration; not the Swarm Manager infrastructure lifecycle core.

No product in this reviewed set was verified to own the complete Swarm Manager lifecycle across local identities, GitHub, Slack, universal protocols, heterogeneous runtime provisioning, commissioning, reconciliation, and archive/deprovision.

## 12. Functional implementation sequence

### Phase 0 — Discover existing environment

Before implementation:

- inventory Cloud Configuration Manager API/CLI and object model;
- inventory GitHub/Slack credentials and permission limits;
- define runtime capability matrix for ChatGPT web and Claude Code;
- identify available database/service constraints on the Ubuntu host;
- identify which operations require direct Owner confirmation.

### Phase 1 — Headless lifecycle core

No rich dashboard yet.

Deliver:

- versioned `SwarmSpec` schema;
- blueprint parser;
- provider registry;
- resource ledger;
- planner;
- policy gates;
- persistent lifecycle jobs;
- CLI/API plan/apply/status.

### Phase 2 — First real providers

- Cloud Configuration Manager identity provider;
- GitHub provider;
- Slack provider;
- Protocol Registry;
- Ansible Runner host-automation provider.

### Phase 3 — Two runtime adapters + commissioning

- ChatGPT web bootstrap capability model;
- Claude Code bootstrap/configuration adapter;
- Boot Manifest compiler;
- BOOTLOAD attestation;
- communication/role/recovery commissioning tests.

### Phase 4 — Full create/reconcile/archive vertical slice

Prove:

1. create a two-agent Research & Decision swarm;
2. detect and repair one safe drift condition;
3. update one protocol via explicit upgrade;
4. freeze/archive the swarm;
5. produce a destruction plan without executing destructive deletion by default.

### Phase 5 — Minimal light UI on port 5015

Only after lifecycle APIs are stable:

- fleet/list page;
- `Create swarm` workflow;
- blueprint selector;
- generated plan/review page;
- job/progress page;
- swarm status/lifecycle page.

Visual direction: clean white Google/Material-like interface. Advanced dashboard windows/modules wait until they have demonstrated operational value.

### Phase 6 — Builder and module ecosystem

- full Swarm Builder;
- richer Blueprint Catalog;
- per-swarm dashboard modules;
- additional runtimes/providers;
- advanced security/capability modules.

## 13. Architecture acceptance criteria

The architecture is doing its job if all of these are true:

1. Adding a new runtime does not require modifying the lifecycle engine.
2. Adding Teams/Discord later does not require rewriting swarm logic.
3. Re-running apply after a crash does not duplicate already-created resources.
4. The system can explain every external resource and why it exists.
5. A partially provisioned swarm is visible and recoverable.
6. A swarm cannot become `READY` without commissioning evidence.
7. Protocol changes are reproducible and explicit.
8. The control plane itself does not need broad root/provider privileges.
9. Retirement preserves evidence before deletion.
10. The UI can be replaced without changing provisioning semantics.

## 14. Current recommendation

Proceed with Swarm Manager. Do not build a proprietary agent orchestration framework. Build the lifecycle/control-plane layer around provider contracts, use Cloud Configuration Manager for identities, evaluate Ansible Runner as the host-automation executor, and treat modern agent frameworks/runtimes as pluggable execution targets.

The next executable work is environment/provider discovery and schema design—not dashboard implementation.
