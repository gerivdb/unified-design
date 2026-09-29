---
type: MOC
version: "1.0.0"
date: "2026-09-29"
status: draft
intent_hash: 0xMOC_AUTO_DESIGN_PHASE2_ECOSYSTEM_20260929
parent_prd: PRD-AUTO-DESIGN-PHASE2-ECOSYSTEM-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# MOC — Auto-Design Phase 2 : Industrialisation Écosystémique

## Objectif

Mettre en œuvre le PRD `PRD-AUTO-DESIGN-PHASE2-ECOSYSTEM-20260929.md` :
- industrialisation de NEXUS, CTULU, BRAIN, WAZAA, KG-L, KG-CAUSAL, GATEWAY-MANAGER
- cross-bridges écosystémiques
- rapport global Phase 2

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P0-1 | Industrialisation NEXUS | `designs/nexus/auto-design.yaml` | ✅ |
| P0-2 | Industrialisation CTULU | `designs/ctulu/auto-design.yaml` | ✅ |
| P0-3 | Industrialisation BRAIN | `designs/brain/auto-design.yaml` | ✅ |
| P0-4 | Industrialisation WAZAA | `designs/wazaa/auto-design.yaml` | ✅ |

### P1 — Important

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P1-1 | Industrialisation KG-L | `designs/kg-l/auto-design.yaml` | ✅ |
| P1-2 | Industrialisation KG-CAUSAL | `designs/kg-causal/auto-design.yaml` | ✅ |
| P1-3 | Industrialisation GATEWAY-MANAGER | `designs/gateway-manager/auto-design.yaml` | ✅ |

### P2 — Nice-to-have

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P2-1 | Cross-bridges écosystémiques | `bridges/ecosystem-phase2.yaml` | 🔄 |
| P2-2 | Rapport global Phase 2 | `reports/auto-design-phase2.json` | 🔄 |

## Plan d'exécution SLM

### Phase 1 — P0 (atomic, commits séparés)

1. `feat(auto-design): industrialize nexus` — design.yaml + contracts + bridges
2. `feat(auto-design): industrialize ctulu` — design.yaml + contracts + bridges
3. `feat(auto-design): industrialize brain` — design.yaml + contracts + bridges
4. `feat(auto-design): industrialize wazaa` — design.yaml + contracts + bridges

### Phase 2 — P1 (atomic, commits séparés)

5. `feat(auto-design): industrialize kg-l` — design.yaml + contracts + bridges
6. `feat(auto-design): industrialize kg-causal` — design.yaml + contracts + bridges
7. `feat(auto-design): industrialize gateway-manager` — design.yaml + contracts + bridges

### Phase 3 — P2 (atomic, commits séparés)

8. `feat(bridges): add ecosystem phase2 cross-bridges` — bridges déclaratifs
9. `docs(report): add auto-design phase2 report` — rapport global

## Critères d'Acceptation

1. `auto_design_cli.py verify <repo>` retourne `auto_design_score >= 80` pour tous les repos Phase 2
2. `auto_design_cli.py report --global` montre >= 80% des repos Phase 2 matures
3. Tous les `implementation_contract` sont présents et vérifiés
4. Cross-bridges écosystémiques actifs et médiés

## Références

- **PRD** : `PRD-AUTO-DESIGN-PHASE2-ECOSYSTEM-20260929.md`
- **INTENT** : `INTENTS/INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **MOC** : `MOC-AUTO-DESIGN-AUFHEBUNG-20260929.md`
