# Worker Bootstrap Prompt — Template

Use the generated version in `generated/worker-bootstrap-prompt.md` after running `scripts/bootstrap_swarm.py`.

The generated prompt instructs the Worker to:

- read `CLAUDE.md` and shared Swarm OS instructions;
- return a BOOTLOAD;
- reconcile repository and channels;
- respect direct-owner security gates;
- avoid real work until commissioning is complete;
- post concise notices.
