# Create a New Swarm from the `swarmAgents` Parent Repository

This is the preferred path when the reusable `swarmAgents` library already exists.

## 1. Create the live swarm GitHub repository

Create a new empty/private repository for the actual swarm. Example: `marketResearchSwarm`.

The live swarm repository is where current state, decisions, work orders, and evidence will live. Do not use the parent `swarmAgents` repository as live state for multiple swarms.

## 2. Log into the Worker host

```bash
ssh USER@HOST
mkdir -p ~/swarms
cd ~/swarms
```

Verify prerequisites:

```bash
git --version
python3 --version
ssh -T git@github.com
```

## 3. Clone the parent library

```bash
git clone git@github.com:clinton-x-nichols/swarmAgents.git
```

If it already exists:

```bash
cd ~/swarms/swarmAgents
git pull --ff-only
cd ..
```

## 4. Clone the empty live swarm repository

```bash
git clone git@github.com:YOUR-ACCOUNT/marketResearchSwarm.git
```

## 5. Review available swarm types

```bash
cd ~/swarms/swarmAgents
python3 scripts/create_swarm.py --list
```

## 6. Instantiate the selected type

```bash
python3 scripts/create_swarm.py \
  --type research \
  --target ~/swarms/marketResearchSwarm
```

The command:

1. copies the task-agnostic `core/` Swarm OS;
2. applies the selected swarm type's `overlay/` files;
3. writes profile defaults into `swarm-config.json`;
4. records the chosen type in `swarm-type/PROFILE.json` and `swarm-type/README.md`.

It refuses to overwrite a non-empty non-Git directory unless `--force` is explicitly supplied.

## 7. Run the live swarm bootstrap

```bash
cd ~/swarms/marketResearchSwarm
python3 scripts/bootstrap_swarm.py
python3 scripts/validate_swarm.py
```

Answer the initial identity, mission, role, model, channel, repository, and evidence questions. Detailed commissioning continues conversationally with the ChatGPT Orchestrator.

## 8. Review, commit, and push

```bash
git status
git add -A
git diff --cached
git commit -m "Initialize research swarm"
git push -u origin HEAD
```

Never commit credentials, tokens, private keys, or `.env` secrets.

## 9. Create the two coordination channels

Use one substantive channel and one notices channel. Example:

- `market-research-swarm`
- `market-research-swarm-notices`

Substantive channel: design, questions, decisions, work instructions, evidence, review.

Notices channel: concise `STARTED`, `STILL WORKING`, `BLOCKED`, `DONE`, `IDLE` state markers only.

## 10. Bootstrap the ChatGPT Orchestrator

Paste `generated/chatgpt-bootstrap-prompt.md` into a fresh ChatGPT conversation with access to the live swarm repo and coordination channels.

The Orchestrator first interviews the Owner and performs the required current role/prompt research sidebar. It should present **Adopt / Adapt / Build** choices before finalizing specialized roles.

## 11. Approve the commissioning design

The Owner approves or corrects mission, definition of done, roles, personalities, authority, systems of record, evidence rules, and imported/adapted prompt patterns.

The Orchestrator reconciles that state into Git and moves `CURRENT_STATE.md` to `READY_TO_COMMISSION`.

## 12. Pull on the Worker host and bootstrap the Worker

```bash
cd ~/swarms/marketResearchSwarm
git pull --ff-only
claude
```

Paste `generated/worker-bootstrap-prompt.md` into the Worker environment. The Worker returns a BOOTLOAD rather than starting project execution.

## 13. Run commissioning smoke tests

Use `bootstrap/COMMISSIONING_CHECKLIST.md`. At minimum verify:

- stale-state recovery;
- full-thread read discipline;
- direct-owner security challenge behavior;
- intervening Git commit handling;
- restart/bootstrap recovery;
- distinction between analysis/reconciliation complete and independently VERIFIED.

## 14. Mark the swarm commissioned

Only after both agents reconcile the same durable state and smoke tests pass should `state/CURRENT_STATE.md` become `COMMISSIONED`.

## 15. Begin real work

The Orchestrator activates a bounded work item; the Worker fresh-reads, posts a notice, executes, returns evidence, and updates durable state under the Swarm Protocol.
