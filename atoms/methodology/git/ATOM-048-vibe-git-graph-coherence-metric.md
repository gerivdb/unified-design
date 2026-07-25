---
type: ATOM
id: ATOM-048-vibe-git-graph-coherence-metric
version: 1.0.0
date: 2026-07-19
title: "Vibe Git Graph Coherence Metric — Mesure de cohérence structurelle d'un graphe git"
intent_hash: 0xATOM_048_VIBE_GIT_GRAPH_COHERENCE_METRIC_20260719
status: proposed
strate: L4-TOOLS
tags:
  - git
  - metrics
  - vibe
  - graph
  - archi
---

# ATOM-048 — Vibe Git Graph Coherence Metric

## Contexte

L'analyse de la santé d'un dépôt git passe par la mesure de sa structure de graphe. La **Vibe Git Graph Coherence Metric** fournit une mesure normalisée de la cohérence structurelle d'un historique git, complémentaire aux métriques spectrales Vibe Core.

## Design

La **Vibe Git Graph Coherence Metric** est un indicateur calculé sur le graphe git d'un dépôt. Il mesure le ratio entre la structure attendue (branches, merges, bridges) et la structure observée. Un score élevé indique un historique linéaire et prévisible ; un score bas indique des fusions non résolues ou des branches orphelines.

## Règle / Invariant

**La cohérence d'un graphe git est définie par le ratio entre le nombre de relations structurelles valides et le nombre total de commits analysés.**

### Formule

```python
coherence_index = 1 - (branches_anormales + bridges_anormaux) / total_commits
```

Où :
- `branches_anormales` = branches sans lien de fusion vers `main`
- `bridges_anormaux` = commits spanning plusieurs composants sans merge associé
- `total_commits` = commits analysés dans la fenêtre

### Interprétation

| Score | Interprétation |
|---|---|
| `0.8 - 1.0` | Historique cohérent, peu d'anomalies |
| `0.5 - 0.8` | Anomalies structurelles mineures |
| `< 0.5` | Historique non linéaire, risque de conflit |

## Condition de validation

1. Exécuter `vibe_git_graph.py --repo <path> --format json --max-commits 50`
2. Vérifier que `coherence_index >= 0.8`
3. Si `coherence_index < 0.8`, lister les commits anomalies
4. Corriger les branches orphelines avant nouvelle fusion

## Parents

- ATOM-041 (OperatorT) : base de l'infrastructure ternaire
- ATOM-042 (DAG-3 Runtime) : runtime du méta-graphe
- ATOM-043 (DAG-3 Validator) : validation sémantique
- ATOM-044 (Janus Involution) : symétrie CPT

## Tags

`#git` `#metrics` `#vibe` `#graph` `#archi` `#L4-TOOLS`
