---
type: MOC
version: "1.0.0"
date: "2026-09-29"
status: draft
intent_hash: 0xMOC_AUTO_DESIGN_PHASE3_CITIZEN_20260929
parent_prd: PRD-AUTO-DESIGN-PHASE3-CITIZEN-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# MOC — Auto-Design Phase 3 : Extension Citoyenne

## Objectif

Mettre en œuvre le PRD `PRD-AUTO-DESIGN-PHASE3-CITIZEN-20260929.md` :
- industrialisation de FLUENCE, CANDIDATOR, GERIBOOKING, BANK-BUSTER, DATA-MINER, TOOL-FACTORY-1
- cross-bridges citoyens
- rapport global Phase 3

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P0-1 | Industrialisation FLUENCE | `designs/fluence/auto-design.yaml` | ✅ |
| P0-2 | Industrialisation CANDIDATOR | `designs/candidator/auto-design.yaml` | ❌ chemin non confirmé (L6-WORK) |
| P0-3 | Industrialisation GERIBOOKING | `designs/geribooking/auto-design.yaml` | ❌ absent du SOT local |

### P1 — Important

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P1-1 | Industrialisation BANK-BUSTER | `designs/bank-buster/auto-design.yaml` | ❌ absent du SOT |
| P1-2 | Industrialisation DATA-MINER | `designs/data-miner/auto-design.yaml` | ✅ |
| P1-3 | Industrialisation TOOL-FACTORY-1 | `designs/tool-factory-1/auto-design.yaml` | ✅ |

### P2 — Nice-to-have

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P2-1 | Cross-bridges citoyens | `bridges/citizen-phase3.yaml` | 🔄 |
| P2-2 | Rapport global Phase 3 | `reports/auto-design-phase3.json` | 🔄 |

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

## Critères d'Acceptation

1. `auto_design_cli.py verify <repo>` retourne `auto_design_score >= 80` pour tous les repos Phase 3
2. `auto_design_cli.py report --global` montre >= 80% des repos Phase 3 matures
3. Tous les `implementation_contract` sont présents et vérifiés
4. Cross-bridges citoyens actifs et médiés

## Références

- **PRD** : `PRD-AUTO-DESIGN-PHASE3-CITIZEN-20260929.md`
- **INTENT** : `INTENTS/INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **MOC** : `MOC-AUTO-DESIGN-AUFHEBUNG-20260929.md`
