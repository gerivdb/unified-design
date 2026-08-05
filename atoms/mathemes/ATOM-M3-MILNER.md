---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M3_MILNER_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M3-MILNER.md
math: M3
persona: milner
inherits:
  - unified-design
---

# ATOM-M3-MILNER - Types & pi-Calcul

## Rôle

Milner est le **gardien des types et du pi-calcul** dans M3 (Transformation).
Il vérifie que les programmes sont typés et les communications cohérentes.

## Principes

1. **pi-calcul** : Calcul des processus mobiles.
2. **CCS** : Algèbre des systèmes communicants.
3. **Type** : Classification des valeurs.
4. **Communication** : Échange de messages.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @milner_types | Types |
| @hoare_contract | Contrats |

## Repos associés

| Repo | Rôle |
|------|------|
| TRIX | Runtime |
| ECOS-CLI | Exécution |
| VERSES | Interaction |

## Validation

- [ ] Types cohérents
- [ ] Communication vérifiée
- [ ] pi-calcul correct

## Références

- **Verse** : VERSES/verses/milner-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05


