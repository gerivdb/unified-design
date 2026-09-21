---
type: MOC
version: "1.0"
date: "2026-09-22"
status: in_review
intent_hash: 0xMOC_BRANCH_TAXONOMY_ENFORCEMENT_20260922
---

# MOC — Branch Taxonomy Enforcement

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : proposed  
**Date** : 2026-09-22  
**Version** : 1.0 (détection pré-push branches non conformes)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration du design `branch-taxonomy-gate` dans l'écosystème gerivdb.

## Livrables

| # | Livrable | Chemin cible | Statut | Preuve d'exécution |
|---|----------|--------------|--------|-------------------|
| L1 | Design branch taxonomy gate | `designs/branch-taxonomy-gate.md` | ✅ Créé | Commit `à commettre` |
| L2 | Guard 6 pré-push | `.githooks/pre-push.ps1` | ✅ Fait | Commit `6e8955e` |
| L3 | `allowed_branch_prefixes` par repo | `multi-repo-governance.yaml` | ✅ Fait | Commit `6e8955e` |
| L4 | PRD-MOC | `PRD/PRD-MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922.md` | ✅ Fait | Commit `dbb659e` |

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `designs/branch-taxonomy-gate.md` | pair | Design source |
| `.githooks/pre-push.ps1` | pair | Hook existant |
| `multi-repo-governance.yaml` | pair | Configuration ALFRED |
| `GOVERNANCE-HUB/known_repositories.yaml` | pair | Liste repos |

## Gates et critères d'acceptation

| Gate | Critère formel | Validation | Statut |
|------|---------------|------------|--------|
| **G1** | Design validé par pre-commit hook | `git commit` | ✅ Passe |
| **G2** | Guard 6 bloque branches non conformes | Test pré-push | ✅ Fait |
| **G3** | `allowed_branch_prefixes` déclaré par repo | `multi-repo-governance.yaml` | ✅ Fait |

## Critères d'acceptation

- [x] `designs/branch-taxonomy-gate.md` créé
- [x] Guard 6 bloque branches non conformes en pré-push (`.githooks/pre-push` ÉTAPE 3)
- [x] `multi-repo-governance.yaml` contient `allowed_branch_prefixes` par repo
- [x] PRD-MOC `PRD-MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922.md` créé

## Références

- `designs/branch-taxonomy-gate.md` — Design source
- `PRD/PRD-MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922.md` — Spécification
- `GATES_HIERARCHIQUES.md` — Principes G3 et G7
- `multi-repo-governance.yaml` — Configuration ALFRED

## Preuves d'exécution

| Action | Date | Commit | Référence |
|--------|------|--------|-----------|
| Création design | 2026-09-22 | `9f211a2` | `designs/branch-taxonomy-gate.md` |
| Création PRD-MOC | 2026-09-22 | `dbb659e` | `PRD/PRD-MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922.md` |
| Création MOC | 2026-09-22 | `6f025d2` | `MOC/MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922.md` |
| Implémentation Guard 6 | 2026-09-22 | `6e8955e` | `.githooks/pre-push` |
| Création multi-repo-governance.yaml | 2026-09-22 | `6e8955e` | `multi-repo-governance.yaml` |
