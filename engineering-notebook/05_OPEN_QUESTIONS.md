# Open Questions

Only genuine unresolved design dependencies belong here. Facts that can be resolved by reading code/docs should be researched rather than escalated to the Owner.

| ID | Question | Owner / resolver | Blocking scope | Status |
|---|---|---|---|---|
| SM-Q001 | What API/CLI contract does the existing **Cloud Configuration Manager** expose for creating, configuring, disabling, archiving, and deleting Ubuntu identities? | Technical research / Owner if undocumented | Identity provider implementation | OPEN |
| SM-Q002 | Which Slack workspace/app credentials and scopes may Swarm Manager use to create/archive channels and manage memberships? | Owner + implementation research | Slack provider | OPEN |
| SM-Q003 | Where should provisioned swarm repositories live by default (Owner account, organization, selectable target), and what GitHub permission model should be standard? | Owner | GitHub provider defaults | OPEN |
| SM-Q004 | What exactly counts as “booting” an agent on each platform? ChatGPT web sessions and Claude Code/local processes have different automation/security constraints. | Platform research + Owner | Runtime provider contracts | OPEN |
| SM-Q005 | What secrets backend should Swarm Manager use initially? Existing Cloud Configuration Manager, OS keyring/files, Vault-like service, or another system? | Owner / security design | Credentials/security | OPEN |
| SM-Q006 | Is adding Kubernetes acceptable on this Ubuntu host if Agyn proves valuable, or must initial operation remain non-Kubernetes? | Owner | Agyn runtime evaluation | OPEN |
| SM-Q007 | Should per-swarm dashboards be hosted by one shared Swarm Manager service with swarm-scoped routes, or generated/deployed as separate applications/processes? | Owner after architecture comparison | Swarm dashboard architecture | OPEN |
| SM-Q008 | What archive retention policy applies before destructive deprovisioning? What must be retained: repo bundle, Slack export, user home snapshot, configuration manifest, secrets metadata, runtime logs? | Owner | Retirement policy | OPEN |
| SM-Q009 | Which universal protocols beyond Slack coordination and memory should become registry-managed assets? Candidates include work-order, evidence/QA, recovery, security baseline, notebook synchronization, and agent capability schema. | Owner + architecture evolution | Protocol registry scope | OPEN |
| SM-Q010 | Should protocol upgrades default to manual approval, per-swarm policy, or managed fleet waves? | Owner | Upgrade lifecycle | OPEN |
| SM-Q011 | Do separate agents always require separate OS users, or can some platforms have distinct logical identities without distinct local Unix users? | Owner / platform model | Identity allocation rules | OPEN |
| SM-Q012 | What is the minimum first release: two-agent ChatGPT+Claude swarm only, or must the first vertical slice include a multi-agent (>2) blueprint? | Owner | MVP scope | OPEN |
| SM-Q013 | Should Swarm Manager itself own a project-management UI on day one, or should the first product track lifecycle jobs only while the parent engineering notebook remains Git-first? | Owner | Initial UI scope | OPEN |
| SM-Q014 | What exact external access is allowed for provisioning/deprovisioning actions (network, sudo, systemd, package installs, Docker/Kubernetes)? | Owner/security commissioning | Provider execution boundary | OPEN |

## Non-blocking stance

These questions do not block architecture documentation or interface design. They block specific implementation choices only. The project should continue unaffected design/research work while they remain open.
