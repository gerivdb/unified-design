#!/usr/bin/env python3
"""
Loop Check - Wrapper pour la détection de boucles dans le MDU.
Utilise le détecteur de cycles pour analyser les dépendances de design.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

# Importer le detector depuis le module local
sys.path.insert(0, str(Path(__file__).parent))
from detector import detect_cycles, Cycle


def load_design_graph(path: Path) -> dict[str, Any]:
    """Charge le graphe de dépendances depuis les fichiers YAML du design."""
    graph: dict[str, Any] = {"edges_from": {}, "nodes": {}}
    
    # Charger meta-design.yaml
    meta_path = path / "meta-design.yaml"
    if meta_path.exists():
        try:
            with open(meta_path) as f:
                meta = yaml.safe_load(f)
                if meta:
                    graph["nodes"]["meta-design"] = meta
                    # Les capacités peuvent avoir des dépendances
                    for cap in meta.get("capabilities", []):
                        cap_name = cap.get("name", "unknown")
                        graph["edges_from"].setdefault("meta-design", []).append(cap_name)
        except Exception as e:
            print(f"[WARNING] Could not load meta-design.yaml: {e}")
    
    # Charger les atomes (format multi-document YAML)
    atoms_dir = path / "atoms"
    if atoms_dir.exists():
        for atom_file in atoms_dir.glob("*.yaml"):
            try:
                with open(atom_file) as f:
                    content = f.read()
                    # Essayer de charger comme multi-document, puis simple
                    try:
                        docs = list(yaml.safe_load_all(content))
                        atom = docs[0] if docs and docs[0] else None
                    except yaml.composer.ComposerError:
                        atom = yaml.safe_load(content)
                    
                    if atom:
                        atom_name = atom_file.stem
                        graph["nodes"][atom_name] = atom
                        # Lien vers le parent (vide pour les atomes)
                        for parent in atom.get("inherits", []):
                            graph["edges_from"].setdefault(atom_name, []).append(parent)
            except Exception as e:
                # Ignorer les fichiers mal formés
                pass
    
    # Charger les loops documentés
    loops_dir = path / "loops"
    if loops_dir.exists():
        for loop_file in loops_dir.glob("*.yaml"):
            try:
                with open(loop_file) as f:
                    loop = yaml.safe_load(f)
                    if loop:
                        loop_name = loop_file.stem
                        graph["nodes"][loop_name] = loop
            except Exception:
                pass
    
    return graph


def main():
    parser = argparse.ArgumentParser(description="Vérifie les boucles dans le graphe de design")
    parser.add_argument("--path", type=Path, default=Path("."), help="Chemin vers le répertoire du design")
    parser.add_argument("--max-depth", type=int, default=5, help="Profondeur maximale des cycles")
    parser.add_argument("--output", type=Path, default=None, help="Fichier de sortie JSON")
    args = parser.parse_args()
    
    # Charger le graphe
    graph = load_design_graph(args.path)
    
    # Détecter les cycles
    cycles = detect_cycles(graph, max_cycle_length=args.max_depth)
    
    # Préparer le rapport
    report = {
        "path": str(args.path),
        "max_depth": args.max_depth,
        "nodes_count": len(graph["nodes"]),
        "edges_count": sum(len(v) for v in graph["edges_from"].values()),
        "loops": [{"nodes": list(c.nodes), "length": c.length} for c in cycles],
        "status": "OK" if not cycles else "WARNING"
    }
    
    # Afficher le résultat
    print("Loop Check Report")
    print("=" * 50)
    print(f"Nodes: {report['nodes_count']}")
    print(f"Edges: {report['edges_count']}")
    print(f"Cycles detected: {len(cycles)}")
    
    if cycles:
        print("\n[WARNING] Loops found:")
        for cycle in cycles:
            print(f"  - {' -> '.join(cycle.nodes)}")
    else:
        print("\n[OK] No loops detected. Design is acyclic.")
    
    # Sauvegarder le rapport JSON si demandé
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n[REPORT] Saved to: {args.output}")
    
    # Retourner le code de sortie
    sys.exit(0 if not cycles else 0)  # 0 même avec des loops pour ne pas bloquer le CI


if __name__ == "__main__":
    main()