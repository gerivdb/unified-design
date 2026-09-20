# Workflow — Branch Orphan Conflict Resolver

**IntentHash** : `0xWORKFLOW_BRANCH_ORPHAN_CONFLICT_RESOLVER_20260920`
**Skill** : `branch-orphan-conflict-resolver`
**Design** : `branch-orphan-conflict-resolver`

---

## Déclencheur

- Détection d'une branche orpheline (supprimée, non mergée)
- Conflit git lors d'un merge
- Fin de session KiloCode (PR_LIFECYCLE_GATE)
- BOOT-3 / BOOT-3bis (audit de branches)

## Étapes

### ÉTAPE-1 — Détection

1. Exécuter `git reflog | grep -i "deleted\|pruned\|branch"`
2. Lister les branches distantes mergées dans main sans PR ouverte
3. Identifier les branches orphelines

**Sortie** : liste des SHA et branches orphelines

### ÉTAPE-2 — Analyse de saturation

1. Comparer les commits uniques: `git log main..<branch> --oneline`
2. Vérifier les fichiers clés sur main: `git ls-tree -r main -- <fichier>`
3. Calculer le taux de recouvrement

**Décision** :
- > 80% overlap → absorption main
- < 20% overlap → resurrection + merge
- 20-80% overlap → cherry-pick manuel

### ÉTAPE-3 — Résurrection (si applicable)

1. `git branch <name> <sha>`
2. Vérifier: `git branch -a | grep <name>`
3. Tester le merge: `git checkout main && git merge --no-commit --no-ff <branch>`
4. Analyser les conflits: `git status -s`

### ÉTAPE-4 — Résolution de conflits

| Stratégie | Condition | Action |
|-----------|-----------|--------|
| Main authority | Contenu canonique sur main | `git show main:<file> > <file>` |
| Cherry-pick | Commits spécifiques utiles | `git cherry-pick <sha>` |
| Manual | Conflit complexe | Résolution manuelle HITL |

### ÉTAPE-5 — Finalisation

1. `git add <fichiers>`
2. `git commit -m "merge: integrate <branch> into main"`
3. `git push origin main`

### ÉTAPE-6 — Nettoyage

1. `git branch -d <branch>`
2. `git push origin --delete <branch>`
3. Mettre à jour le rapport de session

## Sortie

- `reports/branch-orphan-resolution-*.md` : rapport Markdown
- `reports/branch-orphan-resolution-*.json` : rapport JSON
- Preuves horodatées dans VOLTX

## Journalisation

```
[RESURRECTION] repo=<REPO> branch=<NOM> sha=<SHA>
[RESURRECTION] phase=diagnostic commits=<N> fichiers_ajoutes=<M>
[RESURRECTION] phase=merge_test conflits=<N> resolution=<main_authority|manual>
[RESURRECTION] phase=merge commit=<SHA> push=<OK|FAIL>
[RESURRECTION] phase=cleanup local_deleted=<OK|SKIP> remote_deleted=<OK|SKIP>
```

## Anti-patterns

- Supprimer une branche sans vérifier `git reflog` d'abord
- Déclarer "perdu" sans avoir tenté la resurrection
- Merge force sans test `--no-commit --no-ff`
- Résoudre les conflits en gardant la version feature quand main a le contenu canonique
- Ignorer les branches orphelines en fin de session

## Governance

- **ADR** : ADR-2026-08-28-001-BRANCH-RESURRECTION-PROTOCOL
- **Design** : branch-orphan-conflict-resolver
- **Atom** : ATOM-053-workspace-draft-convention
- **Workflow** : dryrun-causal-audit
