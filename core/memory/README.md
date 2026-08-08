# Agent Memory

This directory is the durable continuity layer for agent identity, behavioral rules, collaboration conventions, and reusable lessons.

It is deliberately separate from project design/work state.

## What belongs here

- agent identity/persona;
- role and authority boundaries that should survive session loss;
- communication rituals/conventions;
- standing behavioral rules;
- collaboration-model guidance;
- verified reusable lessons;
- bootstrap/recovery pointers.

## What does not belong here

- current work-order status;
- active blockers;
- current document versions;
- transient Slack state;
- project decisions already governed by the engineering notebook/registers;
- claims that an external system currently has a certain state unless freshly verified.

## Governing principle

Memory is a continuity claim, not proof of current external state.

On restart, read memory to recover identity and operating habits, then verify current project state from GitHub, Slack, source systems, and the engineering notebook.

See `INDEX.md` for read order and `../playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md` for the complete model.
