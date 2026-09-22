---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-23"
status: draft
intent_hash: 0xPRD_MOC_PR_MERGE_STRATEGY_20260923
author: gerivdb
source_repo: gerivdb/unified-design
ontology:
  concepts:
    - pr-merge-strategy
    - merge-commit
    - squash-merge
    - rebase-merge
  repo: gerivdb/ONTOLOGY
---

# PRD-MOC — PR Merge Strategy

> **Périmètre** : sélection de la stratégie de merge PR (merge commit, squash, rebase), règles de décision par contexte, et traçabilité du merge.
> **Coordination transverse** : voir `designs/merge-fork-balance.yaml`, `designs/conflict-resolver-pattern/design.yaml`.

---

## 1. Objectif

Garantir que toute PR dans l'écosystème gerivdb est fusionnée avec la stratégie appropriée, documentée, et tracée. Éliminer les merges inconsistants, les histoires polluées, et les pertes de contexte lors de la fusion.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Design `pr-merge-strategy` | `designs/pr-merge-strategy.yaml` | Créer | ⏳ |
| L2 | Atom `ATOM-PR-MERGE-GOVERNANCE` | `atoms/methodology/git/ATOM-PR-MERGE-GOVERNANCE.md` | Créer | ⏳ |
| L3 | Workflow `merge-strategy-validation` | `workflows/merge-strategy-validation.md` | Créer | ⏳ |
| L4 | MOC orchestration | `MOC/MOC-PR-MERGE-STRATEGY-20260923.md` | Créer | ⏳ |

## 3. Tâches

### Phase A — Design

1. **L1** : `designs/pr-merge-strategy.yaml` — documenter les 3 stratégies (merge commit, squash, rebase), les règles de décision, et les cas d'usage.

### Phase B — Atoms

2. **L2** : `atoms/methodology/git/ATOM-PR-MERGE-GOVERNANCE.md` — atomic rules pour sélection de stratégie, validation pre-merge, et traçabilité.

### Phase C — Workflow

3. **L3** : `workflows/merge-strategy-validation.md` — workflow de validation de stratégie avant merge.

### Phase D — Orchestration

4. **L4** : `MOC/MOC-PR-MERGE-STRATEGY-20260923.md` — MOC d'orchestration.

## 4. Contraintes

- **Merge commit par défaut** : stratégie par défaut pour les branches de feature publiques ; preserve l'historique complet.
- **Squash pour WIP** : squash autorisé uniquement pour branches WIP ou `feat/*` avec < 5 commits.
- **Rebase interdit sur PR partagée** : `git rebase` INTERDIT sur une branche avec PR ouverte et reviews.
- **Strategy annotation** : toute PR DOIT avoir la stratégie annotée dans la description (`/merge-strategy merge|squash|rebase`).
- **No merge --no-ff sans reason** : `--no-ff` autorisé uniquement avec justification explicite dans le message de merge.
- **Post-merge cleanup** : suppression automatique de la branche source après merge (sauf WIP).

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `feat(git): add PR merge strategy design` | `designs/pr-merge-strategy.yaml` | L1 |
| `feat(git): add PR merge governance atom` | `atoms/methodology/git/ATOM-PR-MERGE-GOVERNANCE.md` | L2 |
| `feat(git): add merge strategy validation workflow` | `workflows/merge-strategy-validation.md` | L3 |
| `feat(moc): add PR merge strategy MOC` | `MOC/MOC-PR-MERGE-STRATEGY-20260923.md` | L4 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : hooks pre-commit (`check-yaml`, `brgs-verify`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. `designs/pr-merge-strategy.yaml` créé et validé YAML.
2. `ATOM-PR-MERGE-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`.
3. `workflows/merge-strategy-validation.md` créé.
4. MOC `MOC-PR-MERGE-STRATEGY-20260923.md` créé.
5. Tests : dryrun merge sur repo test → stratégie appliquée + traçabilité WAL.

## 8. Proof-of-Life

- [ ] 2026-09-23T00:56:00+02:00 — Création PRD-MOC PR Merge Strategy
- [ ] 2026-09-23T00:56:00+02:00 — Design `pr-merge-strategy.yaml` créé
- [ ] 2026-09-23T00:56:00+02:00 — Atom `ATOM-PR-MERGE-GOVERNANCE.md` créé
- [ ] 2026-09-23T00:56:00+02:00 — Workflow `merge-strategy-validation.md` créé
- [ ] 2026-09-23T00:56:00+02:00 — MOC `MOC-PR-MERGE-STRATEGY-20260923.md` créé
