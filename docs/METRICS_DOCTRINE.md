---
type: CONVENTION
version: "1.0.0"
date: 2026-08-23
status: accepted
intent_hash: 0xCONV_METRICS_DOCTRINE_20260823
design_id: U-C5
layer: L0
source: Rejet documenté de l'entropie H=0.38 (INTENT V3.0 sections 3.9.1, 3.10.2)
---

# METRICS_DOCTRINE.md — Ce qui fait une métrique de gouvernance légitime

## Principe

> **Une métrique sans origine justifiée est un chiffre magique. Les chiffres magiques
> créent une illusion de contrôle et déplacent le désordre au lieu de le mesurer.**

## Les 4 critères de légitimité

| # | Critère | Question de contrôle |
|---|---------|---------------------|
| M1 | **Actionnable** | Chaque valeur de seuil déclenche-t-elle une action connue et nommée ? |
| M2 | **Déductible** | Se calcule-t-elle depuis les fichiers/états réels, sans registre parallèle ? |
| M3 | **Fondée** | Son origine est-elle justifiable (pourquoi ce seuil, cette formule) ? |
| M4 | **Simple** | Un lecteur peut-il la recalculer à la main sur un petit échantillon ? |

## Cas d'école documenté

| Métrique | M1 | M2 | M3 | M4 | Verdict |
|----------|----|----|----|----|---------|
| Entropie H cible 0.38, alerte 0.43 | ❓ | ❌ registre requis | ❌ « héritée du KG Engine » sans lien | ❌ | **Rejetée** |
| TM (taux de mutation) | ❌ action inconnue | ❌ | ❌ | ❌ | **Rejetée** |
| Score de conformité (violations axiomes, profondeur, frontmatter, cross-refs) | ✅ chaque violation → correction connue | ✅ calculé du filesystem | ✅ dérivé des axiomes | ✅ | **Retenu** |
| MC1-MC6 (compteurs de frictions) | ✅ bloquant/consultatif défini | ✅ scan fichiers | ✅ dérivé des contrôles | ✅ | **Retenu** |

## Garde-fou

Toute proposition de nouvelle métrique de gouvernance passe ce questionnaire avant
implémentation. Une métrique rejetée peut être citée en annexe avec sa raison de rejet —
pour éviter sa redécouverte par une session future enthousiaste (cf. entropie H, réintroduite
deux fois en une session avant filtrage définitif).
