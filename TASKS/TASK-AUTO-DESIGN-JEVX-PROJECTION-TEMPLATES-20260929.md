---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P2
intent_hash: 0xTASK_AUTO_DESIGN_JEVX_PROJECTION_TEMPLATES_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — JEVX Projection Templates

## Objectif

Créer les templates de projection JEVX dans `templates/auto_design/jevi_projection/` pour transformer `design.yaml` en formats TALEX/CURX/narratives.

## Périmètre

- **Dossier créé** : `templates/auto_design/jevi_projection/`
- **Fichiers créés** :
  - `templates/auto_design/jevi_projection/talex.j2`
  - `templates/auto_design/jevi_projection/curx.j2`
  - `templates/auto_design/jevi_projection/narrative.j2`
- **Tests** : `tests/test_jevi_projection.py`

## Critères d'acceptation

1. Templates Jinja2 fonctionnels
2. `design.yaml` → TALEX valide
3. `design.yaml` → CURX valide
4. `design.yaml` → Narrative valide
5. Tests passent

## Plan d'exécution

1. Créer le dossier `jevi_projection/`
2. Créer les 3 templates Jinja2
3. Créer un script de projection
4. Tester sur `designs/auto-design/design.yaml`
5. Ajouter tests

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P2-4)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P2-4)
- **JEVX** : mécanisme intégré à CTULU/TALEX
