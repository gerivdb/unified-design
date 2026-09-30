---
name: registry-date-fixer
description: "Skill de correction automatique des dates de changement effectif dans les registres d'écosystème. Détecte les repos sans cycle récent, déduplique les entrées, et réécrit le YAML de manière idempotente."
version: "1.0.0"
status: active
---

# Skill — Registry Date Fixer

## Usage

```bash
python scripts/fix_registry_dates.py
```

## Contrat

- Entrée : `RUNTIME/ecosystem_repo_registry.yaml`
- Sortie : YAML valide, dédupliqué, avec `changement_effectif` daté pour les repos cibles.
- Idempotent : exécution répétée ne crée pas de doublons.

## Validation

- `python scripts/validate_designs.py --strict` sur `designs/registry-date-fixer.md`
- `python scripts/dry_run_causal.py` doit retourner `PROD READY 100%`
