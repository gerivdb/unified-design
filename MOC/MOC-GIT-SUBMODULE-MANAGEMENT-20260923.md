---
type: MOC
version: "1.0"
date: "2026-09-23"
status: draft
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
| **G1** | Design validé par pre-commit hook | `git commit` | ⏳ En attente |
| **G2** | Atom référencé dans atoms_registry.yaml | `mdu-lint --strict` | ⏳ En attente |
| **G3** | Workflow testé sur repo test | dryrun submodule | ⏳ En attente |

## Critères d'acceptation

- [ ] `designs/git-submodule-management.yaml` créé et validé YAML
- [ ] `ATOM-SUBMODULE-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`
- [ ] `workflows/submodule-sync.md` créé
- [ ] MOC `MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` créé
- [ ] Tests : dryrun submodule add/update/remove sur repo test → 0 divergence

## Références

- `PRD/PRD-MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` — Spécification
- `designs/chain-engineering.yaml` — Méta-design de chaînage
- `atoms/photon-pipeline.yaml` — Submodule TRIX

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création PRD-MOC | 2026-09-23 | `à commettre` | `PRD/PRD-MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` |
| Création MOC | 2026-09-23 | `à commettre` | `MOC/MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` |
