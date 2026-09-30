---
name: prd-status-verification-workflow
description: "Workflow qui vérifie la cohérence entre statut PRD/MOC et livrables implémentés. Utilise des checks filesystem avant toute promotion de statut."
version: "1.0.0"
status: active
---

# Workflow — PRD Status Verification

## Déclencheur

- Fin de session multi-repo
- Avant tout commit sur `PRD/`, `MOC/`, `designs/`
- Quand `dry_run_causal.py` signale un gap

## Étapes

1. **Découverte** : lister tous les PRD/MOC non finalisés
2. **Vérification livrables** : pour chaque PRD/MOC, vérifier la présence des chemins déclarés
3. **Évaluation** : si tous les livrables sont présents -> proposer promotion
4. **Validation** : lancer `dry_run_causal.py` + `validate_designs.py --strict`
5. **Commit** : message conventionnel, max 3 fichiers par commit

## Critères d'acceptation

- Aucun PRD/MOC avec statut `proposed`/`draft` dont tous les livrables sont présents
- `dry_run_causal.py` retourne `PROD READY 100%`
- Aucun commit ne contient plus de 3 fichiers modifiés
