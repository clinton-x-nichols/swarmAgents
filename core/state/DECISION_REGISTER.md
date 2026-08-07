# Decision Register

| ID | Area | Decision | Status | Owner | Evidence / Rationale |
|---|---|---|---|---|---|
| D-001 | Swarm OS | Use GitHub as durable coordination/memory plane and channels for live coordination. | Template default — owner to confirm | Owner | Derived from Swarm OS architecture. |
| D-002 | Communications | Use separate substantive and notices channels. | Template default — owner to confirm | Owner | Prevents state pings from burying work content. |
| D-003 | Security | Direct platform-required owner authorization cannot be delegated through another agent or repository. | Binding default | Owner / Platform | Security boundary. |

Add swarm-specific decisions during commissioning. Never reuse an existing ID for a different decision.
