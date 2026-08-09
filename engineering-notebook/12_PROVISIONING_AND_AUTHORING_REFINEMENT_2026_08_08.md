# Provisioning vs Swarm Authoring Refinement — 2026-08-08

**Status:** Owner-directed architecture refinement. This document controls the provisioning/user-experience boundary where it differs from earlier proposals.

## 1. Core separation

Swarm Manager has two distinct user experiences that must not be conflated:

1. **Provisioning** — select an already-defined swarm blueprint from the library, choose deployment-time options, review the plan, provision, commission, and receive the running swarm.
2. **Swarm Creation / Authoring** — design or modify a reusable swarm blueprint: roles, responsibilities, relationships, transactions, sequencing, priorities, conditions, logic gates, default tools/features, and commissioning rules.

The provisioning flow is intentionally **not** a free-form prompt that asks the Owner to invent a swarm every time.

The normal production path is:

```text
Blueprint Library
    ↓
Blueprint Detail
    ↓
Provisioning Options
    ↓
Plan Review
    ↓
Apply / Provision
    ↓
Commission
    ↓
READY
    ↓
Open the swarm's own UI
```

The authoring path feeds the library:

```text
Swarm Creation Tool
    ↓
Role / relationship / workflow authoring
    ↓
Validation + simulation/review
    ↓
Versioned Blueprint
    ↓
Blueprint Library
```

This separation is now a first-class product boundary.

## 2. Blueprint Library — normal provisioning entry point

The Swarm Manager UI on port 5015 opens into a library/fleet-oriented experience rather than an empty natural-language prompt.

For provisioning, the Owner browses or searches preconfigured swarm blueprints such as:

- Explainer Swarm;
- Research & Decision Swarm;
- Software Development Swarm;
- Documentation Swarm;
- Training/learning swarms;
- future specialized teams.

The library should support filtering by outcome/use case, agent count, runtime requirements, capabilities, security assumptions, and available optional modules.

If no blueprint fits, the user deliberately chooses **Create New Swarm Blueprint** / **Open Swarm Creation Tool**. That is an authoring operation, not a hidden branch inside ordinary provisioning.

## 3. Blueprint detail page

The first page for a selected blueprint should remain understandable and high-level.

It should answer:

- **What is this swarm for?**
- **What does it produce?**
- **How does it generally work?**
- **Which roles participate?**
- **What does each role do?**
- **How are the roles related at a high level?**
- **What capabilities/providers does the swarm require?**
- **Which optional modules are supported?**

The detail page should not expose the entire low-level transaction graph by default.

A lightweight relationship view may show, for example:

```text
Presenter
   ↕
Curriculum Architect
   ↕
Subject Matter Expert ←→ Researcher
   ↕
Technical Writer / Materials Designer
   ↓
Independent Reviewer
```

That is explanatory, not the canonical workflow editor.

## 4. Swarm Creation Tool

The Swarm Creation Tool is where a swarm's organization and operating logic are designed.

### Authorable elements

- roles;
- responsibilities;
- personas/behavioral characteristics;
- runtime recommendations/requirements;
- relationships among agents;
- allowed transaction/handoff types;
- sequencing;
- priority rules;
- conditions and logic gates;
- fan-out/fan-in behavior;
- review/approval boundaries;
- evidence obligations;
- default universal protocols;
- tools/skills/MCP capability requirements;
- default optional dashboard modules;
- token/memory stewardship defaults;
- commissioning tests;
- recovery expectations.

### Visual interaction model

The authoring surface should support an editable graph/canvas with connections and logical constructs. The Owner specifically prefers reuse of a suitable **open-source visual workflow/graph editor** rather than building the canvas/connection interaction model from scratch.

However, the blueprint's canonical workflow must be stored in a neutral Swarm Manager schema, not in an editor-specific proprietary format. The editor is a replaceable authoring surface.

A research task will select the OSS component based on:

- license;
- embeddability;
- React/web compatibility;
- custom node/edge types;
- connection validation;
- conditional/gate support;
- layout/navigation at large graph sizes;
- accessibility;
- persistence/import/export model;
- project health/maintainability.

## 5. Provisioning-time configuration

Provisioning configures a blueprint instance without redesigning the organization.

Appropriate choices include:

### Agent placement/runtime

For each agent:

- deployment/runtime target;
- logical or local identity binding;
- available model/configuration profile;
- provider-specific options that are safe to expose;
- whether the runtime requires direct human boot/approval.

### Optional capabilities

Examples:

- Memory Manager enabled for selected/all agents;
- Token Monitor enabled;
- Token & Memory Steward enabled;
- project-management module;
- engineering-notebook module;
- evidence/citation module;
- additional approved tools/skills/MCPs.

### Infrastructure choices

Examples:

- GitHub target/account/org when configurable;
- visibility policy when allowed;
- Slack naming/target defaults when configurable;
- provisioned swarm UI port;
- retention/archive policy selections that are exposed to users.

Provisioning should not normally alter role responsibilities, relationship semantics, handoff logic, or workflow gates. Those changes create a new/modified blueprint version through the authoring tool.

## 6. Plan review

After deployment choices are made, Swarm Manager generates the deterministic plan.

The plan remains the point where the user sees concrete infrastructure actions before apply, including:

- identities to create/configure;
- GitHub resources and permissions;
- Slack channels/access;
- protocol versions/digests;
- runtime configuration/boot actions;
- optional modules;
- swarm UI process/deployment and port;
- commissioning tests;
- any actions requiring explicit approval.

The controls do not need cheerful consumer-product language. They need clarity about what will happen.

## 7. UI information-density standard

The accepted visual direction remains clean, white, and Google/Material-like, but **not sparse at the expense of information**.

The Owner wants efficient use of screen area because operational pages will become dense.

Starting UI rules:

- small but readable fonts;
- compact spacing where information density benefits;
- horizontal and vertical split panes with draggable boundaries;
- scrollbars for bounded regions rather than forcing giant page length;
- collapsible sections;
- detail drawers/panels;
- tooltips, popovers, and mouseover detail for secondary information;
- tables/graphs that maximize viewport usage;
- preserve clear hierarchy despite density;
- avoid decorative cards/panels that consume space without adding information.

The design should feel like a precise professional control surface that happens to use a clean Material visual language—not a dark operations cockpit and not an oversized consumer landing page.

## 8. Cloud Configuration Manager replaces the assumed Ansible layer

The Owner does not have Ansible installed and does not currently want it introduced as an architectural dependency.

The existing **Cloud Configuration Manager** performs the relevant local-user/runtime/configuration role and should remain the authoritative system for that domain.

### Required future dependency

The Cloud Configuration Manager needs an API interface that Swarm Manager can call through its provider contract.

Expected capability classes include:

- discover/list identity capacity;
- reserve identity/name;
- create Ubuntu user;
- configure runtime/platform assets;
- configure shell/environment files;
- enable selected skills/MCPs/configuration;
- inspect current configuration;
- disable/archive/delete according to policy;
- return structured evidence/state to Swarm Manager.

The exact API is future work. Swarm Manager should be designed against the provider contract while the Configuration Manager API is developed separately.

No generic Ansible Runner provider is part of the current assumed architecture. A generic automation backend can be reconsidered later only if a real requirement appears that the Configuration Manager and purpose-built providers do not satisfy.

## 9. Per-swarm UI provisioning

Every provisioned swarm receives a UI/dashboard as part of its managed resources.

During provisioning, the Owner selects an available port from the range:

```text
6000–7000
```

Swarm Manager must only offer ports currently considered available.

### Proposed control-plane behavior

Maintain a port allocation registry with:

- swarm ID;
- selected port;
- reservation state;
- observed bind/listener state;
- deployment/process ID where applicable;
- health status;
- allocation/release timestamps.

Planning reserves the selected port before the UI process is deployed so concurrent provisioning does not allocate the same port twice.

Reconciliation should also compare the registry with actual host listeners so a port occupied outside Swarm Manager is not falsely presented as available.

Retirement releases the port only when the swarm UI has been frozen/stopped according to lifecycle policy.

The exact packaging model—one service process per swarm, generated service unit, container, or another mechanism—remains an implementation question.

## 10. Explainer Swarm as the standing proof of concept

The **Explainer Swarm** is now the principal swarm used to exercise and evolve Swarm Manager while the product is developed.

Starting role model:

- Presenter — Owner-facing interactive teacher;
- Subject Matter Expert — conceptual/technical depth;
- Researcher — current primary-source research;
- Curriculum Architect — learning sequence/prerequisites/adaptation;
- Technical Writer / Materials Designer — slides, flash cards, examples, handouts, exercises;
- Independent Reviewer — correctness/evidence/teaching-quality review.

Future optional role/module:

- Token & Memory Steward — token-efficiency and memory-health monitoring/governance.

### Why this is a good POC

It exercises more than simple agent-to-agent messaging:

- a clear user-facing agent;
- specialist delegation;
- fan-out/fan-in work;
- research and evidence;
- generated artifacts;
- interactive interruption/questions;
- persistent learning/memory state;
- optional dashboard modules;
- role-specific runtime placement;
- review before user delivery;
- token/memory stewardship;
- a meaningful per-swarm UI.

The Explainer blueprint should not be treated as finished now. It is intentionally versioned and evolved alongside Swarm Manager.

## 11. Revised end-user provisioning story

For the Explainer Swarm, the intended provisioning UX is now:

1. Open Swarm Manager on port 5015.
2. Browse/search the Blueprint Library.
3. Select **Explainer Swarm**.
4. Read the high-level description, roles, outputs, and relationships.
5. Choose **Provision**.
6. Select deployment/runtime target per agent.
7. Enable/disable optional supported features such as Memory Manager or Token Monitor.
8. Select one of the currently available swarm UI ports between 6000 and 7000.
9. Review the generated infrastructure/lifecycle plan.
10. Approve apply.
11. Swarm Manager provisions identities through Cloud Configuration Manager, GitHub, Slack, protocols, runtimes, and the swarm UI.
12. Swarm Manager runs commissioning and only declares the swarm `READY` when evidence gates pass.
13. Swarm Manager hands the Owner the swarm UI address and Presenter entry point.
14. The Owner asks the Presenter the first topic/question.

If the Explainer Swarm had not existed in the library, the Owner would leave the provisioning path, open the **Swarm Creation Tool**, design/version the new blueprint, publish it to the library, and then provision that library item through the exact same provisioning flow.

## 12. Architectural consequence

This refinement creates a clean lifecycle boundary:

> **Swarm Creation Tool authors reusable organizations. Blueprint Library publishes them. Provisioning instantiates them.**

That boundary improves reproducibility, reviewability, upgrade behavior, and fleet management because provisioned swarms always have a known blueprint/version provenance rather than being one-off organizations synthesized from an ephemeral provisioning conversation.
