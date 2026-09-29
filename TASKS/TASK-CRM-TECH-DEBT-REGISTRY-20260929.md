---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xTASK_CRM_TECH_DEBT_REGISTRY_20260929
parent_epic: EPIC-CRM-TECH-DEBT-20260929.md
task_id: TASK-CRM-001
priority: P0
assignee: L0-CANON
repo: gerivdb/unified-design
---

# TASK — CRM Tech Debt Registry

## Objectif

Créer `crm/tech_debt_registry.yaml` comme source de vérité de la dette technique cross-repo.

## Critères d’acceptation

1. Registry YAML valide, versionné
2. Structure : repo → items → scoring → statut
3. Compatible avec `auto-design` scoring/génération
4. Exemple de dette pré-rempli

## Livrable

`crm/tech_debt_registry.yaml`

## Références

- **PRD** : `PRD-CRM-TECH-DEBT-20260929.md`
- **MOC** : `MOC-CRM-TECH-DEBT-20260929.md`
