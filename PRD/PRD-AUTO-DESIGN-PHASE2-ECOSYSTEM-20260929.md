---
type: PRD
version: "1.0.0"
date: "2026-09-29"
status: draft
intent_hash: 0xPRD_AUTO_DESIGN_PHASE2_ECOSYSTEM_20260929
parent_intent: INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# PRD — Auto-Design Phase 2 : Industrialisation Écosystémique

## Objectif

Étendre le motif auto-design aux repos d'infrastructure et d'orchestration de l'écosystème : NEXUS, CTULU, BRAIN, WAZAA, KG-L, KG-CAUSAL, GATEWAY-MANAGER.

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P0-1 | Industrialisation NEXUS | `designs/nexus/auto-design.yaml` | `verify_repo(NEXUS) >= 80` |
| P0-2 | Industrialisation CTULU | `designs/ctulu/auto-design.yaml` | `verify_repo(CTULU) >= 80` |
| P0-3 | Industrialisation BRAIN | `designs/brain/auto-design.yaml` | `verify_repo(BRAIN) >= 80` |
| P0-4 | Industrialisation WAZAA | `designs/wazaa/auto-design.yaml` | `verify_repo(WAZAA) >= 80` |

### P1 — Important

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P1-1 | Industrialisation KG-L | `designs/kg-l/auto-design.yaml` | `verify_repo(KG-L) >= 80` |
| P1-2 | Industrialisation KG-CAUSAL | `designs/kg-causal/auto-design.yaml` | `verify_repo(KG-CAUSAL) >= 80` |
| P1-3 | Industrialisation GATEWAY-MANAGER | `designs/gateway-manager/auto-design.yaml` | `verify_repo(GATEWAY-MANAGER) >= 80` |

### P2 — Nice-to-have

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P2-1 | Cross-bridges écosystémiques | `bridges/ecosystem-phase2.yaml` | Tous les bridges Phase 2 actifs |
| P2-2 | Rapport global Phase 2 | `reports/auto-design-phase2.json` | 100% couverture |

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

## État actuel (2026-09-29)

### Industrialisations complétées

| Repo | Commit | Score | Mature |
|---|---|---|---|
| NEXUS | `7f6ae0ea` | 80 | ✅ |
| CTULU | `2dacde6a` | 80 | ✅ |
| BRAIN | `84670ea66` | 80 | ✅ |
| WAZAA | `f598619` | 80 | ✅ |
| KG-L | `7fced6d` | 80 | ✅ |
| KG-CAUSAL | `1c6df30` | 80 | ✅ |
| GATEWAY-MANAGER | `f98ac04` | 80 | ✅ |

### Cross-bridges

| Livrable | Statut |
|---|---|
| `bridges/ecosystem-phase2.yaml` | ✅ |
| `reports/auto-design-phase2.json` | ✅ |

## Critères d'Acceptation

1. `auto_design_cli.py verify <repo>` retourne `auto_design_score >= 80` pour tous les repos Phase 2
2. `auto_design_cli.py report --global` montre >= 80% des repos Phase 2 matures
3. Tous les `implementation_contract` sont présents et vérifiés
4. Cross-bridges écosystémiques actifs et médiés

## Références

- **PRD** : `PRD-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **INTENT** : `INTENTS/INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **MOC** : `MOC-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **Intégration** : `docs/auto-design/INTEGRATION-GUIDE.md`
- **Bénéfices** : `docs/auto-design/BENEFITS.md`
