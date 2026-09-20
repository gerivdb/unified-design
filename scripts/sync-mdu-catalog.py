#!/usr/bin/env python3
"""
Sync MDU Catalog — Synchronisation atomique entre l'arborescence physique
et les catalogues du MDU.

Modes :
  --designs   Met a jour catalog/designs.index.yaml
  --atoms     Met a jour catalog/atoms.index.yaml
  --all       Met a jour tous les catalogues (1 fichier par execution)

Comportement :
  - Scan atomique par dossier (1 tour = 1 dossier)
  - Mode --dry-run : rapport uniquement, aucune ecriture
  - Preservation des metadonnees existantes (status, intent_hash, consumers)
  - Sortie : catalogue mis a jour + rapport JSON

Exit codes :
  0 : sync reussie ou nothing to do
  1 : erreur
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("[SYNC-MDU] ERREUR: PyYAML requis. Installer avec: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = REPO_ROOT / "catalog"
DESIGNS_DIR = REPO_ROOT / "designs"
ATOMS_DIR = REPO_ROOT / "atoms"
PIPELINES_DIR = REPO_ROOT / "pipelines"
WORKFLOWS_DIR = REPO_ROOT / "workflows"
PRIMITIVES_DIR = REPO_ROOT / "primitives"
SKILLS_DIR = REPO_ROOT / "skills"
CITIZENS_DIR = REPO_ROOT / "citizens"
REPORTS_DIR = REPO_ROOT / "reports"


def load_yaml(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    import yaml
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def scan_designs() -> list[dict]:
    entries = []
    if not DESIGNS_DIR.exists():
        return entries
    for yaml_file in sorted(DESIGNS_DIR.rglob("design.yaml")):
        rel = yaml_file.relative_to(REPO_ROOT)
        try:
            data = load_yaml(yaml_file)
        except Exception:
            continue
        name = data.get("name", yaml_file.parent.name)
        entries.append({
            "name": name,
            "path": str(rel),
            "version": data.get("version", "1.0.0"),
            "intent_hash": data.get("intent_hash", ""),
            "status": data.get("status", "ACTIVE"),
            "profile": data.get("profile", "STANDARD"),
            "consumers": data.get("consumers", []),
        })
    # Scan aussi les .yaml racines dans designs/
    for yaml_file in sorted(DESIGNS_DIR.glob("*.yaml")):
        if yaml_file.name == "design.yaml":
            continue
        rel = yaml_file.relative_to(REPO_ROOT)
        if rel in [e["path"] for e in entries]:
            continue
        try:
            data = load_yaml(yaml_file)
        except Exception:
            continue
        name = data.get("name") or yaml_file.stem
        if not name:
            continue
        entries.append({
            "name": name,
            "path": str(rel),
            "version": data.get("version", "1.0.0"),
            "intent_hash": data.get("intent_hash", ""),
            "status": data.get("status", "ACTIVE"),
            "profile": data.get("profile", "STANDARD"),
            "consumers": data.get("consumers", []),
        })
    return entries


def scan_atoms() -> list[dict]:
    entries = []
    if not ATOMS_DIR.exists():
        return entries
    for yaml_file in sorted(ATOMS_DIR.rglob("*.yaml")):
        rel = yaml_file.relative_to(REPO_ROOT)
        try:
            data = load_yaml(yaml_file)
        except Exception:
            continue
        # atoms peuvent etre simples (liste de clefs) ou complexes
        name = data.get("name", yaml_file.stem) if isinstance(data, dict) else yaml_file.stem
        entries.append({
            "name": name,
            "path": str(rel),
            "version": data.get("version", "1.0.0") if isinstance(data, dict) else "1.0.0",
            "intent_hash": data.get("intent_hash", "") if isinstance(data, dict) else "",
            "status": data.get("status", "ACTIVE") if isinstance(data, dict) else "ACTIVE",
            "profile": data.get("profile", "STANDARD") if isinstance(data, dict) else "STANDARD",
            "consumers": data.get("consumers", []) if isinstance(data, dict) else [],
        })
    return entries


def scan_directory(base: Path, pattern: str = "*.yaml") -> list[dict]:
    entries = []
    if not base.exists():
        return entries
    for yaml_file in sorted(base.rglob(pattern)):
        rel = yaml_file.relative_to(REPO_ROOT)
        try:
            data = load_yaml(yaml_file)
        except Exception:
            continue
        if not isinstance(data, dict):
            continue
        name = data.get("name", yaml_file.stem)
        entries.append({
            "name": name,
            "path": str(rel),
            "version": data.get("version", "1.0.0"),
            "intent_hash": data.get("intent_hash", ""),
            "status": data.get("status", "ACTIVE"),
            "profile": data.get("profile", "STANDARD"),
            "consumers": data.get("consumers", []),
        })
    return entries


def merge_catalog(existing: list[dict], scanned: list[dict], key: str = "name") -> tuple[list[dict], list[str]]:
    """
    Merge scanned entries into existing catalog.
    - Nouveaux entries : ajoutés
    - Entries existantes : preserve metadonnees (intent_hash, consumers, status)
    Retourne (merged, changed_paths).
    """
    existing_map = {}
    for e in existing:
        k = e.get(key) or e.get("id") or e.get("name")
        if k:
            existing_map[k] = e
    changed = []
    merged = list(existing)
    for entry in scanned:
        k = entry.get(key) or entry.get("id") or entry.get("name")
        if not k:
            continue
        if k in existing_map:
            # Update path/version seulement si differs
            cur = existing_map[k]
            if cur.get("path") != entry["path"]:
                cur["path"] = entry["path"]
                changed.append(k)
            if cur.get("version") != entry["version"] and entry["version"]:
                cur["version"] = entry["version"]
                changed.append(k)
            if entry.get("status") and cur.get("status") != entry["status"]:
                cur["status"] = entry["status"]
        else:
            merged.append(entry)
            changed.append(k)
    return merged, changed


def sync_designs(dry_run: bool) -> dict:
    catalog_path = CATALOG_DIR / "designs.index.yaml"
    existing = []
    if catalog_path.exists():
        existing = load_yaml(catalog_path).get("entries", [])
    scanned = scan_designs()
    merged, changed = merge_catalog(existing, scanned)
    report = {
        "catalog": "designs.index.yaml",
        "scanned": len(scanned),
        "existing": len(existing),
        "merged": len(merged),
        "changed": changed,
        "dry_run": dry_run,
    }
    if not dry_run and changed:
        write_yaml(catalog_path, {"entries": merged})
    return report


def sync_atoms(dry_run: bool) -> dict:
    catalog_path = CATALOG_DIR / "atoms.index.yaml"
    existing = []
    if catalog_path.exists():
        existing = load_yaml(catalog_path).get("entries", [])
    scanned = scan_atoms()
    merged, changed = merge_catalog(existing, scanned)
    report = {
        "catalog": "atoms.index.yaml",
        "scanned": len(scanned),
        "existing": len(existing),
        "merged": len(merged),
        "changed": changed,
        "dry_run": dry_run,
    }
    if not dry_run and changed:
        write_yaml(catalog_path, {"entries": merged})
    return report


def sync_primitives(dry_run: bool) -> dict:
    catalog_path = CATALOG_DIR / "primitives.index.yaml"
    existing = []
    if catalog_path.exists():
        existing = load_yaml(catalog_path).get("entries", [])
    scanned = scan_directory(PRIMITIVES_DIR, "*.yaml")
    # Inclure les primitives dans des sous-dossiers
    for subdir in [PRIMITIVES_DIR]:
        for yaml_file in sorted(subdir.rglob("design.yaml")):
            rel = yaml_file.relative_to(REPO_ROOT)
            try:
                data = load_yaml(yaml_file)
            except Exception:
                continue
            name = data.get("name", yaml_file.parent.name)
            scanned.append({
                "name": name,
                "path": str(rel),
                "version": data.get("version", "1.0.0"),
                "intent_hash": data.get("intent_hash", ""),
                "status": data.get("status", "ACTIVE"),
                "profile": data.get("profile", "STANDARD"),
                "consumers": data.get("consumers", []),
            })
    merged, changed = merge_catalog(existing, scanned)
    report = {
        "catalog": "primitives.index.yaml",
        "scanned": len(scanned),
        "existing": len(existing),
        "merged": len(merged),
        "changed": changed,
        "dry_run": dry_run,
    }
    if not dry_run and changed:
        write_yaml(catalog_path, {"entries": merged})
    return report


def sync_skills(dry_run: bool) -> dict:
    catalog_path = CATALOG_DIR / "skills.index.yaml"
    existing = []
    if catalog_path.exists():
        existing = load_yaml(catalog_path).get("entries", [])
    scanned = scan_directory(SKILLS_DIR, "SKILL.md")
    # Convertir SKILL.md en entree catalogue
    converted = []
    for yaml_file in scanned:
        rel = yaml_file.relative_to(REPO_ROOT)
        # Lire le SKILL.md pour extraire name/intent_hash si present
        try:
            text = yaml_file.read_text(encoding="utf-8")
        except Exception:
            continue
        name = yaml_file.parent.name
        intent_hash = ""
        if "intent_hash:" in text:
            for line in text.splitlines():
                if line.startswith("intent_hash:"):
                    intent_hash = line.split(":", 1)[1].strip().strip('"').strip("'")
                    break
        converted.append({
            "name": name,
            "path": str(rel),
            "version": "1.0.0",
            "intent_hash": intent_hash,
            "status": "ACTIVE",
            "profile": "STANDARD",
            "consumers": [],
        })
    merged, changed = merge_catalog(existing, converted)
    report = {
        "catalog": "skills.index.yaml",
        "scanned": len(converted),
        "existing": len(existing),
        "merged": len(merged),
        "changed": changed,
        "dry_run": dry_run,
    }
    if not dry_run and changed:
        write_yaml(catalog_path, {"entries": merged})
    return report


def sync_citizens(dry_run: bool) -> dict:
    catalog_path = CATALOG_DIR / "citizens.index.yaml"
    existing = []
    if catalog_path.exists():
        existing = load_yaml(catalog_path).get("entries", [])
    scanned = scan_directory(CITIZENS_DIR, "citizen.yaml")
    merged, changed = merge_catalog(existing, scanned)
    report = {
        "catalog": "citizens.index.yaml",
        "scanned": len(scanned),
        "existing": len(existing),
        "merged": len(merged),
        "changed": changed,
        "dry_run": dry_run,
    }
    if not dry_run and changed:
        write_yaml(catalog_path, {"entries": merged})
    return report


def sync_pipelines(dry_run: bool) -> dict:
    catalog_path = CATALOG_DIR / "pipelines.index.yaml"
    existing = []
    if catalog_path.exists():
        existing = load_yaml(catalog_path).get("entries", [])
    scanned = scan_directory(PIPELINES_DIR, "*.yaml")
    merged, changed = merge_catalog(existing, scanned)
    report = {
        "catalog": "pipelines.index.yaml",
        "scanned": len(scanned),
        "existing": len(existing),
        "merged": len(merged),
        "changed": changed,
        "dry_run": dry_run,
    }
    if not dry_run and changed:
        write_yaml(catalog_path, {"entries": merged})
    return report


def sync_workflows(dry_run: bool) -> dict:
    catalog_path = CATALOG_DIR / "workflows.index.yaml"
    existing = []
    if catalog_path.exists():
        existing = load_yaml(catalog_path).get("entries", [])
    scanned = []
    if WORKFLOWS_DIR.exists():
        for md_file in sorted(WORKFLOWS_DIR.glob("*.md")):
            rel = md_file.relative_to(REPO_ROOT)
            scanned.append({
                "name": md_file.stem,
                "path": str(rel),
                "version": "1.0.0",
                "intent_hash": "",
                "status": "ACTIVE",
                "profile": "STANDARD",
                "consumers": [],
            })
    merged, changed = merge_catalog(existing, scanned)
    report = {
        "catalog": "workflows.index.yaml",
        "scanned": len(scanned),
        "existing": len(existing),
        "merged": len(merged),
        "changed": changed,
        "dry_run": dry_run,
    }
    if not dry_run and changed:
        write_yaml(catalog_path, {"entries": merged})
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync MDU Catalog — synchronisation atomique des catalogues")
    parser.add_argument("--designs", action="store_true", help="Sync designs.index.yaml")
    parser.add_argument("--atoms", action="store_true", help="Sync atoms.index.yaml")
    parser.add_argument("--all", action="store_true", help="Sync tous les catalogues")
    parser.add_argument("--dry-run", action="store_true", help="Rapport uniquement, aucune ecriture")
    parser.add_argument("--json", action="store_true", help="Sortie JSON uniquement")
    args = parser.parse_args()

    if not (args.designs or args.atoms or args.all):
        parser.print_help()
        return 1

    reports = []
    if args.all or args.designs:
        reports.append(sync_designs(args.dry_run))
    if args.all or args.atoms:
        reports.append(sync_atoms(args.dry_run))
    if args.all:
        reports.append(sync_primitives(args.dry_run))
        reports.append(sync_skills(args.dry_run))
        reports.append(sync_citizens(args.dry_run))
        reports.append(sync_pipelines(args.dry_run))
        reports.append(sync_workflows(args.dry_run))

    summary = {
        "status": "OK",
        "dry_run": args.dry_run,
        "reports": reports,
        "total_changed": sum(len(r["changed"]) for r in reports),
    }

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"[SYNC-MDU] dry_run={args.dry_run}")
        for r in reports:
            print(f"  {r['catalog']}: scanned={r['scanned']} existing={r['existing']} merged={r['merged']} changed={len(r['changed'])}")
        print(f"[SYNC-MDU] Total changed: {summary['total_changed']}")

    # Sauvegarder le rapport
    if REPORTS_DIR.exists():
        import datetime
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        report_path = REPORTS_DIR / f"sync-mdu-{ts}.json"
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
