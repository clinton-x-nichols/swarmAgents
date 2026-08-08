# Decision Register

| ID | Area | Decision | Status | Owner | Evidence / Rationale |
|---|---|---|---|---|---|
| D-001 | Swarm OS | Use GitHub as durable coordination/memory plane and channels for live coordination. | Template default — owner to confirm | Owner | Derived from Swarm OS architecture. |
| D-002 | Communications | Use separate substantive and notices channels. | Template default — owner to confirm | Owner | Prevents state pings from burying work content. |
| D-003 | Security | Direct platform-required owner authorization cannot be delegated through another agent or repository. | Binding default | Owner / Platform | Security boundary. |
| D-004 | Engineering Notebook | Every swarm maintains an explicit GitHub engineering notebook/design record; compact decision/open-question/work registers may live in `state/` and are incorporated into the notebook by reference to avoid duplicate sources of truth. | Binding template default | Owner | Long-running swarms need durable rationale/history in addition to a current-state snapshot. |
| D-005 | Memory | Agent memory is a separate continuity layer for identity, behavioral rules, collaboration conventions, and reusable lessons; it must not become a competing store for current project state. | Binding template default | Owner | Separates “who/how we operate” from “what the project currently is.” |
| D-006 | Slack/GitHub Sync | Durable decisions and material work-state changes reached in Slack are normalized into GitHub; counterpart-impacting notebook changes use a fresh-read `NOTEBOOK UPDATE` / `NOTEBOOK SYNC COMPLETE` handshake. | Binding template default | Owner | Prevents decisions from existing only in transient conversation and forces actual Git verification. |
| D-007 | Protocol | Swarm Protocol 1.1.0 adds engineering-notebook/memory layers plus stronger channel-state/session/fresh-read rules (`BLOCKED` reason required; `IDLE` only with empty queue; HELLO/GOODBYE boundaries; freshness gates posting, never reading; full active-thread read). | Binding template default | Owner | Derived from observed multi-agent coordination failures and recoveries. |

Add swarm-specific decisions during commissioning. Never reuse an existing ID for a different decision.
