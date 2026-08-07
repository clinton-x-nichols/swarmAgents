#!/usr/bin/env python3
"""Instantiate a live swarm repository from the swarmAgents library."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
TYPES = ROOT / "swarm-types"


def profiles() -> dict[str, Path]:
    out = {}
    if not TYPES.exists():
        return out
    for child in sorted(TYPES.iterdir()):
        if child.is_dir() and (child / "profile.json").exists():
            out[child.name] = child
    return out


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def deep_update(base: dict, overlay: dict) -> dict:
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            deep_update(base[key], value)
        else:
            base[key] = value
    return base


def copy_tree(src: Path, dst: Path) -> None:
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            copy_tree(item, target)
        else:
            shutil.copy2(item, target)


def target_is_safe(target: Path) -> bool:
    if not target.exists():
        return True
    permitted = {".git", ".gitignore"}
    names = {p.name for p in target.iterdir()}
    return names.issubset(permitted)


def instantiate(profile_name: str, target: Path, force: bool) -> None:
    available = profiles()
    if profile_name not in available:
        raise SystemExit(f"Unknown swarm type: {profile_name}. Use --list.")
    profile_dir = available[profile_name]
    profile = load_json(profile_dir / "profile.json")

    target = target.expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    if not force and not target_is_safe(target):
        raise SystemExit(
            f"Refusing to write into non-empty target {target}. "
            "Use an empty Git clone or pass --force after reviewing contents."
        )

    copy_tree(CORE, target)
    overlay_dir = profile_dir / "overlay"
    if overlay_dir.exists():
        copy_tree(overlay_dir, target)

    config_path = target / "swarm-config.json"
    config = load_json(config_path)
    defaults = profile.get("config_defaults", {})
    deep_update(config, defaults)
    config.setdefault("swarm", {})["type"] = profile_name
    config["swarm_type_profile"] = {
        "name": profile_name,
        "source": f"swarmAgents/swarm-types/{profile_name}",
        "profile_version": profile.get("profile_version", "1.0.0"),
    }
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    type_dir = target / "swarm-type"
    type_dir.mkdir(exist_ok=True)
    shutil.copy2(profile_dir / "profile.json", type_dir / "PROFILE.json")
    if (profile_dir / "README.md").exists():
        shutil.copy2(profile_dir / "README.md", type_dir / "README.md")
    if (profile_dir / "COMMISSIONING.md").exists():
        shutil.copy2(profile_dir / "COMMISSIONING.md", type_dir / "COMMISSIONING.md")

    print(f"Instantiated swarm type '{profile_name}' into {target}")
    print("Next:")
    print(f"  cd {target}")
    print("  python3 scripts/bootstrap_swarm.py")
    print("  python3 scripts/validate_swarm.py")


def main() -> None:
    parser = argparse.ArgumentParser(description="Instantiate a live swarm from swarmAgents")
    parser.add_argument("--type", dest="swarm_type", help="Swarm type profile")
    parser.add_argument("--target", type=Path, help="Target directory / live swarm Git clone")
    parser.add_argument("--list", action="store_true", help="List available swarm types")
    parser.add_argument("--force", action="store_true", help="Allow writing into a non-empty target")
    args = parser.parse_args()

    available = profiles()
    if args.list:
        for name, path in available.items():
            p = load_json(path / "profile.json")
            print(f"{name:22} {p.get('description', '')}")
        return
    if not args.swarm_type or not args.target:
        parser.error("--type and --target are required unless --list is used")
    instantiate(args.swarm_type, args.target, args.force)


if __name__ == "__main__":
    main()
