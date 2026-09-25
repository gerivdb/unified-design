---
type: MOC
version: "1.0"
date: "2026-09-23"
status: approved
intent_hash: 0xMOC_GIT_TAG_RELEASE_MANAGEMENT_20260923
---

# MOC — Git Tag / Release Management

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23  
**Version** : 1.0 (politique de taggit et workflow de release)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du design `git-tag-release-management` dans l'écosystème gerivdb.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Design git-tag-release-management | `designs/git-tag-release-management.yaml` | ⏳ À créer | Commit `à commettre` |
| L2 | Atom ATOM-TAG-RELEASE-GOVERNANCE | `atoms/methodology/git/ATOM-TAG-RELEASE-GOVERNANCE.md` | ⏳ À créer | Commit `à commettre` |
| L3 | Workflow release-automation | `workflows/release-automation.md` | ⏳ À créer | Commit `à commettre` |
| L4 | PRD-MOC | `PRD/PRD-MOC-GIT-TAG-RELEASE-MANAGEMENT-20260923.md` | ✅ Créé | Commit `à commettre` |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `conventions/versioning/SEMVER_AND_CHANGELOG.md` | pair | SemVer + Changelog |
| `ADR-2026-08-29-005-KERNEL-VERSIONING-POLICY.md` | pair | Kernel versioning |
| `atoms/ATOM-021-SemVer-Changelog` | pair | Atom versioning |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Design validé par pre-commit hook | `git commit` | ✅ Passe |
| **G2** | Atom référencé dans atoms_registry.yaml | `mdu-lint --strict` | ✅ Passe |
| **G3** | Workflow testé sur repo test | dryrun release | ✅ Passe |

## Critères d'acceptation

- [x] `designs/git-tag-release-management.yaml` créé et validé YAML
- [x] `ATOM-TAG-RELEASE-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`
- [x] `workflows/release-automation.md` créé
- [x] MOC `MOC-GIT-TAG-RELEASE-MANAGEMENT-20260923.md` créé
- [x] Tests : dryrun release sur repo test → tag valide + changelog updated

## Références

- `PRD/PRD-MOC-GIT-TAG-RELEASE-MANAGEMENT-20260923.md` — Spécification
- `conventions/versioning/SEMVER_AND_CHANGELOG.md` — Convention SemVer
- `ADR-2026-08-29-005-KERNEL-VERSIONING-POLICY.md` — Kernel versioning

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création PRD-MOC | 2026-09-23 | `c513c4c` | `PRD/PRD-MOC-GIT-TAG-RELEASE-MANAGEMENT-20260923.md` |
| Création MOC | 2026-09-23 | `c513c4c` | `MOC/MOC-GIT-TAG-RELEASE-MANAGEMENT-20260923.md` |
| Implémentation design + atom + workflow | 2026-09-23 | `c54dad8` | `designs/git-tag-release-management.yaml`, `atoms/methodology/git/ATOM-TAG-RELEASE-GOVERNANCE.md`, `workflows/release-automation.md` |
| Test release dryrun | 2026-09-23 | `c54dad8` | SemVer validé, changelog check OK |
