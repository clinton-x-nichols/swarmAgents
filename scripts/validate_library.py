#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"

required_core = [
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "swarm-config.json",
    "scripts/bootstrap_swarm.py",
    "scripts/validate_swarm.py",
    "playbooks/SWARM_PROTOCOL.md",
    "playbooks/SECURITY_AND_AUTHORITY.md",
    "playbooks/ENGINEERING_NOTEBOOK_AND_MEMORY.md",
    "playbooks/MEMORY_AND_RECOVERY.md",
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
    "generated/chatgpt-bootstrap-prompt.md",
    "generated/worker-bootstrap-prompt.md",
]

DERIVED_ARTIFACTS = [
    "state/CURRENT_STATE.md",
    "generated/chatgpt-bootstrap-prompt.md",
    "generated/worker-bootstrap-prompt.md",
]

SEMVER_RE = r"(\d+\.\d+\.\d+)"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_version(text: str, pattern: str, label: str, errors: list[str]) -> str | None:
    match = re.search(pattern, text, flags=re.MULTILINE)
    if not match:
        errors.append(f"cannot determine {label} version")
        return None
    return match.group(1)


errors: list[str] = []

for rel in required_core:
    if not (CORE / rel).exists():
        errors.append(f"missing core/{rel}")

config: dict = {}
config_path = CORE / "swarm-config.json"
if config_path.exists():
    try:
        config = json.loads(read(config_path))
    except Exception as exc:
        errors.append(f"invalid core/swarm-config.json: {exc}")
    else:
        if str(config.get("status", "")).strip().upper() != "UNCONFIGURED":
            errors.append("core/swarm-config.json must remain UNCONFIGURED in the parent library")

protocol_version = None
protocol_path = CORE / "playbooks/SWARM_PROTOCOL.md"
if protocol_path.exists():
    protocol_version = extract_version(
        read(protocol_path),
        rf"\*\*Protocol version:\*\*\s*{SEMVER_RE}",
        "canonical Swarm Protocol",
        errors,
    )

if protocol_version:
    version_checks = [
        (
            "core/comms/CHANNEL_PROTOCOL.md",
            rf"\*\*Protocol version:\*\*\s*{SEMVER_RE}",
            "channel protocol",
        ),
        (
            "core/state/CURRENT_STATE.md",
            rf"^- \*\*Protocol:\*\*\s*{SEMVER_RE}\s*$",
            "current-state protocol",
        ),
        (
            "core/scripts/bootstrap_swarm.py",
            rf'^PROTOCOL_VERSION\s*=\s*"{SEMVER_RE}"\s*$',
            "bootstrap generator protocol",
        ),
    ]
    for rel, pattern, label in version_checks:
        path = ROOT / rel
        if not path.exists():
            continue
        found = extract_version(read(path), pattern, label, errors)
        if found and found != protocol_version:
            errors.append(
                f"{rel} protocol version {found} does not match canonical {protocol_version}"
            )

if config and all((CORE / rel).exists() for rel in DERIVED_ARTIFACTS + ["scripts/bootstrap_swarm.py"]):
    with tempfile.TemporaryDirectory(prefix="swarmagents-validate-") as temp_dir:
        temp_core = Path(temp_dir) / "core"
        shutil.copytree(CORE, temp_core)
        proc = subprocess.run(
            [sys.executable, str(temp_core / "scripts/bootstrap_swarm.py"), "--regenerate"],
            cwd=temp_core,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            details = (proc.stderr or proc.stdout).strip()
            errors.append(f"bootstrap regeneration failed during validation: {details}")
        else:
            for rel in DERIVED_ARTIFACTS:
                checked_in = read(CORE / rel)
                regenerated = read(temp_core / rel)
                if checked_in != regenerated:
                    errors.append(
                        f"derived artifact drift: core/{rel} does not match "
                        "scripts/bootstrap_swarm.py --regenerate"
                    )

profiles: list[str] = []
types_dir = ROOT / "swarm-types"
if not types_dir.exists():
    errors.append("missing swarm-types directory")
else:
    for d in sorted(types_dir.iterdir()):
        if not d.is_dir():
            continue
        p = d / "profile.json"
        if not p.exists():
            errors.append(f"missing {d.relative_to(ROOT)}/profile.json")
            continue
        try:
            data = json.loads(read(p))
            if data.get("name") != d.name:
                errors.append(f"profile name mismatch: {d.name}")
            profiles.append(d.name)
        except Exception as exc:
            errors.append(f"invalid {p.relative_to(ROOT)}: {exc}")

if not profiles:
    errors.append("no swarm type profiles found")

if errors:
    print("swarmAgents validation FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("swarmAgents validation PASSED")
print(f"Protocol: {protocol_version}")
print("Profiles: " + ", ".join(profiles))
