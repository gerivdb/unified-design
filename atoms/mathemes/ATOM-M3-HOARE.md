---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M3_HOARE_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M3-HOARE.md
math: M3
persona: hoare
inherits:
  - unified-design
---

# ATOM-M3-HOARE - Contrats & Vérification

## Rôle

Hoare est le **gardien des contrats** dans M3 (Transformation).
Il vérifie que les programmes respectent les spécifications.

## Principes

1. **Logique de Hoare** : {P} C {Q}
2. **Contrat** : Précondition, postcondition, invariant.
3. **Vérification** : Preuve de correction.
4. **Correctitude** : Programme fait ce qu'il dit.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @hoare_contract | Contrats |
| @milner_types | Types |

## Repos associés

| Repo | Rôle |
|------|------|
| REPO-STANDARDS | Normes |
| TRIX | Runtime |
| DevTools | Outils |

## Validation

- [ ] Contrat vérifié
- [ ] Pré/postcondition respectée
- [ ] Invariant préservé

## Références

- **Verse** : VERSES/verses/hoare-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05

