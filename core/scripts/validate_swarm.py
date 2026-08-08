#!/usr/bin/env python3
"""Validate a Swarm OS repository for commissioning readiness."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
SEMVER_RE = r"(\d+\.\d+\.\d+)"

required = [
    "README.md",
    "BOOTSTRAP.md",
    "AGENTS.md",
    "CLAUDE.md",
    "swarm-config.json",
    "playbooks/SWARM_PROTOCOL.md",
    "playbooks/SECURITY_AND_AUTHORITY.md",
    "playbooks/MEMORY_AND_RECOVERY.md",
    "playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md",
    "comms/CHANNEL_PROTOCOL.md",
    "memory/README.md",
    "memory/INDEX.md",
    "engineering-notebook/00_INDEX.md",
    "engineering-notebook/CONSTRUCTION_NOTES.md",
    "engineering-notebook/RECONCILIATION_LOG.md",
    "state/CURRENT_STATE.md",
    "state/DECISION_REGISTER.md",
    "state/OPEN_QUESTIONS.md",
    "state/WORK_QUEUE.md",
    "roles/orchestrator.md",
    "roles/worker.md",
]

errors: list[str] = []


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_version(path: Path, pattern: str, label: str) -> Optional[str]:
    match = re.search(pattern, read(path), flags=re.MULTILINE)
    if not match:
        errors.append(f"Cannot determine {label} version from {path.relative_to(ROOT)}")
        return None
    return match.group(1)


for p in required:
    if not (ROOT / p).exists():
        errors.append(f"Missing required file: {p}")

try:
    cfg = json.loads(read(ROOT / "swarm-config.json"))
except Exception as exc:
    errors.append(f"Cannot parse swarm-config.json: {exc}")
    cfg = {}

if cfg:
    checks = [
        ("swarm.name", cfg.get("swarm", {}).get("name")),
        ("swarm.mission", cfg.get("swarm", {}).get("mission")),
        ("swarm.definition_of_done", cfg.get("swarm", {}).get("definition_of_done")),
        ("swarm.owner", cfg.get("swarm", {}).get("owner")),
        ("orchestrator.name", cfg.get("orchestrator", {}).get("name")),
        ("worker.name", cfg.get("worker", {}).get("name")),
        ("communications.substantive_channel", cfg.get("communications", {}).get("substantive_channel")),
        ("communications.notices_channel", cfg.get("communications", {}).get("notices_channel")),
        ("repository.current_state_file", cfg.get("repository", {}).get("current_state_file")),
        ("repository.engineering_notebook_index", cfg.get("repository", {}).get("engineering_notebook_index")),
        ("repository.memory_index", cfg.get("repository", {}).get("memory_index")),
    ]
    for label, value in checks:
        if not value or str(value).strip().upper() in {"TBD", "UNCONFIGURED SWARM", "UNCONFIGURED"}:
            errors.append(f"Unconfigured value: {label}")

    communications = cfg.get("communications", {})
    if (
        communications.get("substantive_channel") == communications.get("notices_channel")
        and communications.get("substantive_channel") not in {None, "TBD"}
    ):
        errors.append("Substantive and notices channels must be distinct")

protocol_path = ROOT / "playbooks/SWARM_PROTOCOL.md"
if protocol_path.exists():
    protocol_version = extract_version(
        protocol_path,
        rf"\*\*Protocol version:\*\*\s*{SEMVER_RE}",
        "canonical Swarm Protocol",
    )
else:
    protocol_version = None

if protocol_version:
    version_checks = [
        (
            ROOT / "comms/CHANNEL_PROTOCOL.md",
            rf"\*\*Protocol version:\*\*\s*{SEMVER_RE}",
            "channel protocol",
        ),
        (
            ROOT / "state/CURRENT_STATE.md",
            rf"^- \*\*Protocol:\*\*\s*{SEMVER_RE}\s*$",
            "current-state protocol",
        ),
        (
            ROOT / "scripts/bootstrap_swarm.py",
            rf'^PROTOCOL_VERSION\s*=\s*"{SEMVER_RE}"\s*$',
            "bootstrap generator protocol",
        ),
    ]
    for path, pattern, label in version_checks:
        if not path.exists():
            continue
        found = extract_version(path, pattern, label)
        if found and found != protocol_version:
            errors.append(
                f"{path.relative_to(ROOT)} protocol version {found} "
                f"does not match canonical {protocol_version}"
            )

for p in ["generated/chatgpt-bootstrap-prompt.md", "generated/worker-bootstrap-prompt.md"]:
    if not (ROOT / p).exists():
        errors.append(f"Generate bootstrap artifact first: {p}")

if errors:
    print("Swarm OS validation FAILED:\n")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Swarm OS structural validation PASSED.")
if protocol_version:
    print(f"Protocol: {protocol_version}")
print("Commissioning smoke tests are still required; see bootstrap/COMMISSIONING_CHECKLIST.md")
