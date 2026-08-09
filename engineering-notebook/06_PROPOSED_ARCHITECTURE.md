# Proposed Architecture — Swarm Manager

**Status:** Daisy proposal for Owner review. Not yet an accepted architecture.

## 1. Product model

Swarm Manager is a **declarative lifecycle control plane for AI swarms**.

A swarm is not merely a prompt bundle. It is a managed resource composed of identities, agent runtimes, role/persona definitions, tools and permissions, universal protocol versions, communication surfaces, GitHub state, optional dashboard modules, and commissioning evidence.

The core design abstraction is a versioned **`SwarmSpec`** describing desired state. The control plane expands the specification into an execution plan and provider operations. This makes create, update, migrate, repair, archive, and destroy variations of the same lifecycle model instead of unrelated scripts.

## 2. Three primary planes

### A. Swarm Manager control plane

Runs centrally on the Ubuntu host. User-facing web application listens on **port 5015**.

Responsibilities:

- blueprint catalog;
- Swarm Builder;
- spec validation/versioning;
- plan/apply/reconcile lifecycle;
- provider registry and capability discovery;
- provisioning job execution;
- universal protocol registry/API;
- commissioning and health checks;
- archive/deprovision workflow;
- audit/event history;
- fleet view of all swarms.

### B. Per-swarm plane

Every provisioned swarm has its own durable and live operating environment:

- dedicated GitHub repository;
- substantive + notices Slack channels (or future communication provider equivalents);
- role/persona/configuration for every agent;
- pinned universal protocols;
- engineering notebook/current state/work queue/memory structures;
- selected dashboard modules;
- commissioning record;
- archive/retirement metadata.

### C. Per-agent plane

Every agent has an independently configurable identity and capability boundary:

- logical agent ID and display name;
- platform/runtime adapter;
- local OS identity when required;
- role and persona bundle;
- relationships and handoff rules;
- tools, skills, MCP servers, shell/environment configuration;
- command/security policy;
- secret references (not raw secrets in prompts);
- memory protocol configuration;
- communication protocol configuration;
- boot manifest and commissioning attestation;
- health/runtime status.

## 3. Core control-plane components

### 3.1 Web UI

**Technology proposal:** React + TypeScript + Material UI/Material Design 3, built to static assets and served by the backend on port 5015.

Primary navigation:

- **Swarms** — fleet, lifecycle state, health, recent activity.
- **Blueprints** — searchable library of reusable team designs.
- **Builder** — conversational/form-based design of a new blueprint.
- **Protocols** — universal protocol catalog, versions, adoption status.
- **Integrations** — configured providers and health/capabilities.
- **Jobs** — provisioning/reconciliation/retirement job history.
- **Settings** — host, security, defaults, retention, feature flags.

Design language: white surfaces, restrained color, generous spacing, Google/Material-like cards, simple progress indicators, strong empty states, no dense “sysadmin dashboard” aesthetic unless the user drills into diagnostics.

### 3.2 API/service layer

**Technology proposal:** Python + FastAPI + Pydantic.

Reasons:

- existing repository tooling is Python;
- provisioning/configuration work is naturally script/API heavy;
- Pydantic provides explicit versioned schemas for specs/provider capabilities;
- FastAPI makes UI operations and automation use the same contract.

Suggested API groups:

```text
/api/v1/swarms
/api/v1/blueprints
/api/v1/providers
/api/v1/protocols
/api/v1/jobs
/api/v1/archives
/api/v1/health
```

### 3.3 Blueprint Catalog

Stores versioned reusable **swarm blueprints**.

Blueprint content:

- intended outcomes/use cases;
- roles and relationships;
- default agent count;
- evidence/QA model;
- required/optional dashboard modules;
- required provider capabilities;
- default protocol set;
- recommended agent platforms;
- security assumptions;
- customization questions;
- examples and anti-use-cases.

Blueprints are **data**, not custom Python branches. YAML/JSON + JSON Schema/Pydantic is recommended.

Current `swarm-types/` becomes an input/source for this catalog rather than being thrown away.

### 3.4 Swarm Builder

Used when no blueprint fits.

The Builder should feel like **designing an organization**, not editing infrastructure.

Flow:

1. desired outcome;
2. definition of done/evidence;
3. work shape and constraints;
4. proposed roles;
5. role boundaries and relationships;
6. agent/platform choices;
7. identity allocation;
8. tools/security controls;
9. communication topology;
10. memory/protocol choices;
11. dashboard modules;
12. review generated blueprint;
13. save as one-off swarm or reusable blueprint.

The Builder may use LLM assistance to propose a team but the resulting blueprint is an explicit artifact the user reviews.

### 3.5 Swarm Spec Store

A `SwarmSpec` is the desired-state instance created from a blueprint + user customization.

Illustrative shape:

```yaml
apiVersion: swarmmanager/v1alpha1
kind: Swarm
metadata:
  name: runner-security-research
  blueprint: research-decision/v1
spec:
  outcome: Compare GitHub Enterprise Cloud runner approaches and Playwright security implications
  agents:
    - id: research-director
      runtime: chatgpt-web
      identityRef: user-a
      roleRef: roles/research-director/v1
      permissionsRef: policies/reviewer-standard/v1
    - id: primary-researcher
      runtime: claude-code
      identityRef: user-b
      roleRef: roles/primary-source-researcher/v1
  communications:
    provider: slack
    substantiveChannel: auto
    noticesChannel: auto
  repository:
    provider: github
    visibility: private
    create: true
  protocols:
    slack:
      selector: latest-approved
    memory:
      selector: latest-approved
  dashboard:
    modules:
      - overview
      - project-plan
      - engineering-notebook
      - evidence-matrix
      - decisions
  retirement:
    archiveBeforeDestroy: true
    retentionDays: 30
```

After planning, selectors such as `latest-approved` resolve to immutable protocol versions/digests before apply.

### 3.6 Planner

Turns desired state into a deterministic **plan**.

Plan operations might include:

- create OS identity `swarm-runner-researcher`;
- apply Claude Code configuration profile;
- create GitHub repository;
- assign repository permission;
- create Slack channels;
- invite agent identities/app connections;
- resolve protocol versions;
- write Swarm OS/bootstrap files;
- launch runtime/session adapter;
- deploy/enable dashboard modules;
- execute commissioning suite.

The UI presents this plan before consequential apply.

### 3.7 Lifecycle Orchestrator / Job Engine

Lifecycle states should be explicit, for example:

```text
DRAFT
PLANNED
PROVISIONING
COMMISSIONING
READY
DEGRADED
UPDATING
RETIRING
ARCHIVED
DESTROYING
DESTROYED
FAILED
```

Provisioning is long-running and crosses failure domains. The engine must persist job state and support retries/compensation/resume.

**Design recommendation:** define an internal workflow interface from the start. A simple local persistent implementation is acceptable for the first vertical slice; Temporal is a strong future/optional backend if failure-recovery complexity justifies it.

### 3.8 Reconciler

Periodically or on-demand compares desired and observed state.

Examples:

- expected Slack channel missing;
- agent OS user disabled unexpectedly;
- repo permissions drifted;
- protocol version available but not adopted;
- agent bootstrap hash differs from desired spec;
- dashboard module unhealthy.

Reconciler proposes or executes safe repairs depending on policy. It must not silently perform destructive/consequential changes merely because drift exists.

## 4. Provider/plugin architecture

Core must never know Slack API details, GitHub endpoint details, Claude config-file locations, or Cloud Configuration Manager internals.

Each provider advertises capabilities and implements lifecycle operations.

### Common provider contract concepts

```text
name
version
capabilities()
validate_config()
plan(desired, observed)
apply(operation)
observe(resource)
archive(resource)
destroy(resource)
health()
```

### Initial provider families

#### Identity provider

Initial implementation: **Cloud Configuration Manager provider**.

Responsibilities:

- list available local identities;
- create Ubuntu user;
- apply base shell/environment config;
- request installation/configuration of runtime-specific files;
- disable/archive/delete user under lifecycle policy.

#### Git provider

Initial: GitHub.

Responsibilities:

- create repo from Swarm OS/blueprint;
- configure visibility/settings;
- assign permissions;
- read/write commissioning state;
- archive/tag/bundle before retirement;
- optionally archive/delete repo after approval.

#### Communication provider

Initial: Slack.

Responsibilities:

- create substantive/notices channels;
- membership/access;
- health/test messages;
- archive channels;
- future support for other coordination systems via the same contract.

#### Agent runtime providers

Initial:

- ChatGPT web/session adapter;
- Claude Code/local-host adapter.

Future:

- Codex/OpenAI agent runtime;
- Gemini/other CLI agents;
- Agyn-hosted agent;
- Agno-hosted service;
- Hermes or other persistent runtime where appropriate.

Provider capabilities must describe what “boot,” “stop,” “health,” and “direct human confirmation” mean for each platform rather than pretending every runtime can be automated identically.

#### Protocol registry provider

Initial internal service serving immutable protocol artifacts.

#### Dashboard module provider

Registers available per-swarm dashboard modules and required backing services/routes.

#### Secrets/policy provider

Abstract secret references and permission policy from provider implementations. Agents should receive references/capabilities rather than raw credentials wherever possible.

## 5. Protocol Registry

Universal behavior should be a first-class versioned artifact service, not copied lore.

Suggested model:

```text
Protocol
  name: slack-coordination
  channel: stable
  latestApproved: 1.3.0

ProtocolVersion
  name: slack-coordination
  version: 1.3.0
  digest: sha256:...
  schemaVersion: 1
  body: ...
  releasedAt: ...
  status: approved
```

Suggested endpoints:

```text
GET /api/v1/protocols
GET /api/v1/protocols/{name}
GET /api/v1/protocols/{name}/latest-approved
GET /api/v1/protocols/{name}/versions/{version}
GET /api/v1/protocols/{name}/versions/{version}/manifest
```

Commissioning stores which exact artifact each agent loaded.

Potential future protocols:

- work-order/handoff;
- evidence and verification;
- engineering-notebook synchronization;
- restart/recovery;
- baseline agent security;
- capability manifest.

## 6. Per-swarm dashboard architecture

Do **not** generate a unique codebase for every swarm initially.

Recommended first architecture: one Swarm Manager web application with swarm-scoped routes and a **module registry**. A swarm's spec enables modules, and the UI composes the dashboard dynamically.

Example route:

```text
http://host:5015/swarms/runner-security-research
```

Modules:

- Overview / health
- Team / roles
- Project plan / work queue
- Engineering notebook
- Decisions / questions
- Evidence matrix
- Protocols / versions
- Integrations
- Security / capability grants
- Lifecycle / archive

If future swarms truly require standalone UIs, add a deployment provider later. Avoid creating dozens of bespoke frontend applications prematurely.

## 7. Per-agent configuration

Agent configuration is composed from modules and compiled into a **Boot Manifest**.

Boot Manifest fields:

- swarm identity;
- agent identity and role;
- persona files;
- responsibilities / prohibited scope;
- relationships and communication channels;
- source hierarchy;
- protocol version URLs + digests;
- repository and notebook pointers;
- permitted tools/skills/MCPs;
- command/security policy;
- secret references;
- memory configuration;
- commissioning challenge/response requirements;
- expected current Git commit/spec revision.

The agent returns a structured **BOOTLOAD/attestation** proving what it actually read.

## 8. Provisioning transaction

Recommended create sequence:

1. `DRAFT` — user defines outcome/blueprint/customization.
2. Validate spec and provider capabilities.
3. Resolve protocol selectors to versions/digests.
4. Produce `PLAN` including all consequential operations.
5. Owner approves apply.
6. Provision identities.
7. Provision repo and durable Swarm OS state.
8. Provision communications.
9. Apply per-agent runtime/configuration.
10. Enable dashboard modules.
11. Start/prepare runtimes where platform supports it.
12. Run commissioning tests.
13. Persist evidence/attestations.
14. Mark `READY` only if required gates pass.
15. Hand off swarm endpoints/instructions to Owner.

Partial failures remain visible and resumable; they do not cause blind re-creation of already successful resources.

## 9. Commissioning test matrix

At minimum:

### Identity
- expected identity exists;
- correct home/runtime profile applied;
- no unexpected privilege.

### GitHub
- repo exists;
- each agent's expected permission works;
- unauthorized operation is rejected where testable;
- expected Swarm OS/spec commit is loaded.

### Slack
- required channels exist;
- agents/provider can read/post as expected;
- cross-agent ping/reply test succeeds;
- notices/substantive separation is understood.

### Protocols
- registry reachable;
- exact pinned versions/digests retrieved;
- each agent attests loaded versions.

### Role/boot
Each agent reports:
- identity;
- role;
- Owner/counterparts;
- source hierarchy;
- security boundary;
- current work state;
- protocol pins;
- repository commit read.

### Recovery
Restart/reload one agent and prove it reconstructs the same state from durable sources.

## 10. Retirement / deprovisioning

Retirement is a workflow, not `rm -rf` with better branding.

### Phase A — Freeze
- stop accepting new work;
- reconcile current state;
- mark `RETIRING`.

### Phase B — Archive
Capture an **Archive Manifest**:
- final `SwarmSpec` and blueprint version;
- protocol versions/digests;
- Git repository final commit/bundle/archive location;
- engineering notebook/work state;
- Slack channel IDs and export/archive status where available;
- agent identities and capability grants;
- dashboard configuration;
- commissioning/health history;
- secrets *references/identifiers only*, not secret values;
- deprovision plan.

Mark `ARCHIVED` only when required evidence is captured.

### Phase C — Destroy
After explicit Owner confirmation:
- revoke tokens/permissions;
- stop runtimes;
- archive/delete Slack channels according to policy;
- disable/delete local identities according to retention policy;
- archive/delete GitHub resources according to policy;
- remove per-swarm runtime storage;
- record results and residual resources;
- mark `DESTROYED` only when verified.

## 11. Suggested technical layout

```text
swarm-manager/
  backend/
    api/
    domain/
      swarms/
      blueprints/
      protocols/
      jobs/
      archives/
    providers/
      identity/
      git/
      communications/
      runtime/
      dashboard/
      secrets/
    workflows/
    persistence/
    commissioning/
  frontend/
    app/
    features/
      swarms/
      blueprints/
      builder/
      protocols/
      integrations/
      jobs/
    modules/
  blueprints/
  protocols/
  schemas/
  migrations/
```

This can eventually live in this repository or a dedicated application repository; the repository boundary is an Owner decision after architecture acceptance.

## 12. First vertical slice proposal

Do not build every integration first.

Build one end-to-end path whose interfaces are real:

**“Provision a two-agent Research & Decision swarm”**

- UI on 5015;
- select a research blueprint;
- two identities (one ChatGPT-oriented, one Claude Code-oriented);
- GitHub repo creation;
- Slack substantive + notices channels;
- Slack + memory protocol retrieval and pinning;
- per-agent boot manifests;
- minimal shared per-swarm dashboard modules: Overview, Team, Notebook, Lifecycle;
- commissioning test and READY state;
- archive plan (destructive deletion can remain disabled initially).

The key acceptance test is architectural: adding a fake/second communication or runtime provider must require implementing a provider contract, not modifying the lifecycle engine everywhere.

## 13. Example future blueprint: Research & Decision Swarm

For the Owner's example question — researching GitHub Enterprise Cloud runners, Playwright, and making a security recommendation — a richer blueprint could contain:

1. **Research Director / Orchestrator** — frames questions, assigns bounded research, synthesizes, challenges.
2. **Primary Source Researcher** — vendor docs, release notes, technical evidence.
3. **Security Analyst** — threat model, identity/credential/isolation implications.
4. **Validation Engineer** — reproducible tests/prototypes where needed.
5. **Documentation & Evidence Lead** — evidence matrix, citations, decision package.
6. **Independent Reviewer** — verifies load-bearing claims before closure.

That might be named **Research & Decision Swarm** rather than merely “research cloud”: its purpose is not only collecting information, but producing a defensible decision and reusable documentation.
