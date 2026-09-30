---
type: ADR
version: "1.0.0"
date: "2026-09-28"
status: proposed
intent_hash: 0xADR_AUTO_PROMOTE_20260928
---

# ADR — Auto-Promote : promotion automatique des documents de gouvernance

## Contexte

L'écosystème `gerivdb/*` accumule des documents de gouvernance en statut `proposed` :
- 37 ADR en `proposed` avec designs intégrés mais non acceptés
- 6 Designs en `proposed`/`draft` fonctionnels mais non promus `active`
- 3 INTENTS en `proposed` avec livrables réalisés mais non approuvés

Cette dette de traçabilité :
- Bloque les audits de conformité
- Empêche la vérification ADR → Design → Code
- Crée de la confusion sur les documents valides

## Problème

1. Aucune mécanique automatique pour promouvoir les documents de gouvernance
2. Les critères de promotion sont connus mais non formalisés
3. Les promotions manuelles sont oubliées ou retardées
4. Aucune preuve horodatée de promotion

## Décision

Introduire le moteur **auto-promote** avec :

1. **`engine/auto_design/auto_promote.py`** : scan + promotion automatique
2. **`designs/auto-promote/*.yaml`** : critères objectifs par type de document
3. **`.kilocode/hooks/pre-commit-auto-promote.py`** : bloque si promotion manquée
4. **`tests/test_auto_promote.py`** : tests unitaires

## Critères de promotion

### ADR
- Status `proposed` + design intégré (tests passants) → `accepted`

### Design
- Status `proposed`/`draft` + ≥1 consumer fonctionnel + tests passants → `active`

### INTENT
- Status `proposed` + Proof-of-Life complet + livrables réalisés → `approved`

## Conséquences

### Positives
- Réduction de la dette de traçabilité
- Audits débloqués
- Vérification ADR → Design → Code automatisée
- Preuve horodatée de promotion

### Négatives
- Surcoût initial : scan de tous les documents
- Risque de faux positifs si critères mal calibrés
- Hook pre-commit peut bloquer le développement

## Alternatives considérées

| Alternative | Raison du rejet |
|---|---|
| Promotion manuelle | Oubli fréquent, pas scalable |
| Script ad-hoc par type | Duplication, pas de critères formalisés |
| Documentation seulement | Pas de enforcement mécanique |
| CI/CD uniquement | Trop tardif, pas de feedback immédiat |

## Références

- **PRD-MOC** : `PRD/PRD-MOC-AUTO-PROMOTE-20260928.md`
- **MOC** : `MOC/MOC-AUTO-PROMOTE-20260928.md`
- **INTENT** : `INTENTS/INTENT-AUTO-PROMOTE-20260928.md`
- **Design** : `designs/auto-promote/`

## Statut

Proposé — implémenté et testé (3 tests passants), prêt pour production.
