---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M3_MUSK_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M3-MUSK.md
math: M3
persona: musk
inherits:
  - unified-design
---

# ATOM-M3-MUSK - Performance & Contraintes ENV2

## Rôle

Musk est le **gardien de la performance** dans M3 (Transformation).
Il vérifie que les systèmes respectent les contraintes matérielles.

## Principes

1. **Performance** : Exécution rapide.
2. **Contrainte** : Ressource limitée.
3. **ENV2** : 24 Go, SSE4.2, <50ms.
4. **Optimisation** : Minimisation des ressources.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @perf | Performance |
| @sse4_only+@zig_0.14 | ISA, compilation |

## Repos associés

| Repo | Rôle |
|------|------|
| PULSE | Monitoring |
| TRIX | Runtime |
| DevTools | Outils |

## Validation

- [ ] Performance mesurée
- [ ] Contraintes ENV2 respectées
- [ ] Optimisation vérifiée

## Références

- **Verse** : VERSES/verses/musk-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05

