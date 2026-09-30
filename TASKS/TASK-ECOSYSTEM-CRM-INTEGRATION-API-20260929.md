---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xTASK_ECOSYSTEM_CRM_API_20260929
parent_epic: EPIC-ECOSYSTEM-CRM-INTEGRATION-20260929.md
task_id: TASK-ECOSYSTEM-CRM-002
priority: P0
assignee: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Ecosystem CRM Public API

## Objectif

Exposer `_score_tech_debt()` et `generate_crm_tasks()` comme API publique dans `engine/auto_design/`.

## Critères d’acceptation

1. `_score_tech_debt()` dans `analyzer.py` retourne score 0-100
2. `generate_crm_tasks()` dans `generator.py` crée des tickets CRM
3. API documentée, typée
4. Tests unitaires

## Livrable

`engine/auto_design/analyzer.py`, `engine/auto_design/generator.py` modifiés

## Références

- **PRD** : `PRD-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
- **MOC** : `MOC-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
