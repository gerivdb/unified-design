# Workflow — Pre-Push Validation

**IntentHash** : `0xWORKFLOW_PRE_PUSH_VALIDATION_20260920`
**Pipeline** : `pipeline-sot-completeness` + `pipeline-yaml-structure-validation`
**Skill** : `pre-push-auditor`
**Gate** : `safe-action-gate`

---

## Déclencheur

Avant tout `git push` touchant un fichier de gouvernance.

## Étapes

### ÉTAPE-1 — Validation YAML
Valider tous les fichiers YAML modifiés.

### ÉTAPE-2 — Safe Action Gate
Vérifier, via `safe-action-gate`, que les préconditions et invariants sont respectés :
- Préconditions : fichiers de gouvernance valides, pas de doublon d'ID
- Invariants : `max_nesting_depth <= 3`, chemins canoniques, consumers non vides
- Preuve horodatée : commit message avec IntentHash référencé

Si le gate retourne `BLOCK` : arrêt immédiat, pas de push.

### ÉTAPE-3 — Vérification champs SOT
Vérifier que tous les champs requis sont présents dans les fichiers SOT.

### ÉTAPE-4 — Correction automatique
Corriger automatiquement les champs manquants déductibles.

### ÉTAPE-5 — Re-validation
Re-valider après correction.

### ÉTAPE-6 — Tests unitaires
Exécuter les tests unitaires governance.

### ÉTAPE-7 — Push
Push vers origin/main si toutes les validations passent.

## Sortie

- Rapport de validation
- Résultat des tests
- Push status
- Rapport Safe Action Gate (ALLOW/BLOCK + horodatage)

## Anti-patterns

- Push sans validation YAML
- Push sans vérification champs SOT
- Push sans passage par Safe Action Gate
- Ignorer les erreurs de validation
