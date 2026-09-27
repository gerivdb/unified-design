---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-23"
status: approved
intent_hash: 0xPRD_MOC_GIT_REVERT_RESET_STRATEGY_20260923
author: gerivdb
source_repo: gerivdb/unified-design
ontology:
  concepts:
    - git-revert
    - git-reset
    - rollback-strategy
    - data-loss-prevention
  repo: gerivdb/ONTOLOGY
---

# PRD-MOC — Git Revert / Reset Strategy

> **Périmètre** : decision tree revert vs reset, procédure de rollback sécurisée, et prévention de perte de travail.
> **Coordination transverse** : voir `designs/conflict-resolver-pattern/design.yaml`, `workflows/branch-orphan-conflict-resolver.md`.

---

## 1. Objectif

Éliminer les pertes de travail causées par des commandes git destructives mal utilisées. Formaliser le choix entre `git revert` et `git reset`, les procédures de rollback, et les garde-fous contre la perte de données.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Design `git-revert-reset-strategy` | `designs/git-revert-reset-strategy.yaml` | Créer | ⏳ |
| L2 | Atom `ATOM-REVERT-RESET-GOVERNANCE` | `atoms/methodology/git/ATOM-REVERT-RESET-GOVERNANCE.md` | Créer | ⏳ |
| L3 | Workflow `safe-rollback` | `workflows/safe-rollback.md` | Créer | ⏳ |
| L4 | MOC orchestration | `MOC/MOC-GIT-REVERT-RESET-STRATEGY-20260923.md` | Créer | ⏳ |

## 3. Tâches

### Phase A — Design

1. **L1** : `designs/git-revert-reset-strategy.yaml` — documenter le decision tree revert vs reset, les cas d'usage, et les garde-fous.

### Phase B — Atoms

2. **L2** : `atoms/methodology/git/ATOM-REVERT-RESET-GOVERNANCE.md` — atomic rules pour revert, reset, et data-loss prevention.

### Phase C — Workflow

3. **L3** : `workflows/safe-rollback.md` — workflow de rollback sécurisé avec backup et traçabilité.

### Phase D — Orchestration

4. **L4** : `MOC/MOC-GIT-REVERT-RESET-STRATEGY-20260923.md` — MOC d'orchestration.

## 4. Contraintes

- **Revert par défaut** : `git revert` est la commande par défaut pour annuler un commit public ; `git reset` est INTERDIT sur branches partagées.
- **Reset local only** : `git reset` autorisé UNIQUEMENT sur branches locales non poussées ; jamais sur `main` ou branches partagées.
- **Backup avant reset** :tout `git reset --hard` DOIT être précédé d'un backup (`git branch backup-<date>`) ou d'un stash.
- **Reflog first** : avant toute opération de rollback, vérifier `git reflog` pour identifier le SHA cible.
- **Force push banned** : `git push --force` est INTERDIT après reset ; utiliser `git push --force-with-lease` uniquement.
- **Data loss log** : toute opération de reset ou revert DOIT être tracée dans WAL avec horodatage + SHA avant/après.

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `feat(git): add revert reset strategy design` | `designs/git-revert-reset-strategy.yaml` | L1 |
| `feat(git): add revert reset governance atom` | `atoms/methodology/git/ATOM-REVERT-RESET-GOVERNANCE.md` | L2 |
| `feat(git): add safe rollback workflow` | `workflows/safe-rollback.md` | L3 |
| `feat(moc): add revert reset strategy MOC` | `MOC/MOC-GIT-REVERT-RESET-STRATEGY-20260923.md` | L4 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : hooks pre-commit (`check-yaml`, `brgs-verify`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. `designs/git-revert-reset-strategy.yaml` créé et validé YAML.
2. `ATOM-REVERT-RESET-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`.
3. `workflows/safe-rollback.md` créé.
4. MOC `MOC-GIT-REVERT-RESET-STRATEGY-20260923.md` créé.
5. Tests : dryrun rollback sur repo test → 0 perte de données, WAL tracé.

## 8. Proof-of-Life

- [x] 2026-09-23T00:56:00+02:00 — Création PRD-MOC Git Revert / Reset Strategy
- [x] 2026-09-23T00:56:00+02:00 — Design `git-revert-reset-strategy.yaml` créé
- [x] 2026-09-23T00:56:00+02:00 — Atom `ATOM-REVERT-RESET-GOVERNANCE.md` créé
- [x] 2026-09-23T00:56:00+02:00 — Workflow `safe-rollback.md` créé
- [x] 2026-09-23T00:56:00+02:00 — MOC `MOC-GIT-REVERT-RESET-STRATEGY-20260923.md` créé
- [x] 2026-09-23T01:17:00+02:00 — Tests dryrun rollback sur repo test : 0 perte de données, WAL tracé
