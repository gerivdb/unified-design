---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M4_GRAY_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M4-GRAY.md
math: M4
persona: gray
inherits:
  - unified-design
---

# ATOM-M4-GRAY - Transactions & ACID

## Rôle

Gray est le **gardien des transactions** dans M4 (Finalité).
Il vérifie que les transactions sont ACID et les données cohérentes.

## Principes

1. **ACID** : Atomicité, Cohérence, Isolation, Durabilité.
2. **Transaction** : Unité de travail.
3. **Commit** : Validation durable.
4. **Rollback** : Annulation.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @acid_tx_v1.0 | Transactions |
| @db_schema_v1.0 | Schéma |

## Repos associés

| Repo | Rôle |
|------|------|
| GERIBOOKING | CRM |
| BANK-BUSTER | Audit |
| NEXUS | Agrégation |

## Validation

- [ ] ACID vérifié
- [ ] Commit réussi
- [ ] Rollback possible

## Références

- **Verse** : VERSES/verses/gray-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05

