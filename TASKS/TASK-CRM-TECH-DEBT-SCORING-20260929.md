---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xTASK_CRM_TECH_DEBT_SCORING_20260929
parent_epic: EPIC-CRM-TECH-DEBT-20260929.md
task_id: TASK-CRM-002
priority: P0
assignee: L0-CANON
repo: gerivdb/unified-design
---

# TASK — CRM Tech Debt Scoring

## Objectif

Ajouter `_score_tech_debt()` à `engine/auto_design/analyzer.py` pour scorer la dette 0-100.

## Critères d’acceptation

1. `_score_tech_debt()` prend un item de registry
2. Retourne score 0-100 cohérent
3. Intégré au pipeline `auto_design_readiness`
4. Tests unitaires

## Livrable

`engine/auto_design/analyzer.py` modifié

## Références

- **PRD** : `PRD-CRM-TECH-DEBT-20260929.md`
- **MOC** : `MOC-CRM-TECH-DEBT-20260929.md`
