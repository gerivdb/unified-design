#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MDU Conditions — Évaluateur de conditions pour l'orchestration MDU.

Usage:
    python mdu_conditions.py --check has_simple_gaps --report-json /tmp/plan.json
    python mdu_conditions.py --check catalog_dirty
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Add project paths
UNIFIED_DESIGN_ROOT = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design")
ECOS_CLI_ROOT = Path(r"D:\DO\WEB\TOOLS\L1-INFRA\ECOS-CLI")
sys.path.insert(0, str(UNIFIED_DESIGN_ROOT / "scripts"))
sys.path.insert(0, str(ECOS_CLI_ROOT / "citizens" / "mdu-compliance-scanner"))

from compliance_scanner import check_repo_compliance  # type: ignore


class MDUConditions:
    """Évaluateur de conditions pour l'orchestration MDU."""
    
    def __init__(self):
        self.catalog_designs_path = UNIFIED_DESIGN_ROOT / "catalog" / "designs.index.yaml"
        self.catalog_adrs_path = UNIFIED_DESIGN_ROOT / "catalog" / "adrs.index.yaml"
        self.catalog_citizens_path = UNIFIED_DESIGN_ROOT / "catalog" / "citizens.index.yaml"
        self.citizens_yaml_path = UNIFIED_DESIGN_ROOT / "citizens.yaml"
        self.checkpoint_path = UNIFIED_DESIGN_ROOT / ".mdu" / "checkpoint.json"
    
    def has_simple_gaps(self, report_path: Path | None = None) -> dict[str, Any]:
        """Vérifie s'il y a des gaps simples auto-remédiables.
        
        Gaps simples = design_registered, atom_registered, citizen_registered, 
                       adr_indexed, mdu_checkpoint
        Gaps complexes = rss_compliant, argus_clean (nécessitent intervention manuelle)
        """
        if report_path and report_path.exists():
            with report_path.open("r", encoding="utf-8") as f:
                report = json.load(f)
        else:
            # Générer rapport à la volée
            from mdu_compliance_scanner import load_catalog_designs, discover_repos_from_catalog
            catalog_designs = load_catalog_designs(self.catalog_designs_path)
            repos = discover_repos_from_catalog(catalog_designs)
            report = {"results": {}}
            for repo in repos:
                report["results"][repo] = check_repo_compliance(repo)
        
        simple_gap_types = {
            "design_registered", "atom_registered", "citizen_registered",
            "adr_indexed", "mdu_checkpoint"
        }
        
        simple_gaps = []
        complex_gaps = []
        
        for repo, result in report.get("results", {}).items():
            for gap in result.get("gaps", []):
                if gap in simple_gap_types:
                    simple_gaps.append({"repo": repo, "gap": gap})
                else:
                    complex_gaps.append({"repo": repo, "gap": gap})
        
        return {
            "condition": "has_simple_gaps",
            "result": len(simple_gaps) > 0,
            "simple_gaps": simple_gaps,
            "complex_gaps": complex_gaps,
            "total_simple": len(simple_gaps),
            "total_complex": len(complex_gaps),
        }
    
    def catalog_dirty(self) -> dict[str, Any]:
        """Vérifie si les catalogues sont sales (designs/atoms/citizens modifiés sans sync)."""
        # Vérifier si des fichiers designs/, atoms/, citizens.yaml ont été modifiés
        # depuis le dernier commit sans que les catalogues n'aient été mis à jour
        
        import subprocess
        try:
            # Fichiers modifiés non committés dans zones MDU
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=UNIFIED_DESIGN_ROOT, capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                return {"condition": "catalog_dirty", "result": False, "error": "git status failed"}
            
            mdu_files = []
            for line in result.stdout.strip().split('\n'):
                if line and not line.startswith('?'):
                    filepath = line[3:].strip()
                    if filepath.startswith(("designs/", "atoms/", "citizens.yaml")):
                        mdu_files.append(filepath)
            
            # Vérifier si catalogues ont été modifiés après ces fichiers
            catalog_files = [
                "catalog/designs.index.yaml",
                "catalog/adrs.index.yaml", 
                "catalog/citizens.index.yaml"
            ]
            
            dirty = len(mdu_files) > 0
            catalog_modified = False
            
            for cf in catalog_files:
                cpath = UNIFIED_DESIGN_ROOT / cf
                if cpath.exists():
                    # Comparer timestamps
                    ctime = cpath.stat().st_mtime
                    for mf in mdu_files:
                        mpath = UNIFIED_DESIGN_ROOT / mf
                        if mpath.exists() and mpath.stat().st_mtime > ctime:
                            catalog_modified = True
                            break
            
            return {
                "condition": "catalog_dirty",
                "result": dirty and catalog_modified,
                "mdu_files_modified": mdu_files,
                "catalog_outdated": catalog_modified,
                "catalog_files": catalog_files,
            }
        except Exception as e:
            return {"condition": "catalog_dirty", "result": False, "error": str(e)}
    
    def all_repos_compliant(self) -> dict[str, Any]:
        """Vérifie si tous les repos sont conformes MDU."""
        from mdu_compliance_scanner import load_catalog_designs, discover_repos_from_catalog
        
        catalog_designs = load_catalog_designs(self.catalog_designs_path)
        repos = discover_repos_from_catalog(catalog_designs)
        
        non_compliant = []
        for repo in repos:
            result = check_repo_compliance(repo)
            if not result["compliant"]:
                non_compliant.append({"repo": repo, "gaps": result["gaps"]})
        
        return {
            "condition": "all_repos_compliant",
            "result": len(non_compliant) == 0,
            "non_compliant": non_compliant,
            "total_repos": len(repos),
            "compliant_repos": len(repos) - len(non_compliant),
        }
    
    def has_critical_gaps(self) -> dict[str, Any]:
        """Vérifie s'il y a des gaps critiques (design_registered, citizen_registered)."""
        from mdu_compliance_scanner import load_catalog_designs, discover_repos_from_catalog
        
        catalog_designs = load_catalog_designs(self.catalog_designs_path)
        repos = discover_repos_from_catalog(catalog_designs)
        
        critical_gap_types = {"design_registered", "citizen_registered"}
        critical_gaps = []
        
        for repo in repos:
            result = check_repo_compliance(repo)
            for gap in result.get("gaps", []):
                if gap in critical_gap_types:
                    critical_gaps.append({"repo": repo, "gap": gap})
        
        return {
            "condition": "has_critical_gaps",
            "result": len(critical_gaps) > 0,
            "critical_gaps": critical_gaps,
        }
    
    def check_condition(self, condition: str, **kwargs) -> dict[str, Any]:
        """Évalue une condition par nom."""
        conditions_map = {
            "has_simple_gaps": self.has_simple_gaps,
            "catalog_dirty": self.catalog_dirty,
            "all_repos_compliant": self.all_repos_compliant,
            "has_critical_gaps": self.has_critical_gaps,
        }
        
        if condition not in conditions_map:
            return {
                "condition": condition,
                "result": False,
                "error": f"Unknown condition: {condition}. Available: {list(conditions_map.keys())}"
            }
        
        return conditions_map[condition](**kwargs)


def main():
    parser = argparse.ArgumentParser(description="MDU Conditions Evaluator")
    parser.add_argument("--check", required=True, 
                        choices=["has_simple_gaps", "catalog_dirty", "all_repos_compliant", "has_critical_gaps"],
                        help="Condition to evaluate")
    parser.add_argument("--report-json", type=Path, help="Path to compliance report JSON")
    parser.add_argument("--output-json", type=Path, help="Output JSON result")
    args = parser.parse_args()
    
    conditions = MDUConditions()
    
    if args.check == "has_simple_gaps":
        result = conditions.has_simple_gaps(args.report_json)
    elif args.check == "catalog_dirty":
        result = conditions.catalog_dirty()
    elif args.check == "all_repos_compliant":
        result = conditions.all_repos_compliant()
    elif args.check == "has_critical_gaps":
        result = conditions.has_critical_gaps()
    else:
        print(f"Unknown condition: {args.check}")
        return 1
    
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Exit code: 0 if condition is true, 1 if false, 2 if error
    if "error" in result:
        return 2
    return 0 if result.get("result", False) else 1


if __name__ == "__main__":
    sys.exit(main())