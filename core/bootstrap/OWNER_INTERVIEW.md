# Owner Commissioning Interview

The Orchestrator conducts this as a conversation, not a questionnaire dump.

Ask one high-leverage question at a time. Reuse answers already given. Do not ask the Owner to fill information the Orchestrator can reliably infer from connected canonical sources.

## Interview domains

### Goal

- What outcome should this swarm produce?
- What does “done” look like?
- What is explicitly out of scope?

### Work shape

- Is the work primarily coding, research, documentation, analysis, or mixed?
- What artifacts will be created or changed?
- What systems are authoritative?

### Roles

- What should the ChatGPT-side role own?
- What should the Worker-side role own?
- What decisions must remain human-only?
- Are optional specialist agents useful?

### Identity and personality

- Names for Orchestrator and Worker.
- Desired tone/personality.
- Humor/levity boundaries.
- Communication density.
- How strict should each agent be about review?

### Platforms and models

- ChatGPT configuration/model.
- Worker platform/model.
- Tool availability.
- Connectors/integrations.

### Communication

- Substantive channel name.
- Notices channel name.
- Threading expectations.
- How to handle long silence/stale status.

### Authority/security

- Production/destructive/publish/financial/credential gates.
- Actions that must be typed directly by the Owner in a specific product.
- Secrets/data handling.

### Quality/evidence

- Required tests/readback/citations/diffs/screenshots/review.
- Independent verifier needed?
- Acceptance threshold.

### Continuity

- Expected session restarts.
- Required durable state.
- How much history should be preserved versus summarized.

## Finish condition

The interview is complete when the Orchestrator can populate `swarm-config.json`, identify unresolved owner decisions precisely, and explain the swarm back to the Owner in one compact commissioning summary.
