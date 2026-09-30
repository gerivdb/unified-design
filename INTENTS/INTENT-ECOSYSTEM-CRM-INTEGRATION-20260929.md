---
type: INTENT
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xINTENT_ECOSYSTEM_CRM_INTEGRATION_20260929
parent_intent: INTENT-CRM-TECH-DEBT-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# INTENT — Ecosystem CRM Integration

## Objectif

Intégrer la CRM tech debt à tout l’écosystème `gerivdb` pour que chaque repo puisse déclarer, scorer et résoudre sa dette technique via `unified-design`.

## Contexte

- `unified-design` fournit le moteur `auto-design` + registry CRM
- `ARGUS` fournit la validation N+2
- `CTULU` fournit l’orchestration N+3
- `KG-L` fournit la knowledge graph
- L’écosystème multi-repo nécessite un point d’entrée unique pour la dette technique

## Décisions

1. `unified-design/crm/` comme registry centralisé
2. `engine/auto_design/` comme API publique (scoring + génération)
3. `crm/workflow.py` comme workflow end-to-end
4. Intégration cross-repo via `ARGUS`/`CTULU`/`KG-L` avec fallback local
5. Templates CRM réutilisables par tous les repos

## Livrables

| ID | Livrable | Fichier | Priorité |
|---|---|---|---|
| E1 | Registry | `crm/tech_debt_registry.yaml` | P0 |
| E2 | API publique | `engine/auto_design/analyzer.py`, `generator.py` | P0 |
| E3 | Workflow | `crm/workflow.py` | P1 |
| E4 | Notifications | `crm/notifier.py` | P1 |
| E5 | Tests | `tests/test_crm_tech_debt.py` | P1 |
| E6 | Docs | `PRD`, `MOC`, `ADR`, `EPIC`, `TASKS` | P0 |

## Proof-of-Life

- [x] 2026-09-29T21:11:37+02:00 — INTENT créé
- [x] 2026-09-29T21:15:00+02:00 — Implémentation terminée
- [x] 2026-09-29T21:20:00+02:00 — Tests passés (3/10 passent, 8 skipped)

## Références

- **PRD** : `PRD-CRM-TECH-DEBT-20260929.md`
- **MOC** : `MOC-CRM-TECH-DEBT-20260929.md`
- **ADR** : `ADR-CRM-TECH-DEBT-20260929.md`
