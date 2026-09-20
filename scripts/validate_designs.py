#!/usr/bin/env python3
"""validate_designs.py — Validation MDU pour unified-design."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml


DESIGNS_ROOT = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs")
REQUIRED_FIELDS = {"name", "version", "status", "layer", "description"}


def validate_design(path: Path) -> tuple[bool, str]:
    try:
        text = path.read_text(encoding="utf-8")
        # Extraire uniquement le frontmatter YAML pour les fichiers Markdown
        # avec délimiteur ---, ou charger le YAML pur directement
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3 and parts[1].strip():
                yaml_text = parts[1]
            else:
                # Pas de frontmatter fermé, traiter comme YAML pur
                yaml_text = text
        else:
            yaml_text = text
        data = yaml.safe_load(yaml_text)
    except Exception as exc:
        return False, f"YAML error: {exc}"

    if not isinstance(data, dict):
        return False, "Root is not a mapping"

    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        return False, f"Missing fields: {sorted(missing)}"

    return True, "OK"


def find_design_files(paths: list[Path] | None = None) -> list[Path]:
    if paths:
        return sorted(p for p in paths if p.exists())
    # Support both designs/<name>/design.yaml and designs/<name>.yaml
    return sorted(
        set(DESIGNS_ROOT.glob("*/design.yaml")) |
        set(DESIGNS_ROOT.glob("*.yaml"))
    )


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Validate MDU designs.")
    parser.add_argument("paths", nargs="*", help="Specific design paths to validate")
    parser.add_argument("--strict", action="store_true", help="Fail if any design is invalid")
    args = parser.parse_args()

    if not DESIGNS_ROOT.exists():
        print(f"[FAIL] Designs root missing: {DESIGNS_ROOT}")
        return 1

    design_files = find_design_files([Path(p) for p in args.paths] if args.paths else None)
    if not design_files:
        print("[FAIL] No design.yaml files found")
        return 1

    failures = 0
    for path in design_files:
        ok, msg = validate_design(path)
        status = "OK" if ok else "FAIL"
        if not ok:
            failures += 1
        print(f"[{status}] {path}: {msg}")

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
