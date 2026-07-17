#!/usr/bin/env python3
"""
Design-Seeker MVP — Minimal Viable Design Seeker

Scanne un dépôt pour détecter les gaps de design (workflows non documentés,
concepts non ancrés, écarts entre code et spécifications).

Usage:
    python scripts/design_seeker_mvp.py --repo <path> --output <file.json>
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def scan_repo(repo_path: str) -> dict[str, Any]:
    """Scanne un dépôt pour détecter les gaps de design."""
    gaps = []
    
    repo_path = Path(repo_path)
    
    # Scan des fichiers Python pour détecter les workflows non documentés
    for py_file in repo_path.rglob("*.py"):
        if "def " in py_file.read_text(encoding="utf-8", errors="ignore"):
            # Vérifier s'il y a un README ou docstring correspondant
            readme = py_file.parent / "README.md"
            if not readme.exists():
                gaps.append({
                    "type": "undocumented_workflow",
                    "path": str(py_file.relative_to(repo_path)),
                    "description": f"Fonction(s) Python sans documentation associée",
                    "severity": "medium",
                    "suggested_action": "Créer README.md ou documenter dans ONTOLOGY"
                })
    
    # Scan des fichiers YAML pour détecter les schémas non validés
    for yaml_file in repo_path.rglob("*.yaml"):
        if yaml_file.name not in ["README.md", "config.yaml"]:
            # Vérifier s'il y a un fichier d'ancre ONTOLOGY
            ontology = repo_path / "ONTOLOGY" / "schema" / f"{yaml_file.stem}.yaml"
            if not ontology.exists():
                gaps.append({
                    "type": "schema_not_ontology_anchored",
                    "path": str(yaml_file.relative_to(repo_path)),
                    "description": f"Schéma YAML non ancré dans ONTOLOGY",
                    "severity": "high",
                    "suggested_action": "Définir concept dans ONTOLOGY/concepts/core/"
                })
    
    # Scan des conventions SOTA
    conventions_dir = repo_path / "conventions"
    if conventions_dir.exists():
        for conv_file in conventions_dir.rglob("*.md"):
            # Vérifier la présence d'intent_hash
            content = conv_file.read_text(encoding="utf-8", errors="ignore")
            if "intent_hash:" not in content:
                gaps.append({
                    "type": "missing_intent_hash",
                    "path": str(conv_file.relative_to(repo_path)),
                    "description": "Convention sans intent_hash",
                    "severity": "low",
                    "suggested_action": "Ajouter intent_hash dans le frontmatter"
                })
    
    return gaps


def main():
    parser = argparse.ArgumentParser(description="Design-Seeker MVP")
    parser.add_argument("--repo", required=True, help="Chemin vers le dépôt à scanner")
    parser.add_argument("--output", default="design_gaps_report.json", help="Fichier de sortie")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.repo):
        print(f"Erreur: {args.repo} n'est pas un répertoire valide", file=sys.stderr)
        sys.exit(1)
    
    gaps = scan_repo(args.repo)
    
    report = {
        "seeker_version": "1.0.0",
        "repo": os.path.abspath(args.repo),
        "scan_timestamp": datetime.utcnow().isoformat() + "Z",
        "gaps": gaps,
        "summary": {
            "total_gaps": len(gaps),
            "critical": sum(1 for g in gaps if g["severity"] == "critical"),
            "high": sum(1 for g in gaps if g["severity"] == "high"),
            "medium": sum(1 for g in gaps if g["severity"] == "medium"),
            "low": sum(1 for g in gaps if g["severity"] == "low")
        }
    }
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    
    print(f"Scan terminé: {len(gaps)} gaps détectés")
    print(f"Rapport sauvegardé dans: {args.output}")
    
    # Retourner le nombre de gaps pour les tests
    return len(gaps)


if __name__ == "__main__":
    sys.exit(main())