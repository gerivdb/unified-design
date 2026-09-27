---
type: MOC
version: "1.0.0"
date: "2026-09-27"
status: approved
intent_hash: 0xMOC_UNIFIED_DESIGN_STRUCTURAL_METACOHERENCE_CHECKER_20260927
parent_prd: PRD-UNIFIED-DESIGN-STRUCTURAL-METACOHERENCE-CHECKER-20260927.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# MOC — Unified-Design Structural Metacoherence Checker

## Objectif

Mettre en œuvre le PRD `PRD-UNIFIED-DESIGN-STRUCTURAL-METACOHERENCE-CHECKER-20260927.md` :
- vérificateur structurel `.kilo/check_meta_coherence.py`
- alias registry `.kilo/meta_coherence_aliases.yaml`
- documentation `.kilo/CHECK_METACOHERENCE.md`
- tests `.kilo/tests/test_check_meta_coherence.py`
- hook pre-commit `.pre-commit-config.yaml`
- CI step `scripts/run_meta_coherence_check.ps1`

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P0-1 | `check_meta_coherence.py` | `.kilo/check_meta_coherence.py` | ✅ |
| P0-2 | Alias registry | `.kilo/meta_coherence_aliases.yaml` | ✅ |
| P0-3 | Rapport + backup | `reports/meta-coherence/` | ✅ |

### P1 — Important

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P1-1 | Documentation | `.kilo/CHECK_METACOHERENCE.md` | ✅ |
| P1-2 | Tests unitaires | `.kilo/tests/test_check_meta_coherence.py` | ✅ |
| P1-3 | Hook pre-commit | `.pre-commit-config.yaml` | ✅ |

### P2 — Nice-to-have

| ID | Livrable | Chemin cible | Statut |
|---|---|---|---|
| P2-1 | CI step local | `scripts/run_meta_coherence_check.ps1` | ✅ |
| P2-2 | Enrichissement aliases | `.kilo/meta_coherence_aliases.yaml` | 🔄 |

## Plan d'exécution SLM

### Phase 1 — P0 (atomic, 3 commits)

1. `feat(.kilo): add structural metacoherence checker` — script + aliases + rapports
2. `docs(.kilo): add CHECK_METACOHERENCE.md` — guide d'usage
3. `test(.kilo): add meta coherence unit tests` — pytest 3 passed

### Phase 2 — P1 (atomic, 2 commits)

4. `feat(hooks): add meta-coherence pre-commit` — intégration `.pre-commit-config.yaml`
5. `feat(scripts): add run_meta_coherence_check.ps1` — CI step local

### Phase 3 — P2 (atomic, 1 commit)

6. `chore(.kilo): enrich meta_coherence_aliases.yaml` — alias supplémentaires

## Critères d'acceptation globaux

- [x] `python .kilo/check_meta_coherence.py --mode check` : JSON valide sur 283 designs
- [x] `python .kilo/check_meta_coherence.py --mode plan` : fix-plan cohérent
- [ ] `python .kilo/check_meta_coherence.py --mode strict` : exit 0 uniquement si 0 problème
- [x] `python .kilo/check_meta_coherence.py --mode apply` : backups créés, auto-fixes appliqués
- [x] Hook pre-commit bloque si `--strict` échoue
- [x] Tests unitaires passent : `pytest .kilo/tests/test_check_meta_coherence.py -q`

## Références

- **PRD** : `PRD/PRD-UNIFIED-DESIGN-STRUCTURAL-METACOHERENCE-CHECKER-20260927.md`
- **Intent** : `INTENTS/INTENT-UNIFIED-DESIGN-METACOHERENCE-STRUCTURAL-CHECKER-20260927.md`
- **Intent parent** : `INTENTS/INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md`
- **MOC parent** : `MOC/PRD-MOC-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md`
- **MOC** : `MOC/MOC-STRUCTURAL-COHERENCE-20260922.md`
- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Design** : `designs/ecosystem-meta-coherence-gate/design.yaml`
- **Design** : `designs/incremental-growth.yaml`
- **Script** : `.kilo/check_meta_coherence.py`
- **Documentation** : `.kilo/CHECK_METACOHERENCE.md`
- **Tests** : `.kilo/tests/test_check_meta_coherence.py`
- **Aliases** : `.kilo/meta_coherence_aliases.yaml`
- **Hook** : `.pre-commit-config.yaml`

## Proof-of-Life

- [x] 2026-09-27T23:59:08+02:00 — MOC créé, PRD approuvé
- [x] P0-1 : check_meta_coherence.py fonctionnel en modes check/plan/apply/strict
- [x] P0-2 : meta_coherence_aliases.yaml peuplée
- [x] P0-3 : reports/meta-coherence/ générés
- [x] P1-1 : CHECK_METACOHERENCE.md rédigé
- [x] P1-2 : tests unitaires passent
- [x] P1-3 : hook pre-commit intégré
 - [x] P2-1 : run_meta_coherence_check.ps1 fonctionnel
 - [x] P2-2 : aliases enrichis
 - [x] 2026-09-28T00:48:21+02:00 — PR #81 mergée, merge commit `3e19ef3`
 - [x] 2026-09-28T01:15:42+02:00 — PR #83 mergée, merge commit `aa855f0`
 - [x] 2026-09-28T01:34:30+02:00 — PR #85 mergée, merge commit `3d70bfe`
 - [x] 2026-09-28T01:38:30+02:00 — PR #86 mergée, merge commit `8d73450`
 - [x] 2026-09-28T01:42:04+02:00 — PR #87 mergée, merge commit `1a70f10`
