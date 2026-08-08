# swarmAgents

`swarmAgents` is a reusable library and factory for human-supervised AI swarms.

The repository separates the stable **Swarm Operating System** from **swarm-type profiles**. A new swarm is instantiated from `core/` plus one profile under `swarm-types/`, then commissioned conversationally with the human owner.

## Architecture

```text
swarmAgents/
├── TRANSFER_PROMPT.md        # clean bootstrap for a dedicated Swarm Agents ChatGPT session
├── core/                     # task-agnostic Swarm OS copied into every swarm
│   ├── personas/
│   │   └── DAISY.md          # portable Daisy personality; no domain-project state
│   ├── memory/               # agent identity/rules/lessons continuity
│   ├── engineering-notebook/ # durable design/history layer
│   ├── state/                # quick current coordination + compact registers
│   ├── comms/                # Slack/channel behavior
│   └── playbooks/            # protocol, security, memory, notebook, QA
├── swarm-types/              # reusable role/workflow overlays
│   ├── general/
│   ├── research/
│   ├── documentation/
│   └── software-development/
├── scripts/
│   ├── create_swarm.py       # instantiate a new swarm into a target Git clone
│   └── validate_library.py   # validate this parent library
└── docs/
    ├── ARCHITECTURE.md
    ├── CREATE_NEW_SWARM.md
    └── LESSONS_LEARNED.md
```

The instantiated swarm is a separate Git repository. The parent `swarmAgents` repository remains a reusable template library; it should not become the live state store for every swarm.

## Starting a dedicated Swarm Agents session

For a fresh ChatGPT conversation devoted to this repository, paste [`TRANSFER_PROMPT.md`](TRANSFER_PROMPT.md).

That prompt loads [`core/personas/DAISY.md`](core/personas/DAISY.md) for portable personality/working style while requiring all project state and authority to come from the new swarm's own commissioning record.

## Continuity model

Every live swarm deliberately separates:

- **Slack substantive channel** — live work, reasoning, decisions, evidence, review;
- **Slack notices channel** — terse task/session state only;
- **`state/CURRENT_STATE.md`** — small current coordination snapshot;
- **engineering notebook/registers** — durable decisions, rationale, open questions, work history, construction notes, reconciliation;
- **agent memory** — identity, behavioral rules, collaboration conventions, reusable lessons;
- **Git history** — evidence of what actually changed.

The operating loop is explicit: durable Slack outcomes are normalized into GitHub, and counterpart-impacting notebook changes use a fresh-read `NOTEBOOK UPDATE` / `NOTEBOOK SYNC COMPLETE` handshake. The receiving agent reports the commit it actually read.

See [`core/playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md`](core/playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md).

## Quick start

1. Create an empty GitHub repository for the new swarm.
2. Clone both this library and the empty swarm repository on the Worker host.
3. From the `swarmAgents` clone, list available profiles:

   ```bash
   python3 scripts/create_swarm.py --list
   ```

4. Instantiate a profile into the new swarm clone:

   ```bash
   python3 scripts/create_swarm.py \
     --type research \
     --target ~/swarms/market-research-swarm
   ```

5. Enter the new swarm repository and run its interactive bootstrap:

   ```bash
   cd ~/swarms/market-research-swarm
   python3 scripts/bootstrap_swarm.py
   python3 scripts/validate_swarm.py
   ```

6. Commit and push the initialized swarm, then use the generated ChatGPT and Worker bootstrap prompts to commission both agents.

See [`docs/CREATE_NEW_SWARM.md`](docs/CREATE_NEW_SWARM.md) for the full procedure.

## Design principles

**Conversation reasons. Slack coordinates. Notices signal. Current state orients. The engineering notebook remembers the program. Agent memory remembers how the agents operate. Git history proves what changed.**

A second principle is equally important: **agent-to-agent coordination never elevates authorization.** If the Worker platform requires direct human approval, the human owner must provide it directly.

Additional rules include:

- fresh reads outrank remembered summaries;
- primary evidence outranks confident assertions;
- `BLOCKED` names an exact dependency;
- `IDLE` means no executable work remains;
- `HELLO` / `GOODBYE` distinguish session boundaries from task state;
- state freshness gates posting, never reading;
- every queue/status cycle reads the full active thread;
- block the dependency rather than the entire swarm;
- consolidate genuine owner decisions instead of serial micro-escalation;
- use precise completion vocabulary;
- convert repeated failures into protocol changes rather than repeated reminders.

See [`docs/LESSONS_LEARNED.md`](docs/LESSONS_LEARNED.md) for the retrospective that produced these rules.

## Adding a new swarm type

Create `swarm-types/<type>/profile.json` and optionally an `overlay/` directory. `create_swarm.py` copies `core/` first, then copies the overlay on top, and finally applies the profile defaults to `swarm-config.json`.

The goal is to configure new swarms, not reinvent their operating model every time.
