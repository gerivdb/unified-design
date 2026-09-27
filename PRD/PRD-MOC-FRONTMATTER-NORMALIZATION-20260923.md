---
type: PRD
version: "1.0"
date: "2026-09-23"
status: draft
intent_hash: 0xPRD_MOC_FRONTMATTER_NORMALIZATION_20260923
---

# PRD-MOC — Frontmatter Normalization

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23

## Contexte

Les designs YAML de `designs/` avaient des frontmatters incohérents :
- Champs manquants (`intent_hash`, `layer`, `bridges`)
- Formats mixtes (`design.yaml` sous-dossier vs `.yaml` racine)
- Statuts non harmonisés

**Impact** : Validation schema impossible, traçabilité cassée.

## Mission

Normaliser tous les frontmatters des designs YAML pour garantir la conformité au schéma `schemas/design.schema.json`.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Audit frontmatter | ⭐⭐⭐⭐⭐ | P0 | Minimal | Identifie les gaps |
| Correction automatique | ⭐⭐⭐⭐ | P1 | Minimal | Répandable à 150+ designs |
| Validation post-correction | ⭐⭐⭐⭐⭐ | P0 | Minimal | Garantit la conformité |

**Verdict** : 2 P0 + 1 P1. Effort minimal, valeur élevée.

## État d'implémentation (2026-09-23)

| Composant | État | Preuve |
|-----------|------|--------|
| `scripts/normalize_frontmatter.py` | ✅ Créé | Audit FAIL count: 0 |
| `scripts/fix_missing_intent_hash.py` | ✅ Créé | 36 designs corrigés |
| `designs/clm-pipeline/design.yaml` | ✅ Corrigé | Indentation bridges corrigée |
| `designs/regex-safety-validator/design.yaml` | ✅ Corrigé | Caractères Unicode échappés |
| Validation finale | ✅ OK | `normalize_frontmatter.py` retourne 0 FAIL |

## Livrables

1. **`scripts/normalize_frontmatter.py`** — audit + correction
2. **`scripts/fix_missing_intent_hash.py`** — correction intent_hash manquants
3. **Validation** — `python scripts/validate_designs.py --strict` passe sur tous les designs

## Critères d'acceptation

- [x] 100% des designs ont `intent_hash`, `version`, `status` — ATTEINT (0 FAIL)
- [x] `validate_designs.py --strict` passe sur `designs/` — ATTEINT

## Références

- `schemas/design.schema.json`
- `designs/*.yaml`
- `meta-design.yaml`
