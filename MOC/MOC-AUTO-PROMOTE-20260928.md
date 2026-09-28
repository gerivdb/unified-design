---
type: MOC
version: "1.0.0"
date: "2026-09-28"
status: approved
intent_hash: 0xMOC_AUTO_PROMOTE_20260928
---

# MOC — Auto-Promote

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-28

## Vue d'ensemble

Ce MOC orchestre la promotion automatique des ADR, Designs et INTENTS quand les critères métier sont remplis.

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| `auto_promote.py` | Script | `scripts/auto_promote.py` | ✅ Créé |
| `auto-promotion.yaml` | Politique | `policies/auto-promotion.yaml` | ⏳ À créer |
| Tests | Script | `tests/test_auto_promote.py` | ⏳ À créer |
| Documentation | Doc | `docs/auto-promote.md` | ⏳ À créer |
| Hook pre-commit | Hook | `.kilocode/hooks/pre-commit-auto-promote.py` | ⏳ À créer |

## Séquence d'implémentation

### Phase 1 — Script core (P0)

1. ✅ Créer `scripts/auto_promote.py`
2. Créer `policies/auto-promotion.yaml`
3. Tester dry-run

### Phase 2 — Tests et documentation (P1)

4. Créer `tests/test_auto_promote.py`
5. Créer `docs/auto-promote.md`

### Phase 3 — Intégration CI (P0)

6. Intégrer dans `cross_repo_ci.py`
7. Planifier exécution quotidienne

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Dry-run valide | `python auto_promote.py --dry-run` propose ≥5 promotions | ✅ |
| G2 — Apply sans erreur | `python auto_promote.py --apply` fonctionne | ⏳ En attente |
| G3 — Tests passants | `pytest tests/test_auto_promote.py` passe | ⏳ En attente |
| G4 — Politique respectée | Aucune promotion non autorisée | ⏳ En attente |

## Références

- PRD : `PRD/PRD-MOC-AUTO-PROMOTE-20260928.md`
- Framework : `PRD/PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- CI Pipeline : `PRD/PRD-MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
- Traceability : `PRD/PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY-20260928.md`
