# Workflow — Emergency Merge

**IntentHash** : `0xWORKFLOW_EMERGENCY_MERGE_20260923`  
**Design** : `hotfix-workflow`  
**Atom** : `ATOM-HOTFIX-GOVERNANCE`

---

## Déclencheur

Toute demande de merge d'urgence pour un correctif critique.

## Étapes

### ÉTAPE-1 — Création hotfix branch

1. Vérifier que la branche part de `main` : `git merge-base --is-ancestor main HEAD`
2. Créer la branche : `git checkout -b hotfix/<slug> main`
3. Annoncer la création : `git push -u origin hotfix/<slug>`

### ÉTAPE-2 — Implémentation du fix

1. Implémenter le correctif
2. Commit : `git add -A && git commit -m "fix: <description>"`
3. Push : `git push origin hotfix/<slug>`

### ÉTAPE-3 — Merge d'urgence

1. Vérifier la branche : `git status --short`
2. Merger : `git checkout main && git merge --no-ff hotfix/<slug>`
3. Tracer dans WAL : `Write-WAL "HOTFIX_MERGE: branch=hotfix/<slug> sha=<merge_sha> ts=$(Get-Date)"`
4. Push : `git push origin main`

### ÉTAPE-4 — Documentation rollback

1. Récupérer le SHA du merge : `$mergeSha = git rev-parse HEAD`
2. Créer le plan de rollback : `git revert $mergeSha` (dryrun)
3. Documenter : écrire `rollback-plan-<slug>.md` avec la commande de rollback

### ÉTAPE-5 — Post-mortem (si > 2h)

1. Calculer le temps de résolution : `$resolutionTime = (Get-Date) - $startTime`
2. Si > 2h : générer `incident/post-mortem-<date>.md`
3. Annoter la PR avec le temps de résolution

### ÉTAPE-6 — Cleanup

1. Supprimer la branche locale : `git branch -d hotfix/<slug>`
2. Supprimer la branche distante : `git push origin --delete hotfix/<slug>`
3. Vérifier : `git branch -r | grep hotfix/<slug>` → doit être vide

## Sortie

- Rapport de merge d'urgence
- SHA du merge commit
- Plan de rollback documenté
- Post-mortem généré (si applicable)
- Branche hotfix/* supprimée

## Anti-patterns

- Hotfix créé depuis feature branch
- Merge sans rollback plan
- Branche hotfix/* conservée > 7 jours
- Merge sans WAL trace
- Post-mortem oublié pour hotfix > 2h

## Journalisation

```
[HOTFIX] branch=<name> merge=<sha> rollback=<documented> post_mortem=<generated|skipped> cleanup=<done>
```

## Governance

- **Design** : `designs/hotfix-workflow.yaml`
- **Atom** : `ATOM-HOTFIX-GOVERNANCE`
- **ADR** : ADR-014-git-policy, ADR-030-hitl-session-protocol
