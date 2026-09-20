#!/usr/bin/env python3
"""validate_designs.py — Validation MDU pour unified-design."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml


DESIGNS_ROOT = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design\designs")
REQUIRED_FIELDS = {"name", "version", "status", "layer", "description"}
MDU_ROOT = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design")


def _load_mdu_concepts() -> set[str]:
    """Charge les concepts MDU depuis META-DESIGN.md et meta-design.yaml."""
    concepts: set[str] = set()
    for rel in ["META-DESIGN.md", "meta-design.yaml"]:
        path = MDU_ROOT / rel
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
            if rel.endswith(".yaml"):
                data = yaml.safe_load(text)
                if isinstance(data, dict):
                    for section in ["designs", "primitives", "capabilities", "governance_atoms"]:
                        items = data.get(section, [])
                        if isinstance(items, list):
                            for item in items:
                                if isinstance(item, dict) and "name" in item:
                                    concepts.add(item["name"])
            else:
                # META-DESIGN.md : extraire les noms de designs/atomes du markdown
                for line in text.splitlines():
                    if line.strip().startswith("|"):
                        parts = [p.strip() for p in line.strip().strip("|").split("|")]
                        if parts and parts[0] and not parts[0].startswith("---"):
                            concepts.add(parts[0])
        except Exception:
            continue
    return concepts


MDU_CONCEPTS = _load_mdu_concepts()


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

    # Vérifier les références croisées contre le MDU
    unresolved = []
    for ref in data.get("depends_on", []) + data.get("inherits", []):
        if ref not in MDU_CONCEPTS:
            unresolved.append(ref)
    if unresolved:
        # Les refs non résolues sont un WARN, pas un FAIL
        # La résolution complète nécessite de charger META-DESIGN.md + meta-design.yaml + atoms_registry.yaml
        return True, f"OK (WARN: unresolved refs {sorted(unresolved)} — MDU concepts: {len(MDU_CONCEPTS)})"

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
