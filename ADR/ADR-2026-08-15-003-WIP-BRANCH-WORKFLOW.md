---
type: ADR
status: proposed
date: "2026-08-15"
intent_hash: 0xADR_GOVERNANCE_HUB_WIP_BRANCH_WORKFLOW_20260815
author: gerivdb
source_repo: gerivdb/GOVERNANCE-HUB
source_path: ADR/ADR-2026-08-15-003-WIP-BRANCH-WORKFLOW.md
---

# ADR-2026-08-15-003 - WIP Branch Workflow (Stash -> Branch)

## Contexte

L'audit du 2026-08-15 a révélé **13 stashes** dans `gerivdb/GOVERNANCE-HUB`, dont certains datant de plus de 2 mois. L'utilisation de `git stash` comme mécanisme de sauvegarde de WIP a conduit à :

1. 13 stashes orphelins totalisant des heures de travail non documentées
2. `stash@{5}` contenant du travail DUPLIQUÉ déjà présent dans `main`
3. `stash@{8}` contenant des modifications de governance hooks Risky
4. Une perte de temps significative pour l'audit et la classification

## Problème

`git stash` est utilisé comme mécanisme de sauvegarde rapide avant des opérations git risquées (merge, rebase, switch). Mais les stashes sont :
- **Opacques** : pas de message structuré, pas de métadonnées
- **Volatils** : facilement oubliés, pas de rappel automatique
- **Non tracés** : pas d'entrée dans WAL, pas de lien avec la branche source
- **Dangereux** : un `git stash drop` mal placé supprime du travail irrécupérable

## Décision

### Remplacer `git stash` par un workflow `wip-branch`

```
Ancien workflow (dangereux):
  git stash push -m "WIP before risky operation"
  -> stash oublié, pas de traçabilité, risque de perte

Nouveau workflow (sûr):
  git checkout -b wip/session-{session_id}-{date}
  git add -A && git commit -m "wip: session {session_id} checkpoint"
  -> Branche tracée, WAL loggé, récupérable
```

### Règles

| Règle | Description |
|-------|-------------|
| **R-WIP-001** | Interdiction d'utiliser `git stash` pour sauvegarder du WIP avant une opération risquée |
| **R-WIP-002** | Obligation de créer une branche `wip/*` pour tout checkpoint de travail |
| **R-WIP-003** | Les branches `wip/*` doivent être supprimées dans les 7 jours |
| **R-WIP-004** | Tout commit `wip/*` doit être loggé dans le WAL (NEXUS) |
| **R-WIP-005** | Les stashes existants doivent être convertis en branches `wip/*` ou supprimés |

### Implementation

```yaml
# unified-design/atoms/wip-branch-workflow.yaml
name: wip-branch-workflow
version: 1.0.0
rules:
  - id: R-WIP-001
    trigger: git stash push
    action: block_and_suggest_wip_branch
  - id: R-WIP-002
    trigger: pre_risky_operation (merge/rebase/switch)
    action: require_wip_branch_or_commit
  - id: R-WIP-003
    trigger: wip_branch_age > 7d
    action: alert_owner + auto_delete_after_14d
  - id: R-WIP-004
    trigger: wip_branch_commit
    action: log_to_wal_nexus
  - id: R-WIP-005
    trigger: existing_stash
    action: audit_and_convert_or_drop
```

### Git alias

```bash
# Dans ~/.gitconfig
[alias]
    wip = "!f() { git checkout -b wip/$(date +%Y%m%d-%H%M%S) && git add -A && git commit -m \"wip: checkpoint $(date +%Y-%m-%dT%H:%M:%S)\"; }; f"
    wip-done = "!f() { git checkout main && git branch -d $1; }; f"
```

### Skills associés

| Skill | Description |
|-------|-------------|
| `wip-branch-manager` | Automatise la création/suppression des branches WIP |
| `stash-hygiene-auditor` | Audit les stashes existants, propose conversion ou suppression |

### Migration des stashes existants

```powershell
# Script de migration : stash-to-wip-branch.ps1
foreach ($stash in (git stash list)) {
    $stashName = $stash.Split(":")[0]
    $branchName = "wip/migrated-$(Get-Date -Format 'yyyyMMdd-HHmmss')-$($stashName.Replace('stash@{','').Replace('}',''))"
    git stash show -p $stashName | git apply
    git checkout -b $branchName
    git add -A
    git commit -m "wip: migrated from $stashName"
    git stash drop $stashName
}
```

## Conséquences

- **Positif** : Plus de stash oublié, tout WIP est tracé
- **Positif** : Les branches WIP sont visibles dans `git branch`
- **Positif** : WAL loggue automatiquement les commits WIP
- **Négatif** : Plus de branches temporaires (nettoyage automatique requis)
- **Négatif** : Courbe d'apprentissage pour les agents

## Alternatives écartées

| Alternative | Raison |
|-------------|--------|
| Garder `git stash` avec amélioration | Les stashes restent opaques et non tracés |
| `git commit --amend` pour WIP | Risque de réécrire l'historique |
| `git worktree` pour WIP | Overkill pour un simple checkpoint |

## Validation

- **Spécification** : Ce ADR + PRD MOC `PRD-MOC-GOVERNANCE-HUB-GIT-GRAPH-RECOVERY-2026-08-15.md`
- **Preuve** : Session 2026-08-15 - 13 stashes découverts, 12 supprimés, 1 converti en PR
- **RSS-v2.3** : Conforme

## Référence

- **PRD MOC** : `PRD-MOC-GOVERNANCE-HUB-GIT-GRAPH-RECOVERY-2026-08-15.md`
- **IntentHash** : `0xADR_GOVERNANCE_HUB_WIP_BRANCH_WORKFLOW_20260815`
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed

