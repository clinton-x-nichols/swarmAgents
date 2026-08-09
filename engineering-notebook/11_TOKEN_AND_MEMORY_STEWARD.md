# Future Module — Token Monitor and Memory Manager

**Status:** Owner-accepted future capability. Detailed implementation remains intentionally evolvable.

## Purpose

Add a future per-swarm observability and governance capability that continuously answers two questions:

1. **Are agents using model tokens efficiently without losing required functionality or quality?**
2. **Do agents remember what durable memory says they should remember, and is memory drift visible and manageable?**

The capability has two surfaces:

- a **Token Monitor / Token Efficiency** dashboard module;
- a **Memory Manager** dashboard module.

A participating swarm agent may own the combined stewardship role. Working name: **Token & Memory Steward**. The final role name, whether this remains one role or splits into two roles, and the exact dashboard layout are future design decisions.

## 1. Token Monitor — accepted functional direction

The Token Monitor tracks token usage for every participating agent as first-class telemetry.

At minimum, capture per agent and per model interaction:

- input/prompt tokens sent;
- output/completion tokens received;
- total tokens;
- model/runtime identity;
- timestamp;
- request/work-item correlation;
- optional latency/cost metadata when available;
- context-window utilization when the runtime exposes it.

Aggregate views should support:

- per interaction;
- per work item;
- per session;
- per agent;
- per swarm;
- trend over time.

### Prompt-efficiency analysis

The monitoring path should be able to observe the prompts sent by each agent to its model and compare those prompts against configurable token-efficiency best practices.

Examples of analysis dimensions:

- repeated context that could be referenced rather than resent;
- redundant instructions;
- unnecessarily verbose role/system material;
- duplicate evidence or conversation history;
- failure to summarize/archive older context;
- prompts that request more output than the task requires;
- context that is irrelevant to the current operation;
- opportunities to use structured references, retrieval, or memory rather than full-text repetition;
- excessive retry/rephrase patterns;
- poor division between durable memory, current work state, and transient prompt context.

The system maintains a **Token Efficiency Report Card** for each agent.

Possible report-card fields:

- token efficiency score;
- input/output ratio;
- repeated-context ratio;
- avoidable-context estimate;
- average tokens per successful work unit;
- trend versus prior period;
- recommendations;
- confidence/evidence for each recommendation.

The goal is not simply to minimize tokens. The optimization objective is:

> **minimize unnecessary token consumption while retaining required capability, evidence quality, safety, reliability, and user experience.**

A lower-token prompt is not "better" if it loses required context or degrades the agent's work.

## 2. Token observability architecture — proposed guardrails

Prompt/response capture may contain secrets, private data, proprietary material, or large copyrighted/source content. Therefore token telemetry should support distinct capture levels rather than assuming raw prompt retention is always acceptable.

Proposed levels:

1. **metrics only** — token counts, model, timing, work-item IDs;
2. **structural analysis** — prompt sections, hashes, duplication fingerprints, lengths, but no full content retention;
3. **redacted content capture** — prompt text after secret/PII filtering;
4. **full content capture** — explicitly enabled for environments where policy allows it.

The Token Monitor is an observer/recommender by default. Recommendations to alter role prompts, context strategy, memory behavior, or runtime configuration should become reviewable configuration changes rather than silent self-modification.

## 3. Memory Manager — accepted functional direction

The Memory Manager provides a user-visible view of durable agent memories and monitors drift between expected memory and an agent's current reported recall.

### Configurable memory-recall checks

For each agent, configure a recurrence for a **memory reconciliation check**.

At each check:

1. identify the durable memories the agent is expected to retain under the memory protocol;
2. ask the agent, through its runtime adapter, what it currently remembers about the relevant durable-memory domains;
3. normalize the agent's response into comparable claims;
4. compare reported recall with durable stored memory;
5. log discrepancies;
6. classify the result;
7. surface material drift to the user and/or Token & Memory Steward.

Initial drift vocabulary may include:

```text
IN_SYNC
MISSING_MEMORY
STALE_MEMORY
CONTRADICTORY_MEMORY
UNEXPECTED_MEMORY
AMBIGUOUS_RECALL
UNOBSERVABLE
```

This is not intended to treat model recall as a perfect database query. The monitor is detecting operational continuity risk: the difference between **what durable memory says should govern the agent** and **what the agent currently demonstrates that it knows**.

### Durable-memory activity feed

The Memory Manager should surface newly created durable memories as an activity stream, including where possible:

- agent;
- memory identifier;
- category/type;
- creation time;
- provenance/source;
- reason it became durable;
- current status;
- supersedes/superseded-by links;
- trust/verification state when applicable.

### User management functions

The user can browse durable memories by swarm and agent and should eventually be able to:

- view;
- search/filter;
- inspect provenance;
- edit/modify;
- supersede;
- delete, subject to retention/security policy;
- trigger a fresh memory-reconciliation check.

Edits/deletions are governance actions and should be auditable. Where the memory model uses immutable decisions or append/supersede semantics, the UI should respect those rules rather than mechanically overwriting history.

## 4. Memory Manager UI — starting direction

The future swarm dashboard includes a **Memory Manager** page/module.

Potential views:

- swarm-level memory health summary;
- one tile/summary per agent;
- memory drift indicators;
- most recent reconciliation time;
- new durable-memory activity;
- memory browser/editor;
- per-agent recall history;
- manual "check memory now" action;
- recurrence configuration.

It remains intentionally undecided whether:

- all agents appear on one page as tiles/panels;
- each agent receives a dedicated memory page;
- or the interface uses a fleet summary with drill-down pages.

That decision should follow real scale and usability evidence.

## 5. Token & Memory Steward agent

A future swarm may include a dedicated **Token & Memory Steward** agent responsible for monitoring and analysis across the swarm.

Proposed responsibilities:

### Token stewardship

- review token telemetry;
- analyze prompt-efficiency patterns;
- maintain agent report cards;
- identify regressions/trends;
- propose context/prompt/memory optimizations;
- estimate likely token savings;
- verify that recommended optimizations preserve required behavior before acceptance.

### Memory stewardship

- schedule or initiate memory-reconciliation checks;
- review memory-drift findings;
- distinguish harmless phrasing variance from material continuity drift;
- surface newly durable memories;
- recommend memory cleanup/consolidation/supersession;
- identify memory bloat, duplication, stale guidance, or contradiction;
- escalate material discrepancies for review.

### Boundary

The Steward does **not** gain authority merely because it observes every agent.

By default it may:

- observe;
- score;
- analyze;
- recommend;
- create review items.

Changing another agent's durable memory, role prompt, security policy, protocol pin, or runtime configuration should follow the normal approval/change path for that resource.

## 6. Data and telemetry model — initial proposal

Future operational entities may include:

```text
ModelInteraction
TokenUsageSample
PromptAnalysis
AgentEfficiencyScorecard
EfficiencyRecommendation
MemoryRecord
MemoryReconciliationRun
MemoryRecallClaim
MemoryDriftFinding
MemoryChangeEvent
```

These records belong in operational/observability storage appropriate to their function. Durable memory content remains in the configured memory system of record; the dashboard should not create a second competing canonical copy.

## 7. Runtime/provider implications

Runtime adapters will need explicit capabilities such as:

```text
reports_token_usage
exposes_prompt_content
exposes_response_content
exposes_context_window
supports_memory_query
supports_memory_attestation
supports_interaction_correlation
```

Some platforms may provide precise token usage directly. Others may require tokenizer-based estimation. The UI should distinguish **reported** versus **estimated** token counts rather than pretending the measurements have equal confidence.

Likewise, some runtimes may permit a structured memory-recall challenge while others may only support conversational interrogation. Memory reconciliation must record the method used and its confidence.

## 8. Monitoring and alerts

Potential future alerts:

- sudden token-use regression for an agent;
- repeated identical context being resent;
- token use exceeds configurable threshold;
- scorecard efficiency falls below target;
- memory reconciliation detects missing/contradictory durable memory;
- memory check overdue;
- rapid growth in durable memories;
- duplicate/stale memory accumulation;
- memory edit/delete pending governance approval.

Thresholds should be configurable per swarm and potentially per role; a deep-research agent and a lightweight status agent should not be judged by identical token budgets.

## 9. Relationship to existing architecture

This capability fits the current Swarm Manager design without changing the lifecycle core:

- **Dashboard module provider** exposes Token Monitor and Memory Manager UI modules.
- **Runtime providers** expose interaction/token/memory-observation capabilities.
- **Operational database/telemetry store** holds token samples, analyses, scorecards, and reconciliation runs.
- **Agent memory system of record** remains canonical for durable memory contents.
- **Memory protocol** defines what should become durable and how memory is managed.
- **Reconciler** can treat material memory drift as an operational condition.
- **Token & Memory Steward** is an optional swarm role/agent, selected by blueprint or user configuration.

## 10. Evolution rule

This is the starting design, not a frozen final specification.

Expected future questions include:

- one combined Steward versus separate Token and Memory agents;
- one combined UI versus separate modules/pages;
- scoring algorithms and baselines;
- cost accounting by provider/model;
- automatic prompt compression versus recommendation-only mode;
- memory importance/decay models;
- safe deletion/retention policy;
- privacy/redaction requirements for prompt capture;
- whether memory drift should affect commissioning/READY or only ongoing health;
- swarm-level benchmarking across different role types and models.

Changes should be driven by operational evidence and recorded as new decisions rather than silently redefining this requirement.
