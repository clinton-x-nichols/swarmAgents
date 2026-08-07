#!/usr/bin/env python3
"""Validate a Swarm OS repository for commissioning readiness."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
required=[
    "README.md","BOOTSTRAP.md","AGENTS.md","CLAUDE.md","swarm-config.json",
    "playbooks/SWARM_PROTOCOL.md","playbooks/SECURITY_AND_AUTHORITY.md",
    "playbooks/MEMORY_AND_RECOVERY.md","comms/CHANNEL_PROTOCOL.md",
    "state/CURRENT_STATE.md","state/DECISION_REGISTER.md","state/OPEN_QUESTIONS.md",
    "state/WORK_QUEUE.md","roles/orchestrator.md","roles/worker.md",
]
errors=[]
for p in required:
    if not (ROOT/p).exists():
        errors.append(f"Missing required file: {p}")

try:
    cfg=json.loads((ROOT/"swarm-config.json").read_text())
except Exception as exc:
    errors.append(f"Cannot parse swarm-config.json: {exc}")
    cfg={}

if cfg:
    checks=[
        ("swarm.name", cfg.get("swarm",{}).get("name")),
        ("swarm.mission", cfg.get("swarm",{}).get("mission")),
        ("swarm.definition_of_done", cfg.get("swarm",{}).get("definition_of_done")),
        ("swarm.owner", cfg.get("swarm",{}).get("owner")),
        ("orchestrator.name", cfg.get("orchestrator",{}).get("name")),
        ("worker.name", cfg.get("worker",{}).get("name")),
        ("communications.substantive_channel", cfg.get("communications",{}).get("substantive_channel")),
        ("communications.notices_channel", cfg.get("communications",{}).get("notices_channel")),
    ]
    for label,value in checks:
        if not value or str(value).strip().upper() in {"TBD","UNCONFIGURED SWARM","UNCONFIGURED"}:
            errors.append(f"Unconfigured value: {label}")
    c=cfg.get("communications",{})
    if c.get("substantive_channel") == c.get("notices_channel") and c.get("substantive_channel") not in {None,"TBD"}:
        errors.append("Substantive and notices channels must be distinct")

for p in ["generated/chatgpt-bootstrap-prompt.md","generated/worker-bootstrap-prompt.md"]:
    if not (ROOT/p).exists():
        errors.append(f"Generate bootstrap artifact first: {p}")

if errors:
    print("Swarm OS validation FAILED:\n")
    for e in errors:
        print(f"- {e}")
    sys.exit(1)

print("Swarm OS structural validation PASSED.")
print("Commissioning smoke tests are still required; see bootstrap/COMMISSIONING_CHECKLIST.md")
