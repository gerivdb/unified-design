---
type: TASK
version: "1.0.0"
date: "2026-09-29"
status: pending
priority: P0
intent_hash: 0xTASK_AUTO_DESIGN_COMMIT_MESSAGE_GENERATION_20260929
parent_epic: EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
owner: L0-CANON
repo: gerivdb/unified-design
---

# TASK — Commit Message Generation

## Objectif

Ajouter `generate_commit_message()` à `generator.py` pour générer des messages de commit conventionnels standardisés.

## Périmètre

- **Fichier modifié** : `engine/auto_design/generator.py`
- **Dépendance** : Aucune (fonction pure)
- **Tests** : `tests/test_auto_design_argus_ctulu.py::test_commit_message_generation`

## Critères d'acceptation

1. `generate_commit_message(change_type, scope, description)` retourne `str`
2. Format : `{type}({scope}): {description}`
3. `change_type` valide : `feat|fix|docs|test|refactor|chore|ci|build|revert|style|perf`
4. `scope` optionnel (si vide, pas de parenthèses)
5. Test unitaire passe

## Plan d'exécution

1. Ajouter méthode `generate_commit_message()` à `AutoDesignGenerator`
2. Valider `change_type` contre la liste des types autorisés
3. Formater le message selon conventional commits
4. Ajouter test unitaire

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P0-3)
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` (P0-3)
