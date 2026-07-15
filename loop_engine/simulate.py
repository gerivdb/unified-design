#!/usr/bin/env python3
"""
simulate.py — Simulateur d'impact de nouveaux designs sur le graphe.

Prend un design en projet et prédit :
1. Les cycles créés
2. Les conflits de capacités
3. L'incrémentalité du design
4. L'impact sur les designs existants
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from detector import detect_cycles, Cycle


@dataclass
class SimulationResult:
    path: str
    design_name: str
    would_create_cycles: list[list[str]]
    capability_conflicts: list[str]
    incremental_score: float
    affected_designs: list[str]
    suggestions: list[str]


def load_design(path: Path) -> dict[str, Any]:
    """Charge un design.yaml."""
    with open(path) as f:
        return yaml.safe_load(f)


def load_meta_design(path: Path) -> dict[str, Any]:
    """Charge le meta-design.yaml."""
    with open(path) as f:
        return yaml.safe_load(f)


def build_mock_graph(design: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    """Construit un graphe factice incluant le nouveau design."""
    graph = {"edges_from": {}, "nodes": {}}
    
    # Ajouter le nouveau design
    name = design.get("name", "unknown")
    inherits = design.get("inherits", [])
    graph["nodes"][name] = design
    graph["edges_from"][name] = inherits
    
    # Ajouter les parents
    for parent in inherits:
        if parent not in graph["edges_from"]:
            graph["edges_from"][parent] = []
    
    return graph


def calculate_incremental_score(design: dict[str, Any], meta: dict[str, Any]) -> float:
    """Calcule le score d'incrémentalité (0-100)."""
    capabilities = design.get("capabilities", [])
    inherits = design.get("inherits", [])
    
    # Score de base
    score = 100.0
    
    # Pénalité pour héritage profond
    if len(inherits) > 2:
        score -= 20 * (len(inherits) - 2)
    
    # Pénalité pour nouvelles capacités non standard
    standard_caps = [cap.get("name") for cap in meta.get("capabilities", [])]
    for cap in capabilities:
        if isinstance(cap, dict):
            cap_name = cap.get("name", "")
            if cap_name not in standard_caps:
                score -= 5
    
    return max(0, min(100, score))


def suggest_fixes(result: SimulationResult) -> list[str]:
    """Génère des suggestions pour corriger les problèmes."""
    suggestions = []
    
    if result.would_create_cycles:
        suggestions.append("Consider refactoring to avoid circular dependencies")
        suggestions.append("Use composition over inheritance for this capability")
    
    if result.capability_conflicts:
        suggestions.append("Review capability parameters for conflicts")
        suggestions.append("Consider using a different capability combination")
    
    if result.incremental_score < 80:
        suggestions.append("Increase incremental score by reusing existing capabilities")
        suggestions.append("Consider moving shared logic to a parent design")
    
    return suggestions


def simulate(design_path: Path, meta_path: Path | None = None) -> SimulationResult:
    """Simule l'ajout d'un design au graphe."""
    design = load_design(design_path)
    meta = load_meta_design(meta_path) if meta_path else {}
    
    # Construire le graphe factice
    graph = build_mock_graph(design, meta)
    
    # Détecter les cycles
    cycles = detect_cycles(graph, max_cycle_length=5)
    
    # Vérifier les conflits de capacités
    conflicts = []
    capabilities = design.get("capabilities", [])
    for cap in capabilities:
        if isinstance(cap, dict):
            name = cap.get("name", "")
            params = cap.get("parameters", {})
            if name == "latency-bound" and params.get("max_latency_ms", 100) <= 1:
                conflicts.append("latency-bound <= 1ms conflicts with power-capped <= 1W")
    
    # Calculer le score d'incrémentalité
    incremental_score = calculate_incremental_score(design, meta)
    
    return SimulationResult(
        path=str(design_path),
        design_name=design.get("name", "unknown"),
        would_create_cycles=[list(c.nodes) for c in cycles],
        capability_conflicts=conflicts,
        incremental_score=incremental_score,
        affected_designs=design.get("inherits", []),
        suggestions=suggest_fixes(SimulationResult(
            path=str(design_path),
            design_name=design.get("name", "unknown"),
            would_create_cycles=[list(c.nodes) for c in cycles],
            capability_conflicts=conflicts,
            incremental_score=incremental_score,
            affected_designs=[],
            suggestions=[]
        ))
    )


def main():
    parser = argparse.ArgumentParser(description="Simule l'impact d'un design")
    parser.add_argument("design", type=Path, help="Chemin vers design.yaml")
    parser.add_argument("--meta-design", type=Path, default=None, help="Chemin vers meta-design.yaml")
    parser.add_argument("--output", type=Path, default=None, help="Fichier de sortie JSON")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    args = parser.parse_args()
    
    result = simulate(args.design, args.meta_design)
    
    if args.json:
        output = {
            "path": result.path,
            "design_name": result.design_name,
            "would_create_cycles": result.would_create_cycles,
            "capability_conflicts": result.capability_conflicts,
            "incremental_score": result.incremental_score,
            "affected_designs": result.affected_designs,
            "suggestions": result.suggestions,
            "status": "OK" if not result.would_create_cycles and not result.capability_conflicts else "WARNING"
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"[SIMULATE] Impact analysis for: {result.design_name}")
        print(f"{'=' * 50}")
        
        if result.would_create_cycles:
            print(f"[WARN] Would create {len(result.would_create_cycles)} cycle(s):")
            for cycle in result.would_create_cycles:
                print(f"  - {' -> '.join(cycle)}")
        else:
            print("[OK] No cycles would be created")
        
        if result.capability_conflicts:
            print(f"[WARN] {len(result.capability_conflicts)} capability conflict(s):")
            for conflict in result.capability_conflicts:
                print(f"  - {conflict}")
        else:
            print("[OK] No capability conflicts")
        
        print(f"\n[SCORE] Incremental: {result.incremental_score:.1f}/100")
        
        if result.suggestions:
            print("\n[SUGGESTIONS]")
            for s in result.suggestions:
                print(f"  - {s}")
    
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump({
                "path": result.path,
                "design_name": result.design_name,
                "would_create_cycles": result.would_create_cycles,
                "capability_conflicts": result.capability_conflicts,
                "incremental_score": result.incremental_score,
                "affected_designs": result.affected_designs,
                "suggestions": result.suggestions
            }, f, indent=2)
        print(f"\n[REPORT] Saved to: {args.output}")


if __name__ == "__main__":
    main()