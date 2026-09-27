# Workflow — Rebase Validation

**IntentHash** : `0xWORKFLOW_REBASE_VALIDATION_20260923`  
**Design** : `git-rebase-workflow`  
**Atom** : `ATOM-REBASE-WORKFLOW`

---

## Déclencheur

Avant tout `git rebase` sur une branche non triviale.

## Étapes

### ÉTAPE-1 — Décision rebase vs merge

1. Vérifier si la branche est partagée : `git branch -r | grep <branch>`
2. Si partagée → merge obligatoire, STOP.
3. Si locale → continuer.

### ÉTAPE-2 — Backup branch

1. Créer une branche de backup : `git branch backup-<date>-<branch>`
2. Vérifier : `git branch | grep backup`

### ÉTAPE-3 — Pre-rebase validation

1. Vérifier le working tree : `git status --short`
2. Si sale → stash ou commit avant rebase.
3. Vérifier l'historique : `git log --oneline -5`

### ÉTAPE-4 — Exécution rebase

1. Lancer le rebase : `git rebase -i --autosquash <base>`
2. Si conflit :
   - Compter les fichiers en conflit : `git diff --name-only --diff-filter=U`
   - Si > 5 → STOP + HITL
   - Sinon → résoudre avec `git mergetool`
   - Continuer : `git rebase --continue`

### ÉTAPE-5 — Post-rebase validation

1. Vérifier le working tree : `git status --short`
2. Vérifier l'historique : `git log --oneline -5`
3. Vérifier le diff avec main : `git diff main...HEAD --stat`

### ÉTAPE-6 — Cleanup

1. Supprimer la branche de backup : `git branch -d backup-<date>-<branch>`
2. Vérifier : `git branch | grep backup` → doit être vide.

## Sortie

- Rapport de validation
- Résultat du rebase (OK/FAIL)
- Nombre de conflits résolus
- Backup branch supprimée

## Anti-patterns

- Rebase sans backup
- Rebase sur branche partagée
- Rebase avec > 5 conflits sans HITL
- Skip conflit sans inspection
- Supprimer la backup avant validation post-rebase

## Journalisation

```
[REBASE] branch=<name> base=<base> backup=<sha> conflicts=<n> result=<OK|FAIL>
```

## Governance

- **Design** : `designs/git-rebase-workflow.yaml`
- **Atom** : `ATOM-REBASE-WORKFLOW`
- **ADR** : ADR-2026-08-15-003-WIP-BRANCH-WORKFLOW
