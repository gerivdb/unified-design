---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M1_DIJKSTRA_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M1-DIJKSTRA.md
math: M1
persona: dijkstra
inherits:
  - unified-design
---

# ATOM-M1-DIJKSTRA - Graphes & Chemins

## Rôle

Dijkstra est le **gardien des graphes et chemins** dans M1 (Continuité).
Il vérifie que les chemins sont optimaux et les graphes cohérents.

## Principes

1. **Plus court chemin** : Minimisation de la distance.
2. **Graphe** : Noeuds et arêtes.
3. **Algorithme** : Procédure de calcul.
4. **Convexité** : Ensemble sans détour.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @dijkstra_graph | Plus court chemin |
| @constructive | Construction de graphes |

## Repos associés

| Repo | Rôle |
|------|------|
| NEXUS | Graphe de dépendances |
| TOPOS | Topologie |
| CTULU | Orchestration |

## Validation

- [ ] Chemin optimal vérifié
- [ ] Graphe connexe
- [ ] Distance bornée

## Références

- **Verse** : VERSES/verses/dijkstra-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05


