# Daisy Portable Memory Bundle

This directory is the modular, cross-project memory layer for Daisy's conversational identity and collaboration style.

It is intentionally narrower than any live swarm's project memory. It must never become a second store for mission, current work, project decisions, source-system state, or authorization.

## Single-home map

- `IDENTITY.md` — who Daisy is.
- `AUTHORITY-BOUNDARY.md` — portable authority boundary.
- `VOICE-AND-RITUALS.md` — voice, greetings, humor, and conversational texture.
- `CHALLENGE-AND-ENRICHMENT.md` — reviewer/orchestrator challenge duty.
- `COLLABORATION-MODEL.md` — how Daisy works with the Owner, Worker, evidence, and durable state.

`../DAISY.md` is only the entry point and read-order declaration. Do not duplicate detailed rules there.

## Boot rule

When `../DAISY.md` is loaded, fresh-read every file in this directory named by its required bundle read order before relying on remembered personality or collaboration habits.

After loading this bundle, leave the persona layer and fresh-read the live swarm's own protocol, security model, engineering notebook, current state, Git head, channels, and external systems of record.

## Provenance and scope

This bundle was generalized from `clinton-x-nichols/ddcrm-risk-management/daisy-memories/`, whose own scope separates Daisy continuity from DDCRM project state. Source snapshot checked 2026-08-07 at commit `485c3bf29cf018b0617d7808656cd15ac0cddc4c`.

The source tree included DDCRM-specific authority and operational history. Those details are not portable and were not copied. The portable rule is the opposite: persona memory never manufactures authority in a new swarm.
