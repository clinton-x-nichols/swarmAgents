# Swarm Operating System (Swarm OS)

A reusable, human-supervised operating system for a two-agent AI swarm: a conversational **Orchestrator** (typically ChatGPT) and an execution-focused **Worker** (typically Claude Code), coordinated through a GitHub repository and two communication channels.

Swarm OS is intentionally **task-agnostic**. The swarm may write code, perform research, produce documentation, analyze evidence, or support another bounded workflow. What changes between swarms are the names, personalities, models, tools, domain goals, and definition of done. The coordination architecture stays stable.

## What this repository gives you

- A commissioning interview that converts a vague goal into a concrete swarm configuration.
- A required research sidebar that looks for current role/prompt patterns before you reinvent them.
- A durable `AGENTS.md` shared instruction layer plus a Claude-specific `CLAUDE.md` adapter.
- A versioned Swarm Protocol covering authority, channels, state, work dispatch, security, QA, and recovery.
- A GitHub-backed current-state file so agents can reconcile state without replaying long chat history.
- A two-channel communications model: substantive coordination + terse notices.
- Role templates for orchestrator, worker, researcher, reviewer, and documentarian.
- Paste-ready bootstrap prompts generated from `swarm-config.json`.
- A full cold-start / restart / recovery runbook.
- Validation scripts that catch missing files, unresolved placeholders, and inconsistent config.
- Lessons learned from the DDCRM Daisy/Fable swarm, generalized into reusable operating rules.

## The mental model

```text
                      HUMAN OWNER
                  final authority / goals
                           |
                           v
               CONVERSATIONAL ORCHESTRATOR
              design / synthesis / decisions / QA
                  |                    ^
        bounded work orders            | results / questions
                  v                    |
                    EXECUTION WORKER
             implementation / evidence / git
                           |
                           v
                  DURABLE COORDINATION PLANE
             GitHub: protocol + state + decisions
                           |
                  +--------+--------+
                  |                 |
            substantive channel   notices channel
          design/work/evidence    STARTED/BLOCKED/
                                  DONE/IDLE only
```

The GitHub repository is the shared durable coordination plane. Slack (or equivalent) is live coordination, not durable memory. The owner remains the authority. Neither GitHub nor Slack can bypass an agent platform's security or consent requirements.

## Quick start

If you are starting from the downloadable ZIP, use **[`bootstrap/CREATE_FROM_ZIP.md`](bootstrap/CREATE_FROM_ZIP.md)** for the complete host → clone → extract → bootstrap → commission procedure.

1. Create a new Git repository from this template.
2. Clone it locally.
3. Run:

   ```bash
   python scripts/bootstrap_swarm.py
   ```

4. Review the generated `swarm-config.json`, `generated/chatgpt-bootstrap-prompt.md`, and `generated/worker-bootstrap-prompt.md`.
5. Create the substantive and notices channels named in the config.
6. Commit and push the initialized repository.
7. Start a new ChatGPT conversation and paste the generated ChatGPT bootstrap prompt.
8. Let the Orchestrator interview you, research current role/prompt patterns, and propose **adopt / adapt / build** choices.
9. After you approve the configuration, start the Worker in the repository and paste the generated Worker bootstrap prompt.
10. Run the commissioning smoke tests in `bootstrap/COMMISSIONING_CHECKLIST.md`.
11. Begin real work only after both agents agree on the same role, protocol version, current state, active work item, owner decisions, and security boundaries.

For the complete procedure, read [BOOTSTRAP.md](BOOTSTRAP.md).

## Core files

| File | Purpose |
|---|---|
| `swarm-config.json` | Names, models, channels, purpose, systems of record, and owner-approved defaults. |
| `AGENTS.md` | Tool-agnostic shared operating instructions. |
| `CLAUDE.md` | Claude Code bootstrap adapter; points Claude to shared canonical instructions. |
| `playbooks/SWARM_PROTOCOL.md` | Binding coordination protocol. |
| `state/CURRENT_STATE.md` | Single quick-reference current state. |
| `state/DECISION_REGISTER.md` | Durable accepted decisions and authority. |
| `state/OPEN_QUESTIONS.md` | Genuine unresolved questions and owner dependencies. |
| `state/WORK_QUEUE.md` | Bounded work items and sequencing. |
| `comms/CHANNEL_PROTOCOL.md` | Substantive-channel and notices-channel rules. |
| `playbooks/MEMORY_AND_RECOVERY.md` | Cold boot, restart, reconciliation, and stale-state handling. |
| `playbooks/FAILURE_MODES.md` | Known coordination failures and exact recovery actions. |
| `playbooks/QUALITY_GATES.md` | Commissioning, dispatch, verification, and closure QA. |
| `playbooks/SECURITY_AND_AUTHORITY.md` | Human authorization, platform guardrails, and no instruction laundering. |
| `research/ROLE_PROMPT_RESEARCH.md` | Mandatory ecosystem research and adopt/adapt/build rubric. |
| `LESSONS_LEARNED.md` | What worked, what failed, and the operating rules derived from both. |

## Design principle

**Conversation is for reasoning. Git is for memory. Notices are for state. The owner is for genuine decisions.**

If those four jobs get mixed together, the swarm becomes noisy, stale, and difficult to recover. Swarm OS keeps them separate.
