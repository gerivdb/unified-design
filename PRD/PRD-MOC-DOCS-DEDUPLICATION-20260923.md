---
type: PRD
version: "1.0"
date: "2026-09-23"
status: draft
intent_hash: 0xPRD_MOC_DOCS_DEDUPLICATION_20260923
---

# PRD-MOC — Documentation Deduplication

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23

## Contexte

La documentation présente des doublons identifiés par `detect_duplicate_docs.py` :

### Doublons confirmés (contenu identique)

| Fichier | Statut | Action |
|---------|--------|--------|
| `DESIGNS_GOVERNANCE.md` (racine) | Source de vérité | ✅ Conservé |
| `docs/guides/DESIGNS_GOVERNANCE.md` | Doublon identique | ✅ Supprimé (2026-09-23) |

### Faux doublons (contenu différent)

| Fichier | Statut | Action |
|---------|--------|--------|
| `META-DESIGN.md` (racine) | Source de vérité | ✅ Conservé |
| `docs/META-DESIGN.md` | Export/documentation | ✅ Conservé (référencé par `generator/create_design.py`) |

### Cas légitimes (même nom, contexte différent)

| Fichier | Statut | Action |
|---------|--------|--------|
| `README.md` multiples | Par répertoire | ✅ Conservés (conventions) |
| `design.yaml` dans `designs/*/` | Secondary design files | ✅ Conservés (fallbacks) |

**Impact** : Drift éliminé pour `DESIGNS_GOVERNANCE.md`, liens internes cohérents.

## Mission

Établir une source de vérité unique pour chaque document et supprimer les doublons confirmés.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Choisir source unique | ⭐⭐⭐⭐⭐ | P0 | Minimal | Élimine le drift |
| Supprimer doublons | ⭐⭐⭐⭐⭐ | P0 | Minimal | Nettoie le repo |
| Mettre à jour liens | ⭐⭐⭐⭐ | P1 | Minimal | Garantit la cohérence |

**Verdict** : 2 P0 + 1 P1. Effort minimal, valeur élevée.

## Livrables

1. **Décision** : racine ou `docs/` comme source unique
2. **Script de vérification** — détecte les doublons
3. **Suppression des doublons** — commit atomique

## Critères d'acceptation

- [ ] Chaque document n'existe qu'en un seul exemplaire
- [ ] Liens internes mis à jour

## Références

- `META-DESIGN.md`
- `DESIGNS_GOVERNANCE.md`
- `README.md`
