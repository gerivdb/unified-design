# Workflow — Merge Strategy Validation

**IntentHash** : `0xWORKFLOW_MERGE_STRATEGY_VALIDATION_20260923`  
**Design** : `pr-merge-strategy`  
**Atom** : `ATOM-PR-MERGE-GOVERNANCE`

---

## Déclencheur

Avant tout merge de PR dans l'écosystème gerivdb.

## Étapes

### ÉTAPE-1 — Annotation de stratégie

1. Lire la description de la PR
2. Extraire la stratégie : `/merge-strategy merge|squash|rebase`
3. Si absente → défaut = `merge`

### ÉTAPE-2 — Vérification de la stratégie

| Branche | Commits | Stratégie autorisée |
|---------|---------|---------------------|
| `wip/*` | any | `squash` |
| `feat/*` | < 5 | `squash` autorisé |
| `feat/*` | >= 5 | `merge` |
| `hotfix/*` | any | `merge` |
| Branche partagée | any | `merge` uniquement |

### ÉTAPE-3 — Dryrun pré-merge

1. Vérifier le working tree : `git status --short` → clean
2. Tester le merge : `git merge --no-commit --no-ff <branch>`
3. Compter les conflits : `git diff --name-only --diff-filter=U`
4. Si > 5 conflits → STOP + HITL
5. Abort : `git merge --abort`

### ÉTAPE-4 — Validation taxonomy

1. Vérifier le pattern de branche : `type/jurisdiction-slug-id`
2. Si non conforme → bloquer le merge

### ÉTAPE-5 — Exécution du merge

**Merge commit**
```powershell
git merge --no-ff <branch>
git push origin main
```

**Squash**
```powershell
git merge --squash <branch>
git commit -m "feat: merge <branch> (squash)"
git push origin main
```

### ÉTAPE-6 — Traçabilité

1. Récupérer le SHA : `$mergeSha = git rev-parse HEAD`
2. Logger dans WAL : `Write-WAL "MERGE: strategy=<strategy> sha=$mergeSha branch=<branch> ts=$(Get-Date)"`

### ÉTAPE-7 — Cleanup

1. Supprimer la branche locale : `git branch -d <branch>`
2. Supprimer la branche distante : `git push origin --delete <branch>`

## Sortie

- Rapport de merge
- Stratégie appliquée
- SHA du merge commit
- WAL tracé
- Branche supprimée

## Anti-patterns

- Squash sur branche partagée avec > 5 commits
- Rebase sur branche avec PR ouverte
- Merge sans dryrun
- Merge sans annotation de stratégie
- Oublier le cleanup de branche

## Journalisation

```
[MERGE] strategy=<merge|squash> sha=<sha> branch=<name> wal=<logged> cleanup=<done>
```

## Governance

- **Design** : `designs/pr-merge-strategy.yaml`
- **Atom** : `ATOM-PR-MERGE-GOVERNANCE`
- **ADR** : ADR-014-git-policy, ADR-2026-08-29-001-BRANCH-RESURRECTION-PROTOCOL
