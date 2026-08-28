#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compliance_scanner — MDU Compliance Scanner for ARGUS (O2/O4).

Invocable par ARGUS via `argus scan --check compliance --repo <REPO>`
Produit un rapport JSON avec checks: design_registered, atom_registered,
citizen_registered, adr_indexed, mdu_checkpoint.
"""

from __future__ import annotations

import argparse
import json
import sys
import yaml
from pathlib import Path
from typing import Literal

# --- Configuration paths ---
UNIFIED_DESIGN_ROOT = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design")
DESIGNS_DIR = UNIFIED_DESIGN_ROOT / "designs"
ATOMS_DIR = UNIFIED_DESIGN_ROOT / "atoms"
CITIZENS_YAML = UNIFIED_DESIGN_ROOT / "citizens.yaml"
CATALOG_DESIGNS_INDEX = UNIFIED_DESIGN_ROOT / "catalog" / "designs.index.yaml"
CATALOG_ADRS_INDEX = UNIFIED_DESIGN_ROOT / "catalog" / "adrs.index.yaml"
CHECKPOINT_JSON = UNIFIED_DESIGN_ROOT / ".mdu" / "checkpoint.json"


def load_citizens() -> list[dict]:
    """Charge la liste des citoyens depuis citizens.yaml."""
    if not CITIZENS_YAML.exists():
        return []
    with CITIZENS_YAML.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("concepts", [])


def load_catalog_designs() -> dict[str, dict]:
    """Charge l'index des designs depuis catalog/designs.index.yaml."""
    if not CATALOG_DESIGNS_INDEX.exists():
        return {}
    with CATALOG_DESIGNS_INDEX.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    entries = data.get("entries", [])
    catalog = {}
    for entry in entries:
        if entry.get("type") == "design":
            design_id = entry.get("id")
            if design_id:
                catalog[design_id] = entry
    return catalog


def load_catalog_adrs() -> dict[str, dict]:
    """Charge l'index des ADRs depuis catalog/adrs.index.yaml."""
    if not CATALOG_ADRS_INDEX.exists():
        return {}
    with CATALOG_ADRS_INDEX.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    entries = data.get("entries", [])
    catalog = {}
    for entry in entries:
        if entry.get("type") == "adr":
            adr_id = entry.get("id")
            if adr_id:
                catalog[adr_id] = entry
    return catalog


def load_checkpoint() -> dict | None:
    """Charge le checkpoint MDU."""
    if not CHECKPOINT_JSON.exists():
        return None
    with CHECKPOINT_JSON.open("r", encoding="utf-8") as f:
        return json.load(f)


def discover_designs(designs_dir: Path) -> list[str]:
    """Auto-découvre les designs (format .yaml racine + design.yaml sous-dossier)."""
    discovered = set()
    # Format 1: sous-dossiers avec design.yaml
    for design_yaml in designs_dir.rglob("design.yaml"):
        if any(part.startswith(".") or part.startswith("__") for part in design_yaml.relative_to(designs_dir).parts):
            continue
        discovered.add(design_yaml.parent.name)
    # Format 2: fichiers .yaml à la racine
    for yaml_file in designs_dir.glob("*.yaml"):
        if yaml_file.name == "design.yaml":
            continue
        if any(part.startswith(".") or part.startswith("__") for part in yaml_file.relative_to(designs_dir).parts):
            continue
        discovered.add(yaml_file.stem)
    return sorted(discovered)


def check_repo_compliance(repo_name: str) -> dict:
    """Vérifie la conformité MDU complète pour un repo donné."""
    
    # 1. Design registered (dans catalog ou discovery)
    catalog_designs = load_catalog_designs()
    discovered_designs = discover_designs(DESIGNS_DIR)
    has_design = repo_name in catalog_designs or repo_name in discovered_designs
    
    # 2. Atom registered
    atom_path = ATOMS_DIR / f"{repo_name}.yaml"
    has_atom = atom_path.exists()
    
    # 3. Citizen registered
    citizens = load_citizens()
    has_citizen = any(c.get("id") == repo_name for c in citizens)
    
    # 4. ADR indexed (cherche ADRs du repo dans catalog)
    catalog_adrs = load_catalog_adrs()
    repo_adrs = [adr for adr, entry in catalog_adrs.items() 
                 if entry.get("source_repo") == repo_name]
    has_adr_indexed = len(repo_adrs) > 0
    
    # 5. MDU checkpoint
    checkpoint = load_checkpoint()
    has_checkpoint = False
    if checkpoint:
        # Vérifier si le repo est dans le checkpoint
        checkpoint_repos = checkpoint.get("repo", "")
        has_checkpoint = repo_name in checkpoint_repos or checkpoint_repos == "gerivdb/" + repo_name
    
    checks = {
        "design_registered": has_design,
        "atom_registered": has_atom,
        "citizen_registered": has_citizen,
        "adr_indexed": has_adr_indexed,
        "mdu_checkpoint": has_checkpoint,
    }
    
    gaps = [k for k, v in checks.items() if not v]
    compliant = len(gaps) == 0
    
    return {
        "repo": repo_name,
        "compliant": compliant,
        "checks": checks,
        "gaps": gaps,
        "details": {
            "catalog_designs": list(catalog_designs.keys()),
            "discovered_designs": discovered_designs,
            "repo_adrs": repo_adrs,
            "checkpoint_repo": checkpoint.get("repo") if checkpoint else None,
        }
    }


def main():
    parser = argparse.ArgumentParser(description="MDU Compliance Scanner for ARGUS (O2/O4)")
    parser.add_argument("--repo", required=True, help="Repo to check (e.g., RADX)")
    parser.add_argument("--report-json", type=Path, help="Output JSON report path")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if not compliant")
    args = parser.parse_args()
    
    result = check_repo_compliance(args.repo)
    
    if args.report_json:
        args.report_json.parent.mkdir(parents=True, exist_ok=True)
        args.report_json.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"[INFO] Report written to {args.report_json}")
    
    # Output JSON for ARGUS consumption
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if args.strict and not result["compliant"]:
        return 1
    return 0 if result["compliant"] else 1


if __name__ == "__main__":
    sys.exit(main())