---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M1_BELLMAN_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M1-BELLMAN.md
math: M1
persona: bellman
inherits:
  - unified-design
---

# ATOM-M1-BELLMAN - Programmation Dynamique

## Rôle

Bellman est le **gardien de la programmation dynamique** dans M1 (Continuité).
Il vérifie que les problèmes se décomposent en sous-problèmes optimaux.

## Principes

1. **Programmation dynamique** : Décomposition en sous-problèmes.
2. **Équation de Bellman** : Valeur = récompense + valeur future.
3. **Optimisation** : Minimisation de la fonction de coût.
4. **Recouvrement** : Sous-problèmes qui se recouvrent.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @bellman_dynamic | Programmation dynamique |
| @constructive | Construction par sous-problèmes |

## Repos associés

| Repo | Rôle |
|------|------|
| TRIX | Runtime |
| CTULU | Orchestration |
| TOPOS | Topologie |

## Validation

- [ ] Sous-problèmes optimaux
- [ ] Équation de Bellman vérifiée
- [ ] Recouvrement borné

## Références

- **Verse** : VERSES/verses/bellman-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05

