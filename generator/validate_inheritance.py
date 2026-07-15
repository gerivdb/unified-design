#!/usr/bin/env python3
"""
validate_inheritance.py — Valide le graphe d'héritage et détecte les cycles.

Usage:
    python validate_inheritance.py <design.yaml> [--meta-design <meta_design.yaml>]
"""

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml


def load_design(design_path: Path) -> dict[str, Any]:
    with open(design_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def detect_cycles(design: dict[str, Any], meta: dict[str, Any]) -> list[list[str]]:
    """Détecte les cycles dans le graphe d'héritage (DFS)."""
    graph: dict[str, list[str]] = {}
    for d in meta.get("designs", []):
        name = d.get("name")
        inherits = d.get("inherits", [])
        if name:
            graph[name] = inherits if isinstance(inherits, list) else [inherits]

    # Ajouter le design courant
    name = design.get("name", "current")
    inherits = design.get("inherits", [])
    graph[name] = inherits if isinstance(inherits, list) else [inherits]

    cycles = []
    visited = set()
    rec_stack = set()

    def dfs(node: str, path: list[str]) -> None:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
        path.pop()
        rec_stack.remove(node)

    for node in graph:
        if node not in visited:
            dfs(node, [])

    return cycles


def validate_conflicts(design: dict[str, Any]) -> list[str]:
    """Valide qu'aucune capacité n'est en conflit avec une autre."""
    conflicts = []
    caps = {c["name"]: c.get("parameters", {}) for c in design.get("capabilities", [])}
    lat = caps.get("latency-bound", {}).get("max_latency_ms")
    pow_ = caps.get("power-capped", {}).get("max_power_w")
    if lat is not None and pow_ is not None and lat <= 1 and pow_ <= 1:
        conflicts.append(
            "deadlock: latency-bound <= 1ms et power-capped <= 1W sont mutuellement exclusifs"
        )
    return conflicts


def main() -> int:
    parser = argparse.ArgumentParser(description="Valide l'héritage et détecte les cycles")
    parser.add_argument("design", type=Path, help="Chemin vers design.yaml")
    parser.add_argument(
        "--meta-design",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "meta-design.yaml",
        help="Chemin vers meta-design.yaml",
    )
    args = parser.parse_args()

    meta = load_design(args.meta_design) if args.meta_design.exists() else {}
    design = load_design(args.design)

    cycles = detect_cycles(design, meta)
    conflicts = validate_conflicts(design)

    ok = True
    if cycles:
        print("❌ Cycles détectés :")
        for cycle in cycles:
            print(f"  {' → '.join(cycle)}")
        ok = False
    else:
        print("✅ Aucun cycle d'héritage détecté.")

    if conflicts:
        print("❌ Conflits de capacités :")
        for c in conflicts:
            print(f"  - {c}")
        ok = False
    else:
        print("✅ Aucun conflit de capacités.")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
