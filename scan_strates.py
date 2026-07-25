#!/usr/bin/env python3
"""
scan_strates.py — Scanner les strates pour identifier les dépôts candidats MDU.

Analyse les dépôts des strates L1-L5 pour identifier :
1. Les dépôts qui pourraient être des designs (design.yaml, parent explicite)
2. Les dépôts qui pourraient fournir des atomes (patterns de gouvernance)
3. Les dépôts avec des boucles potentielles
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


# Strates à scanner
STRATES = {
    "L1_CAUSALITY": "D:/DO/WEB/TOOLS/L1-INFRA",
    "L2_COMPOSITION": "D:/DO/WEB/TOOLS/L2-PLATFORM",
    "L3_EMERGENCE": "D:/DO/WEB/TOOLS/L3-CITIZENS",
    "L4_TOOLS": "D:/DO/WEB/TOOLS/L4-TOOLS",
    "L5_ARCHIVE": "D:/DO/WEB/TOOLS/L5-ARCHIVE",
}


def load_yaml_safe(path: Path) -> dict[str, Any] | None:
    """Charge un fichier YAML en sécurité."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None


def check_repo_is_design(repo_path: Path) -> dict[str, Any]:
    """Vérifie si un dépôt est un candidat design."""
    result = {
        "path": str(repo_path),
        "is_design_candidate": False,
        "has_design_yaml": False,
        "has_parent": False,
        "parent": None,
        "atomes_possibles": [],
        "issues": [],
    }
    
    # Vérifier design.yaml rapidement
    design_file = repo_path / "design.yaml"
    if design_file.exists():
        result["has_design_yaml"] = True
        try:
            with open(design_file, "r", encoding="utf-8") as f:
                content = f.read(5000)  # Lire max 5KB
                if "inherits:" in content or "parent:" in content:
                    result["has_parent"] = True
                    result["is_design_candidate"] = True
        except Exception as e:
            result["issues"].append(str(e))
    
    return result


def extract_potential_atomes(repo_path: Path) -> list[str]:
    """Extrait les patterns potentiels qui pourraient devenir des atomes."""
    atomes = []
    
    # Vérifier spécifiquement certains fichiers clés
    key_files = ["REPO.yaml", "design.yaml", "schema.yaml", "ONTOLOGY_DECLARATION.yaml"]
    
    for filename in key_files:
        f = repo_path / filename
        if f.exists():
            atomes.append(str(f.relative_to(repo_path)))
    
    return atomes


def scan_strate(strate_name: str, strate_path: Path) -> dict[str, Any]:
    """Scanne une strate entière."""
    result = {
        "strate": strate_name,
        "path": str(strate_path),
        "repos": [],
        "design_candidates": 0,
        "total_repos": 0,
    }
    
    if not strate_path.exists():
        result["issues"] = ["Path does not exist"]
        return result
    
    # Lister les dépôts (répertoires avec .git ou REPO.yaml)
    for item in strate_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            # Vérifier si c'est un dépôt
            is_repo = (item / ".git").exists() or (item / "REPO.yaml").exists()
            if is_repo:
                result["total_repos"] += 1
                repo_result = check_repo_is_design(item)
                
                # Extraire des atomes potentiels
                repo_result["atomes_possibles"] = extract_potential_atomes(item)
                
                result["repos"].append(repo_result)
                if repo_result["is_design_candidate"]:
                    result["design_candidates"] += 1
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Scanne les strates pour les candidats MDU")
    parser.add_argument("--output", type=Path, default=None, help="Fichier de sortie JSON")
    parser.add_argument("--strate", type=str, default=None, help="Strate à scanner (toutes si non spécifiée)")
    args = parser.parse_args()
    
    results = {
        "scan_date": __import__("datetime").datetime.now().isoformat(),
        "strates": [],
        "summary": {
            "total_repos": 0,
            "design_candidates": 0,
            "strates_scanned": 0,
        },
    }
    
    strates_to_scan = {k: v for k, v in STRATES.items() if args.strate is None or k == args.strate}
    
    for strate_name, strate_path in strates_to_scan.items():
        print(f"[SCAN] Scanning {strate_name} at {strate_path}")
        strate_result = scan_strate(strate_name, Path(strate_path))
        results["strates"].append(strate_result)
        results["summary"]["total_repos"] += strate_result["total_repos"]
        results["summary"]["design_candidates"] += strate_result["design_candidates"]
        results["summary"]["strates_scanned"] += 1
    
    # Afficher le résumé
    print("\n" + "=" * 60)
    print("MDU MULTI-STRATE SCAN REPORT")
    print("=" * 60)
    print(f"Strates scanned: {results['summary']['strates_scanned']}")
    print(f"Total repos: {results['summary']['total_repos']}")
    print(f"Design candidates: {results['summary']['design_candidates']}")
    
    # Afficher les candidats design
    print("\n[DESIGN CANDIDATES]")
    for strate in results["strates"]:
        for repo in strate.get("repos", []):
            if repo.get("is_design_candidate"):
                print(f"  - {repo['path']}")
                if repo.get("parent"):
                    print(f"    Parent: {repo['parent']}")
    
    # Afficher les atomes potentiels
    print("\n[ATOMES POTENTIELS]")
    for strate in results["strates"]:
        for repo in strate.get("repos", []):
            if repo.get("atomes_possibles"):
                print(f"  {repo['path']}:")
                for atom in repo["atomes_possibles"][:3]:
                    print(f"    - {atom}")
    
    # Sauvegarder le rapport
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n[REPORT] Saved to: {args.output}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())