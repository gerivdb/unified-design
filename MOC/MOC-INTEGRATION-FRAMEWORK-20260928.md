---
type: MOC
version: "1.0.0"
date: "2026-09-28"
status: approved
intent_hash: 0xMOC_INTEGRATION_FRAMEWORK_20260928
---

# MOC — Integration Framework

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-28

## Vue d'ensemble

Ce MOC orchestre le framework d'intégration des designs unified-design dans les consumers.

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| `integration_framework.py` | Module | `tools/integration_framework.py` | ✅ Existe |
| `integration-template.py` | Template | `templates/integration-template.py` | ✅ Créé |
| Tests | Script | `tests/test_integration_framework.py` | ✅ Existe |
| Documentation | Doc | `docs/integration-framework.md` | ✅ Créé |

## Séquence d'implémentation

### Phase 1 — Framework core (P0)

1. ✅ Module `tools/integration_framework.py` existant
2. ✅ Template `templates/integration-template.py` créé
3. ✅ Tests `tests/test_integration_framework.py` existants

### Phase 2 — Documentation (P1)

4. ✅ Documentation `docs/integration-framework.md` créée

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Module fonctionnel | `python -m pytest tests/test_integration_framework.py` passe | ✅ |
| G2 — Template utilisable | Template copié et adapté dans un consumer | ✅ |
| G3 — Documentation complète | `docs/integration-framework.md` présent | ✅ |

## Références

- PRD : `PRD/PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- Registry : `PRD/PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md`
- CI Pipeline : `PRD/PRD-MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
- Traceability : `PRD/PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY-20260928.md`
- Usage : `PRD/PRD-MOC-CONSUMER-INTEGRATION-USAGE-20260928.md`
- Auto-Promote : `PRD/PRD-MOC-AUTO-PROMOTE-20260928.md`
