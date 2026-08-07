#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required_core = [
    "README.md", "AGENTS.md", "CLAUDE.md", "swarm-config.json",
    "scripts/bootstrap_swarm.py", "scripts/validate_swarm.py",
    "playbooks/SWARM_PROTOCOL.md", "playbooks/SECURITY_AND_AUTHORITY.md",
    "state/CURRENT_STATE.md", "state/DECISION_REGISTER.md",
    "state/OPEN_QUESTIONS.md", "state/WORK_QUEUE.md",
]
errors=[]
for rel in required_core:
    if not (ROOT / "core" / rel).exists():
        errors.append(f"missing core/{rel}")
profiles=[]
for d in sorted((ROOT / "swarm-types").iterdir()):
    if not d.is_dir():
        continue
    p=d / "profile.json"
    if not p.exists():
        errors.append(f"missing {d.relative_to(ROOT)}/profile.json")
        continue
    try:
        data=json.loads(p.read_text())
        if data.get("name") != d.name:
            errors.append(f"profile name mismatch: {d.name}")
        profiles.append(d.name)
    except Exception as exc:
        errors.append(f"invalid {p.relative_to(ROOT)}: {exc}")
if not profiles:
    errors.append("no swarm type profiles found")
if errors:
    print("swarmAgents validation FAILED")
    for e in errors:
        print(f"- {e}")
    raise SystemExit(1)
print("swarmAgents validation PASSED")
print("Profiles: " + ", ".join(profiles))
