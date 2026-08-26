#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""design_coverage_scanner — Scanner de couverture des designs (GEN-011).

Scanne le repertoire unified-design/designs et verifie que tous les designs
requis par PRD-MOC-GEN-011 sont presents et conformes.

Usage:
    python design_coverage_scanner.py [--strict]

Exit codes:
    0 = tous les designs requis presents et conformes
    1 = designs manquants ou non conformes
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_DESIGNS = [
    "balise",
    "argus",
    "limbo",
    "recovery",
    "gguf",
    "kg35",
    "inter-repo-migration",
    "meta-coherence",
    "limbo-governance",
    "recovery-tooling-governance",
]

DESIGNS_DIR = Path(__file__).parent.parent / "designs"
ONTOLOGY_CONCEPTS_DIR = Path(r"D:\DO\WEB\ONTOLOGY\concepts")
REQUIRED_CONCEPTS = [
    "balise",
    "argus",
    "limbo",
    "recovery",
    "gguf",
    "kg35",
    "inter-repo-migration",
    "meta-coherence",
    "limbo-governance",
    "recovery-tooling-governance",
]

def check_designs(designs_dir: Path) -> tuple[list[str], list[str]]:
    """Retourne (presents, manquants)"""
    present = []
    missing = []
    for design in REQUIRED_DESIGNS:
        design_dir = designs_dir / design
        md_file = design_dir / f"{design}.md"
        if design_dir.is_dir() and md_file.is_file():
            present.append(design)
        else:
            missing.append(design)
    return present, missing

def check_concepts(ontology_dir: Path) -> tuple[list[str], list[str]]:
    """Verifie que les concepts requis existent dans ONTOLOGY/concepts"""
    present = []
    missing = []
    for concept in REQUIRED_CONCEPTS:
        concept_file = ontology_dir / f"{concept}.md"
        if concept_file.is_file():
            present.append(concept)
        else:
            missing.append(concept)
    return present, missing

def check_atom_053() -> bool:
    """Verifie que ATOM-053 existe"""
    atom_path = Path(r"D:\DO\WEB\ONTOLOGY\atoms\ATOM-053-workspace-draft-convention.md")
    return atom_path.is_file()

def main():
    parser = argparse.ArgumentParser(description="Scanner de couverture des designs (GEN-011)")
    parser.add_argument("--strict", action="store_true", help="Mode strict : echoue si designs manquants")
    args = parser.parse_args()

    designs_dir = Path(__file__).parent.parent / "designs"
    ontology_dir = Path(r"D:\DO\WEB\ONTOLOGY\concepts")

    present, missing = check_designs(designs_dir)
    concepts_present, concepts_missing = check_concepts(Path(r"D:\DO\WEB\ONTOLOGY\concepts"))
    atom_053_ok = check_atom_053()

    print(f"Designs requis: {len(REQUIRED_DESIGNS)}")
    print(f"  Présents: {len(present)}")
    print(f"  Manquants: {len(missing)}")
    if missing:
        for m in missing:
            print(f"  - {m}")

    print(f"\nConcepts ONTOLOGY requis: {len(REQUIRED_CONCEPTS)}")
    print(f"  Présents: {len(concepts_present)}")
    print(f"  Manquants: {len(concepts_missing)}")
    if concepts_missing:
        for m in concepts_missing:
            print(f"  - {m}")

    print(f"\nATOM-053: {'OK' if atom_053_ok else 'MANQUANT'}")

    all_ok = len(missing) == 0 and len(concepts_missing) == 0 and atom_053_ok

    if args.strict:
        if not all_ok:
            print("\n[FAIL] Mode strict: designs/concepts manquants")
            return 1
        print("\n[OK] Tous les designs et concepts requis sont présents")
        return 0
    else:
        if not all_ok:
            print("\n[WARN] Designs/concepts manquants (mode lenient)")
        else:
            print("\n[OK] Tous les designs et concepts requis sont présents")
        return 0


if __name__ == "__main__":
    sys.exit(main())
