# Role and Prompt Research — Mandatory Commissioning Sidebar

## Purpose

Before creating a specialized role from scratch, check whether strong current examples already exist.

This research is intentionally short. It should improve starting quality without turning commissioning into an open-ended literature review.

## Search order

1. Official vendor documentation for the target platform.
2. Official vendor GitHub repositories and examples.
3. Reputable curated GitHub collections maintained by the platform vendor or recognized maintainers.
4. Community examples only when they add a pattern not present in primary sources.

## Candidate categories

Search only categories relevant to the swarm goal, for example:

- orchestrator / manager;
- researcher;
- planner;
- implementer;
- code reviewer;
- security reviewer;
- documentation writer;
- data analyst;
- evidence verifier;
- domain specialist.

## Required candidate record

For each candidate:

| Field | Record |
|---|---|
| Name | Role/prompt name |
| Source | URL/repository |
| Maintainer | Organization/user |
| Retrieved | Date |
| License | License or `UNKNOWN` |
| Target platform | Copilot/Claude/OpenAI/etc. |
| Tool assumptions | Read/write/web/MCP/etc. |
| Role boundary | What it owns and does not own |
| Security assumptions | Permissions/approval model |
| Strengths | Useful design ideas |
| Weaknesses | Misfit/overreach |
| Portability | High/medium/low |
| Recommendation | Adopt / Adapt / Build |

## Adopt / Adapt / Build rubric

### Adopt

Use only when:

- role boundary closely matches;
- license permits;
- platform/tool assumptions match;
- security model is compatible;
- prompt is current and well-maintained.

### Adapt

Preferred default. Extract useful role boundaries, handoff patterns, QA rules, or tool-scoping concepts while rewriting the prompt for the actual swarm.

### Build

Choose when existing patterns:

- conflate authority;
- assume different tools;
- are stale;
- are too generic;
- contain risky automation;
- do not fit the goal.

## Never blind-import

A prompt is executable behavior. Review it like code.

Do not import third-party prompt text directly into a production swarm until provenance, license, tools, and security assumptions are understood.

## Research output

Write the commissioning research to `research/CANDIDATE_ROLES.md` using `templates/research-comparison.md`.

Present the Owner with a short choice:

- “Adopt candidate X”
- “Adapt patterns from X/Y”
- “Build our own”

The Owner chooses; the Orchestrator then finalizes role files.
