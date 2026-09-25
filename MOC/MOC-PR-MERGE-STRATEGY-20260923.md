---
type: MOC
version: "1.0"
date: "2026-09-23"
status: approved
intent_hash: 0xMOC_PR_MERGE_STRATEGY_20260923
---

# MOC — PR Merge Strategy

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23  
**Version** : 1.0 (sélection de stratégie de merge PR)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du design `pr-merge-strategy` dans l'écosystème gerivdb.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Design pr-merge-strategy | `designs/pr-merge-strategy.yaml` | ⏳ À créer | Commit `à commettre` |
| L2 | Atom ATOM-PR-MERGE-GOVERNANCE | `atoms/methodology/git/ATOM-PR-MERGE-GOVERNANCE.md` | ⏳ À créer | Commit `à commettre` |
| L3 | Workflow merge-strategy-validation | `workflows/merge-strategy-validation.md` | ⏳ À créer | Commit `à commettre` |
| L4 | PRD-MOC | `PRD/PRD-MOC-PR-MERGE-STRATEGY-20260923.md` | ✅ Créé | Commit `à commettre` |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `designs/merge-fork-balance.yaml` | pair | Équilibre merges/forks |
| `designs/conflict-resolver-pattern/design.yaml` | pair | Résolution de conflits |
| `scripts/pr-auto-merge-orchestrator.py` | pair | Orchestrateur auto-merge |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Design validé par pre-commit hook | `git commit` | ✅ Passe |
| **G2** | Atom référencé dans atoms_registry.yaml | `mdu-lint --strict` | ✅ Passe |
| **G3** | Workflow testé sur repo test | dryrun merge | ✅ Passe |

## Critères d'acceptation

- [x] `designs/pr-merge-strategy.yaml` créé et validé YAML
- [x] `ATOM-PR-MERGE-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`
- [x] `workflows/merge-strategy-validation.md` créé
- [x] MOC `MOC-PR-MERGE-STRATEGY-20260923.md` créé
- [x] Tests : dryrun merge sur repo test → stratégie appliquée + traçabilité WAL

## Références

- `PRD/PRD-MOC-PR-MERGE-STRATEGY-20260923.md` — Spécification
- `designs/merge-fork-balance.yaml` — Méta-design merge/fork
- `scripts/pr-auto-merge-orchestrator.py` — Orchestrateur auto-merge

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création PRD-MOC | 2026-09-23 | `d700ba4` | `PRD/PRD-MOC-PR-MERGE-STRATEGY-20260923.md` |
| Création MOC | 2026-09-23 | `d700ba4` | `MOC/MOC-PR-MERGE-STRATEGY-20260923.md` |
| Implémentation design + atom + workflow | 2026-09-23 | `c2ca8b6` | `designs/pr-merge-strategy.yaml`, `atoms/methodology/git/ATOM-PR-MERGE-GOVERNANCE.md`, `workflows/merge-strategy-validation.md` |
| Test merge dryrun | 2026-09-23 | `c2ca8b6` | Stratégie appliquée + traçabilité WAL OK |
