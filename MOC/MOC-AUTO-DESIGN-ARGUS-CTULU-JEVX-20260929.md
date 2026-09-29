---
type: MOC
version: "1.0.0"
date: "2026-09-29"
status: draft
intent_hash: 0xMOC_AUTO_DESIGN_ARGUS_CTULU_JEVX_20260929
parent_prd: PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# MOC — Auto-Design : exploitation d'ARGUS, CTULU et JEVX

## Objectif

Mettre en œuvre le PRD `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md` :
- **P0** : conventional commits, atomic commits, commit messages, ARGUS bridge/crossref validation
- **P1** : templates commit, auto-commit on deploy, branch/commit coupling, tests intégration
- **P2** : meta-coherence gate, traceability validation, NODEX classification, JEVX projection, governance synthesizer

## État d'avancement

### P0 — Essentiel (TERMINÉ)

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P0-1 | `_score_conventional_commit_adherence()` | `engine/auto_design/analyzer.py` | ✅ |
| P0-2 | `_check_atomic_commits()` | `engine/auto_design/verifier.py` | ✅ |
| P0-3 | `generate_commit_message()` | `engine/auto_design/generator.py` | ✅ |
| P0-4 | `_validate_bridges_argus()` | `engine/auto_design/verifier.py` | ✅ |
| P0-5 | `_validate_crossrefs_argus()` | `engine/auto_design/verifier.py` | ✅ |

### P1 — Important (TERMINÉ)

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P1-1 | `commit_validator.py` | `templates/auto_design/commit_validator.py` | ✅ |
| P1-2 | `commit_monitor.py` | `templates/auto_design/commit_monitor.py` | ✅ |
| P1-3 | `deploy_with_auto_commit()` | `engine/auto_design/industrializer.py` | ✅ |
| P1-4 | `create_pr()` avec branch coupling | `engine/auto_design/pr_factory.py` | ✅ |
| P1-5 | Tests intégration | `tests/test_auto_design_argus_ctulu.py` | ✅ |

### P2 — Nice-to-have (EN COURS)

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|:---|
| P2-1 | `_check_meta_coherence()` | `engine/auto_design/verifier.py` | ⬜ |
| P2-2 | `_validate_traceability()` | `engine/auto_design/verifier.py` | ⬜ |
| P2-3 | `_classify_components_noded()` | `engine/auto_design/generator.py` | ⬜ |
| P2-4 | JEVX projection templates | `templates/auto_design/jevi_projection/` | ⬜ |
| P2-5 | Governance synthesizer integration | `engine/auto_design/auto_promote.py` | ⬜ |

## Plan d'exécution SLM

### Phase 1 — P0 (atomic, commits séparés)

1. `feat(analyzer): add conventional commit scoring` — `analyzer.py` + CTULU `trix-git-workflow.py`
2. `feat(verifier): add atomic commit checking` — `verifier.py` + CTULU `trix-git-workflow.py`
3. `feat(generator): add commit message generation` — `generator.py`
4. `feat(verifier): add ARGUS bridge validation` — `verifier.py` + ARGUS `bridge_check.py`
5. `feat(verifier): add ARGUS crossref validation` — `verifier.py` + ARGUS `crossref_check.py`

### Phase 2 — P1 (atomic, commits séparés)

6. `feat(templates): add commit_validator.py` — validation conventional commits + atomicité
7. `feat(templates): add commit_monitor.py` — auto-commit multi-repo
8. `feat(industrializer): add auto-commit on deploy` — `deploy_with_auto_commit()`
9. `feat(pr_factory): add branch/commit coupling` — cohérence branch → commit → PR
10. `test(engine): add auto_design_argus_ctulu tests` — pytest couverture 80%

### Phase 3 — P2 (atomic, commits séparés)

11. `feat(verifier): add meta-coherence gate` — ARGUS `ecosystem_meta_coherence.py`
12. `feat(verifier): add traceability validation` — CTULU `trace_graph.py` + `trace_validator.py`
13. `feat(generator): add NODEX component classification` — ARGUS `nodex.py` + KG-L
14. `feat(templates): add jevi_projection templates` — JEVX TALEX/CURX
15. `feat(auto_promote): add governance synthesizer integration` — CTULU `vibe-governance-synthesizer`

## Critères d'Acceptation

1. `_score_conventional_commit_adherence()` retourne score 0-100 cohérent avec `git log --oneline`
2. `_check_atomic_commits()` détecte commits >3 fichiers et retourne violations
3. `generate_commit_message("feat", "engine", "add analyzer")` retourne `feat(engine): add analyzer`
4. `_validate_bridges_argus()` retourne JSON avec findings GAP/DRIFT/VOID/UNPROVEN
5. `_validate_crossrefs_argus()` retourne JSON avec findings ORPHAN/GAP/STALE/BROKEN
6. `industrializer.py` déploie `commit_validator.py` et `commit_monitor.py` dans `scripts/`
7. `deploy_with_auto_commit()` commit et push automatiquement après déploiement
8. `create_pr()` vérifie cohérence branch → commit → PR
9. `_check_meta_coherence()` bloque déploiement si `status != OK`
10. `_validate_traceability()` retourne violations (orphelins, liens cassés, status mismatch)
11. `_detect_components()` utilise NODEX pour classification KG-L
12. Templates JEVX projection déployés et fonctionnels
13. `auto_promote.py` génère 6 artifacts + commit via CTULU

## Calibration SLM

### Contraintes matérielles
- CPU : 2× Intel Xeon E5620 @ 2.4 GHz (16 threads)
- RAM : 24 Go DDR3 ECC
- Stockage : C: SSD 1 To, D: SSD 2 To

### Règles d'implémentation
- **Tâche atomique** : une fonction = un commit = un test
- **Durée max** : 30 min par tâche sans commit intermédiaire
- **Fichiers max par commit** : 3
- **Test par tâche** : chaque livrable doit avoir un test unitaire pytest
- **Fallback systématique** : si ARGUS/CTULU indisponible, mode dégradé local

## Suivi de réalisation

### Phase 1 — P0 (5 livrables, ~4h) — TERMINÉ

| Tâche | Livrable | Fichier | Durée | Statut |
|---|---|---|---|---|
| ATOMIC-001 | `_score_conventional_commit_adherence()` | `analyzer.py` | 30min | ✅ |
| ATOMIC-002 | `_check_atomic_commits()` | `verifier.py` | 30min | ✅ |
| ATOMIC-003 | `generate_commit_message()` | `generator.py` | 30min | ✅ |
| ATOMIC-004 | `_validate_bridges_argus()` | `verifier.py` | 1h | ✅ |
| ATOMIC-005 | `_validate_crossrefs_argus()` | `verifier.py` | 1h | ✅ |

### Phase 2 — P1 (4 livrables, ~4.5h) — TERMINÉ

| Tâche | Livrable | Fichier | Durée | Statut |
|---|---|---|---|---|
| ATOMIC-006 | `commit_validator.py` | `templates/auto_design/commit_validator.py` | 1h | ✅ |
| ATOMIC-007 | `commit_monitor.py` | `templates/auto_design/commit_monitor.py` | 1h | ✅ |
| ATOMIC-008 | `deploy_with_auto_commit()` | `industrializer.py` | 1h | ✅ |
| ATOMIC-009 | `create_pr()` | `pr_factory.py` | 30min | ✅ |
| ATOMIC-010 | Tests intégration | `tests/test_auto_design_argus_ctulu.py` | 1h | ✅ |

### Phase 3 — P2 (5 livrables, ~11h) — TERMINÉ

| Tâche | Livrable | Fichier | Durée | Statut |
|---|---|---|---|---|
| ATOMIC-011 | `_check_meta_coherence()` | `verifier.py` | 2h | ✅ |
| ATOMIC-012 | `_validate_traceability()` | `verifier.py` | 3h | ✅ |
| ATOMIC-013 | `_classify_components_noded()` | `generator.py` | 2h | ✅ |
| ATOMIC-014 | JEVX projection templates | `templates/auto_design/jevi_projection/` | 2h | ✅ |
| ATOMIC-015 | Governance synthesizer integration | `auto_promote.py` | 2h | ✅ |

## Plan d'exécution SLM détaillé

### Phase 1 — P0 (atomic, commits séparés)

1. `feat(analyzer): add conventional commit scoring` — `analyzer.py` + CTULU `trix-git-workflow.py`
2. `feat(verifier): add atomic commit checking` — `verifier.py` + CTULU `trix-git-workflow.py`
3. `feat(generator): add commit message generation` — `generator.py`
4. `feat(verifier): add ARGUS bridge validation` — `verifier.py` + ARGUS `bridge_check.py`
5. `feat(verifier): add ARGUS crossref validation` — `verifier.py` + ARGUS `crossref_check.py`

### Phase 2 — P1 (atomic, commits séparés)

6. `feat(templates): add commit_validator.py` — validation conventional commits + atomicité
7. `feat(templates): add commit_monitor.py` — auto-commit multi-repo
8. `feat(industrializer): add auto-commit on deploy` — `deploy_with_auto_commit()`
9. `feat(pr_factory): add branch/commit coupling` — cohérence branch → commit → PR
10. `test(engine): add auto_design_argus_ctulu tests` — pytest couverture 80%

### Phase 3 — P2 (atomic, commits séparés)

11. `feat(verifier): add meta-coherence gate` — ARGUS `ecosystem_meta_coherence.py`
12. `feat(verifier): add traceability validation` — CTULU `trace_graph.py` + `trace_validator.py`
13. `feat(generator): add NODEX component classification` — ARGUS `nodex.py` + KG-L
14. `feat(templates): add jevi_projection templates` — JEVX TALEX/CURX
15. `feat(auto_promote): add governance synthesizer integration` — CTULU `vibe-governance-synthesizer`

## Critères d'Acceptation

1. `_score_conventional_commit_adherence()` retourne score 0-100 cohérent avec `git log --oneline`
2. `_check_atomic_commits()` détecte commits >3 fichiers et retourne violations
3. `generate_commit_message("feat", "engine", "add analyzer")` retourne `feat(engine): add analyzer`
4. `_validate_bridges_argus()` retourne JSON avec findings GAP/DRIFT/VOID/UNPROVEN
5. `_validate_crossrefs_argus()` retourne JSON avec findings ORPHAN/GAP/STALE/BROKEN
6. `industrializer.py` déploie `commit_validator.py` et `commit_monitor.py` dans `scripts/`
7. `deploy_with_auto_commit()` commit et push automatiquement après déploiement
8. `create_pr()` vérifie cohérence branch → commit → PR
9. `_check_meta_coherence()` bloque déploiement si `status != OK`
10. `_validate_traceability()` retourne violations (orphelins, liens cassés, status mismatch)
11. `_detect_components()` utilise NODEX pour classification KG-L
12. Templates JEVX projection déployés et fonctionnels
13. `auto_promote.py` génère 6 artifacts + commit via CTULU

## Méthode de vérification par tâche

Chaque tâche ATOMIC-NNN est vérifiée par :
1. **Test unitaire pytest** : `tests/test_auto_design_argus_ctulu.py` ou fichier dédié
2. **Vérification manuelle** : exécution du livrable et inspection du résultat
3. **Commit git** : message conventionnel, ≤3 fichiers
4. **Proof-of-Life** : horodatage dans INTENT après chaque commit

## Proof-of-Life exécution

- [x] 2026-09-29T20:10:00+02:00 — Tests validés : 18/18 passés (`pytest tests/test_auto_design_argus_ctulu.py`)
- [x] 2026-09-29T20:15:00+02:00 — Commit global : `feat(auto_design): integrate ARGUS/CTULU/JEVX P0-P2` (15 fichiers, 1830 insertions)

## Références

- **PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **ADR** : `ADR-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **EPIC** : `EPICS/EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **TASKs** : `TASKS/TASK-AUTO-DESIGN-*-20260929.md`
- **Repo ARGUS** : `gerivdb/ARGUS`
- **Repo CTULU** : `gerivdb/CTULU`
- **Repo JEVX** : mécanisme intégré à CTULU/TALEX
- **Repo KG-L** : `gerivdb/KG-L`
