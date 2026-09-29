---
type: PRD
version: "1.0.0"
date: "2026-09-29"
status: draft
intent_hash: 0xPRD_AUTO_DESIGN_ARGUS_CTULU_JEVX_20260929
parent_intent: INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# PRD — Auto-Design : exploitation d'ARGUS, CTULU et JEVX pour la gestion automatique des commits et la validation cross-repo

## Objectif

Exploiter les capacités existantes d'**ARGUS** (couche N+2 de détection), **CTULU** (couche N+3 d'orchestration et traçabilité) et **JEVX** (couche de projection/synchronisation) pour transformer `auto-design` d'un scoreur local en validateur sémantique écosystémique et pour automatiser la gestion des commits.

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P0-1 | `_score_conventional_commit_adherence()` | `engine/auto_design/analyzer.py` | Retourne score 0-100 via CTULU `trix-git-workflow.py` |
| P0-2 | `_check_atomic_commits()` | `engine/auto_design/verifier.py` | Détecte commits >3 fichiers, retourne violations |
| P0-3 | `generate_commit_message()` | `engine/auto_design/generator.py` | Génère message conventionnel `type(scope): description` |
| P0-4 | `_validate_bridges_argus()` | `engine/auto_design/verifier.py` | Appelle ARGUS `bridge_check.py --json`, agrège findings |
| P0-5 | `_validate_crossrefs_argus()` | `engine/auto_design/verifier.py` | Appelle ARGUS `crossref_check.py --json`, agrège findings |

### P1 — Important

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P1-1 | Templates commit | `templates/auto_design/commit_validator.py`, `templates/auto_design/commit_monitor.py` | Templates déployés dans `scripts/` |
| P1-2 | Auto-commit on deploy | `engine/auto_design/industrializer.py` | `deploy_with_auto_commit()` commit + push après déploiement |
| P1-3 | Branch/commit coupling | `engine/auto_design/pr_factory.py` | `create_pr()` vérifie cohérence branch → commit |
| P1-4 | Tests intégration | `tests/test_auto_design_argus_ctulu.py` | 8 tests couvrant les 5 intégrations P0 |

## État d'avancement réel (dry-run causal 2026-09-30, implémentation partielle)

### P0 — Essentiel (IMPLÉMENTÉ)

| ID | Livrable | Chemin cible | Critère d'acceptation | Statut |
|---|---|---|---|---|
| P0-1 | `_score_conventional_commit_adherence()` | `engine/auto_design/analyzer.py` | Retourne score 0-100 via CTULU `trix-git-workflow.py` | ✅ Implémenté |
| P0-2 | `_check_atomic_commits()` | `engine/auto_design/verifier.py` | Détecte commits >3 fichiers, retourne violations | ✅ Implémenté |
| P0-3 | `generate_commit_message()` | `engine/auto_design/generator.py` | Génère message conventionnel `type(scope): description` | ✅ Implémenté |
| P0-4 | `_validate_bridges_argus()` | `engine/auto_design/verifier.py` | Appelle ARGUS `bridge_check.py --json`, agrège findings | ✅ Implémenté |
| P0-5 | `_validate_crossrefs_argus()` | `engine/auto_design/verifier.py` | Appelle ARGUS `crossref_check.py --json`, agrège findings | ✅ Implémenté |

### P1 — Important (IMPLÉMENTÉ)

| ID | Livrable | Chemin cible | Critère d'acceptation | Statut |
|---|---|---|---|---|
| P1-1 | Templates commit | `templates/auto_design/commit_validator.py`, `templates/auto_design/commit_monitor.py` | Templates déployés dans `scripts/` | ✅ Implémenté |
| P1-2 | Auto-commit on deploy | `engine/auto_design/industrializer.py` | `deploy_with_auto_commit()` commit + push après déploiement | ✅ Implémenté |
| P1-3 | Branch/commit coupling | `engine/auto_design/pr_factory.py` | `create_pr()` vérifie cohérence branch → commit | ✅ Implémenté |
| P1-4 | Tests intégration | `tests/test_auto_design_argus_ctulu.py` | 8 tests couvrant les 5 intégrations P0 | ✅ Implémenté |

### P2 — Nice-to-have (IMPLÉMENTÉ)

| ID | Livrable | Chemin cible | Critère d'acceptation | Statut |
|---|---|---|---|---|
| P2-1 | Meta-coherence gate | `engine/auto_design/verifier.py` | `_check_meta_coherence()` bloque si ARGUS `status != OK` | ✅ Implémenté |
| P2-2 | Traceability validation | `engine/auto_design/verifier.py` | `_validate_traceability()` via CTULU `trace_graph.py` | ✅ Implémenté |
| P2-3 | NODEX component classification | `engine/auto_design/generator.py` | `_detect_components()` utilise ARGUS `nodex.py` + KG-L | ✅ Implémenté |
| P2-4 | JEVX projection templates | `templates/auto_design/jevi_projection/` | `design.yaml` → TALEX/CURX/narratives | ✅ Implémenté |
| P2-5 | Governance synthesizer integration | `engine/auto_design/auto_promote.py` | Appelle CTULU `vibe-governance-synthesizer` pour 6 artifacts + commit | ✅ Implémenté |

### P3 — Auto PR workflow (PARTIEL)

| ID | Livrable | Chemin cible | Critère d'acceptation | Statut |
|---|---|---|---|---|
| P3-1 | `pr_review_auto.py` | `engine/auto_design/pr_review_auto.py` | Workflow PR/review/merge automatique depuis n'importe quel repo | ❌ Non implémenté |
| P3-2 | `auto_operator.py` | `engine/auto_design/auto_operator.py` | Orchestrateur full cycle analyze→generate→verify→deploy→PR→merge | ❌ Non implémenté |

### Compléments implémentés

| ID | Livrable | Chemin cible | Critère d'acceptation | Statut |
|---|---|---|---|---|
| EXT-1 | Reporter | `engine/auto_design/reporter.py` | Agrège findings bridges + crossrefs | ✅ Implémenté |
| EXT-2 | Cycle runner template | `templates/auto_design/cycle_runner.py` | Séquence analyze->generate->verify->report | ✅ Implémenté |
| EXT-3 | Bridge executor template | `templates/auto_design/bridge_executor.py` | Exécution bridges déclarés | ✅ Implémenté |
| EXT-4 | Trace gate template | `templates/auto_design/trace_gate.py` | Vérifie traçabilité via CTULU | ✅ Implémenté |
| EXT-5 | CRM registry | `crm/tech_debt_registry.yaml` | Agrège dette cross-repo | ✅ Implémenté |
| EXT-6 | CRM notifier | `crm/notifier.py` | Envoie notifications CRM | ✅ Implémenté |
| EXT-7 | CRM workflow | `crm/workflow.py` | Orchestre détection→scoring→génération→notification | ✅ Implémenté |
| EXT-8 | Tests CRM | `tests/test_crm_tech_debt.py` | 10 tests couvrant P0/P1 CRM | ✅ Implémenté |
| EXT-9 | Tests analyzer | `tests/test_auto_design_analyzer.py` | 6 tests unitaires analyzer | ✅ Implémenté |

## Architecture cible

```
unified-design/
├── engine/
│   └── auto_design/
│       ├── analyzer.py          # + conventional commit scoring (CTULU)
│       ├── generator.py         # + NODEX classification (ARGUS) + JEVX projection
│       ├── industrializer.py    # + auto-commit (CTULU) + templates commit
│       ├── verifier.py          # + ARGUS bridge/crossref/meta-coherence + CTULU trace
│       ├── reporter.py          # + ARGUS meta_cycle_feedback
│       └── auto_promote.py      # + CTULU vibe-governance-synthesizer
├── templates/
│   └── auto_design/
│       ├── cycle_runner.py
│       ├── bridge_executor.py
│       ├── pr_factory.py
│       ├── commit_validator.py   # Conventional commits + atomic check
│       ├── commit_monitor.py     # Auto-commit via CTULU
│       └── trace_gate.py         # Traceability gate via CTULU
└── INTENTS/
    └── INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
```

## Plan d'exécution SLM

### Phase 1 — P0 (atomic, commits séparés)

1. `feat(analyzer): add conventional commit scoring` — `analyzer.py`
2. `feat(verifier): add atomic commit checking` — `verifier.py`
3. `feat(generator): add commit message generation` — `generator.py`
4. `feat(verifier): add ARGUS bridge validation` — `verifier.py`
5. `feat(verifier): add ARGUS crossref validation` — `verifier.py`

### Phase 2 — P1 (atomic, commits séparés)

6. `feat(templates): add commit_validator.py` — `templates/auto_design/commit_validator.py`
7. `feat(templates): add commit_monitor.py` — `templates/auto_design/commit_monitor.py`
8. `feat(industrializer): add auto-commit on deploy` — `industrializer.py`
9. `feat(pr_factory): add branch/commit coupling` — `pr_factory.py`
10. `test(engine): add auto_design_argus_ctulu tests` — `tests/test_auto_design_argus_ctulu.py`

### Phase 3 — P2 (atomic, commits séparés)

11. `feat(verifier): add meta-coherence gate` — `verifier.py`
12. `feat(verifier): add traceability validation` — `verifier.py`
13. `feat(generator): add NODEX component classification` — `generator.py`
14. `feat(templates): add jevi_projection templates` — `templates/auto_design/jevi_projection/`
15. `feat(auto_promote): add governance synthesizer integration` — `auto_promote.py`

## Critères d'Acceptation

1. **Conventional commits** : `_score_conventional_commit_adherence()` retourne un score 0-100 cohérent avec `git log --oneline`
2. **Atomic commits** : `_check_atomic_commits()` détecte les commits >3 fichiers et retourne les violations
3. **Commit message** : `generate_commit_message("feat", "engine", "add analyzer")` retourne `feat(engine): add analyzer`
4. **Bridge validation** : `_validate_bridges_argus()` retourne un rapport JSON avec findings GAP/DRIFT/VOID/UNPROVEN
5. **Crossref validation** : `_validate_crossrefs_argus()` retourne un rapport JSON avec findings ORPHAN/GAP/STALE/BROKEN
6. **Templates** : `industrializer.py` déploie `commit_validator.py` et `commit_monitor.py` dans `scripts/`
7. **Auto-commit** : `industrializer.deploy_with_auto_commit()` commit et push automatiquement après déploiement
8. **Branch coupling** : `pr_factory.create_pr()` vérifie que la branche courante correspond à la branche cible
9. **Meta-coherence** : `_check_meta_coherence()` bloque le déploiement si `status != OK`
10. **Traceability** : `_validate_traceability()` retourne un rapport de violations (orphelins, liens cassés, status mismatch)
11. **NODEX** : `_detect_components()` utilise NODEX pour classifier les composants avec KG-L
12. **JEVX** : Templates de projection TALEX/CURX déployés et fonctionnels
13. **Governance synthesizer** : `auto_promote.py` génère 6 artifacts + commit via CTULU

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

### Estimation d'effort par livrable

| ID | Livrable | Effort SLM | Tâches atomiques | Risque |
|---|---|---|---|---|
| P0-1 | Conventional commit scoring | 1h | 3 | Faible |
| P0-2 | Atomic commit checking | 30min | 2 | Faible |
| P0-3 | Commit message generation | 30min | 2 | Faible |
| P0-4 | ARGUS bridge validation | 1h | 3 | Moyen |
| P0-5 | ARGUS crossref validation | 1h | 3 | Moyen |
| P1-1 | Commit templates | 1h | 2 | Faible |
| P1-2 | Auto-commit on deploy | 1h | 2 | Moyen |
| P1-3 | Branch/commit coupling | 30min | 2 | Faible |
| P1-4 | Tests intégration | 2h | 4 | Faible |
| P2-1 | Meta-coherence gate | 2h | 3 | Moyen |
| P2-2 | Traceability validation | 3h | 4 | Élevé |
| P2-3 | NODEX classification | 2h | 3 | Élevé |
| P2-4 | JEVX projection templates | 2h | 3 | Moyen |
| P2-5 | Governance synthesizer | 2h | 3 | Moyen |

**Effort total** : ~19h de développement SLM réparties en 37 tâches atomiques

## Plan d'exécution SLM détaillé

### Phase 1 — P0 (5 livrables, ~4h)

#### Tâche ATOMIC-001 : Conventional commit scoring
- **Fichier** : `engine/auto_design/analyzer.py`
- **Action** : ajouter `_score_conventional_commit_adherence()`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_conventional_commit_scoring`
- **Commit** : `feat(analyzer): add conventional commit scoring`
- **Durée** : 30min

#### Tâche ATOMIC-002 : Atomic commit checking
- **Fichier** : `engine/auto_design/verifier.py`
- **Action** : ajouter `_check_atomic_commits()`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_atomic_commit_checking`
- **Commit** : `feat(verifier): add atomic commit checking`
- **Durée** : 30min

#### Tâche ATOMIC-003 : Commit message generation
- **Fichier** : `engine/auto_design/generator.py`
- **Action** : ajouter `generate_commit_message()`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_commit_message_generation`
- **Commit** : `feat(generator): add commit message generation`
- **Durée** : 30min

#### Tâche ATOMIC-004 : ARGUS bridge validation
- **Fichier** : `engine/auto_design/verifier.py`
- **Action** : ajouter `_validate_bridges_argus()`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_argus_bridge_validation`
- **Commit** : `feat(verifier): add ARGUS bridge validation`
- **Durée** : 1h

#### Tâche ATOMIC-005 : ARGUS crossref validation
- **Fichier** : `engine/auto_design/verifier.py`
- **Action** : ajouter `_validate_crossrefs_argus()`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_argus_crossref_validation`
- **Commit** : `feat(verifier): add ARGUS crossref validation`
- **Durée** : 1h

### Phase 2 — P1 (4 livrables, ~4.5h)

#### Tâche ATOMIC-006 : Commit validator template
- **Fichier** : `templates/auto_design/commit_validator.py`
- **Action** : créer template
- **Test** : déploiement test sur repo factice
- **Commit** : `feat(templates): add commit_validator.py`
- **Durée** : 1h

#### Tâche ATOMIC-007 : Commit monitor template
- **Fichier** : `templates/auto_design/commit_monitor.py`
- **Action** : créer template
- **Test** : déploiement test sur repo factice
- **Commit** : `feat(templates): add commit_monitor.py`
- **Durée** : 1h

#### Tâche ATOMIC-008 : Auto-commit on deploy
- **Fichier** : `engine/auto_design/industrializer.py`
- **Action** : ajouter `deploy_with_auto_commit()`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_auto_commit_on_deploy`
- **Commit** : `feat(industrializer): add auto-commit on deploy`
- **Durée** : 1h

#### Tâche ATOMIC-009 : Branch/commit coupling
- **Fichier** : `engine/auto_design/pr_factory.py`
- **Action** : créer module avec `create_pr()`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_branch_commit_coupling`
- **Commit** : `feat(pr_factory): add branch/commit coupling`
- **Durée** : 30min

#### Tâche ATOMIC-010 : Tests intégration
- **Fichier** : `tests/test_auto_design_argus_ctulu.py`
- **Action** : créer 8 tests couvrant P0
- **Test** : `pytest tests/test_auto_design_argus_ctulu.py -v`
- **Commit** : `test(engine): add auto_design_argus_ctulu tests`
- **Durée** : 1h

### Phase 3 — P2 (5 livrables, ~11h)

#### Tâche ATOMIC-011 : Meta-coherence gate
- **Fichier** : `engine/auto_design/verifier.py`
- **Action** : ajouter `_check_meta_coherence()`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_meta_coherence_gate`
- **Commit** : `feat(verifier): add meta-coherence gate`
- **Durée** : 2h

#### Tâche ATOMIC-012 : Traceability validation
- **Fichier** : `engine/auto_design/verifier.py`
- **Action** : ajouter `_validate_traceability()`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_traceability_validation`
- **Commit** : `feat(verifier): add traceability validation`
- **Durée** : 3h

#### Tâche ATOMIC-013 : NODEX classification
- **Fichier** : `engine/auto_design/generator.py`
- **Action** : ajouter `_classify_components_noded()`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_nortex_classification`
- **Commit** : `feat(generator): add NODEX component classification`
- **Durée** : 2h

#### Tâche ATOMIC-014 : JEVX projection templates
- **Fichier** : `templates/auto_design/jevi_projection/*.j2`
- **Action** : créer 3 templates Jinja2
- **Test** : `tests/test_jevi_projection.py`
- **Commit** : `feat(templates): add jevi_projection templates`
- **Durée** : 2h

#### Tâche ATOMIC-015 : Governance synthesizer integration
- **Fichier** : `engine/auto_design/auto_promote.py`
- **Action** : intégrer CTULU `vibe-governance-synthesizer`
- **Test** : `tests/test_auto_design_argus_ctulu.py::test_governance_synthesizer_integration`
- **Commit** : `feat(auto_promote): add governance synthesizer integration`
- **Durée** : 2h

- ARGUS : `bridge_check.py`, `crossref_check.py`, `ecosystem_meta_coherence.py`, `nodex.py` fonctionnels
- CTULU : `trix-git-workflow.py`, `trix-commit-monitor.py`, `trace_graph.py`, `trace_validator.py`, `trace_drift.py`, `vibe-governance-synthesizer/` fonctionnels
- JEVX : Templates de projection TALEX/CURX définis
- KG-L : `ecosystem_kg_full.json` accessible

## Risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| ARGUS/CTULU changent d'API | Moyenne | Élevé | Versionner les appels, fallback local |
| JEVX templates manquants | Faible | Moyen | Dégradation gracieuse, skip si absent |
| Performance scanners ARGUS | Moyenne | Moyen | Timeout 120s, cache disque |
| KG-L non disponible | Faible | Élevé | Fallback classification heuristique |

## Références

- **INTENT** : `INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **MOC** : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **ADR** : `ADR-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **Repo ARGUS** : `gerivdb/ARGUS`
- **Repo CTULU** : `gerivdb/CTULU`
- **Repo JEVX** : mécanisme intégré à CTULU/TALEX
- **Repo KG-L** : `gerivdb/KG-L`
