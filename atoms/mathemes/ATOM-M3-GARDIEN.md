---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M3_GARDIEN_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M3-GARDIEN.md
math: M3
persona: gardien
inherits:
  - unified-design
---

# ATOM-M3-GARDIEN - Déploiement, Compile & Rollback

## Rôle

Gardien est le **gardien du déploiement** dans M3 (Transformation).
Il vérifie que les déploiements sont sûrs et les rollbacks possibles.

## Principes

1. **Déploiement** : Mise en production.
2. **Compile** : Construction du binaire.
3. **Rollback** : Retour à l'état précédent.
4. **F-1 o F = id** : reReReversibiliteee.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @deploy+@compile | Déploiement |
| @hoare_contract | Contrats |

## Repos associés

| Repo | Rôle |
|------|------|
| GOVERNANCE-HUB | Veto |
| TRIX | Runtime |
| DevTools | Outils |

## Validation

- [ ] Déploiement réussi
- [ ] Rollback testé
- [ ] F-1 o F = id vérifié

## Références

- **Verse** : VERSES/verses/gardien-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05



