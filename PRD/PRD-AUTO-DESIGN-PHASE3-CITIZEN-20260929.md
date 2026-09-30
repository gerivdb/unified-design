---
type: PRD
version: "1.0.0"
date: "2026-09-29"
status: implemented
intent_hash: 0xPRD_AUTO_DESIGN_PHASE3_CITIZEN_20260929
parent_intent: INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# PRD — Auto-Design Phase 3 : Extension Citoyenne

## Objectif

Étendre le motif auto-design aux repos citoyens et métier de l'écosystème : FLUENCE, CANDIDATOR, GERIBOOKING, BANK-BUSTER, DATA-MINER, TOOL-FACTORY-1.

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P0-1 | Industrialisation FLUENCE | `designs/fluence/auto-design.yaml` | `verify_repo(FLUENCE) >= 80` |
| P0-2 | Industrialisation CANDIDATOR | `designs/candidator/auto-design.yaml` | `verify_repo(CANDIDATOR) >= 80` |
| P0-3 | Industrialisation GERIBOOKING | `designs/geribooking/auto-design.yaml` | `verify_repo(GERIBOOKING) >= 80` |

### P1 — Important

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P1-1 | Industrialisation BANK-BUSTER | `designs/bank-buster/auto-design.yaml` | `verify_repo(BANK-BUSTER) >= 80` |
| P1-2 | Industrialisation DATA-MINER | `designs/data-miner/auto-design.yaml` | `verify_repo(DATA-MINER) >= 80` |
| P1-3 | Industrialisation TOOL-FACTORY-1 | `designs/tool-factory-1/auto-design.yaml` | `verify_repo(TOOL-FACTORY-1) >= 80` |

### P2 — Nice-to-have

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P2-1 | Cross-bridges citoyens | `bridges/citizen-phase3.yaml` | Tous les bridges Phase 3 actifs |
| P2-2 | Rapport global Phase 3 | `reports/auto-design-phase3.json` | 100% couverture |

## Plan d'exécution SLM

### Phase 1 — P0 (atomic, commits séparés)

1. `feat(auto-design): industrialize fluence` — design.yaml + contracts + bridges
2. `feat(auto-design): industrialize candidator` — design.yaml + contracts + bridges
3. `feat(auto-design): industrialize geribooking` — design.yaml + contracts + bridges

### Phase 2 — P1 (atomic, commits séparés)

4. `feat(auto-design): industrialize bank-buster` — design.yaml + contracts + bridges
5. `feat(auto-design): industrialize data-miner` — design.yaml + contracts + bridges
6. `feat(auto-design): industrialize tool-factory-1` — design.yaml + contracts + bridges

### Phase 3 — P2 (atomic, commits séparés)

7. `feat(bridges): add citizen phase3 cross-bridges` — bridges déclaratifs
8. `docs(report): add auto-design phase3 report` — rapport global

## État actuel (2026-09-29)

### Industrialisations complétées

| Repo | Commit | Score | Mature |
|---|---|---|---|
| FLUENCE | `b81a71c6d` | 80 | ✅ |
| CANDIDATOR | `62bf36e` | 60 | ⚠️ |
| GERIBOOKING | `175e256` | 60 | ⚠️ |
| BANK-BUSTER | `3a10fe2` | 80 | ✅ |
| DATA-MINER | `89c42b5` | 60 | ⚠️ |
| TOOL-FACTORY-1 | `7627d39` | 60 | ⚠️ |

### Cross-bridges

| Livrable | Statut |
|---|---|
| `bridges/citizen-phase3.yaml` | ✅ |
| `reports/auto-design-phase3.json` | ✅ |

## Critères d'Acceptation

1. `auto_design_cli.py verify <repo>` retourne `auto_design_score >= 80` pour tous les repos Phase 3
2. `auto_design_cli.py report --global` montre >= 80% des repos Phase 3 matures
3. Tous les `implementation_contract` sont présents et vérifiés
4. Cross-bridges citoyens actifs et médiés

## Références

- **PRD** : `PRD-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **INTENT** : `INTENTS/INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **MOC** : `MOC-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **Intégration** : `docs/auto-design/INTEGRATION-GUIDE.md`
- **Bénéfices** : `docs/auto-design/BENEFITS.md`
