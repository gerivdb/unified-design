#!/usr/bin/env python3
"""
fix_missing_intent_hash.py — Corriger les designs sans intent_hash.

Ajoute un intent_hash manquant basé sur le nom du design.
Format: 0xDESIGN_<NOM>_<YYYYMMDD>
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DESIGNS_DIR = REPO_ROOT / "designs"


def find_design_files() -> list[Path]:
    files = set(DESIGNS_DIR.glob("*/design.yaml")) | set(DESIGNS_DIR.glob("*.yaml"))
    return sorted(files)


def add_intent_hash(path: Path, dry_run: bool) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"[ERROR] Cannot read {path}: {exc}")
        return False

    try:
        data = yaml.safe_load(text)
    except Exception as exc:
        print(f"[ERROR] YAML parse error in {path}: {exc}")
        return False

    if not isinstance(data, dict):
        print(f"[ERROR] {path}: root is not a mapping")
        return False

    if data.get("intent_hash"):
        return False  # déjà présent

    # Générer un intent_hash à partir du nom
    name = data.get("name", path.stem)
    slug = name.upper().replace(" ", "_").replace("-", "_")
    date_str = datetime.now().strftime("%Y%m%d")
    intent_hash = f"0xDESIGN_{slug}_{date_str}"

    data["intent_hash"] = intent_hash

    if dry_run:
        print(f"[dry-run] Would add intent_hash to {path}: {intent_hash}")
        return True

    try:
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(f"[OK] Added intent_hash to {path}: {intent_hash}")
        return True
    except Exception as exc:
        print(f"[ERROR] Cannot write {path}: {exc}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Fix missing intent_hash in designs")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()

    design_files = find_design_files()
    if not design_files:
        print("[FAIL] No design files found")
        return 1

    fixed = 0
    for path in design_files:
        if add_intent_hash(path, args.dry_run):
            fixed += 1

    print(f"\n{fixed} design(s) processed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
