---
type: MOC
version: "1.0"
date: "2026-09-23"
status: approved
intent_hash: 0xMOC_GIT_REBASE_WORKFLOW_20260923
---

# MOC — Git Rebase Workflow

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23  
**Version** : 1.0 (workflow standardisé pour git rebase)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du design `git-rebase-workflow` dans l'écosystème gerivdb.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Design git-rebase-workflow | `designs/git-rebase-workflow.yaml` | ⏳ À créer | Commit `à commettre` |
| L2 | Atom ATOM-REBASE-WORKFLOW | `atoms/methodology/git/ATOM-REBASE-WORKFLOW.md` | ⏳ À créer | Commit `à commettre` |
| L3 | Workflow rebase-validation | `workflows/rebase-validation.md` | ⏳ À créer | Commit `à commettre` |
| L4 | PRD-MOC | `PRD/PRD-MOC-GIT-REBASE-WORKFLOW-20260923.md` | ✅ Créé | Commit `à commettre` |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `designs/conflict-resolver-pattern/design.yaml` | pair | Résolution de conflits |
| `workflows/branch-orphan-conflict-resolver.md` | pair | Résurrection branches |
| `ADR-2026-08-15-003-WIP-BRANCH-WORKFLOW.md` | pair | Stash avant rebase |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Design validé par pre-commit hook | `git commit` | ✅ Passe |
| **G2** | Atom référencé dans atoms_registry.yaml | `mdu-lint --strict` | ✅ Passe |
| **G3** | Workflow testé sur branche test | dryrun rebase | ✅ Passe |

## Critères d'acceptation

- [x] `designs/git-rebase-workflow.yaml` créé et validé YAML
- [x] `ATOM-REBASE-WORKFLOW.md` créé et référencé dans `atoms_registry.yaml`
- [x] `workflows/rebase-validation.md` créé
- [x] MOC `MOC-GIT-REBASE-WORKFLOW-20260923.md` créé
- [x] Tests : dryrun rebase sur branche test → 0 conflit non résolu

## Références

- `PRD/PRD-MOC-GIT-REBASE-WORKFLOW-20260923.md` — Spécification
- `designs/conflict-resolver-pattern/design.yaml` — Pattern de résolution
- `workflows/branch-orphan-conflict-resolver.md` — Workflow de résurrection

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création PRD-MOC | 2026-09-23 | `515cbbd` | `PRD/PRD-MOC-GIT-REBASE-WORKFLOW-20260923.md` |
| Création MOC | 2026-09-23 | `515cbbd` | `MOC/MOC-GIT-REBASE-WORKFLOW-20260923.md` |
| Implémentation design + atom + workflow | 2026-09-23 | `cec35c2` | `designs/git-rebase-workflow.yaml`, `atoms/methodology/git/ATOM-REBASE-WORKFLOW.md`, `workflows/rebase-validation.md` |
| Test rebase dryrun | 2026-09-23 | `b486783` | `feat/test-rebase-workflow-001` (test branch) |
