# Repository and Channel Setup

Use this when creating a swarm from scratch rather than cloning an already-configured swarm.

## 1. Create the GitHub repository

### GitHub web

1. Create a new empty repository.
2. Choose private/internal/public visibility appropriate to the project.
3. Do not add secrets to the repository.
4. Copy the Swarm OS template files into the repository.
5. Clone locally and run the bootstrap script.

### GitHub CLI alternative

If `gh` is installed and authenticated:

```bash
mkdir my-new-swarm
cd my-new-swarm
# Copy the Swarm OS template contents here first.
git init
git branch -M main
gh repo create <OWNER>/<REPO> --private --source=. --remote=origin
python scripts/bootstrap_swarm.py
python scripts/validate_swarm.py || true
git add .
git commit -m "Initialize Swarm OS commissioning scaffold"
git push -u origin main
```

The validator is expected to fail before configuration is complete; rerun it after the interview/bootstrap values are populated.

## 2. Create communication channels

Create two channels in Slack or the chosen collaboration platform.

Recommended naming:

```text
<swarm-slug>
<swarm-slug>-notices
```

Example:

```text
research-market-map
research-market-map-notices
```

Set the first as the substantive channel and the second as the notices channel in `swarm-config.json`.

## 3. Verify access independently

Do not assume both products see the same integrations.

Verify separately that:

- the Orchestrator can read GitHub;
- the Worker can read/write GitHub as required;
- the Orchestrator can read/post to the substantive and notices channels if expected;
- the Worker can read/post to those channels if expected;
- the Owner can directly reach the Worker environment for security confirmations.

If one integration is unavailable, record that explicitly in `state/CURRENT_STATE.md`. Do not claim the integration is present because the other agent has it.

## 4. Initial commit

After `scripts/bootstrap_swarm.py` has been run and the owner has reviewed the basic values:

```bash
git add .
git commit -m "Configure Swarm OS bootstrap"
git push
```

The commissioning interview may still change role files and config. Those changes receive a second commit after owner approval.

## 5. Start ChatGPT Orchestrator

Open a new ChatGPT conversation with repository access if available. Paste:

`generated/chatgpt-bootstrap-prompt.md`

Do not simultaneously ask it to start the project. Commission first.

## 6. Start Worker only after role design is approved

Open Claude Code (or the selected Worker environment) in the repository root. Paste:

`generated/worker-bootstrap-prompt.md`

The Worker should return a BOOTLOAD before modifying project files.

## 7. Commissioning commit

After the Owner approves the commissioning package and both agents pass the smoke tests:

```bash
git add swarm-config.json AGENTS.md CLAUDE.md roles playbooks state research generated
# Include other commissioning files actually changed.
git commit -m "Commission swarm roles, protocol, and operating state"
git push
```

Set `state/CURRENT_STATE.md` to `COMMISSIONED` only when both agents agree on the state and QA tests have passed.
