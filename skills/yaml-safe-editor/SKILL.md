---
name: yaml-safe-editor
description: "Skill d'édition sécurisée des fichiers YAML d'écosystème. Empêche les doublons, garantit l'idempotence, et valide la structure après chaque modification."
version: "1.0.0"
status: active
---

# Skill — YAML Safe Editor

## Usage

```bash
python scripts/fix_registry_dates.py
python scripts/validate_designs.py --strict
```

## Contrat

- Entrée : fichier YAML
- Sortie : YAML valide, dédupliqué, sans champ manquant
- Idempotent : exécution répétée ne crée pas de doublons

## Validation

- `python scripts/validate_designs.py --strict` sur les YAML modifiés
- `python scripts/dry_run_causal.py` doit retourner `PROD READY 100%`
