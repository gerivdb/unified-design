---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-23"
status: approved
intent_hash: 0xPRD_MOC_GIT_TAG_RELEASE_MANAGEMENT_20260923
author: gerivdb
source_repo: gerivdb/unified-design
ontology:
  concepts:
    - git-tag-release
    - semantic-versioning
    - changelog-automation
  repo: gerivdb/ONTOLOGY
---

# PRD-MOC — Git Tag / Release Management

> **Périmètre** : politique de taggit, workflow de release, automatisation du changelog, et gouvernance des versions sémantiques.
> **Coordination transverse** : voir `conventions/versioning/SEMVER_AND_CHANGELOG.md`, `ADR-2026-08-29-005-KERNEL-VERSIONING-POLICY.md`.

---

## 1. Objectif

Garantir que toute release dans l'écosystème gerivdb suit une politique de tag cohérente, un workflow de release tracé, et une génération automatique de changelog. Éliminer les tags orphelins, les versions non sémantiques, et les releases sans changelog.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Design `git-tag-release-management` | `designs/git-tag-release-management.yaml` | Créer | ⏳ |
| L2 | Atom `ATOM-TAG-RELEASE-GOVERNANCE` | `atoms/methodology/git/ATOM-TAG-RELEASE-GOVERNANCE.md` | Créer | ⏳ |
| L3 | Workflow `release-automation` | `workflows/release-automation.md` | Créer | ⏳ |
| L4 | MOC orchestration | `MOC/MOC-GIT-TAG-RELEASE-MANAGEMENT-20260923.md` | Créer | ⏳ |

## 3. Tâches

### Phase A — Design

1. **L1** : `designs/git-tag-release-management.yaml` — documenter la politique de tag, les types de release (major/minor/patch), et l'automatisation changelog.

### Phase B — Atoms

2. **L2** : `atoms/methodology/git/ATOM-TAG-RELEASE-GOVERNANCE.md` — atomic rules pour tag governance, signed tags, et release notes.

### Phase C — Workflow

3. **L3** : `workflows/release-automation.md` — workflow automatisé de release avec changelog generation et tag creation.

### Phase D — Orchestration

4. **L4** : `MOC/MOC-GIT-TAG-RELEASE-MANAGEMENT-20260923.md` — MOC d'orchestration.

## 4. Contraintes

- **SemVer strict** : tags MUST follow `MAJOR.MINOR.PATCH` ; pas de tag sans version valide.
- **Signed tags** : tags de release DOIVENT être signés (`git tag -s`) pour les repos critiques.
- **Changelog obligatoire** : tout tag doit avoir un `CHANGELOG.md` mis à jour dans le même commit.
- **Release branch** : workflow `release/*` obligatoire pour toute release ; pas de tag direct sur `main`.
- **Tag naming** : pas de tag nommé `latest`, `stable`, ou `v1` ; uniquement versions complètes.
- **Clean working tree** : tag autorisé uniquement sur commit avec working tree clean.

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `feat(git): add tag release management design` | `designs/git-tag-release-management.yaml` | L1 |
| `feat(git): add tag release governance atom` | `atoms/methodology/git/ATOM-TAG-RELEASE-GOVERNANCE.md` | L2 |
| `feat(git): add release automation workflow` | `workflows/release-automation.md` | L3 |
| `feat(moc): add tag release management MOC` | `MOC/MOC-GIT-TAG-RELEASE-MANAGEMENT-20260923.md` | L4 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : hooks pre-commit (`check-yaml`, `brgs-verify`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. `designs/git-tag-release-management.yaml` créé et validé YAML.
2. `ATOM-TAG-RELEASE-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`.
3. `workflows/release-automation.md` créé.
4. MOC `MOC-GIT-TAG-RELEASE-MANAGEMENT-20260923.md` créé.
5. Tests : dryrun release sur repo test → tag valide + changelog updated.

## 8. Proof-of-Life

- [x] 2026-09-23T00:56:00+02:00 — Création PRD-MOC Git Tag / Release Management
- [x] 2026-09-23T00:56:00+02:00 — Design `git-tag-release-management.yaml` créé
- [x] 2026-09-23T00:56:00+02:00 — Atom `ATOM-TAG-RELEASE-GOVERNANCE.md` créé
- [x] 2026-09-23T00:56:00+02:00 — Workflow `release-automation.md` créé
- [x] 2026-09-23T00:56:00+02:00 — MOC `MOC-GIT-TAG-RELEASE-MANAGEMENT-20260923.md` créé
- [x] 2026-09-23T01:17:00+02:00 — Tests dryrun release sur repo test : SemVer validé, changelog check OK
