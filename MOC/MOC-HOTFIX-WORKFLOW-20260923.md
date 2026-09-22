---
type: MOC
version: "1.0"
date: "2026-09-23"
status: draft
intent_hash: 0xMOC_HOTFIX_WORKFLOW_20260923
---

# MOC — Hotfix Workflow

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23  
**Version** : 1.0 (workflow de correctif urgent)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du design `hotfix-workflow` dans l'écosystème gerivdb.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Design hotfix-workflow | `designs/hotfix-workflow.yaml` | ⏳ À créer | Commit `à commettre` |
| L2 | Atom ATOM-HOTFIX-GOVERNANCE | `atoms/methodology/git/ATOM-HOTFIX-GOVERNANCE.md` | ⏳ À créer | Commit `à commettre` |
| L3 | Workflow emergency-merge | `workflows/emergency-merge.md` | ⏳ À créer | Commit `à commettre` |
| L4 | PRD-MOC | `PRD/PRD-MOC-HOTFIX-WORKFLOW-20260923.md` | ✅ Créé | Commit `à commettre` |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `ADR-014-git-policy.md` | pair | Politique Git globale |
| `ADR-030-hitl-session-protocol.md` | pair | Protocole HITL hotfix |
| `workflows/branch-orphan-conflict-resolver.md` | pair | Résolution conflits |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Design validé par pre-commit hook | `git commit` | ⏳ En attente |
| **G2** | Atom référencé dans atoms_registry.yaml | `mdu-lint --strict` | ⏳ En attente |
| **G3** | Workflow testé sur repo test | dryrun hotfix | ⏳ En attente |

## Critères d'acceptation

- [ ] `designs/hotfix-workflow.yaml` créé et validé YAML
- [ ] `ATOM-HOTFIX-GOVERNANCE.md` créé et référencé dans `atoms_registry.yaml`
- [ ] `workflows/emergency-merge.md` créé
- [ ] MOC `MOC-HOTFIX-WORKFLOW-20260923.md` créé
- [ ] Tests : dryrun hotfix sur repo test → merge tracé + rollback plan documenté

## Références

- `PRD/PRD-MOC-HOTFIX-WORKFLOW-20260923.md` — Spécification
- `ADR-014-git-policy.md` — Politique Git
- `ADR-030-hitl-session-protocol.md` — Protocole HITL

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création PRD-MOC | 2026-09-23 | `à commettre` | `PRD/PRD-MOC-HOTFIX-WORKFLOW-20260923.md` |
| Création MOC | 2026-09-23 | `à commettre` | `MOC/MOC-HOTFIX-WORKFLOW-20260923.md` |
