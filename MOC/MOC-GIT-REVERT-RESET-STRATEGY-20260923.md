---
type: MOC
version: "1.0"
date: "2026-09-23"
status: draft
intent_hash: 0xMOC_GIT_REVERT_RESET_STRATEGY_20260923
---

# MOC — Git Revert / Reset Strategy

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23  
**Version** : 1.0 (decision tree revert vs reset, rollback sécurisé)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du design `git-revert-reset-strategy` dans l'écosystème gerivdb.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Design git-revert-reset-strategy | `designs/git-revert-reset-strategy.yaml` | ⏳ À créer | Commit `à commettre` |
| L2 | Atom ATOM-REVERT-RESET-GOVERNANCE | `atoms/methodology/git/ATOM-REVERT-RESET-GOVERNANCE.md` | ⏳ À créer | Commit `à commettre` |
| L3 | Workflow safe-rollback | `workflows/safe-rollback.md` | ⏳ À créer | Commit `à commettre` |
| L4 | PRD-MOC | `PRD/PRD-MOC-GIT-REVERT-RESET-STRATEGY-20260923.md` | ✅ Créé | Commit `à commettre` |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `designs/conflict-resolver-pattern/design.yaml` | pair | Résolution de conflits |
| `workflows/branch-orphan-conflict-resolver.md` | pair | Résurrection branches |
| `atoms/git-remote-safety.yaml` | pair | Remote safety |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Design validé par pre-commit hook | `git commit` | ⏳ En attente |
| **G2** | Atom référencé dans atoms_registry.yaml | `mdu-lint --strict` | ⏳ En attente |
| **G3** | Workflow testé sur repo test | dryrun rollback | ⏳ En attente |

## Critères d'acceptation

- [ ] `designs/git-revert-reset-strategy.yaml` créé et validé YAML
- [ ] `ATOM-REVERT-RESET-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`
- [ ] `workflows/safe-rollback.md` créé
- [ ] MOC `MOC-GIT-REVERT-RESET-STRATEGY-20260923.md` créé
- [ ] Tests : dryrun rollback sur repo test → 0 perte de données, WAL tracé

## Références

- `PRD/PRD-MOC-GIT-REVERT-RESET-STRATEGY-20260923.md` — Spécification
- `designs/conflict-resolver-pattern/design.yaml` — Pattern de résolution
- `atoms/git-remote-safety.yaml` — Remote safety

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création PRD-MOC | 2026-09-23 | `à commettre` | `PRD/PRD-MOC-GIT-REVERT-RESET-STRATEGY-20260923.md` |
| Création MOC | 2026-09-23 | `à commettre` | `MOC/MOC-GIT-REVERT-RESET-STRATEGY-20260923.md` |
