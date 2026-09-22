---
type: MOC
version: "1.0"
date: "2026-09-23"
status: draft
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
| **G1** | Design validé par pre-commit hook | `git commit` | ⏳ En attente |
| **G2** | Atom référencé dans atoms_registry.yaml | `mdu-lint --strict` | ⏳ En attente |
| **G3** | Workflow testé sur branche test | dryrun rebase | ⏳ En attente |

## Critères d'acceptation

- [ ] `designs/git-rebase-workflow.yaml` créé et validé YAML
- [ ] `ATOM-REBASE-WORKFLOW.md` créé et référencé dans `atoms_registry.yaml`
- [ ] `workflows/rebase-validation.md` créé
- [ ] MOC `MOC-GIT-REBASE-WORKFLOW-20260923.md` créé
- [ ] Tests : dryrun rebase sur branche test → 0 conflit non résolu

## Références

- `PRD/PRD-MOC-GIT-REBASE-WORKFLOW-20260923.md` — Spécification
- `designs/conflict-resolver-pattern/design.yaml` — Pattern de résolution
- `workflows/branch-orphan-conflict-resolver.md` — Workflow de résurrection

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création PRD-MOC | 2026-09-23 | `à commettre` | `PRD/PRD-MOC-GIT-REBASE-WORKFLOW-20260923.md` |
| Création MOC | 2026-09-23 | `à commettre` | `MOC/MOC-GIT-REBASE-WORKFLOW-20260923.md` |
