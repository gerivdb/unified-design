---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-22"
status: proposed
intent_hash: 0xPRD_MOC_BRANCH_TAXONOMY_ENFORCEMENT_20260922
author: gerivdb
source_repo: gerivdb/unified-design
---

# PRD-MOC — Branch Taxonomy Enforcement

> **Périmètre** : détection et blocage pré-push des branches non conformes au pattern `type/jurisdiction-slug-id`.
> **Coordination transverse** : voir ALFRED `multi-repo-governance.yaml` branch_routing.

---

## 1. Objectif

Garantir que toute branche créée dans l'écosystème gerivdb respecte le pattern de taxonomie défini, avant le push.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Design `branch-taxonomy-gate` | `designs/branch-taxonomy-gate.md` | Créé | ✅ |
| L2 | Guard 6 pré-push | `.githooks/pre-push` | Modifier | ✅ |
| L3 | `allowed_branch_prefixes` par repo | `multi-repo-governance.yaml` | Créé | ✅ |
| L4 | MOC orchestration | `MOC/MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922.md` | Créer | ⬜ |

## 3. Tâches

### Phase A — Design

1. **L1** : `designs/branch-taxonomy-gate.md` — documenter le pattern canonique, les règles, et l'application.

### Phase B — Implémentation

2. **L2** : `.githooks/pre-push` — ajouter Guard 6 (validation taxonomie branches) avec blocage et exemptions `main`/`dev`.
3. **L3** : `multi-repo-governance.yaml` — déclarer `allowed_branch_prefixes` par repo.

### Phase C — Orchestration

4. **L4** : `MOC/MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922.md` — créer le MOC d'orchestration.

## 4. Contraintes

- **Pattern canonique** : `type/jurisdiction-slug-id`
- **Exemptions** : `main`, `dev`
- **Blocage** : pré-push uniquement, pas post-push
- **Message d'erreur** : indiquer le pattern attendu et un exemple

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `feat(branch): add branch taxonomy gate design` | `designs/branch-taxonomy-gate.md` | L1 |
| `feat(hooks): add Guard 6 branch taxonomy validation` | `.githooks/pre-push` | L2 |
| `feat(governance): add multi-repo-governance.yaml` | `multi-repo-governance.yaml` | L3 |
| `feat(moc): add branch taxonomy enforcement MOC` | `MOC/MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922.md` | L4 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : hooks pre-commit (`brgs-verify`, `check-yaml`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. `designs/branch-taxonomy-gate.md` créé et validé.
2. Guard 6 dans `.githooks/pre-push` bloque les branches non conformes en pré-push.
3. `multi-repo-governance.yaml` contient `allowed_branch_prefixes` par repo.
4. MOC `MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922.md` créé.

## 8. Proof-of-Life

- [x] 2026-09-22T01:15:20+02:00 — Création PRD-MOC Branch Taxonomy Enforcement
- [x] 2026-09-22T01:15:20+02:00 — Design `branch-taxonomy-gate.md` créé
- [x] 2026-09-22T01:15:20+02:00 — Guard 6 implémenté dans `.githooks/pre-push` (BLOCK + exemptions main/dev)
- [x] 2026-09-22T01:15:20+02:00 — `multi-repo-governance.yaml` créé avec allowed_branch_prefixes
- [x] 2026-09-22T01:15:20+02:00 — MOC `MOC-BRANCH-TAXONOMY-ENFORCEMENT-20260922.md` créé
