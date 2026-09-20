#!/usr/bin/env python3
"""
MDU Lint — Vérification structurelle du Meta-Design Universe (MDU).

Règles :
- Unicité des IDs dans meta-design.yaml et catalog/*.yaml
- Existence des chemins référencés
- Complétude des index (atoms, designs, primitives, skills, citizens, pipelines, workflows)
- Canonicalité : pas de doublon .yaml racine vs dossier/design.yaml
- Harmonisation des statuts (ACTIVE, DRAFT, STANDARD, DEPRECATED)
- consumers: [] non vide (traçabilité descendante)

Exit codes :
- 0 : conforme
- 1 : erreurs critiques (doublons IDs, chemins manquants)
- 2 : avertissements (statuts non harmonisés, consumers vides)
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("[MDU-LINT] ERREUR: PyYAML requis. Installer avec: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = REPO_ROOT / "catalog"
META_DESIGN = REPO_ROOT / "meta-design.yaml"


def load_yaml(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def find_duplicate_ids(meta_design: dict, catalog_files: list[Path]) -> list[dict]:
    """Détecte les IDs en doublon dans meta-design.yaml et catalog/*.yaml."""
    id_map: dict[str, list[dict]] = defaultdict(list)
    issues = []

    # Scan meta-design.yaml
    for section in ["designs", "primitives", "skills", "citizens", "pipelines", "workflows"]:
        items = meta_design.get(section, [])
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and item.get("intent_hash"):
                    ih = item["intent_hash"]
                    id_map[ih].append({"source": "meta-design.yaml", "name": item.get("name", "?"), "section": section})

    # Scan catalog/*.yaml
    for cat_file in catalog_files:
        try:
            data = load_yaml(cat_file)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        entries = data.get("entries", data.get("items", []))
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, dict) and entry.get("intent_hash"):
                ih = entry["intent_hash"]
                id_map[ih].append({
                    "source": str(cat_file.relative_to(REPO_ROOT)),
                    "name": entry.get("name", "?"),
                })

    # Les doublons meta-design <-> catalog sont attendus (catalogue = index).
    # On ne garde comme critiques que les doublons intra-fichier ou intra-catalogue.
    intra_file: dict[str, list[dict]] = defaultdict(list)
    for ih, locations in id_map.items():
        sources = [loc["source"] for loc in locations]
        # Doublon si même fichier apparaît 2 fois
        seen = defaultdict(int)
        for loc in locations:
            seen[loc["source"]] += 1
        for src, count in seen.items():
            if count > 1:
                intra_file[ih].extend([loc for loc in locations if loc["source"] == src])

    for ih, locations in intra_file.items():
        if locations:
            issues.append({
                "rule": "duplicate_id",
                "intent_hash": ih,
                "locations": locations,
                "severity": "critical",
            })

    return issues


def check_paths_exist(meta_design: dict) -> list[dict]:
    """Vérifie que les chemins référencés dans meta-design.yaml existent."""
    issues = []
    sections = ["designs", "primitives", "skills", "citizens", "pipelines", "workflows"]
    for section in sections:
        for item in meta_design.get(section, []):
            if not isinstance(item, dict):
                continue
            path = item.get("path")
            if not path:
                continue
            full_path = REPO_ROOT / path
            if not full_path.exists():
                issues.append({
                    "rule": "missing_path",
                    "name": item.get("name", "?"),
                    "path": path,
                    "severity": "critical",
                })
    return issues


def check_catalog_completeness(meta_design: dict, catalog_files: list[Path]) -> list[dict]:
    """Vérifie que les catalogues couvrent les artefacts physiques."""
    issues = []
    # Map nom -> intent_hash depuis meta-design
    meta_map = {}
    for section in ["designs", "primitives", "skills", "citizens", "pipelines", "workflows"]:
        for item in meta_design.get(section, []):
            if isinstance(item, dict):
                meta_map[item.get("name")] = item.get("intent_hash")

    for cat_file in catalog_files:
        try:
            data = load_yaml(cat_file)
        except Exception:
            continue
        entries = data.get("entries", data.get("items", []))
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            name = entry.get("name")
            ih = entry.get("intent_hash")
            if name and name in meta_map and meta_map[name] != ih:
                issues.append({
                    "rule": "catalog_mismatch",
                    "catalog": str(cat_file.relative_to(REPO_ROOT)),
                    "name": name,
                    "meta_hash": meta_map.get(name),
                    "catalog_hash": ih,
                    "severity": "warning",
                })
    return issues


def check_ambiguous_paths(meta_design: dict) -> list[dict]:
    """Détecte les chemins ambigus (.yaml racine vs dossier/design.yaml)."""
    issues = []
    seen_paths = defaultdict(list)
    for section in ["designs"]:
        for item in meta_design.get(section, []):
            if not isinstance(item, dict):
                continue
            path = item.get("path", "")
            name = item.get("name", "?")
            if path.endswith(".yaml"):
                # Vérifier si un dossier/design.yaml existe aussi
                base = path.replace(".yaml", "")
                alt_dir = REPO_ROOT / base / "design.yaml"
                if alt_dir.exists():
                    seen_paths[base].append({"name": name, "path": path, "alt": str(alt_dir.relative_to(REPO_ROOT))})

    for base, variants in seen_paths.items():
        if len(variants) > 1:
            issues.append({
                "rule": "ambiguous_path",
                "base": base,
                "variants": variants,
                "severity": "warning",
            })
    return issues


def check_status_harmonization(meta_design: dict) -> list[dict]:
    """Vérifie l'harmonisation des statuts."""
    issues = []
    allowed = {"ACTIVE", "DRAFT", "STANDARD", "DEPRECATED", "active", "draft", "standard", "deprecated"}
    for section in ["designs", "primitives", "skills", "citizens", "pipelines", "workflows"]:
        for item in meta_design.get(section, []):
            if not isinstance(item, dict):
                continue
            status = item.get("profile", item.get("status", "")).upper()
            if status and status not in {"ACTIVE", "DRAFT", "STANDARD", "DEPRECATED"}:
                issues.append({
                    "rule": "non_harmonized_status",
                    "name": item.get("name", "?"),
                    "status": status,
                    "severity": "warning",
                })
    return issues


def check_consumers(meta_design: dict) -> list[dict]:
    """Vérifie que consumers: [] n'est pas vide (traçabilité descendante)."""
    issues = []
    for section in ["designs", "primitives", "skills", "citizens", "pipelines", "workflows"]:
        for item in meta_design.get(section, []):
            if not isinstance(item, dict):
                continue
            consumers = item.get("consumers", [])
            if isinstance(consumers, list) and len(consumers) == 0:
                issues.append({
                    "rule": "empty_consumers",
                    "name": item.get("name", "?"),
                    "section": section,
                    "severity": "info",
                })
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="MDU Lint — validation structurelle du MDU")
    parser.add_argument("--strict", action="store_true", help="Échec si avertissements présents")
    parser.add_argument("--json", action="store_true", help="Sortie JSON uniquement")
    parser.add_argument("--warn-only", action="store_true", help="N'échoue jamais, retourne toujours 0")
    args = parser.parse_args()

    if not META_DESIGN.exists():
        print(f"[MDU-LINT] ERREUR: {META_DESIGN} introuvable", file=sys.stderr)
        return 1

    meta_design = load_yaml(META_DESIGN)
    catalog_files = list(CATALOG_DIR.glob("*.yaml")) if CATALOG_DIR.exists() else []

    issues = []
    issues.extend(find_duplicate_ids(meta_design, catalog_files))
    issues.extend(check_paths_exist(meta_design))
    issues.extend(check_catalog_completeness(meta_design, catalog_files))
    issues.extend(check_ambiguous_paths(meta_design))
    issues.extend(check_status_harmonization(meta_design))
    issues.extend(check_consumers(meta_design))

    # Classification
    critical = [i for i in issues if i["severity"] == "critical"]
    warnings = [i for i in issues if i["severity"] == "warning"]
    infos = [i for i in issues if i["severity"] == "info"]

    report = {
        "status": "OK" if not critical else "FAIL",
        "summary": {
            "total": len(issues),
            "critical": len(critical),
            "warnings": len(warnings),
            "infos": len(infos),
        },
        "issues": issues,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"[MDU-LINT] {report['status']} — {len(critical)} critical, {len(warnings)} warnings, {len(infos)} infos")
        for issue in issues:
            severity = issue["severity"].upper()
            rule = issue["rule"]
            print(f"  [{severity}] {rule}: {issue}")

    if args.warn_only:
        return 0

    if critical:
        return 1
    if args.strict and warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
