# Create a New Swarm from the ZIP — Complete Installation Runbook

This procedure starts with only three things:

1. the Swarm OS ZIP file on your workstation;
2. a GitHub account/repository you can access; and
3. a local or remote host where the Worker will run.

The ZIP is installation media. The cloned Git repository is the actual swarm workspace.

## 1. Create the GitHub repository

Create a new repository for the swarm, for example:

`my-research-swarm`

Recommended starting state:

- private unless the swarm is intentionally public;
- no generated application code yet;
- README/license are optional; an empty repository is simplest;
- give the human Owner and the Worker host the required repository access.

Copy both the SSH and HTTPS repository URLs. Prefer SSH on a persistent Worker host once SSH keys are configured.

Example:

```text
git@github.com:OWNER/my-research-swarm.git
```

## 2. Log into the host

For a remote Linux/macOS host:

```bash
ssh USER@HOSTNAME
```

For a local workstation, open Terminal, PowerShell, Windows Terminal, or the terminal in your IDE and continue there.

Choose a stable parent directory for swarm repositories:

```bash
mkdir -p ~/swarms
cd ~/swarms
```

## 3. Verify prerequisites

The bootstrap scripts use only the Python standard library, so no pip install is required.

Check:

```bash
git --version
python3 --version
unzip -v | head
```

Python 3.9+ is recommended.

Verify GitHub authentication if using SSH:

```bash
ssh -T git@github.com
```

A successful GitHub authentication message is sufficient; GitHub does not provide an interactive shell.

If Git authentication is not configured, configure an SSH key or use the HTTPS repository URL and your approved Git credential method before continuing.

## 4. Clone the new repository

From the parent directory:

```bash
git clone git@github.com:OWNER/my-research-swarm.git
cd my-research-swarm
```

Confirm the remote:

```bash
git remote -v
```

This directory is now the swarm repository root. All remaining commands in this runbook are run from here unless stated otherwise.

## 5. Put the Swarm OS ZIP on the host

If the ZIP is already on the host, note its path and continue.

If it is on your workstation and the Worker host is remote, from a workstation terminal run:

```bash
scp Swarm_Operating_System_Repo_Template.zip USER@HOSTNAME:~/
```

Then return to the SSH session.

Other acceptable transfer methods include SFTP, VS Code Remote upload, a secure file share, or another owner-approved method.

Do not commit the ZIP itself into the new swarm repository unless you intentionally want to retain the installation archive.

## 6. Extract the template outside the Git clone

From the swarm repository root:

```bash
rm -rf /tmp/swarm-os-template
mkdir -p /tmp/swarm-os-template
unzip -q ~/Swarm_Operating_System_Repo_Template.zip -d /tmp/swarm-os-template
```

If your ZIP is somewhere else, substitute its real path.

The archive contains a top-level directory named:

```text
swarm-operating-system-template/
```

## 7. Copy the template into the cloned repository

While still inside the cloned repository root, use one of these methods.

Preferred when `rsync` is installed:

```bash
rsync -av /tmp/swarm-os-template/swarm-operating-system-template/ ./
```

Portable fallback:

```bash
cp -a /tmp/swarm-os-template/swarm-operating-system-template/. ./
```

The trailing `/.` matters: it copies dotfiles such as `.gitignore` and `.github/` as well as ordinary files.

Do **not** replace or delete the clone's `.git/` directory.

## 8. Confirm the repository layout

Run:

```bash
pwd
ls -la
find scripts state playbooks roles bootstrap -maxdepth 2 -type f | sort
```

At minimum, the root should now contain:

```text
README.md
BOOTSTRAP.md
AGENTS.md
CLAUDE.md
swarm-config.json
scripts/
state/
playbooks/
roles/
bootstrap/
research/
comms/
generated/
```

Also confirm that Git still recognizes this as the cloned repository:

```bash
git status
```

## 9. Decide/create the two communication channels

Before running the interactive bootstrap, choose the channel names because the script asks for them.

Recommended pattern:

```text
<swarm-slug>
<swarm-slug>-notices
```

For example:

```text
research-swarm
research-swarm-notices
```

Create them in Slack or the communication system you intend to use, or at least reserve the exact names now.

The substantive channel is for work, design, questions, decisions, results, and evidence.

The notices channel is only for terse state markers such as `STARTED`, `STILL WORKING`, `BLOCKED`, `DONE`, and `IDLE`.

## 10. Run the interactive bootstrap

From the repository root:

```bash
python3 scripts/bootstrap_swarm.py
```

On systems where `python` already means Python 3, this is also valid:

```bash
python scripts/bootstrap_swarm.py
```

The script asks for:

- swarm name and slug;
- Owner name;
- mission / desired outcome;
- definition of done;
- Orchestrator name, platform, model/configuration, role, and personality;
- Worker name, platform, model/configuration, role, and personality;
- substantive channel name;
- notices channel name;
- whether threaded work is used;
- Git repository URL;
- evidence / QA standard; and
- whether current public role/prompt research is required during commissioning.

The script does not create the GitHub repository or Slack channels. It records and generates configuration for resources you created or named in the earlier steps.

It writes or regenerates:

```text
swarm-config.json
state/CURRENT_STATE.md
generated/chatgpt-bootstrap-prompt.md
generated/worker-bootstrap-prompt.md
```

## 11. Review the generated configuration

Inspect:

```bash
cat swarm-config.json
cat state/CURRENT_STATE.md
cat generated/chatgpt-bootstrap-prompt.md
cat generated/worker-bootstrap-prompt.md
```

Pay particular attention to:

- whether the mission describes an outcome rather than a task list;
- whether definition of done is objectively observable;
- whether Orchestrator and Worker roles are distinct;
- correct model/platform names;
- correct channel names;
- correct repository URL;
- security/approval assumptions; and
- evidence expectations.

Edit obvious typos now if necessary.

## 12. Run structural validation

From the repository root:

```bash
python3 scripts/validate_swarm.py
```

Expected result:

```text
Swarm OS structural validation PASSED.
Commissioning smoke tests are still required; see bootstrap/COMMISSIONING_CHECKLIST.md
```

A validation pass means the repository is structurally ready. It does not mean the swarm is commissioned.

## 13. Review the initial Git diff

Run:

```bash
git status
git diff -- . ':!generated/*'
git diff -- generated/
```

The exact output depends on whether the GitHub repo began empty or already contained files.

Do not commit secrets, tokens, credentials, private keys, or local environment files.

## 14. Commit and push the initialized Swarm OS

```bash
git add -A
git commit -m "Initialize Swarm OS"
git push -u origin HEAD
```

Then verify:

```bash
git status
git log -1 --oneline
```

The working tree should be clean.

## 15. Start the ChatGPT Orchestrator

Open a fresh ChatGPT conversation for this swarm.

Connect/enable GitHub and Slack access if your ChatGPT environment supports them and the swarm is intended to use them.

Paste the contents of:

```text
generated/chatgpt-bootstrap-prompt.md
```

Do not give the Orchestrator a giant finished project prompt instead. Its first task is commissioning.

The Orchestrator should:

1. fresh-read the repository;
2. interview the Owner one high-leverage question at a time;
3. clarify mission, definition of done, roles, personality, tools, systems of record, authority, security, QA/evidence, continuity, and communications;
4. perform the required current web/GitHub role-and-prompt research sidebar;
5. present Adopt / Adapt / Build options;
6. obtain Owner approval for genuine choices; and
7. reconcile the approved design into durable swarm state.

The target pre-Worker state is `READY_TO_COMMISSION`, not `COMMISSIONED`.

## 16. Synchronize the Worker host before starting Claude Code

Back on the Worker host:

```bash
cd ~/swarms/my-research-swarm
git pull --ff-only
```

Read the current status before launching the Worker:

```bash
cat state/CURRENT_STATE.md
```

## 17. Start the Worker in the repository root

For Claude Code, launch it from the repository root so `CLAUDE.md` is in scope.

For example:

```bash
cd ~/swarms/my-research-swarm
claude
```

Use the actual command for your installed Claude Code environment if it differs.

Paste the contents of:

```text
generated/worker-bootstrap-prompt.md
```

The Worker should fresh-read the required files and return a concise BOOTLOAD. It should not start substantive project execution yet.

## 18. Reconcile both agents

The Orchestrator and Worker must independently agree on:

- Owner identity;
- Orchestrator name and role;
- Worker name and role;
- Swarm Protocol version;
- mission;
- current state;
- work-queue head;
- open owner decisions;
- systems-of-record/source hierarchy;
- security and direct-owner approval gates;
- substantive and notices channel names; and
- latest relevant Git commit.

If they disagree, resolve the repository/state mismatch before proceeding.

Do not use Slack scrollback or either model's conversation memory as the deciding source when committed current state says otherwise.

## 19. Run the commissioning handshake and smoke tests

Follow:

```text
bootstrap/COMMISSIONING_CHECKLIST.md
```

At minimum test:

1. harmless read-only dispatch;
2. stale chat state versus correct committed state;
3. a direct-owner security boundary;
4. an intervening Git commit before a Worker write; and
5. restart/recovery from durable state.

Only after those tests pass should the repository record the swarm as `COMMISSIONED`.

## 20. Start the first real bounded work item

The Orchestrator should create or activate one bounded work item in `state/WORK_QUEUE.md` and dispatch it through the substantive channel/thread.

The Worker should:

1. fresh-read current state and the active thread;
2. post `STARTED` in notices;
3. execute only the bounded work;
4. preserve security and intervening-change controls;
5. return evidence/results in the substantive thread;
6. post `DONE` or a precise `BLOCKED` state in notices; and
7. update durable state as defined by the protocol.

## 21. Normal restart procedure

For every later Worker session:

```bash
cd ~/swarms/my-research-swarm
git pull --ff-only
```

Then fresh-read `state/CURRENT_STATE.md`, the protocol, decisions, open questions, work queue, notices, and the full active substantive thread before acting.

For every later Orchestrator session, likewise use committed state plus fresh channel/thread reads rather than reconstructing the project from old chat memory.

## One-line mental model

**The ZIP installs the operating system. The Git clone is the swarm. GitHub is durable memory. The substantive channel is coordination. Notices are state. The human Owner is final authority.**
