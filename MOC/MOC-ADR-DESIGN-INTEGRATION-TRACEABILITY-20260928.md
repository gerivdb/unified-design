---
type: MOC
version: "1.0.0"
date: "2026-09-28"
status: approved
intent_hash: 0xMOC_ADR_DESIGN_INTEGRATION_TRACEABILITY_20260928
---

# MOC — ADR-Design-Integration Traceability

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-28

## Vue d'ensemble

Ce MOC orchestre la traçabilité ADR → Design → Consumer → Integration.

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| `adr_design_traceability.py` | Script | `scripts/adr_design_traceability.py` | ⏳ À créer |
| Mise à jour PRD-MOC consumers | Modification | Consumer repos | ⏳ À faire |
| Promotion ADR | Modification | `ADR/` | ⏳ À faire |
| Hook pre-commit traçabilité | Hook | `.kilocode/hooks/pre-commit-traceability.py` | ⏳ À créer |
| Documentation | Doc | `docs/traceability.md` | ⏳ À créer |

## Séquence d'implémentation

### Phase 1 — Script de vérification (P0)

1. Créer `scripts/adr_design_traceability.py`
2. Tester sur `main`

### Phase 2 — Mise à jour PRD-MOC (P0)

3. Mettre à jour 126 PRD-MOC consumers avec `related_adr` valide

### Phase 3 — Promotion ADR (P1)

4. Promouvoir 37 ADR de `proposed` à `accepted`

### Phase 4 — Hook et documentation (P1)

5. Créer hook pre-commit traçabilité
6. Créer documentation

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Script fonctionnel | `python scripts/adr_design_traceability.py --check-all` passe | ⏳ En attente |
| G2 — PRD-MOC à jour | 126/126 PRD-MOC ont `related_adr` valide | ⏳ En attente |
| G3 — ADR promus | 37/37 ADR promus | ⏳ En attente |
| G4 — Hook actif | Pre-commit bloque si traçabilité cassée | ⏳ En attente |

## Références

- PRD : `PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY-20260928.md`
- Registry : `PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md`
- Framework : `PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- CI Pipeline : `PRD-MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
