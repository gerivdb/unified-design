#!/usr/bin/env python3
"""
mdu-lint.py — Linter MDU pour unified-design.

Vérifie la cohérence structurelle du MDU :
- Unicité des IDs dans meta-design.yaml et catalogues
- Canonicalité des chemins
- Harmonisation des statuts
- Complétude des cross-références

Exit codes:
  0 = conforme
  1 = erreurs critiques
  2 = avertissements seulement
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
META_DESIGN = REPO_ROOT / "meta-design.yaml"
CATALOG_DIR = REPO_ROOT / "catalog"
DESIGNS_DIR = REPO_ROOT / "designs"
ATOMS_DIR = REPO_ROOT / "atoms"
PIPELINES_DIR = REPO_ROOT / "pipelines"
WORKFLOWS_DIR = REPO_ROOT / "workflows"
PRIMITIVES_DIR = REPO_ROOT / "primitives"
SKILLS_DIR = REPO_ROOT / "skills"
CITIZENS_DIR = REPO_ROOT / "citizens"


def load_yaml(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_unique_ids(meta: dict, catalogs: dict) -> list[str]:
    ids: set[str] = set()
    duplicates: list[str] = []
    entries = []
    for section in ["designs", "primitives", "skills", "citizens", "pipelines", "workflows", "governance_atoms"]:
        entries.extend(meta.get(section, []))
    for entry in entries:
        id_ = entry.get("intent_hash") or entry.get("id")
        if not id_:
            continue
        if id_ in ids:
            duplicates.append(id_)
        ids.add(id_)
    for name, items in catalogs.items():
        for item in items:
            id_ = item.get("intent_hash") or item.get("id")
            if not id_:
                continue
            if id_ in ids:
                duplicates.append(id_)
            ids.add(id_)
    return duplicates


def check_path_existence(meta: dict) -> list[str]:
    missing: list[str] = []
    for section in ["designs", "primitives", "skills", "citizens", "pipelines", "workflows"]:
        for entry in meta.get(section, []):
            path = REPO_ROOT / entry.get("path", "")
            if not path.exists():
                missing.append(str(path))
    return missing


def check_status_harmonization(meta: dict) -> list[str]:
    valid_statuses = {"active", "draft", "deprecated", "archived", "approved", "in_review", "proposed"}
    anomalies: list[str] = []
    for section in ["designs", "primitives", "skills", "citizens", "pipelines", "workflows"]:
        for entry in meta.get(section, []):
            status = entry.get("status")
            if status and status not in valid_statuses:
                anomalies.append(f"{entry.get('name')}: status={status}")
    return anomalies


def check_consumers(meta: dict) -> list[str]:
    empty: list[str] = []
    for section in ["designs", "primitives"]:
        for entry in meta.get(section, []):
            if entry.get("consumers") == []:
                empty.append(entry.get("name"))
    return empty


def lint_strict() -> tuple[list[str], list[str]]:
    meta = load_yaml(META_DESIGN)
    catalogs = {}
    for cat in CATALOG_DIR.glob("*.yaml"):
        try:
            catalogs[cat.stem] = load_yaml(cat)
        except Exception:
            pass
    errors = []
    warnings = []
    dupes = check_unique_ids(meta, catalogs)
    if dupes:
        errors.append(f"Duplicate IDs: {dupes}")
    missing = check_path_existence(meta)
    if missing:
        errors.append(f"Missing paths: {missing}")
    status_anomalies = check_status_harmonization(meta)
    if status_anomalies:
        warnings.append(f"Status anomalies: {status_anomalies}")
    empty_consumers = check_consumers(meta)
    if empty_consumers:
        warnings.append(f"Empty consumers: {empty_consumers}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Linter MDU pour unified-design")
    parser.add_argument("--strict", action="store_true", help="Mode strict : les avertissements deviennent erreurs")
    parser.add_argument("--warn-only", action="store_true", help="Mode avertissement seulement")
    args = parser.parse_args()

    errors, warnings = lint_strict()
    if args.warn_only:
        errors = []

    if errors:
        print("ERRORS:")
        for err in errors:
            print(f"  - {err}")
    if warnings:
        print("WARNINGS:")
        for warn in warnings:
            print(f"  - {warn}")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    if warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
