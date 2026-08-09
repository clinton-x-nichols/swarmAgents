# Open Questions

Only genuine unresolved design dependencies belong here. Facts that can be resolved by reading code/docs should be researched rather than escalated to the Owner.

| ID | Question | Owner / resolver | Blocking scope | Status |
|---|---|---|---|---|
| SM-Q001 | What exact API contract should be added to the existing **Cloud Configuration Manager** so Swarm Manager can reserve/create/configure/inspect/disable/archive/delete Ubuntu identities and related runtime configuration? | Technical design / Owner if manager internals are undocumented | Cloud Configuration Manager provider | OPEN |
| SM-Q002 | Which Slack workspace/app credentials and scopes may Swarm Manager use to create/archive channels and manage memberships? | Owner + implementation research | Slack provider | OPEN |
| SM-Q003 | Where should provisioned swarm repositories live by default (Owner account, organization, selectable target), and what GitHub permission model should be standard? | Owner | GitHub provider defaults | OPEN |
| SM-Q004 | What exactly counts as “booting” an agent on each platform? ChatGPT web sessions and Claude Code/local processes have different automation/security constraints. | Platform research + Owner | Runtime provider contracts | OPEN |
| SM-Q005 | What secrets backend should Swarm Manager use initially? Existing Cloud Configuration Manager, OS keyring/files, Vault-like service, or another system? | Owner / security design | Credentials/security | OPEN |
| SM-Q006 | Is adding Kubernetes acceptable on this Ubuntu host if Agyn proves valuable, or must initial operation remain non-Kubernetes? | Owner | Agyn runtime evaluation | OPEN |
| SM-Q007 | How should each separately provisioned swarm UI be packaged and hosted while preserving the accepted one-port-per-swarm model in the 6000–7000 range? | Architecture / implementation research | Per-swarm UI deployment | OPEN |
| SM-Q008 | What archive retention policy applies before destructive deprovisioning? What must be retained: repo bundle, Slack export, user home snapshot, configuration manifest, secrets metadata, runtime logs? | Owner | Retirement policy | OPEN |
| SM-Q009 | Which universal protocols beyond Slack coordination and memory should become registry-managed assets? Candidates include work-order, evidence/QA, recovery, security baseline, notebook synchronization, and agent capability schema. | Owner + architecture evolution | Protocol registry scope | OPEN |
| SM-Q010 | Should protocol upgrades default to manual approval, per-swarm policy, or managed fleet waves? | Owner | Upgrade lifecycle | OPEN |
| SM-Q011 | Do separate agents always require separate OS users, or can some platforms have distinct logical identities without distinct local Unix users? | Owner / platform model | Identity allocation rules | OPEN |
| SM-Q012 | For the first Explainer Swarm vertical slice, should commissioning start with the full Presenter/SME/Researcher/Curriculum/Writer/Reviewer team or a reduced role subset that expands as provider support matures? | Daisy + Owner at implementation boundary | First vertical-slice scope | OPEN |
| SM-Q013 | Should Swarm Manager itself own a project-management UI on day one, or should the first product track provisioning/lifecycle while each provisioned swarm owns its own operational/project UI? | Owner | Initial UI scope | OPEN |
| SM-Q014 | What exact external access is allowed for provisioning/deprovisioning actions (network, sudo, systemd, package installs, containers/Kubernetes)? | Owner/security commissioning | Provider execution boundary | OPEN |
| SM-Q015 | Which open-source visual workflow/graph editor best fits the Swarm Creation Tool requirements for editable agent connections, transactions, priorities, conditions, and logic gates while allowing Swarm Manager to keep a neutral underlying graph schema? | Technical research | Swarm Creation Tool | OPEN |
| SM-Q016 | How should ports in the 6000–7000 range be detected, reserved, persisted, reconciled against externally occupied ports, and released during retirement? | Technical design | Per-swarm UI lifecycle | OPEN |
| SM-Q017 | What should be the first/default **Memory Store backend** for mandatory Memory Manager: local directory, Git-backed store, Context Keep, or a hybrid? What memory classes belong in which backend if more than one is used? | Daisy + technical research + Owner at implementation boundary | Memory Manager implementation | OPEN |
| SM-Q018 | What are the canonical durable-memory classes, mutability/supersession rules, retention rules, and shared-vs-agent-private memory boundaries? | Memory architecture research | Memory Manager schema/governance | OPEN |
| SM-Q019 | How should transfer/recovery prompts be generated, refreshed, versioned, and validated so they remain useful recovery entry points without becoming stale competing sources of truth? | Memory/recovery architecture research | Agent recovery | OPEN |

## Resolved direction

The Owner has resolved the prior architectural question about shared-vs-separate swarm dashboards: **every provisioned swarm receives a UI/dashboard and provisioning selects an available port in the 6000–7000 range.** Only the packaging/process model remains open (`SM-Q007`).

The Owner has also resolved the provisioning entry-point question: normal provisioning starts from the preconfigured Blueprint Library. Designing a new swarm occurs in the separate Swarm Creation Tool.

The Owner has resolved whether Memory Manager is optional: **every swarm requires it as baseline infrastructure.** The remaining memory questions are implementation/storage/schema choices, not whether the capability exists.

## Non-blocking stance

These questions do not block architecture documentation or interface design. They block specific implementation choices only. The project should continue unaffected design/research work while they remain open.
