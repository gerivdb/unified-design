---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-23"
status: draft
intent_hash: 0xPRD_MOC_HOTFIX_WORKFLOW_20260923
author: gerivdb
source_repo: gerivdb/unified-design
ontology:
  concepts:
    - hotfix-workflow
    - emergency-merge
    - rollback-procedure
  repo: gerivdb/ONTOLOGY
---

# PRD-MOC — Hotfix Workflow

> **Périmètre** : workflow de correctif urgent (`hotfix/*`), merge d'urgence, rollback, et procédure de post-mortem.
> **Coordination transverse** : voir `ADR-014-git-policy.md`, `ADR-030-hitl-session-protocol.md`.

---

## 1. Objectif

Garantir que les correctifs urgents (`hotfix/*`) suivent un workflow sécurisé, tracé, et réversible. Éliminer les merges chaotiques en urgence, les pertes de travail, et les rollbacks non documentés.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Design `hotfix-workflow` | `designs/hotfix-workflow.yaml` | Créer | ⏳ |
| L2 | Atom `ATOM-HOTFIX-GOVERNANCE` | `atoms/methodology/git/ATOM-HOTFIX-GOVERNANCE.md` | Créer | ⏳ |
| L3 | Workflow `emergency-merge` | `workflows/emergency-merge.md` | Créer | ⏳ |
| L4 | MOC orchestration | `MOC/MOC-HOTFIX-WORKFLOW-20260923.md` | Créer | ⏳ |

## 3. Tâches

### Phase A — Design

1. **L1** : `designs/hotfix-workflow.yaml` — documenter le workflow hotfix, les étapes d'urgence, et le rollback.

### Phase B — Atoms

2. **L2** : `atoms/methodology/git/ATOM-HOTFIX-GOVERNANCE.md` — atomic rules pour hotfix creation, merge d'urgence, et rollback.

### Phase C — Workflow

3. **L3** : `workflows/emergency-merge.md` — workflow de merge d'urgence avec validation minimale et traçabilité.

### Phase D — Orchestration

4. **L4** : `MOC/MOC-HOTFIX-WORKFLOW-20260923.md` — MOC d'orchestration.

## 4. Contraintes

- **Hotfix branch** : création obligatoire depuis `main` ; pas de commit direct sur `main`.
- **Emergency merge** : autorisé uniquement avec validation minimale (1 review) et traçabilité WAL.
- **Rollback obligatoire** : tout hotfix merge DOIT avoir un plan de rollback documenté.
- **Post-mortem** : tout hotfix > 2h de résolution DOIT générer un post-mortem dans `incident/`.
- **TTL hotfix** : branche `hotfix/*` DOIT être supprimée dans les 7 jours post-merge.
- **No force push** : hotfix interdit sur branches protégées sans HITL explicite.

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `feat(git): add hotfix workflow design` | `designs/hotfix-workflow.yaml` | L1 |
| `feat(git): add hotfix governance atom` | `atoms/methodology/git/ATOM-HOTFIX-GOVERNANCE.md` | L2 |
| `feat(git): add emergency merge workflow` | `workflows/emergency-merge.md` | L3 |
| `feat(moc): add hotfix workflow MOC` | `MOC/MOC-HOTFIX-WORKFLOW-20260923.md` | L4 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : hooks pre-commit (`check-yaml`, `brgs-verify`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. `designs/hotfix-workflow.yaml` créé et validé YAML.
2. `ATOM-HOTFIX-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`.
3. `workflows/emergency-merge.md` créé.
4. MOC `MOC-HOTFIX-WORKFLOW-20260923.md` créé.
5. Tests : dryrun hotfix sur repo test → merge tracé + rollback plan documenté.

## 8. Proof-of-Life

- [ ] 2026-09-23T00:56:00+02:00 — Création PRD-MOC Hotfix Workflow
- [ ] 2026-09-23T00:56:00+02:00 — Design `hotfix-workflow.yaml` créé
- [ ] 2026-09-23T00:56:00+02:00 — Atom `ATOM-HOTFIX-GOVERNANCE.md` créé
- [ ] 2026-09-23T00:56:00+02:00 — Workflow `emergency-merge.md` créé
- [ ] 2026-09-23T00:56:00+02:00 — MOC `MOC-HOTFIX-WORKFLOW-20260923.md` créé
