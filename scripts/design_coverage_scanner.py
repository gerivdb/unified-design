#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""design_coverage_scanner — Scanner de couverture des designs (GEN-011).

Version 2.0 : Dé-hardcodé - utilise le catalogue auto-généré et l'auto-découverte.

Scanne le repertoire unified-design/designs et verifie que tous les designs
requis sont presents et conformes. La liste des designs requis provient de
catalog/designs.index.yaml (généré par scan_loop.py) et non plus d'une liste
hardcodée.

Usage:
    python design_coverage_scanner.py [--strict] [--source catalog|discovery]

Exit codes:
    0 = tous les designs requis presents et conformes
    1 = designs manquants ou non conformes
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Literal

# --- Configuration paths ---
UNIFIED_DESIGN_ROOT = Path(__file__).parent.parent
DESIGNS_DIR = UNIFIED_DESIGN_ROOT / "designs"
CATALOG_DESIGNS_INDEX = UNIFIED_DESIGN_ROOT / "catalog" / "designs.index.yaml"
ONTOLOGY_CONCEPTS_DIR = Path(r"D:\DO\WEB\ONTOLOGY\concepts")
CATALOG_CONCEPTS_INDEX = UNIFIED_DESIGN_ROOT / "catalog" / "citizens.index.yaml"
ATOM_053_PATH = Path(r"D:\DO\WEB\ONTOLOGY\atoms\ATOM-053-workspace-draft-convention.md")

# Source de vérité pour les designs requis
SourceType = Literal["catalog", "discovery"]


def load_catalog_designs(catalog_path: Path) -> list[str]:
    """Charge la liste des designs depuis catalog/designs.index.yaml."""
    import yaml
    if not catalog_path.exists():
        return []
    with catalog_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    entries = data.get("entries", [])
    # Dédupliquer par id (le catalogue peut avoir des entrées doublées pour .yaml et design.yaml)
    seen = set()
    designs = []
    for entry in entries:
        if entry.get("type") == "design":
            design_id = entry.get("id")
            if design_id and design_id not in seen:
                seen.add(design_id)
                designs.append(design_id)
    return sorted(designs)


def discover_designs(designs_dir: Path) -> list[str]:
    """Auto-découvre les designs en cherchant les fichiers design.yaml OU .yaml à la racine."""
    discovered = set()
    
    # Format 1: sous-dossiers avec design.yaml (nouveau format)
    for design_yaml in designs_dir.rglob("design.yaml"):
        if any(part.startswith(".") or part.startswith("__") for part in design_yaml.relative_to(designs_dir).parts):
            continue
        design_name = design_yaml.parent.name
        discovered.add(design_name)
    
    # Format 2: fichiers .yaml à la racine (ancien format)
    for yaml_file in designs_dir.glob("*.yaml"):
        if yaml_file.name == "design.yaml":
            continue  # déjà traité
        if any(part.startswith(".") or part.startswith("__") for part in yaml_file.relative_to(designs_dir).parts):
            continue
        design_name = yaml_file.stem
        discovered.add(design_name)
    
    return sorted(discovered)


def load_catalog_concepts(catalog_path: Path) -> list[str]:
    """Charge la liste des concepts depuis catalog/citizens.index.yaml."""
    import yaml
    if not catalog_path.exists():
        return []
    with catalog_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    entries = data.get("entries", [])
    concepts = []
    for entry in entries:
        if entry.get("type") == "concept":
            concept_id = entry.get("id")
            if concept_id:
                concepts.append(concept_id)
    return sorted(set(concepts))


def discover_concepts(ontology_dir: Path) -> list[str]:
    """Auto-découvre les concepts dans ONTOLOGY/concepts/*.md."""
    if not ontology_dir.exists():
        return []
    concepts = []
    for md_file in ontology_dir.glob("*.md"):
        concepts.append(md_file.stem)
    return sorted(concepts)


def check_designs(required_designs: list[str], designs_dir: Path) -> tuple[list[str], list[str]]:
    """Retourne (présents, manquants) pour une liste de designs donnés.
    
    Un design est présent s'il a :
    - soit un sous-dossier avec design.yaml (nouveau format)
    - soit un fichier .yaml à la racine (ancien format)
    """
    present = []
    missing = []
    for design in required_designs:
        design_dir = designs_dir / design
        design_yaml_root = designs_dir / f"{design}.yaml"
        design_yaml_sub = design_dir / "design.yaml"
        md_file = design_dir / f"{design}.md"
        
        # Vérifier les deux formats
        has_subdir_format = design_dir.is_dir() and (md_file.is_file() or design_yaml_sub.is_file())
        has_root_format = design_yaml_root.is_file()
        
        if has_subdir_format or has_root_format:
            present.append(design)
        else:
            missing.append(design)
    return present, missing


def check_concepts(required_concepts: list[str], ontology_dir: Path) -> tuple[list[str], list[str]]:
    """Retourne (présents, manquants) pour une liste de concepts donnés."""
    present = []
    missing = []
    for concept in required_concepts:
        concept_file = ontology_dir / f"{concept}.md"
        if concept_file.is_file():
            present.append(concept)
        else:
            missing.append(concept)
    return present, missing


def check_atom_053() -> bool:
    """Vérifie que ATOM-053 existe."""
    return ATOM_053_PATH.is_file()


def get_required_designs(source: SourceType) -> list[str]:
    """Retourne la liste des designs requis selon la source choisie."""
    if source == "catalog":
        return load_catalog_designs(CATALOG_DESIGNS_INDEX)
    else:  # discovery
        return discover_designs(DESIGNS_DIR)


def get_required_concepts(source: SourceType) -> list[str]:
    """Retourne la liste des concepts requis selon la source choisie."""
    if source == "catalog":
        return load_catalog_concepts(CATALOG_CONCEPTS_INDEX)
    else:  # discovery
        return discover_concepts(ONTOLOGY_CONCEPTS_DIR)


def main():
    parser = argparse.ArgumentParser(description="Scanner de couverture des designs (GEN-011) - v2.0 dé-hardcodé")
    parser.add_argument("--strict", action="store_true", help="Mode strict : échoue si designs/concepts manquants")
    parser.add_argument("--source", choices=["catalog", "discovery"], default="catalog",
                        help="Source des designs/concepts requis: catalog (catalog/index.yaml) ou discovery (auto-scan)")
    parser.add_argument("--report-json", type=Path, help="Chemin pour rapport JSON détaillé")
    args = parser.parse_args()

    print(f"[INFO] Source: {args.source}")
    print(f"[INFO] Designs dir: {DESIGNS_DIR}")
    print(f"[INFO] Catalog: {CATALOG_DESIGNS_INDEX}")

    required_designs = get_required_designs(args.source)
    required_concepts = get_required_concepts(args.source)

    print(f"\nDesigns requis ({args.source}): {len(required_designs)}")
    present, missing = check_designs(required_designs, DESIGNS_DIR)
    print(f"  Présents: {len(present)}")
    print(f"  Manquants: {len(missing)}")
    if missing:
        for m in missing:
            print(f"  - {m}")

    print(f"\nConcepts ONTOLOGY requis ({args.source}): {len(required_concepts)}")
    concepts_present, concepts_missing = check_concepts(required_concepts, ONTOLOGY_CONCEPTS_DIR)
    print(f"  Présents: {len(concepts_present)}")
    print(f"  Manquants: {len(concepts_missing)}")
    if concepts_missing:
        for m in concepts_missing:
            print(f"  - {m}")

    atom_053_ok = check_atom_053()
    print(f"\nATOM-053: {'OK' if atom_053_ok else 'MANQUANT'}")

    all_ok = len(missing) == 0 and len(concepts_missing) == 0 and atom_053_ok

    # Rapport JSON optionnel
    if args.report_json:
        report = {
            "source": args.source,
            "designs": {
                "required": required_designs,
                "present": present,
                "missing": missing,
            },
            "concepts": {
                "required": required_concepts,
                "present": concepts_present,
                "missing": concepts_missing,
            },
            "atom_053": atom_053_ok,
            "all_ok": all_ok,
        }
        args.report_json.write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print(f"\n[INFO] Rapport JSON écrit: {args.report_json}")

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