---
type: MOC
version: "1.0"
date: "2026-09-23"
status: approved
intent_hash: 0xMOC_LOCAL_CI_PIPELINE_20260923
---

# MOC — Local CI Pipeline

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-23

## Vue d'ensemble

Ce MOC orchestre l'implémentation du pipeline CI local.

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| `local_ci.py` | Script | `scripts/local_ci.py` | ⏳ À réparer |
| Pre-push hook | Hook | `.githooks/pre-push` | ⏳ À configurer |
| Rapport CI | Sortie | `reports/ci-*.json` | ⏳ À créer |

## Séquence d'implémentation

### Phase 1 — Script core (P0)

1. Réparer `scripts/local_ci.py`
2. Tester sur `main`

### Phase 2 — Intégration (P1)

3. Configurer pre-push hook
4. Ajouter rapport CI

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Script fonctionnel | `python scripts/local_ci.py` passe sur `main` | ⏳ En attente |
| G2 — Hook actif | Pre-push bloque si CI échoue | ⏳ En attente |

## Références

- PRD : `PRD-MOC-LOCAL-CI-PIPELINE-20260923.md`
- MDU : `.pre-commit-config.yaml`
