---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M4_CODD_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M4-CODD.md
math: M4
persona: codd
inherits:
  - unified-design
---

# ATOM-M4-CODD - Relations & Bases de Données

## Rôle

Codd est le **gardien des relations** dans M4 (Finalité).
Il vérifie que les données sont structurées et les requêtes cohérentes.

## Principes

1. **Relation** : Table à attributs.
2. **Clé** : Identifiant unique.
3. **Jointure** : Combinaison de relations.
4. **Normalisation** : Réduction de la redondance.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @db_schema_v1.0 | Schéma |
| @acid_tx_v1.0 | Transactions |

## Repos associés

| Repo | Rôle |
|------|------|
| GERIBOOKING | CRM |
| BANK-BUSTER | Audit |
| NEXUS | Agrégation |

## Validation

- [ ] Schéma cohérent
- [ ] Clé unique vérifiée
- [ ] Jointure correcte

## Références

- **Verse** : VERSES/verses/codd-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05

