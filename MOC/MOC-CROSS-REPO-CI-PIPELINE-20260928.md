---
type: MOC
version: "1.0.0"
date: "2026-09-28"
status: approved
intent_hash: 0xMOC_CROSS_REPO_CI_PIPELINE_20260928
---

# MOC — Cross-Repo CI Pipeline

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-28

## Vue d'ensemble

Ce MOC orchestre l'implémentation du pipeline CI cross-repo pour unified-design.

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| `cross_repo_ci.py` | Script | `scripts/cross_repo_ci.py` | ⏳ À créer |
| `validate-all.sh` | Script | `pipeline/validate-all.sh` | ⏳ À créer |
| `report-generator.py` | Script | `pipeline/report-generator.py` | ⏳ À créer |
| `alert-dispatcher.py` | Script | `pipeline/alert-dispatcher.py` | ⏳ À créer |
| Tests | Script | `tests/test_cross_repo_ci.py` | ⏳ À créer |
| Documentation | Doc | `docs/cross-repo-ci.md` | ⏳ À créer |
| KIVA pipeline | Config | `KIVA-CLI` | ⏳ À activer |

## Séquence d'implémentation

### Phase 1 — Script core (P0)

1. Créer `scripts/cross_repo_ci.py`
2. Créer `pipeline/validate-all.sh`
3. Tester sur `main`

### Phase 2 — Rapports et alertes (P1)

4. Créer `pipeline/report-generator.py`
5. Créer `pipeline/alert-dispatcher.py`

### Phase 3 — Tests et documentation (P1)

6. Créer `tests/test_cross_repo_ci.py`
7. Créer `docs/cross-repo-ci.md`

### Phase 4 — Intégration KIVA-CLI (P0)

8. Activer pipeline KIVA `unified-design-consumers`

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Script fonctionnel | `python scripts/cross_repo_ci.py --all` passe | ⏳ En attente |
| G2 — Rapport généré | Sortie JSON valide | ⏳ En attente |
| G3 — Alertes WAZAA | Message swarm.alert envoyé en cas d'échec | ⏳ En attente |
| G4 — Pipeline KIVA | `kiva pipeline run unified-design-consumers` passe | ⏳ En attente |

## Références

- PRD : `PRD-MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
- Framework : `PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- Registry : `PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md`
