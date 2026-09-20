#!/usr/bin/env python3
"""
Analyse tous les skills, citizens, pipelines, primitives, workflows inédits
à déduire de la conversation et/ou à mettre à jour.
"""

import yaml
from pathlib import Path

REPO = Path(r"D:\DO\WEB\TOOLS\L0-CANON\unified-design")

def load_catalog(name):
    path = REPO / "catalog" / name
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if data else {}

def main():
    skills = load_catalog("skills.index.yaml")
    primitives = load_catalog("primitives.index.yaml")
    citizens = load_catalog("citizens.index.yaml")
    designs = load_catalog("designs.index.yaml")

    print("=== SKILLS (unified-design) ===")
    for s in skills.get("entries", []):
        if "unified-design" in s.get("source_repo", ""):
            print(f"  {s['id']} -> {s['source_path']}")

    print()
    print("=== PRIMITIVES (unified-design) ===")
    for p in primitives.get("entries", []):
        if "unified-design" in p.get("source_repo", ""):
            print(f"  {p['id']} -> {p['source_path']}")

    print()
    print("=== CITIZENS (unified-design) ===")
    for c in citizens.get("entries", []):
        if "unified-design" in c.get("source_repo", ""):
            print(f"  {c['id']} -> {c['source_path']}")

    print()
    print("=== DESIGNS (unified-design, registered) ===")
    for d in designs.get("entries", []):
        if "unified-design" in d.get("source_repo", ""):
            print(f"  {d['id']} -> {d['source_path']}")

    print()
    print("=== WORKFLOWS (filesystem) ===")
    for p in sorted((REPO / "workflows").glob("*")):
        if p.is_file():
            print(f"  {p.name}")

    print()
    print("=== PIPELINES (filesystem) ===")
    for p in sorted((REPO / "pipelines").glob("*")):
        if p.is_file():
            print(f"  {p.name}")

if __name__ == "__main__":
    main()
