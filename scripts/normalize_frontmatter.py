#!/usr/bin/env python3
"""
normalize_frontmatter.py — Audit et normalisation des frontmatters designs YAML.

Vérifie la présence des champs obligatoires :
  - name
  - version
  - status
  - layer (optionnel mais recommandé)
  - description

Signale les designs non conformes sans les modifier (mode read-only).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DESIGNS_DIR = REPO_ROOT / "designs"
REQUIRED_FIELDS = {"name", "version", "status"}
RECOMMENDED_FIELDS = {"layer", "description", "intent_hash"}


def find_design_files() -> list[Path]:
    """Trouve tous les fichiers design.yaml (sous-dossiers + racine)."""
    files = set(DESIGNS_DIR.glob("*/design.yaml")) | set(DESIGNS_DIR.glob("*.yaml"))
    return sorted(files)


def validate_frontmatter(path: Path) -> tuple[bool, list[str]]:
    """Valide le frontmatter d'un design. Retourne (ok, erreurs)."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        return False, [f"Read error: {exc}"]

    # Extraire le YAML frontmatter si c'est un fichier Markdown
    if path.suffix == ".md":
        parts = text.split("---", 2)
        if len(parts) < 3:
            return False, ["Missing YAML frontmatter delimiter ---"]
        yaml_text = parts[1]
    else:
        yaml_text = text

    try:
        data = yaml.safe_load(yaml_text)
    except Exception as exc:
        return False, [f"YAML parse error: {exc}"]

    if not isinstance(data, dict):
        return False, ["Root is not a mapping"]

    errors = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    for field in RECOMMENDED_FIELDS:
        if field not in data:
            errors.append(f"Missing recommended field: {field}")

    return len(errors) == 0, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize design frontmatters")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any design is invalid")
    args = parser.parse_args()

    design_files = find_design_files()
    if not design_files:
        print("[FAIL] No design files found")
        return 1

    failures = 0
    for path in design_files:
        ok, errors = validate_frontmatter(path)
        status = "OK" if ok else "FAIL"
        if not ok:
            failures += 1
        print(f"[{status}] {path.relative_to(REPO_ROOT)}")
        for err in errors:
            print(f"       {err}")

    total = len(design_files)
    valid = total - failures
    print(f"\n{valid}/{total} designs valid")

    if failures:
        msg = f"[FAIL] {failures} invalid design(s) detected"
        if args.strict:
            print(msg)
            return 1
        print(msg)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
