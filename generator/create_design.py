#!/usr/bin/env python3
"""
create_design.py — Générateur de dépôt de design unifié.

Lit le méta-design, fusionne les héritages, détecte les conflits,
et génère un design.yaml valide prêt à être déployé.

Usage:
    python create_design.py <design_name> --parent <parent_design> [--capability <cap> ...]
"""

import argparse
import os
import sys
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


def generate_design_yaml(
    name: str, parent: str | None, capabilities: dict[str, Any], output_dir: Path
) -> Path:
    """Génère le fichier design.yaml dans le répertoire cible."""
    design = {
        "version": "1.0.0",
        "name": name,
        "inherits": [parent] if parent else [],
        "capabilities": capabilities,
        "generated_by": "unified-design/create_design.py",
    }
    out_file = output_dir / "design.yaml"
    with open(out_file, "w", encoding="utf-8") as f:
        yaml.dump(design, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return out_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Génère un nouveau design unifié")
    parser.add_argument("design_name", help="Nom du design à créer")
    parser.add_argument("--parent", help="Design parent (héritage)", default=None)
    parser.add_argument(
        "--capability",
        action="append",
        default=[],
        help="Capacité à inclure (peut être répété)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("../generated-designs"),
        help="Répertoire de sortie",
    )
    parser.add_argument(
        "--meta-design",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "meta-design.yaml",
        help="Chemin vers meta-design.yaml",
    )
    args = parser.parse_args()

    meta = load_meta_design(args.meta_design)
    capabilities = resolve_capabilities(meta, args.capability)
    conflicts = detect_conflicts(capabilities)

    if conflicts:
        print("❌ Conflits détectés :")
        for c in conflicts:
            print(f"  - {c}")
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_file = generate_design_yaml(
        args.design_name, args.parent, capabilities, args.output_dir
    )
    print(f"✅ Design généré : {out_file}")
    print(f"   Capacités : {list(capabilities.keys())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
