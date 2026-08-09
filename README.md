# swarmAgents

`swarmAgents` is a reusable library and factory for human-supervised AI swarms, and the design home for the emerging **Swarm Manager** lifecycle control plane.

The repository separates the stable **Swarm Operating System** from **swarm-type profiles**. A new swarm is instantiated from `core/` plus one profile under `swarm-types/`, then commissioned conversationally with the human owner.

## Architecture

```text
swarmAgents/
├── TRANSFER_PROMPT.md        # clean bootstrap for a dedicated Swarm Agents ChatGPT session
├── engineering-notebook/     # durable design/history for THIS parent project / Swarm Manager
├── core/                     # task-agnostic Swarm OS copied into every live swarm
│   ├── personas/
│   │   └── DAISY.md          # portable Daisy persona entry point; no domain-project state
│   ├── memory/               # agent identity/rules/lessons continuity
│   ├── engineering-notebook/ # reusable notebook TEMPLATE copied into each live swarm
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

The instantiated swarm is a separate Git repository. The parent `swarmAgents` repository remains a reusable template library and product-development repository; it should not become the live state store for every swarm.

## Parent-project engineering notebook

The root [`engineering-notebook/`](engineering-notebook/) is the canonical durable design/history layer for **this repository and the Swarm Manager product**. It records the project charter, accepted/proposed decisions, engineering narrative, construction notes, failures/alternatives, open questions, architecture proposals, landscape research, and work queue.

This is intentionally distinct from [`core/engineering-notebook/`](core/engineering-notebook/), which is a generic notebook template copied into each new live swarm.

Start with [`engineering-notebook/00_INDEX.md`](engineering-notebook/00_INDEX.md).

## Swarm Manager direction

The Owner-defined product direction is a modular, open-source swarm lifecycle control plane with a Google/Material-style web UI on port **5015**. It should let a user choose or design a swarm, provision the required identities/repositories/communications/protocols/configuration, commission the agents automatically, then later archive and safely deprovision the swarm.

The current architecture is still under review. See [`engineering-notebook/06_PROPOSED_ARCHITECTURE.md`](engineering-notebook/06_PROPOSED_ARCHITECTURE.md) and [`engineering-notebook/07_LANDSCAPE_RESEARCH.md`](engineering-notebook/07_LANDSCAPE_RESEARCH.md).

## Starting a dedicated Swarm Agents session

For a fresh ChatGPT conversation devoted to this repository, paste [`TRANSFER_PROMPT.md`](TRANSFER_PROMPT.md).

That prompt loads the root project notebook for current Swarm Manager intent and [`core/personas/DAISY.md`](core/personas/DAISY.md) for portable personality/working style. Project state and authority still come from the current repository and Owner instructions, never from another project's chat history.

## Continuity model for provisioned swarms

Every live swarm deliberately separates:

- **Slack substantive channel** — live work, reasoning, decisions, evidence, review;
- **Slack notices channel** — terse task/session state only;
- **`state/CURRENT_STATE.md`** — small current coordination snapshot;
- **engineering notebook/registers** — durable decisions, rationale, open questions, work history, construction notes, reconciliation;
- **agent memory** — identity, behavioral rules, collaboration conventions, reusable lessons;
- **Git history** — evidence of what actually changed.

The operating loop is explicit: durable Slack outcomes are normalized into GitHub, and counterpart-impacting notebook changes use a fresh-read `NOTEBOOK UPDATE` / `NOTEBOOK SYNC COMPLETE` handshake. The receiving agent reports the commit it actually read.

See [`core/playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md`](core/playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md).

## Quick start — current file-based factory

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

The Swarm Manager product is intended to automate this manual path and extend it to external resource lifecycle management rather than discard the Swarm OS foundation.

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
