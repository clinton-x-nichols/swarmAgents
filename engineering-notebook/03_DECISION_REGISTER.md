# Decision Register

Decision status vocabulary: `ACCEPTED`, `PROPOSED`, `DEFERRED`, `REJECTED`, `SUPERSEDED`.

`ACCEPTED` means the Owner explicitly established or affirmed the point. `PROPOSED` is architecture proposed by Daisy and must not be treated as Owner-approved merely because it is documented here.

| ID | Area | Decision | Status | Owner | Rationale / source |
|---|---|---|---|---|---|
| SM-D001 | Product | Product working name is **Swarm Manager**. | ACCEPTED | Owner | 2026-08-07 design session. |
| SM-D002 | UI | Primary Swarm Manager UI will listen on **port 5015** and use a clean white Google/Material-style visual language. | ACCEPTED | Owner | 2026-08-07 design session. |
| SM-D003 | Architecture | Modularity is a first-class requirement across the control plane, each swarm, and each agent. | ACCEPTED | Owner | Repeated Owner emphasis during design session. |
| SM-D004 | Lifecycle | Product scope includes provisioning **and** archive/deprovisioning of swarms. | ACCEPTED | Owner | End-of-life flow explicitly requested. |
| SM-D005 | Blueprints | Provide a library of preconfigured swarm types plus a **Swarm Builder** for cases that need a new team design. | ACCEPTED | Owner | 2026-08-07 design session. |
| SM-D006 | Identity | Each participating agent requires a separate system identity; Swarm Manager should coordinate identity creation through the existing Cloud Configuration Manager. | ACCEPTED | Owner | 2026-08-07 design session. |
| SM-D007 | Integrations | Initial external provisioning includes GitHub repo/access and fit-for-purpose Slack channels. | ACCEPTED | Owner | 2026-08-07 design session. |
| SM-D008 | Protocols | Universal Slack-coordination and memory protocols should be served through APIs and loaded during swarm boot/commissioning. | ACCEPTED | Owner | Initial known universal protocols. |
| SM-D009 | Commissioning | A swarm must be tested after provisioning to prove agents can communicate and understand their roles before human handoff. | ACCEPTED | Owner | 2026-08-07 design session. |
| SM-D010 | Swarm UI | Each provisioned swarm may receive its own modular dashboard with selectable capabilities such as engineering notebook and project management. | ACCEPTED | Owner | 2026-08-07 design session. |
| SM-D011 | Agent config | Individual agents must support modular configuration of role/persona, capabilities, tools, security controls, commands, skills/MCPs, memory, and related settings. | ACCEPTED | Owner | 2026-08-07 design session. |
| SM-D012 | Notebook | The parent project maintains a durable engineering notebook recording decisions, reasoning, experiments, successes, failures, abandoned paths, and work state. | ACCEPTED | Owner | Explicit Owner requirement. |
| SM-D013 | Build-vs-buy | If an open-source product already provides the complete desired outcome, prefer using it rather than duplicating it. | ACCEPTED | Owner | Explicit Owner instruction. |
| SM-D014 | Project method | Project goals and outstanding items should be re-evaluated at session boundaries instead of assuming early design is final. | ACCEPTED | Owner | Owner described requirements as intentionally evolving. |
| SM-P001 | Architecture | Represent each swarm as a versioned declarative `SwarmSpec`; core lifecycle logic reconciles external systems toward desired state through provider interfaces. | PROPOSED | Daisy | Crossplane/Ansible-style control-plane pattern; minimizes hard-coded integration coupling. |
| SM-P002 | Protocols | Resolve “latest approved” protocol at provisioning time, then **pin exact version + digest** in the swarm spec; upgrades are explicit lifecycle operations. | PROPOSED | Daisy | Prevents silent behavior drift and preserves reproducibility. |
| SM-P003 | Backend | Use a Python service layer (FastAPI/Pydantic) with provider contracts; serve a bundled React/TypeScript Material UI on port 5015. | PROPOSED | Daisy | Fits existing Python tooling and desired Google-style UX while keeping UI/API independent. |
| SM-P004 | Workflow | Define a pluggable durable-workflow interface; begin local/simple if necessary, but preserve an upgrade path to Temporal or equivalent for long-running retries/recovery. | PROPOSED | Daisy | Provisioning spans multiple external systems and must recover from partial failure. |
| SM-P005 | Runtime | Evaluate Agyn as an optional secure agent-runtime provider rather than reimplementing Kubernetes isolation/credential brokering immediately. | PROPOSED | Daisy | Current landscape research shows strong overlap in runtime/security but not complete Swarm Manager lifecycle. |
| SM-P006 | UI | Organize the Swarm Manager shell around `Swarms`, `Blueprints`, `Builder`, `Protocols`, `Integrations`, `Jobs`, and `Settings`. | PROPOSED | Daisy | Maps directly to product mental model and keeps lifecycle visible. |
| SM-P007 | Retirement | Retirement uses two phases: `ARCHIVED/RETIRED` first, then `DESTROYED` only after evidence capture and explicit Owner confirmation. | PROPOSED | Daisy | Makes destructive behavior safer and auditable. |

## Decision maintenance rule

Do not change the meaning of an accepted row silently. When the Owner changes direction, add a new decision and mark the prior one `SUPERSEDED` with a pointer to the replacement.
