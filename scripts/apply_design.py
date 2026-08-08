#!/usr/bin/env python3
"""Apply a unified-design to target repos via bridge contracts.

Usage:
    python apply_design.py <design_name> [--dry-run] [--target <repo>]

Reads a design from unified-design/designs/<design_name>.yaml,
validates it, and generates contract artifacts in target repos
based on the declared bridges.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
DESIGNS_DIR = REPO_ROOT / "designs"
SCHEMA_PATH = REPO_ROOT / "schemas" / "design.schema.json"
INTEGRATION_DIR = REPO_ROOT / "integration"
KNOWN_REPOS_PATH = REPO_ROOT.parent.parent / "GOVERNANCE-HUB" / "known_repositories.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_known_repos() -> dict[str, Any]:
    if not KNOWN_REPOS_PATH.exists():
        return {}
    data = load_yaml(KNOWN_REPOS_PATH)
    repos = {}
    for repo in data.get("repositories", []):
        full_name = repo.get("full_name", "")
        if full_name:
            repos[full_name] = repo
    return repos


def validate_design(design: dict[str, Any]) -> list[str]:
    """Minimal validation matching engine/validator.py."""
    errors: list[str] = []
    import re

    if "name" not in design:
        errors.append("missing name")
    if "version" not in design:
        errors.append("missing version")
    if "status" not in design:
        errors.append("missing status")
    if "layer" not in design:
        errors.append("missing layer")
    if "intent_hash" not in design:
        errors.append("missing intent_hash")

    name = design.get("name", "")
    if name and not re.fullmatch(r"[a-z0-9-]+", name):
        errors.append(f"non-universal design name: '{name}'")

    depends_on = design.get("depends_on", [])
    if isinstance(depends_on, list):
        for dep in depends_on:
            if not re.fullmatch(r"ATOM-[0-9]+-[a-z0-9-]+", dep):
                errors.append(f"invalid depends_on id: '{dep}'")

    bridges = design.get("bridges", [])
    if isinstance(bridges, list):
        for bridge in bridges:
            if not isinstance(bridge, dict):
                errors.append(f"invalid bridge entry: {bridge}")
                continue
            role = bridge.get("role", "")
            if role and role not in ("consumer", "provider", "bidirectional"):
                errors.append(f"invalid bridge role: '{role}'")

    return errors


def generate_contract(design: dict[str, Any], bridge: dict[str, Any]) -> dict[str, Any]:
    """Generate a contract artifact for a single bridge target."""
    return {
        "design_name": design.get("name"),
        "design_version": design.get("version"),
        "design_intent_hash": design.get("intent_hash"),
        "target": bridge.get("target"),
        "role": bridge.get("role"),
        "protocol": bridge.get("protocol"),
        "contract_type": "design_declination",
        "generated_by": "apply_design.py",
    }


def apply_design(design_name: str, dry_run: bool = False, target: str | None = None) -> int:
    design_path = DESIGNS_DIR / f"{design_name}.yaml"
    if not design_path.exists():
        print(f"[ERROR] Design not found: {design_path}")
        return 1

    design = load_yaml(design_path)
    errors = validate_design(design)
    if errors:
        print(f"[ERROR] Design validation failed for {design_name}:")
        for err in errors:
            print(f"  - {err}")
        return 1

    bridges = design.get("bridges", [])
    if not bridges:
        print(f"[INFO] No bridges declared in design '{design_name}'. Nothing to apply.")
        return 0

    known_repos = load_known_repos()
    applied = []

    for bridge in bridges:
        bridge_target = bridge.get("target", "")
        if target and bridge_target != target:
            continue

        contract = generate_contract(design, bridge)
        contract_filename = f"contract-{design.get('name')}-{bridge_target}.yaml"
        contract_dir = INTEGRATION_DIR / "contracts"
        contract_dir.mkdir(exist_ok=True)
        contract_path = contract_dir / contract_filename

        if dry_run:
            print(f"[DRY-RUN] Would write contract: {contract_path}")
        else:
            with open(contract_path, "w", encoding="utf-8") as f:
                yaml.dump(contract, f, default_flow_style=False, sort_keys=False)
            print(f"[APPLY] Contract written: {contract_path}")

        applied.append(contract_filename)

    print(f"[OK] Applied design '{design_name}' to {len(applied)} target(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply unified-design to target repos")
    parser.add_argument("design_name", help="Name of the design (without .yaml)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--target", help="Limit to a specific bridge target")
    args = parser.parse_args()

    return apply_design(args.design_name, dry_run=args.dry_run, target=args.target)


if __name__ == "__main__":
    sys.exit(main())
