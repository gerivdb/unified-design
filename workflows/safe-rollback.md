# Workflow — Safe Rollback

**IntentHash** : `0xWORKFLOW_SAFE_ROLLBACK_20260923`  
**Design** : `git-revert-reset-strategy`  
**Atom** : `ATOM-REVERT-RESET-GOVERNANCE`

---

## Déclencheur

Toute demande de rollback (annulation de commit) dans l'écosystème gerivdb.

## Étapes

### ÉTAPE-1 — Inspection reflog

1. Lister le reflog : `git reflog | tail -20`
2. Identifier le SHA cible : `git reflog | grep <description>`
3. Vérifier le commit : `git show <sha> --stat`

### ÉTAPE-2 — Décision revert vs reset

1. Vérifier si la branche est partagée : `git branch -r | grep <branch>`
2. Si partagée → revert obligatoire
3. Si locale → reset autorisé avec backup

### ÉTAPE-3 — Backup (si reset)

1. Créer une branche de backup : `git branch backup-<date>-<branch>`
2. Vérifier : `git branch | grep backup`

### ÉTAPE-4 — Exécution

**Revert (branche partagée)**
```powershell
git revert <sha>
if ($LASTEXITCODE -ne 0) {
    # Conflit : résoudre ou abandonner
    git revert --abort
    exit 1
}
git push origin main
```

**Reset (branche locale)**
```powershell
git reset --hard <sha>
if ($LASTEXITCODE -ne 0) {
    Write-Error "[ROLLBACK] Reset failed - restore backup"
    git reset --hard backup-<date>-<branch>
    exit 1
}
```

### ÉTAPE-5 — Validation

1. Vérifier le working tree : `git status --short`
2. Vérifier l'historique : `git log --oneline -5`
3. Vérifier le diff : `git diff main...HEAD --stat`

### ÉTAPE-6 — Cleanup

1. Supprimer la branche de backup : `git branch -d backup-<date>-<branch>`
2. Tracer dans WAL : `Write-WAL "ROLLBACK: action=<revert|reset> sha=<sha> result=<OK|FAIL> ts=$(Get-Date)"`

## Sortie

- Rapport de rollback
- Action effectuée (revert/reset)
- SHA du commit annulé
- Backup supprimée (si applicable)
- WAL tracé

## Anti-patterns

- Reset sur branche partagée
- Reset --hard sans backup
- Force push sans --force-with-lease
- Revert sans vérifier le diff
- Ignorer le reflog avant rollback
- Supprimer la backup avant validation

## Journalisation

```
[ROLLBACK] action=<revert|reset> sha=<sha> backup=<sha|null> branch=<name> result=<OK|FAIL>
```

## Governance

- **Design** : `designs/git-revert-reset-strategy.yaml`
- **Atom** : `ATOM-REVERT-RESET-GOVERNANCE`
- **ADR** : ADR-094-git-remote-safety-protocol
