---
type: EPIC
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xEPIC_CRM_TECH_DEBT_20260929
parent_prd: PRD-CRM-TECH-DEBT-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# EPIC — CRM Tech Debt Management

## Objectif

Livrer un système CRM de gestion de la dette technique intégré à `auto-design`, exploitable par tout l’écosystème `gerivdb`.

## Scope

### P0 — Essentiel

| ID | Livrable | Fichier | Priorité |
|---|---|---|---|
| E1 | Registry dette | `crm/tech_debt_registry.yaml` | P0 |
| E2 | Scoring dette | `engine/auto_design/analyzer.py` | P0 |
| E3 | Génération CRM | `engine/auto_design/generator.py` | P0 |

### P1 — Important

| ID | Livrable | Fichier | Priorité |
|---|---|---|---|
| E4 | Notification | `crm/notifier.py` | P1 |
| E5 | Workflow | `crm/workflow.py` | P1 |
| E6 | Tests | `tests/test_crm_tech_debt.py` | P1 |

## Critères d’Acceptation

1. Registry agrège la dette cross-repo
2. Scoring retourne score 0-100 cohérent
3. Génération crée des tickets CRM exploitables
4. Notification fonctionne vers repos cibles
5. Workflow orchestre détection → scoring → génération → notification
6. Tests : 10/10 passent

## Références

- **PRD** : `PRD-CRM-TECH-DEBT-20260929.md`
- **INTENT** : `INTENT-CRM-TECH-DEBT-20260929.md`
- **ADR** : `ADR-CRM-TECH-DEBT-20260929.md`
