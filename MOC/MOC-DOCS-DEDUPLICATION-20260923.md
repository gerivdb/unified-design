---
type: MOC
version: "1.0"
date: "2026-09-23"
status: approved
intent_hash: 0xMOC_DOCS_DEDUPLICATION_20260923
---

# MOC — Documentation Deduplication

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-23

## Vue d'ensemble

Ce MOC orchestre la déduplication de la documentation.

## Résultats de l'audit (2026-09-23)

### Doublon confirmé supprimé

| Fichier supprimé | Raison |
|------------------|--------|
| `docs/guides/DESIGNS_GOVERNANCE.md` | Identique à `DESIGNS_GOVERNANCE.md` racine (hash MD5 identique) |
| `docs/guides/` (répertoire) | Répertoire vide après suppression |

### Faux doublons conservés

| Fichier | Raison conservation |
|---------|---------------------|
| `docs/META-DESIGN.md` | Contenu différent de la racine, référencé par `generator/create_design.py` |
| `README.md` multiples | Conventions par répertoire, pas des doublons |

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| Décision source unique | Décision | `README.md` | ✅ Statuée |
| Script de détection | Script | `scripts/detect_duplicate_docs.py` | ✅ Créé |
| Suppression doublons | Action | `docs/guides/DESIGNS_GOVERNANCE.md` | ✅ Réalisé |

## Séquence d'implémentation

### Phase 1 — Décision (P0) — ✅ Réalisé

1. Statuer : racine ou `docs/` comme source unique
2. Documenter la règle dans `DESIGNS_GOVERNANCE.md`

### Phase 2 — Nettoyage (P0) — ✅ Réalisé

3. Créer script de détection de doublons
4. Supprimer les doublons confirmés
5. Vérifier les liens internes

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Décision statuée | Règle documentée | ✅ OK |
| G2 — Doublons supprimés | 0 doublon confirmé restant | ✅ OK |

## Références

- PRD : `PRD-MOC-DOCS-DEDUPLICATION-20260923.md`
- MDU : `DESIGNS_GOVERNANCE.md`
