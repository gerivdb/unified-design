---
type: MOC
version: "1.0"
date: "2026-09-23"
status: approved
intent_hash: 0xMOC_FRONTMATTER_NORMALIZATION_20260923
---

# MOC — Frontmatter Normalization

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-23

## Vue d'ensemble

Ce MOC orchestre la normalisation des frontmatters des designs YAML.

## Résultats (2026-09-23)

| Composant | État | Preuve |
|-----------|------|--------|
| `normalize_frontmatter.py` | ✅ Créé | Audit FAIL count: 0 |
| `fix_missing_intent_hash.py` | ✅ Créé | 36 designs corrigés |
| `clm-pipeline/design.yaml` | ✅ Corrigé | Indentation bridges corrigée |
| `regex-safety-validator/design.yaml` | ✅ Corrigé | Caractères Unicode échappés |

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| `normalize_frontmatter.py` | Script | `scripts/normalize_frontmatter.py` | ✅ Créé |
| `fix_missing_intent_hash.py` | Script | `scripts/fix_missing_intent_hash.py` | ✅ Créé |
| Validation | Gate | `validate_designs.py --strict` | ✅ OK |

## Séquence d'implémentation

### Phase 1 — Audit (P0) — ✅ Réalisé

1. Scanner `designs/**/*.yaml` et identifier les champs manquants
2. Générer rapport d'écarts

### Phase 2 — Correction (P1) — ✅ Réalisé

3. Corriger les frontmatters manquants
4. Valider avec `validate_designs.py --strict`

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Audit complet | 100% designs scannés | ✅ OK |
| G2 — Conformité | `validate_designs.py --strict` passe | ✅ OK (0 FAIL) |

## Références

- PRD : `PRD-MOC-FRONTMATTER-NORMALIZATION-20260923.md`
- MDU : `schemas/design.schema.json`
