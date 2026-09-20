# Workflow — Pre-Push Validation

**IntentHash** : `0xWORKFLOW_PRE_PUSH_VALIDATION_20260920`
**Pipeline** : `pipeline-sot-completeness` + `pipeline-yaml-structure-validation`
**Skill** : `pre-push-auditor`

---

## Déclencheur

Avant tout `git push` touchant un fichier de gouvernance.

## Étapes

### ÉTAPE-1 — Validation YAML
Valider tous les fichiers YAML modifiés.

### ÉTAPE-2 — Vérification champs SOT
Vérifier que tous les champs requis sont présents dans les fichiers SOT.

### ÉTAPE-3 — Correction automatique
Corriger automatiquement les champs manquants déductibles.

### ÉTAPE-4 — Re-validation
Re-valider après correction.

### ÉTAPE-5 — Tests unitaires
Exécuter les tests unitaires governance.

### ÉTAPE-6 — Push
Push vers origin/main si toutes les validations passent.

## Sortie

- Rapport de validation
- Résultat des tests
- Push status

## Anti-patterns

- Push sans validation YAML
- Push sans vérification champs SOT
- Ignorer les erreurs de validation
