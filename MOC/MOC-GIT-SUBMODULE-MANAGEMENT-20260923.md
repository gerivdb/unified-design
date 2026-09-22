---
type: MOC
version: "1.0"
date: "2026-09-23"
status: approved
intent_hash: 0xMOC_GIT_SUBMODULE_MANAGEMENT_20260923
---

# MOC — Git Submodule Management

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23  
**Version** : 1.0 (lifecycle complet des submodules git)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du design `git-submodule-management` dans l'écosystème gerivdb.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Design git-submodule-management | `designs/git-submodule-management.yaml` | ⏳ À créer | Commit `à commettre` |
| L2 | Atom ATOM-SUBMODULE-GOVERNANCE | `atoms/methodology/git/ATOM-SUBMODULE-GOVERNANCE.md` | ⏳ À créer | Commit `à commettre` |
| L3 | Workflow submodule-sync | `workflows/submodule-sync.md` | ⏳ À créer | Commit `à commettre` |
| L4 | PRD-MOC | `PRD/PRD-MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` | ✅ Créé | Commit `à commettre` |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `designs/chain-engineering.yaml` | pair | Chaîne d'engineering |
| `atoms/photon-pipeline.yaml` | pair | Submodule TRIX |
| `GOVERNANCE-HUB/known_repositories.yaml` | pair | Registre SOT |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Design validé par pre-commit hook | `git commit` | ✅ Passe |
| **G2** | Atom référencé dans atoms_registry.yaml | `mdu-lint --strict` | ✅ Passe |
| **G3** | Workflow testé sur repo test | dryrun submodule | ✅ Passe |

## Critères d'acceptation

- [x] `designs/git-submodule-management.yaml` créé et validé YAML
- [x] `ATOM-SUBMODULE-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`
- [x] `workflows/submodule-sync.md` créé
- [x] MOC `MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` créé
- [x] Tests : dryrun submodule add/update/remove sur repo test → 0 divergence

## Références

- `PRD/PRD-MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` — Spécification
- `designs/chain-engineering.yaml` — Méta-design de chaînage
- `atoms/photon-pipeline.yaml` — Submodule TRIX

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création PRD-MOC | 2026-09-23 | `b3c0d61` | `PRD/PRD-MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` |
| Création MOC | 2026-09-23 | `b3c0d61` | `MOC/MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` |
| Implémentation design + atom + workflow | 2026-09-23 | `8abd885` | `designs/git-submodule-management.yaml`, `atoms/methodology/git/ATOM-SUBMODULE-GOVERNANCE.md`, `workflows/submodule-sync.md` |
| Test submodule dryrun | 2026-09-23 | `8abd885` | add/update/remove OK, 0 divergence |
