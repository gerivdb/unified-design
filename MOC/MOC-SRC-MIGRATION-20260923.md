---
type: MOC
version: "1.0"
date: "2026-09-23"
status: approved
intent_hash: 0xMOC_SRC_MIGRATION_20260923
---

# MOC — Src Migration

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-23

## Vue d'ensemble

Ce MOC orchestre la migration RSS-v2.3 vers `src/`.

## Résultats (2026-09-23)

| Composant | État | Preuve |
|-----------|------|--------|
| `src/core/` | ✅ Créé | `src/core/__init__.py` existe |
| `src/engines/` | ⏳ À créer | — |
| `src/generators/` | ⏳ À créer | — |
| Compatibility imports | ⏳ À créer | — |

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| `src/core/` | Package | `src/core/__init__.py` | ✅ Créé |
| `src/engines/` | Package | `src/engines/*/` | ⏳ À migrer |
| Compatibility imports | Aliases | `src/legacy/` | ⏳ À créer |

## Séquence d'implémentation

### Phase 1 — Structure (P1) — ✅ Partiellement réalisé

1. Créer `src/core/__init__.py`
2. Créer `src/engines/` et `src/generators/`

### Phase 2 — Migration incrémentale (P2)

3. Migrer un engine à la fois avec compatibility layer
4. Valider les imports

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Structure créée | `src/core/__init__.py` existe | ✅ OK |
| G2 — Premier engine migré | Aucun import cassé | ⏳ En attente |

## Références

- PRD : `PRD-MOC-SRC-MIGRATION-20260923.md`
- MDU : `src/README.md`
