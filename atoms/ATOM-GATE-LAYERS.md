# ATOM-GATE-LAYERS

## Description

Barrière de contrôle à 4 couches — Inspiré de D:\GG-knox\engineering ideas\300-kimi-k3\2.md.

Toute opération critique passe par 4 couches de validation successives :

1. **L1 — Technique** : tests unitaires, lint, build
2. **L2 — Architecture** : conformité ADR, DAG, dépendances
3. **L3 — Gouvernance** : PoL, pre-commit hooks, ADR backing
4. **L4 — Humain** : HITL validation pour modifications critiques

## Règles

1. Toute opération critique doit passer les 4 couches
2. L'échec à une couche bloque l'opération
3. Les couches sont séquentielles, pas parallèles
4. L4 (HITL) peut être bypassé seulement pour les opérations P3/P4
5. Chaque couche émet un verdict : PASS / WARN / FAIL

## Références

- **Source** : `D:\GG-knox\engineering ideas\300-kimi-k3\2.md`
- **Concept** : Barrière de contrôle à 4 couches
