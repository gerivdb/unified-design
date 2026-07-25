#!/usr/bin/env python3
"""
create_design.py — Générateur de dépôt de design unifié.

Lit le méta-design, fusionne les héritages, détecte les conflits,
et génère un design.yaml valide prêt à être déployé.

Usage:
    python create_design.py <design_name> --parent <parent_design> [--capability <cap> ...] [--template <template_path>]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


def load_meta_design(meta_path: Path) -> dict[str, Any]:
    with open(meta_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def resolve_capabilities(meta: dict[str, Any], requested: list[str]) -> dict[str, Any]:
    """Fusionne les capacités héritées avec les paramètres demandés."""
    caps = {}
    for cap in meta.get("capabilities", []):
        name = cap["name"]
        if name in requested or not requested:
            caps[name] = cap.get("parameters", {})
    return caps


def detect_conflicts(caps: dict[str, Any]) -> list[str]:
    """Détecte les conflits entre capacités (ex: latence vs puissance impossibles)."""
    conflicts = []
    # Règle simple : si latency-bound <= 1ms ET power-capped <= 1W → conflit
    lat = caps.get("latency-bound", {}).get("max_latency_ms")
    pow_ = caps.get("power-capped", {}).get("max_power_w")
    if lat is not None and pow_ is not None and lat <= 1 and pow_ <= 1:
        conflicts.append(
            "deadlock: latency-bound <= 1ms et power-capped <= 1W sont mutuellement exclusifs"
        )
    return conflicts


def create_template_structure(output_dir: Path, design_name: str) -> None:
    """Crée la structure de base d'un dépôt de design."""
    # Structure minimale d'un dépôt de design
    structure = [
        ".github/workflows/ci.yml",
        "docs/META-DESIGN.md",
        "atoms/",
        "loops/",
        "ADR/",
    ]
    
    for item in structure:
        item_path = output_dir / item
        if item.endswith("/"):
            item_path.mkdir(parents=True, exist_ok=True)
        else:
            item_path.parent.mkdir(parents=True, exist_ok=True)
            if not item_path.exists():
                # Créer un fichier placeholder
                if item.endswith(".yml"):
                    item_path.write_text(f"# {design_name} - {item}\n")


def generate_design_yaml(
    name: str, parents: list[str], capabilities: dict[str, Any], output_dir: Path, meta: dict[str, Any]
) -> Path:
    """Génère le fichier design.yaml dans le répertoire cible."""
    design = {
        "version": "1.0.0",
        "name": name,
        "inherits": parents,
        "capabilities": capabilities,
        "generated_by": "unified-design/create_design.py",
        "generated_at": datetime.now().isoformat(),
        "parent_mdu": meta.get("name", "unified-design"),
        "intent_hash": f"0x{name.upper().replace('-', '_')}_DESIGN_{datetime.now().strftime('%Y%m%d')}",
    }
    out_file = output_dir / "design.yaml"
    with open(out_file, "w", encoding="utf-8") as f:
        yaml.dump(design, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return out_file


def generate_repo_yaml(output_dir: Path, design_name: str, parents: list[str]) -> Path:
    """Génère le fichier REPO.yaml avec les métadonnées du dépôt."""
    repo = {
        "name": design_name,
        "full_name": f"gerivdb/{design_name}",
        "local_path": f"D:/DO/WEB/TOOLS/L0-CANON/{design_name}",
        "parents": parents,
        "status": "active",
        "stratum": "L0-CANON",
        "description": f"Design unifié hérité de {', '.join(parents)}" if parents else "Design unifié racine",
        "capabilities": ["latency-bound", "power-capped"],
        "created_at": datetime.now().isoformat(),
    }
    out_file = output_dir / "REPO.yaml"
    with open(out_file, "w", encoding="utf-8") as f:
        yaml.dump(repo, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return out_file


def generate_ci_workflow(output_dir: Path, design_name: str) -> Path:
    """Génère le workflow CI pour ce design."""
    ci_content = f"""name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyyaml

      - name: Validate design.yaml
        run: |
          python3 -c "import yaml; d=yaml.safe_load(open('design.yaml')); assert 'name' in d, 'Missing name'; assert 'inherits' in d, 'Missing inherits'; print('[OK] design.yaml valid')"

      - name: Validate YAML files
        run: |
          for f in atoms/*.yaml loops/*.yaml; do
            python3 -c "import yaml; yaml.safe_load(open('$f'))" && echo "[OK] $f valid"
          done
"""
    out_file = output_dir / ".github" / "workflows" / "ci.yml"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(ci_content)
    return out_file


def generate_gitignore(output_dir: Path) -> Path:
    """Génère le fichier .gitignore standard."""
    content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.eggs/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Generated
*.generated.yaml
"""
    out_file = output_dir / ".gitignore"
    out_file.write_text(content)
    return out_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Génère un nouveau design unifié")
    parser.add_argument("design_name", help="Nom du design à créer")
    parser.add_argument("--parent", help="Design parent (héritage)", default=None)
    parser.add_argument(
        "--parents",
        nargs="+",
        help="Designs parents multiples pour héritage multiple (ordre = priorité)",
        default=None,
    )
    parser.add_argument(
        "--capability",
        action="append",
        default=[],
        help="Capacité à inclure (peut être répété)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Répertoire de sortie (défaut: ../generated-designs)",
    )
    parser.add_argument(
        "--meta-design",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "meta-design.yaml",
        help="Chemin vers meta-design.yaml",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=None,
        help="Chemin vers un template de dépôt à utiliser",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Affiche ce qui serait généré sans créer les fichiers",
    )
    args = parser.parse_args()

    # Support héritage multiple : combiner --parent et --parents
    parents = []
    if args.parent:
        parents.append(args.parent)
    if args.parents:
        parents.extend(args.parents)
    parents = list(dict.fromkeys(parents))  # dédoublonner en préservant l'ordre

    meta = load_meta_design(args.meta_design)
    capabilities = resolve_capabilities(meta, args.capability)
    conflicts = detect_conflicts(capabilities)

    if conflicts:
        print("[FAIL] Conflicts detected:")
        for c in conflicts:
            print(f"  - {c}")
        return 1

    # Déterminer le répertoire de sortie
    output_dir = args.output_dir or Path(__file__).resolve().parent.parent / "generated-designs" / args.design_name
    
    if args.dry_run:
        print(f"[DRY-RUN] Would create in: {output_dir}")
        print(f"   Design: {args.design_name}")
        print(f"   Parents: {', '.join(parents) if parents else 'none'}")
        print(f"   Capacities: {list(capabilities.keys())}")
        return 0

    # Créer le répertoire de sortie
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Créer la structure de base
    create_template_structure(output_dir, args.design_name)
    
    # Générer les fichiers
    design_file = generate_design_yaml(args.design_name, parents, capabilities, output_dir, meta)
    repo_file = generate_repo_yaml(output_dir, args.design_name, parents)
    ci_file = generate_ci_workflow(output_dir, args.design_name)
    gitignore_file = generate_gitignore(output_dir)
    
    print(f"[OK] Design generated: {design_file}")
    print(f"   Parents: {', '.join(parents) if parents else 'none'}")
    print(f"   Capacities: {list(capabilities.keys())}")
    print(f"   Structure: {list(output_dir.rglob('*'))}")
    print(f"   Files created:")
    print(f"     - {design_file}")
    print(f"     - {repo_file}")
    print(f"     - {ci_file}")
    print(f"     - {gitignore_file}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
