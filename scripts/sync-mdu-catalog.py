#!/usr/bin/env python3
"""
sync-mdu-catalog.py — Synchronisation atomique des catalogues MDU.

Modes:
  --designs   Synchronise catalog/designs.index.yaml
  --atoms     Synchronise catalog/atoms.index.yaml
  --all       Synchronise tous les catalogues
  --dry-run   Affiche les changements sans écrire

Atomicité : 1 catalogue modifié par exécution.
"""

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = REPO_ROOT / "catalog"
DESIGNS_DIR = REPO_ROOT / "designs"
ATOMS_DIR = REPO_ROOT / "atoms"
PIPELINES_DIR = REPO_ROOT / "pipelines"
WORKFLOWS_DIR = REPO_ROOT / "workflows"
PRIMITIVES_DIR = REPO_ROOT / "primitives"
SKILLS_DIR = REPO_ROOT / "skills"
CITIZENS_DIR = REPO_ROOT / "citizens"


def scan_designs() -> list[dict[str, Any]]:
    items = []
    for path in DESIGNS_DIR.glob("*/design.yaml"):
        rel = path.relative_to(REPO_ROOT)
        items.append({"name": path.parent.name, "path": str(rel), "status": "active"})
    return items


def scan_atoms() -> list[dict[str, Any]]:
    items = []
    for path in ATOMS_DIR.glob("*.md"):
        rel = path.relative_to(REPO_ROOT)
        items.append({"name": path.stem, "path": str(rel), "status": "active"})
    return items


def load_catalog(name: str) -> dict[str, Any]:
    path = CATALOG_DIR / f"{name}.yaml"
    if not path.exists():
        return {"items": []}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {"items": []}


def save_catalog(name: str, data: dict[str, Any], dry_run: bool) -> None:
    path = CATALOG_DIR / f"{name}.yaml"
    if dry_run:
        print(f"[dry-run] would write {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def sync_designs(dry_run: bool) -> None:
    current = {item["name"]: item for item in load_catalog("designs.index").get("items", [])}
    scanned = {item["name"]: item for item in scan_designs()}
    merged = list(scanned.values())
    for name, item in scanned.items():
        if name in current:
            item["status"] = current[name].get("status", item["status"])
    save_catalog("designs.index", {"items": merged}, dry_run)


def sync_atoms(dry_run: bool) -> None:
    current = {item["name"]: item for item in load_catalog("atoms.index").get("items", [])}
    scanned = {item["name"]: item for item in scan_atoms()}
    merged = list(scanned.values())
    for name, item in scanned.items():
        if name in current:
            item["status"] = current[name].get("status", item["status"])
    save_catalog("atoms.index", {"items": merged}, dry_run)


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync MDU catalogues")
    parser.add_argument("--designs", action="store_true")
    parser.add_argument("--atoms", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not any([args.designs, args.atoms, args.all]):
        parser.error("Choisir --designs, --atoms ou --all")

    if args.all or args.designs:
        sync_designs(args.dry_run)
    if args.all or args.atoms:
        sync_atoms(args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
