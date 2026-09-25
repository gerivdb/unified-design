#!/usr/bin/env python3
"""
meta-design-gen.py — Générateur auto-généré de meta-design.yaml
à partir de manifests .atom.yaml et de l'arborescence physique.

Usage:
    python tools/meta-design-gen.py [--dry-run] [--output meta-design.yaml]

Header obligatoire:
    # AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY
    # Source: manifests .atom.yaml + tools/meta-design-gen.py
    # Regenerate: python tools/meta-design-gen.py
"""

import argparse
import glob
import os
from datetime import datetime
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
HEADER = """\
# AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY
# Source: manifests .atom.yaml + tools/meta-design-gen.py
# Regenerate: python tools/meta-design-gen.py
"""


def scan_atoms(root: Path) -> list:
    atoms = []
    for path in sorted(root.glob("atoms/*.atom.yaml")):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        atoms.append({
            "name": data.get("atom_id", path.stem),
            "path": f"atoms/{path.name}",
            "version": data.get("version", "1.0.0"),
            "intent_hash": data.get("intent_hash", ""),
            "consumers": data.get("consumers", []),
            "profile": data.get("profile", "STANDARD"),
        })
    return atoms


def scan_primitives(root: Path) -> list:
    primitives = []
    for path in sorted(root.glob("primitives/*.yaml")):
        if path.suffix == ".atom.yaml":
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        primitives.append({
            "name": data.get("name", path.stem),
            "path": f"primitives/{path.name}",
            "version": data.get("version", "1.0.0"),
            "intent_hash": data.get("intent_hash", ""),
            "consumers": data.get("consumers", []),
            "profile": data.get("profile", "STANDARD"),
        })
    return primitives


def scan_designs(root: Path) -> list:
    designs = []
    for path in sorted(root.glob("designs/*/design.yaml")):
        rel = path.relative_to(root)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            print(f"[WARN] Skipping invalid YAML: {rel} ({e})", flush=True)
            continue
        designs.append({
            "name": data.get("name", path.parent.name),
            "path": str(rel),
            "version": data.get("version", "1.0.0"),
            "intent_hash": data.get("intent_hash", ""),
            "consumers": data.get("consumers", []),
            "profile": data.get("profile", "STANDARD"),
        })
    for path in sorted(root.glob("designs/*.yaml")):
        rel = path.relative_to(root)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            print(f"[WARN] Skipping invalid YAML: {rel} ({e})", flush=True)
            continue
        designs.append({
            "name": data.get("name", path.stem),
            "path": str(rel),
            "version": data.get("version", "1.0.0"),
            "intent_hash": data.get("intent_hash", ""),
            "consumers": data.get("consumers", []),
            "profile": data.get("profile", "STANDARD"),
        })
    return designs


def scan_skills(root: Path) -> list:
    skills = []
    for path in sorted(root.glob("skills/*/SKILL.md")):
        rel = path.relative_to(root)
        skills.append({
            "name": path.parent.name,
            "path": str(rel),
            "version": "1.0.0",
            "intent_hash": "",
            "consumers": [],
            "profile": "STANDARD",
        })
    return skills


def scan_citizens(root: Path) -> list:
    citizens = []
    for path in sorted(root.glob("citizens/*/citizen.yaml")):
        rel = path.relative_to(root)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            print(f"[WARN] Skipping invalid YAML: {rel} ({e})", flush=True)
            continue
        citizens.append({
            "name": data.get("name", path.parent.name),
            "path": str(rel),
            "version": data.get("version", "1.0.0"),
            "intent_hash": data.get("intent_hash", ""),
            "consumers": data.get("consumers", []),
            "profile": data.get("profile", "STANDARD"),
        })
    return citizens


def scan_pipelines(root: Path) -> list:
    pipelines = []
    for path in sorted(root.glob("pipelines/*.yaml")):
        rel = path.relative_to(root)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            print(f"[WARN] Skipping invalid YAML: {rel} ({e})", flush=True)
            continue
        pipelines.append({
            "name": data.get("name", path.stem),
            "path": str(rel),
            "version": data.get("version", "1.0.0"),
            "intent_hash": data.get("intent_hash", ""),
            "status": data.get("status", "active"),
        })
    return pipelines


def scan_workflows(root: Path) -> list:
    workflows = []
    for path in sorted(root.glob("workflows/*.md")):
        rel = path.relative_to(root)
        workflows.append({
            "name": path.stem,
            "path": str(rel),
            "version": "1.0.0",
            "intent_hash": "",
            "status": "active",
        })
    return workflows


def load_existing_meta_design(root: Path) -> dict:
    path = root / "meta-design.yaml"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def build_meta_design() -> dict:
    existing = load_existing_meta_design(REPO_ROOT)
    designs = scan_designs(REPO_ROOT)
    primitives = scan_primitives(REPO_ROOT)
    skills = scan_skills(REPO_ROOT)
    citizens = scan_citizens(REPO_ROOT)
    pipelines = scan_pipelines(REPO_ROOT)
    workflows = scan_workflows(REPO_ROOT)

    meta = {
        "version": existing.get("version", "2.1.0"),
        "intent_hash": existing.get("intent_hash", "0xMDU_SCHEMA_20260731_V2_1_GRAPH_OF_LOOPS"),
        "status": existing.get("status", "active"),
        "inherits": existing.get("inherits", []),
        "capabilities": existing.get("capabilities", []),
        "design_rules": existing.get("design_rules", []),
        "complexity_gates": existing.get("complexity_gates", {
            "cognitive_complexity": 15,
            "max_capabilities_per_design": 8,
            "max_rules_per_atom": 10,
            "max_nesting_depth": 3,
        }),
        "design_schema": existing.get("design_schema", {}),
        "industrialization": existing.get("industrialization", {}),
        "designs": designs,
        "piliers": existing.get("piliers", []),
        "regles_transversales": existing.get("regles_transversales", []),
        "governance_atoms": existing.get("governance_atoms", []),
        "think_do_check": existing.get("think_do_check", {}),
        "agents_par_pilier": existing.get("agents_par_pilier", {}),
        "validation": existing.get("validation", {}),
        "git_policy": existing.get("git_policy", {}),
        "references": existing.get("references", []),
        "pipelines": pipelines,
        "workflows": workflows,
        "primitives": primitives,
        "skills": skills,
        "citizens": citizens,
    }
    return meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate meta-design.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout instead of writing")
    parser.add_argument("--output", default="meta-design.yaml", help="Output file path")
    args = parser.parse_args()

    meta = build_meta_design()
    output_path = REPO_ROOT / args.output

    if args.dry_run:
        print(HEADER)
        print(yaml.dump(meta, default_flow_style=False, sort_keys=False, allow_unicode=True))
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(HEADER)
            yaml.dump(meta, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
