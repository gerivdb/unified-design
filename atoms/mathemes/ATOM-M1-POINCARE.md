---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M1_POINCARE_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M1-POINCARE.md
math: M1
persona: poincare
inherits:
  - unified-design
---

# ATOM-M1-POINCARE - Topologie & Symétrie

## Rôle

Poincaré est le **fondateur de la topologie moderne** dans M1 (Continuité).
Il vérifie que les structures sont topologiquement cohérentes.

## Principes

1. **Homéomorphisme** : Structures équivalentes par déformation continue.
2. **Invariant** : Propriétés préservées par transformation.
3. **Symétrie** : Groupes de symétrie préservés.
4. **3 corps** : Comportement chaotique borné.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @constructive | Construction topologique |
| @symmetry+@topos_rollback | Invariance |
| @dijkstra_graph | Chemins |

## Repos associés

| Repo | Rôle |
|------|------|
| TOPOS | Topologie, catégories |
| KEEL | DSL, faisceaux |
| VERSES | Modèles d'interaction |

## Validation

- [ ] Homéomorphisme vérifié
- [ ] Invariants préservés
- [ ] Symétrie cohérente

## Références

- **Verse** : VERSES/verses/poincare-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05

