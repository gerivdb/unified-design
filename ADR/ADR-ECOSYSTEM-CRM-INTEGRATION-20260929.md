---
type: ADR
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xADR_ECOSYSTEM_CRM_INTEGRATION_20260929
parent_intent: INTENT-ECOSYSTEM-CRM-INTEGRATION-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# ADR — Ecosystem CRM Integration via unified-design

## Contexte

L’écosystème `gerivdb` multi-repo n’a pas de point d’entrée unique pour la gestion de la dette technique. Chaque repo gère sa dette isolément.

## Décision

Utiliser `unified-design` comme registry centralisé et API publique pour la dette technique, avec intégration `ARGUS`/`CTULU`/`KG-L`.

## Options

| # | Option | Description |
|---|---|---|
| 1 | Aucune | Laisser chaque repo gérer sa dette isolément |
| 2 | Registry centralisé dans `unified-design` | Point d’entrée unique, intégration cross-repo |

## Décision

Option 2.

## Conséquences

- `unified-design/crm/` devient le registry de référence
- `engine/auto_design/` expose l’API publique
- `crm/workflow.py` orchestre le cycle complet
- Fallback local si `ARGUS`/`CTULU` indisponibles

## Rationale

- Dette technique multi-repo nécessite une vue agrégée
- `unified-design` est le repo L0-CANON, point d’entrée naturel
- YAML simple, versionné, compatible BDCP

## Références

- **PRD** : `PRD-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
- **INTENT** : `INTENT-ECOSYSTEM-CRM-INTEGRATION-20260929.md`
