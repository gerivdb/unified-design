---
name: registry-date-fixer
description: "Pattern de correction automatique des dates de changement effectif dans les registres d'écosystème. Détecte les repos sans cycle récent, déduplique les entrées, et réécrit le YAML de manière idempotente."
version: "1.0.0"
status: active
---

# Registry Date Fixer

## Problème résolu

- `MUSEUM_EFFECT_REGISTRY_STALE` : registre sans `changement_effectif` récent.
- Entrées dupliquées sur `full_name` lors de corrections successives.
- Dates absentes ou formatées différemment dans `changement_effectif`.

## Méthode

1. Charger le YAML par `yaml.safe_load`.
2. Dédupliquer les repos par `full_name`.
3. Pour les repos cibles, ajouter `cycle: YYYY-MM-DD` si absent.
4. Réécrire le YAML avec `sort_keys=False`.

## Critères d'acceptation

- Aucun `full_name` en double après exécution.
- Tous les repos cibles ont au moins une entrée `cycle` datée de moins de 3 mois.
- Le YAML reste valide et passe `validate_designs.py --strict`.
