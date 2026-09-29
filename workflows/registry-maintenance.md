---
name: registry-maintenance
description: "Workflow de maintenance automatique des registres d'écosystème : correction des dates, déduplication, validation YAML, et détection du museum effect."
version: "1.0.0"
status: active
---

# Workflow — Registry Maintenance

## Déclencheur

- Début de session multi-repo (BOOT-4)
- Fin de session (BOOT-7)
- Détection `MUSEUM_EFFECT_REGISTRY_STALE` par `dry_run_causal.py`

## Étapes

1. Exécuter `python scripts/fix_registry_dates.py`.
2. Exécuter `python scripts/dry_run_causal.py`.
3. Si `MUSEUM_EFFECT_REGISTRY_STALE` persiste → signaler HITL.
4. Committer les changements avec message conventionnel.

## Critères d'acceptation

- `dry_run_causal.py` retourne `PROD READY 100%`.
- Aucun doublon `full_name` dans `ecosystem_repo_registry.yaml`.
- Tous les `changement_effectif` sont datés de moins de 3 mois.
