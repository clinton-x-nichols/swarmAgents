# Reconciliation Log

Record material discrepancies between conversation, project notebook, repository state, external product evidence, and implementation. Do not log trivial no-change checks.

## 2026-08-07 — Parent project lacked a dedicated engineering notebook

**Sources compared:**

- Owner design-session requirement for a durable project engineering notebook;
- `swarmAgents/core/engineering-notebook/`;
- DDCRM `engineering-notebook/` structure.

**Discrepancy:**

`core/engineering-notebook/` is a reusable notebook template copied into provisioned swarms. It is not an appropriate canonical home for decisions about the parent `swarmAgents` library and Swarm Manager product. The parent project did not yet have its own equivalent durable design layer.

**Authority by information type:**

Owner instruction establishes the requirement. Repository architecture establishes that `core/` is copied into live swarms and therefore should remain task-agnostic.

**Resolution:**

Create root `engineering-notebook/` for the parent project. Adapt the successful structural pattern from DDCRM while excluding all DDCRM domain content.

**Residual uncertainty:** none on notebook separation; exact notebook files may evolve as the product matures.

---

## 2026-08-07 — “Latest protocol” versus reproducible running swarm

**Sources compared:**

- Owner requirement that new agents hit APIs for latest universal protocols;
- Swarm OS lesson that fresh state must remain auditable/recoverable;
- current control-plane design requirements.

**Discrepancy:**

If “latest” is dereferenced dynamically during normal agent operation, a running swarm could change behavior without its own spec/history changing.

**Resolution proposed:**

Use `latest-approved` only during create/upgrade planning, resolve it to immutable version + digest, store that pin in the swarm spec, and make upgrades explicit.

**Status:** proposed, not Owner-accepted yet (`SM-P002`).

---

## 2026-08-07 — Existing-product replacement check

**Sources compared:** current official/public materials for Agyn, Agno, CrewAI, Microsoft Agent Framework/AutoGen, LangGraph, Dify, Flowise, Hermes Agent, Crossplane, Backstage, Temporal, and AWX.

**Finding:**

Agyn and Agno overlap materially with agent runtime/control-plane concerns, but no verified product in this pass covered the complete requested lifecycle across local identities, GitHub, Slack, protocol registry, per-swarm modules, commissioning, and archive/deprovision.

**Resolution:**

Continue Swarm Manager architecture while treating Agyn/Agno as serious runtime/provider candidates. Do not duplicate their runtime/security capabilities without a proof-of-fit.

**Residual uncertainty:** a deeper hands-on evaluation may reveal more overlap than public docs show; this is explicitly queued as `SM-W005`.
