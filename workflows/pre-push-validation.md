# Workflow — Pre-Push Validation

**IntentHash** : `0xWORKFLOW_PRE_PUSH_VALIDATION_20260920`
**Pipeline** : `pipeline-sot-completeness` + `pipeline-yaml-structure-validation`
**Skill** : `pre-push-auditor`
**Gates** : `safe-action-gate` + `ecosystem-meta-coherence-gate`

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

### ÉTAPE-3 — Ecosystem Meta-Coherence Gate
Vérifier, via `ecosystem-meta-coherence-gate`, que les invariants écosystémiques sont respectés :
- Think : besoins écosystémiques identifiés (signaux faibles, gaps)
- Do : mutations respectent les invariants cross-repo
- Check : cross-références canoniques, chemins valides
- Preuve horodatée : traçabilité causale, IntentHash référencé

Si le gate retourne `FAIL` : arrêt immédiat, pas de push.

### ÉTAPE-4 — Vérification champs SOT
Vérifier que tous les champs requis sont présents dans les fichiers SOT.

### ÉTAPE-5 — Correction automatique
Corriger automatiquement les champs manquants déductibles.

### ÉTAPE-6 — Re-validation
Re-valider après correction.

### ÉTAPE-7 — Tests unitaires
Exécuter les tests unitaires governance.

### ÉTAPE-8 — Push
Push vers origin/main si toutes les validations passent.

## Sortie

- Rapport de validation
- Résultat des tests
- Push status
- Rapport Safe Action Gate (ALLOW/BLOCK + horodatage)
- Rapport Ecosystem Meta-Coherence Gate (PASS/FAIL + horodatage)

## Anti-patterns

- Push sans validation YAML
- Push sans vérification champs SOT
- Push sans passage par Safe Action Gate
- Push sans passage par Ecosystem Meta-Coherence Gate
- Ignorer les erreurs de validation
