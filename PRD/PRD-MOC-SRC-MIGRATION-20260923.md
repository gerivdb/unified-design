---
type: PRD
version: "1.0"
date: "2026-09-23"
status: approved
intent_hash: 0xPRD_MOC_SRC_MIGRATION_20260923
---

# PRD-MOC — Src Migration (RSS-v2.3)

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23

## Contexte

Le répertoire `src/` est **vide** (seulement un README). Les moteurs existent à la racine :
- `engine/`, `generator/`, `loop_engine/`, `trix/`, `rlm/`, `piano/`, `llux/`, `gateway/`, `spidx/`, `triade/`, `runners/`, `loops/`

La migration RSS-v2.3 documentée dans `src/README.md` n'est pas réalisée.

## Mission

Migrer progressivement les moteurs vers `src/engines/` et `src/generators/` sans casser les imports existants.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Structure `src/` | ⭐⭐⭐⭐ | P1 | Moyen | Conformité RSS-v2.3 |
| Compatibility layers | ⭐⭐⭐⭐ | P1 | Moyen | Pas de breaking change |
| Migration incrémentale | ⭐⭐⭐ | P2 | Élevé | Par engine, par PRD |

**Verdict** : 2 P1 + 1 P2. Effort moyen, valeur architecturale.

## État d'implémentation (2026-09-30)

| Composant | État | Preuve |
|-----------|------|--------|
| `src/core/__init__.py` | ✅ Créé | Fichier existe |
| `src/engines/auto_design/` | ✅ Migré | 8 modules réexportés vers src/ |
| `src/engines/loop_engine/` | ✅ Migré | graph + detector réexportés |
| `src/engines/validator.py` | ✅ Migré | Réexporté vers src/ |
| `src/generators/create_design.py` | ✅ Migré | Réexporté vers src/ |
| `src/generators/validate_inheritance.py` | ✅ Migré | Réexporté vers src/ |
| Compatibility imports | ✅ Créés | engine/__init__.py, generator/__init__.py, src/engines/* réexports |
| Aucun import cassé | ✅ Vérifié | 52 tests passent, 8 skips |

## Livrables

1. **`src/core/__init__.py`** — package core
2. **`src/engines/<engine>/`** — migration par engine
3. **Compatibility imports** — alias pour ne pas casser les imports existants

## Critères d'acceptation

- [x] `src/` contient au moins `core/`, `engines/`, `generators/` — ATTEINT
- [x] Aucun import cassé après migration d'un engine — ATTEINT (52 tests passent)

## Références

- `src/README.md`
- `REPO.yaml` (rss_depth: 4)
