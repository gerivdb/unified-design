---
type: MOC
version: "1.0.0"
date: "2026-09-28"
status: approved
intent_hash: 0xMOC_CONSUMER_INTEGRATION_USAGE_20260928
---

# MOC — Consumer Integration Usage

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : approved  
**Date** : 2026-09-28

## Vue d'ensemble

Ce MOC orchestre la documentation et vérification de l'utilisation des modules d'intégration dans le code métier des consumers.

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| Section PRD-MOC | Template | `PRD/PRD-MOC-CONSUMER-INTEGRATION-USAGE-20260928.md` | ✅ Créé |
| `verify_integration_usage.py` | Script | `scripts/verify_integration_usage.py` | ⏳ À créer |
| Mise à jour PRD-MOC consumers | Modification | Consumer repos | ⏳ À faire |

## Séquence d'implémentation

### Phase 1 — Script de vérification (P0)

1. Créer `scripts/verify_integration_usage.py`
2. Tester sur `main`

### Phase 2 — Mise à jour PRD-MOC (P0)

3. Ajouter section "Utilisation dans le code métier" à tous les PRD-MOC consumers

### Phase 3 — Vérification (P1)

4. Exécuter vérification pour tous les consumers

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Script fonctionnel | `python scripts/verify_integration_usage.py --all` passe | ⏳ En attente |
| G2 — PRD-MOC à jour | 126/126 PRD-MOC ont section "Utilisation dans le code métier" | ⏳ En attente |
| G3 — Imports vérifiés | 126/126 modules d'intégration importés dans le code métier | ⏳ En attente |

## Références

- PRD : `PRD/PRD-MOC-CONSUMER-INTEGRATION-USAGE-20260928.md`
- Framework : `PRD/PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- CI Pipeline : `PRD/PRD-MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
- Traceability : `PRD/PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY-20260928.md`
