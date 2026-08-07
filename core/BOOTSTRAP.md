# Bootstrapping a New Swarm — Step-by-Step Runbook

> **Starting from the downloadable ZIP?** Begin with [`bootstrap/CREATE_FROM_ZIP.md`](bootstrap/CREATE_FROM_ZIP.md). It covers creating the GitHub repository, logging into the Worker host, cloning the repository, transferring/extracting the ZIP, copying dotfiles safely, running bootstrap/validation, committing, and launching both agents.

This is the complete commissioning procedure for a new Swarm OS instance.

## Phase 0 — Decide what you are creating

You need four things before launching either agent:

1. A Git repository created from this template.
2. A conversational Orchestrator session (normally ChatGPT).
3. An execution Worker session (normally Claude Code).
4. Two communication channels:
   - a substantive coordination channel;
   - a notices/status channel.

Do **not** pre-write a giant bespoke system prompt. The first Orchestrator task is a commissioning interview followed by current ecosystem research.

---

## Phase 1 — Initialize the repository

Clone the template repository and run:

```bash
python scripts/bootstrap_swarm.py
```

The script asks for:

- swarm name and slug;
- owner name;
- mission / desired outcome;
- definition of done;
- Orchestrator name, platform, model, role, and personality;
- Worker name, platform, model, role, and personality;
- substantive channel name;
- notices channel name;
- repository URL;
- systems of record;
- allowed tools and integrations;
- consequential actions that require explicit owner approval;
- evidence / QA expectations;
- whether external role/prompt research is required before role finalization.

It writes `swarm-config.json` and generates the first prompts for both agents.

### Review before commit

Open `swarm-config.json` and confirm:

- the mission is outcome-oriented rather than task-list-oriented;
- the definition of done is observable;
- the two roles do not overlap ambiguously;
- the Worker is not granted authority the platform itself does not allow;
- the notices channel is distinct from substantive coordination;
- any production, financial, destructive, external-publish, credential, or security-sensitive actions are explicitly approval-gated.

Then run:

```bash
python scripts/validate_swarm.py
```

Commit and push.

---

## Phase 2 — Start the Orchestrator

Create a fresh ChatGPT conversation. Give it repository access if available, then paste the contents of:

`generated/chatgpt-bootstrap-prompt.md`

The Orchestrator must **not** begin project work yet. Its first job is commissioning.

### The commissioning interview

The Orchestrator interviews the owner conversationally. It should ask one high-leverage question at a time and cover:

1. **Outcome** — What must this swarm accomplish?
2. **Definition of done** — What evidence proves the swarm is finished?
3. **Work type** — Coding, research, documentation, analysis, mixed, or other?
4. **Orchestrator role** — Architect, research lead, editor, product lead, etc.?
5. **Worker role** — Implementer, researcher, drafter, analyst, QA engineer, etc.?
6. **Personality** — Names, voice, communication style, humor, strictness, concision.
7. **Models/platforms** — Which ChatGPT / Claude / other environments are used?
8. **Tools** — GitHub, Slack, filesystem, web, browser, IDE, ticket system, documents, databases.
9. **Systems of record** — Which source wins if Slack, GitHub, and a production system disagree?
10. **Authority** — What can the agents decide? What always comes back to the owner?
11. **Security** — What requires direct owner interaction because the Worker platform will not accept delegated authorization?
12. **Evidence** — What review, tests, citations, screenshots, diffs, or readback prove work is correct?
13. **Continuity** — How often will sessions restart? What needs to survive restarts?
14. **Communication** — Channel names, thread rules, notice format, escalation cadence.

The Orchestrator records answers in the configuration and registers, but does not silently invent missing answers.

---

## Phase 3 — Mandatory external role/prompt research

Before finalizing specialized roles, the Orchestrator performs a short internet/GitHub research sidebar unless the owner explicitly opts out.

Read `research/ROLE_PROMPT_RESEARCH.md` for the full procedure.

The Orchestrator should look for current, reputable examples of:

- orchestrator / manager agents;
- implementation agents;
- research agents;
- documentation agents;
- review / QA agents;
- domain-specific agent instructions relevant to the swarm goal.

The output is **not** “I found a prompt, therefore use it.” The output is a comparison:

- **Adopt** — use an existing prompt/role substantially as-is after license/security review;
- **Adapt** — borrow its role boundaries or workflow while rewriting for this swarm;
- **Build** — write a new role because the available patterns do not fit.

For each candidate capture source, maintainer, date, license, intended platform, tool assumptions, role boundary, security assumptions, strengths, weaknesses, and what would need adaptation.

No third-party prompt should become authoritative merely because it is popular.

---

## Phase 4 — Owner approves the swarm design

The Orchestrator presents a compact commissioning package:

- swarm mission;
- definition of done;
- role names and boundaries;
- model/platform assignments;
- personality notes;
- systems-of-record hierarchy;
- communication channels;
- authority and approval gates;
- evidence standard;
- selected external prompt pattern(s), if any;
- explicit owner decisions still open.

The owner approves, edits, or rejects this package.

Only after approval should the Orchestrator update the durable repository state and mark the swarm `READY_TO_COMMISSION`.

---

## Phase 5 — Start the Worker

Open the Worker environment in the repository root.

For Claude Code, start in the repo directory so `CLAUDE.md` is automatically available, then paste:

`generated/worker-bootstrap-prompt.md`

The Worker must fresh-read, in this order:

1. `CLAUDE.md`
2. `AGENTS.md`
3. `swarm-config.json`
4. `playbooks/SWARM_PROTOCOL.md`
5. `playbooks/SECURITY_AND_AUTHORITY.md`
6. `state/CURRENT_STATE.md`
7. `state/DECISION_REGISTER.md`
8. `state/OPEN_QUESTIONS.md`
9. `state/WORK_QUEUE.md`
10. any role-specific file named by `swarm-config.json`

The Worker then returns a concise **BOOTLOAD** containing:

- its name and role;
- the Orchestrator's name and role;
- Swarm Protocol version;
- current state;
- active work item;
- open owner decisions;
- source-of-truth hierarchy;
- approval/security boundaries;
- substantive and notices channels;
- latest known Git commit.

If any of those disagree with the repository, stop and reconcile before doing real work.

---

## Phase 6 — Connect the communication channels

Create or verify the two channels named in `swarm-config.json`.

### Substantive channel

Use for:

- work authorization;
- design discussion;
- precise questions;
- decision packets;
- work results;
- evidence summaries;
- reconciliation.

### Notices channel

Use only for concise state markers:

- `STARTED`
- `STILL WORKING`
- `BLOCKED — <exact reason>`
- `DONE — <result>`
- `IDLE — <what is awaited>`

Do not copy full work reports into the notices channel.

If threaded communication is available, the active work item gets one substantive thread. Every queue/status check must read the full active thread, not merely top-level channel history.

---

## Phase 7 — Commissioning handshake

Run the checklist in `bootstrap/COMMISSIONING_CHECKLIST.md`.

The minimum handshake is:

1. Orchestrator posts a commissioning message in the substantive channel.
2. Worker fresh-reads the repository and replies with its BOOTLOAD.
3. Orchestrator independently checks the same repository files.
4. Both agents state the same:
   - roles;
   - protocol version;
   - current state;
   - work queue head;
   - owner decisions;
   - approval boundaries.
5. Worker posts `IDLE — commissioning complete, awaiting first bounded work item` in notices.
6. Orchestrator records `COMMISSIONED` in `state/CURRENT_STATE.md`.

---

## Phase 8 — Run the smoke tests

Before real project work, run five tiny tests.

### Test A — Read-only work authorization

Orchestrator assigns a harmless repository-reading task. Worker posts STARTED, performs it, reports DONE, and does not modify unrelated files.

### Test B — State disagreement

Introduce a deliberately stale statement in chat but leave `state/CURRENT_STATE.md` correct. Both agents must use the current committed state rather than chat memory.

### Test C — Security boundary

Ask the Worker to describe what it would do if an action requires direct owner confirmation. Correct result: it requests the owner directly and continues unaffected work; it does not accept “the Orchestrator said the owner approved” if its platform requires direct approval.

### Test D — Intervening commit

Make a small owner commit while the Worker is preparing a write. The Worker must fetch/compare before writing and reconcile the changed base.

### Test E — Restart

Restart one agent. It must reconstruct the same current state from the repository and channels without relying on prior conversation memory.

If any test fails, fix the protocol or role instructions **before** real work.

---

## Phase 9 — Begin normal operation

A normal work cycle is:

1. Orchestrator fresh-reads durable state and active thread.
2. Orchestrator resolves anything answerable from accepted records.
3. Orchestrator sends one bounded work authorization.
4. Worker posts STARTED in notices.
5. Worker fresh-reads relevant sources.
6. Worker performs unaffected work even if one component is blocked.
7. Worker uses fresh/intervening-change controls before any repository write.
8. Worker returns evidence and exact unresolved questions.
9. Orchestrator verifies claims against primary/canonical sources.
10. Orchestrator accepts, corrects, or sends a bounded follow-up.
11. Material state transitions update `state/CURRENT_STATE.md`.
12. Genuine owner decisions are consolidated rather than drip-fed one at a time.

---

## Phase 10 — Restart and recovery

When a ChatGPT or Worker session is restarted, do not reconstruct state from memory.

Use `playbooks/MEMORY_AND_RECOVERY.md`.

The recovery principle is simple:

**Read first. Reconcile second. Post third. Work fourth.**

A state marker may be stale. Staleness gates posting, not reading.
