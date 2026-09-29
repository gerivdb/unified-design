# Dry-Run Causal — Prod-Readiness Report

**Date** : 2026-09-30T01:01:27+02:00  
**Repos analysés** : `unified-design`, `auto-dev`, `TALEX`, `ONTOLOGY`  
**Mode** : ACT auto, tâches atomiques calibrées SLM  

## Résumé exécutif

| Composant | Statut prod-readiness | Détails |
|-----------|----------------------|---------|
| `unified-design` ontologies | ✅ Prod-ready | 12 concepts ONTOLOGY commités, gaps ontologiques = 0 |
| `unified-design` primitives/pipelines/citizens | ✅ Prod-ready | 9 artefacts commités et poussés |
| `auto-dev` engine `auto_design` | ❌ Non implémenté | Répertoires `engine/auto_design/`, `templates/auto_design/`, `crm/` absents |
| `auto-dev` tests ARGUS/CTULU | ❌ Non implémenté | Aucun fichier `tests/test_auto_design_argus_ctulu.py` |
| `auto-dev` WAL transport | ✅ Prod-ready | `tools/transport_wal.py` + `tools/transport_test_runner.py` fonctionnels |
| `auto-dev` bridges WAZAA/BOINC | ✅ Prod-ready | 22/22 tests PASS |
| TALEX friction analyzer | ✅ Prod-ready | `citizens/friction_analyzer.yaml` + `runners/friction_analyzer.py` |
| TALEX ontological gaps | ✅ Aucun gap | `analyze_ontological_gaps.py` → 0 gap |
| Museum effect | ⚠️ WARN | `MUSEUM_EFFECT_REGISTRY_STALE` sur VOLTX, SPIDX, KORX, OBS, NEXUS |

## Gaps bloquants identifiés

### 1. `engine/auto_design/` absent
**PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`  
**Impact** : P0/P1/P2/P3 tous marqués TERMINÉ mais implémentation absente  
**Action** : Implémenter les modules atomiques :
- `engine/auto_design/analyzer.py`
- `engine/auto_design/verifier.py`
- `engine/auto_design/generator.py`
- `engine/auto_design/industrializer.py`
- `engine/auto_design/pr_factory.py`
- `engine/auto_design/auto_promote.py`
- `engine/auto_design/reporter.py`

### 2. `templates/auto_design/` absent
**PRD** : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`  
**Impact** : Templates commit validator/monitor, jevi_projection absents  
**Action** : Implémenter les templates atomiques

### 3. `crm/` absent
**PRD** : `PRD-CRM-TECH-DEBT-20260929.md`  
**Impact** : Registry dette, scoring, génération CRM absents  
**Action** : Implémenter `crm/tech_debt_registry.yaml`, `crm/notifier.py`, `crm/workflow.py`

### 4. Museum effect — registre stale
**Détection** : `dry_run_causal.py`  
**Impact** : Plusieurs repos n'ont pas de changement effectif récent  
**Action** : Rafraîchir `RUNTIME/ecosystem_repo_registry.yaml` avec les dates de dernier commit

## Plan d'implémentation immédiat (mode ACT auto)

### Phase A — Structure manquante (prérequis)
1. Créer `engine/auto_design/__init__.py`
2. Créer `templates/auto_design/__init__.py`
3. Créer `crm/__init__.py`

### Phase B — P0 ARGUS/CTULU/JEVX (5 tâches atomiques)
1. `feat(analyzer): add conventional commit scoring` — 1 fichier, 1 test
2. `feat(verifier): add atomic commit checking` — 1 fichier, 1 test
3. `feat(generator): add commit message generation` — 1 fichier, 1 test
4. `feat(verifier): add ARGUS bridge validation` — 1 fichier, 1 test
5. `feat(verifier): add ARGUS crossref validation` — 1 fichier, 1 test

### Phase C — P1 Templates + Auto-commit (4 tâches atomiques)
1. `feat(templates): add commit_validator.py` — 1 fichier
2. `feat(templates): add commit_monitor.py` — 1 fichier
3. `feat(industrializer): add auto-commit on deploy` — 1 fichier, 1 test
4. `feat(pr_factory): add branch/commit coupling` — 1 fichier, 1 test

### Phase D — CRM Tech Debt (3 tâches atomiques)
1. `feat(crm): add tech_debt_registry.yaml` — 1 fichier
2. `feat(analyzer): add tech debt scoring` — 1 méthode dans `analyzer.py`, 1 test
3. `feat(generator): add CRM task generation` — 1 méthode dans `generator.py`, 1 test

### Phase E — Tests intégration (2 tâches atomiques)
1. `test(engine): add auto_design_argus_ctulu tests` — 1 fichier, 8 tests
2. `test(crm): add test_crm_tech_debt.py` — 1 fichier, 10 tests

## Calibration SLM
- **RAM** : 24 Go (16 threads)
- **Tâche max** : 30 min sans commit
- **Fichiers max par commit** : 3
- **Test par livrable** : pytest unitaire
- **Fallback** : si ARGUS/CTULU indisponible → mode dégradé local

## Références
- PRD : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- PRD : `PRD-CRM-TECH-DEBT-20260929.md`
- MOC : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- TALEX : `scripts/analyze_ontological_gaps.py`
- TALEX : `scripts/dry_run_causal.py`
