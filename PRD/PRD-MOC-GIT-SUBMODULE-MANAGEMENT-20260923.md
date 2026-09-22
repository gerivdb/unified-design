---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-23"
status: draft
intent_hash: 0xPRD_MOC_GIT_SUBMODULE_MANAGEMENT_20260923
author: gerivdb
source_repo: gerivdb/unified-design
ontology:
  concepts:
    - git-submodule
    - multi-repo-dependency
    - submodule-sync
  repo: gerivdb/ONTOLOGY
---

# PRD-MOC — Git Submodule Management

> **Périmètre** : lifecycle complet des submodules git (add, update, sync, remove), synchronisation cross-repo, et gouvernance des dépendances binaires.
> **Coordination transverse** : voir `atoms/photon-pipeline.yaml`, `designs/chain-engineering.yaml`.

---

## 1. Objectif

Garantir que les submodules git dans l'écosystème gerivdb suivent un lifecycle sécurisé, tracé, et synchronisé. Éliminer les submodules orphelins, les divergences de version, et les dépendances binaires non versionnées.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Design `git-submodule-management` | `designs/git-submodule-management.yaml` | Créer | ⏳ |
| L2 | Atom `ATOM-SUBMODULE-GOVERNANCE` | `atoms/methodology/git/ATOM-SUBMODULE-GOVERNANCE.md` | Créer | ⏳ |
| L3 | Workflow `submodule-sync` | `workflows/submodule-sync.md` | Créer | ⏳ |
| L4 | MOC orchestration | `MOC/MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` | Créer | ⏳ |

## 3. Tâches

### Phase A — Design

1. **L1** : `designs/git-submodule-management.yaml` — documenter le lifecycle submodule, les règles de sync, et la gouvernance des dépendances.

### Phase B — Atoms

2. **L2** : `atoms/methodology/git/ATOM-SUBMODULE-GOVERNANCE.md` — atomic rules pour submodule add, update, sync, remove.

### Phase C — Workflow

3. **L3** : `workflows/submodule-sync.md` — workflow de synchronisation cross-repo des submodules.

### Phase D — Orchestration

4. **L4** : `MOC/MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` — MOC d'orchestration.

## 4. Contraintes

- **Submodule registry** : tout submodule DOIT être enregistré dans `known_repositories.yaml` avant `git submodule add`.
- **Sync obligatoire** : `git submodule update --init --recursive` obligatoire après `git pull` sur repo parent.
- **Version pinning** : submodules DOIVENT être pinnés sur un commit SHA, jamais sur une branche mobile.
- **No submodule in hotpath** : interdiction de submodule dans les chemins critiques (`src/`, `bin/`, `config/`).
- **Remove trace** : suppression de submodule DOIT être tracée dans WAL + mise à jour `.gitmodules`.
- **Cross-repo consistency** : si un submodule est utilisé par > 1 repo, sa version DOIT être synchronisée via release tag.

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `feat(git): add submodule management design` | `designs/git-submodule-management.yaml` | L1 |
| `feat(git): add submodule governance atom` | `atoms/methodology/git/ATOM-SUBMODULE-GOVERNANCE.md` | L2 |
| `feat(git): add submodule sync workflow` | `workflows/submodule-sync.md` | L3 |
| `feat(moc): add submodule management MOC` | `MOC/MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` | L4 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : hooks pre-commit (`check-yaml`, `brgs-verify`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. `designs/git-submodule-management.yaml` créé et validé YAML.
2. `ATOM-SUBMODULE-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`.
3. `workflows/submodule-sync.md` créé.
4. MOC `MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` créé.
5. Tests : dryrun submodule add/update/remove sur repo test → 0 divergence.

## 8. Proof-of-Life

- [ ] 2026-09-23T00:56:00+02:00 — Création PRD-MOC Git Submodule Management
- [ ] 2026-09-23T00:56:00+02:00 — Design `git-submodule-management.yaml` créé
- [ ] 2026-09-23T00:56:00+02:00 — Atom `ATOM-SUBMODULE-GOVERNANCE.md` créé
- [ ] 2026-09-23T00:56:00+02:00 — Workflow `submodule-sync.md` créé
- [ ] 2026-09-23T00:56:00+02:00 — MOC `MOC-GIT-SUBMODULE-MANAGEMENT-20260923.md` créé
