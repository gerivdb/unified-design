---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-23"
status: draft
intent_hash: 0xPRD_MOC_GIT_REBASE_WORKFLOW_20260923
author: gerivdb
source_repo: gerivdb/unified-design
ontology:
  concepts:
    - git-rebase-workflow
    - conflict-resolution
    - branch-synchronization
  repo: gerivdb/ONTOLOGY
---

# PRD-MOC — Git Rebase Workflow

> **Périmètre** : workflow standardisé pour `git rebase` (interactive, autosquash, rebase vs merge), résolution de conflits, et synchronisation de branches.
> **Coordination transverse** : voir `designs/conflict-resolver-pattern/design.yaml`, `workflows/branch-orphan-conflict-resolver.md`.

---

## 1. Objectif

Éliminer les frictions et les risques de perte de travail lors des opérations de rebase dans l'écosystème gerivdb. Formaliser le choix rebase vs merge, les étapes de rebase interactif, la résolution de conflits, et le cleanup post-rebase.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Design `git-rebase-workflow` | `designs/git-rebase-workflow.yaml` | Créer | ⏳ |
| L2 | Atom `ATOM-REBASE-WORKFLOW` | `atoms/methodology/git/ATOM-REBASE-WORKFLOW.md` | Créer | ⏳ |
| L3 | Workflow `rebase-validation` | `workflows/rebase-validation.md` | Créer | ⏳ |
| L4 | MOC orchestration | `MOC/MOC-GIT-REBASE-WORKFLOW-20260923.md` | Créer | ⏳ |

## 3. Tâches

### Phase A — Design

1. **L1** : `designs/git-rebase-workflow.yaml` — documenter le workflow rebase, les règles de décision rebase vs merge, et la résolution de conflits.

### Phase B — Atoms

2. **L2** : `atoms/methodology/git/ATOM-REBASE-WORKFLOW.md` — atomic rules pour rebase interactif, autosquash, et conflict resolution.

### Phase C — Workflow

3. **L3** : `workflows/rebase-validation.md` — workflow de validation pre-rebase et post-rebase.

### Phase D — Orchestration

4. **L4** : `MOC/MOC-GIT-REBASE-WORKFLOW-20260923.md` — MOC d'orchestration.

## 4. Contraintes

- **Rebase vs Merge** : rebase autorisé uniquement sur branches locales non partagées ; merge obligatoire pour branches partagées.
- **Conflict limit** : max 5 conflits par rebase, sinon STOP + HITL.
- **Autosquash** : autorisé uniquement avec `--autosquash` et validation préalable du message.
- **Backup** : branche de backup obligatoire avant rebase interactif.
- **Post-rebase** : `git status --short` + `git log --oneline -5` obligatoires après rebase.

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `feat(git): add rebase workflow design` | `designs/git-rebase-workflow.yaml` | L1 |
| `feat(git): add rebase workflow atom` | `atoms/methodology/git/ATOM-REBASE-WORKFLOW.md` | L2 |
| `feat(git): add rebase validation workflow` | `workflows/rebase-validation.md` | L3 |
| `feat(moc): add rebase workflow MOC` | `MOC/MOC-GIT-REBASE-WORKFLOW-20260923.md` | L4 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : hooks pre-commit (`check-yaml`, `brgs-verify`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. `designs/git-rebase-workflow.yaml` créé et validé YAML.
2. `ATOM-REBASE-WORKFLOW.md` créé et référencé dans `atoms_registry.yaml`.
3. `workflows/rebase-validation.md` créé.
4. MOC `MOC-GIT-REBASE-WORKFLOW-20260923.md` créé.
5. Tests : dryrun rebase sur branche test → 0 conflit non résolu.

## 8. Proof-of-Life

- [ ] 2026-09-23T00:56:00+02:00 — Création PRD-MOC Git Rebase Workflow
- [ ] 2026-09-23T00:56:00+02:00 — Design `git-rebase-workflow.yaml` créé
- [ ] 2026-09-23T00:56:00+02:00 — Atom `ATOM-REBASE-WORKFLOW.md` créé
- [ ] 2026-09-23T00:56:00+02:00 — Workflow `rebase-validation.md` créé
- [ ] 2026-09-23T00:56:00+02:00 — MOC `MOC-GIT-REBASE-WORKFLOW-20260923.md` créé
