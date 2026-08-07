# swarmAgents

`swarmAgents` is a reusable library and factory for human-supervised AI swarms.

The repository separates the stable **Swarm Operating System** from **swarm-type profiles**. A new swarm is instantiated from `core/` plus one profile under `swarm-types/`, then commissioned conversationally with the human owner.

## Architecture

```text
swarmAgents/
├── core/                     # task-agnostic Swarm OS copied into every swarm
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

**Conversation is for reasoning. Git is for memory. Notices are for state. The owner is for genuine decisions.**

A second principle is equally important: **agent-to-agent coordination never elevates authorization.** If the Worker platform requires direct human approval, the human owner must provide it directly.

## Adding a new swarm type

Create `swarm-types/<type>/profile.json` and optionally an `overlay/` directory. `create_swarm.py` copies `core/` first, then copies the overlay on top, and finally applies the profile defaults to `swarm-config.json`.

The goal is to configure new swarms, not reinvent their operating model every time.
