---
type: PRD-MOC
version: "1.0.0"
date: "2026-10-01"
status: proposed
intent_hash: 0xPRD_MOC_LOOPX_PROOF_OF_LIFE_AUTOMATION_20261001
parent_prd: INTENT-LOOPX-PROOF-OF-LIFE-AUTOMATION-20260921.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# PRD-MOC — LOOPX Proof-of-Life Automation

## Objectif

Éliminer la classe d'erreurs « [x] sans preuve » dans les PRD/MOC LOOPX :
- Toute implémentation validée est horodatée, tracée et synchronisée avec les documents de gouvernance.
- Toute preuve contient la commande exacte, le résultat vérifiable et l'horodatage UTC.
- Les références croisées entre PRD parent et enfants sont validées mécaniquement.

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P0-1 | `proof_of_life_capture.py` | `scripts/proof_of_life_capture.py` | Capture pytest --tb=short -q avec horodatage ISO |
| P0-2 | `proof_of_life_updater.py` | `scripts/proof_of_life_updater.py` | Met à jour section Proof-of-Life du PRD/MOC |
| P0-3 | `cross_ref_validator.py` | `scripts/cross_ref_validator.py` | Valide cohérence entre PRD parent et enfants |

### P1 — Important

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P1-1 | Skill `proof-of-life-automation` | `skills/proof-of-life-automation/SKILL.md` | Skill documenté et testé |
| P1-2 | Hook pre-commit proof-of-life | `.kilocode/hooks/pre-commit-proof-of-life.py` | Bloque commit si preuve manquante ou stale |
| P1-3 | `proof_staleness_scanner.py` | `scripts/proof_staleness_scanner.py` | Détecte preuves > 24h dans PRD/MOC |

### P2 — Nice-to-have

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P2-1 | `proof_of_life_aggregator.py` | `scripts/proof_of_life_aggregator.py` | Agrège preuves multi-repos en rapport unique |
| P2-2 | WAZAA channel `governance/proof-of-life/*` | `channels/proof-of-life.yaml` | Canal WAZAA opérationnel |
| P2-3 | ADR backing | `ADR/ADR-LOOPX-PROOF-OF-LIFE-AUTOMATION.md` | ADR créé et approuvé |

## Plan d'exécution SLM

### Phase 1 — P0 (atomic, 3 commits)

1. `feat(scripts): add proof_of_life_capture` — capture pytest avec horodatage ISO
2. `feat(scripts): add proof_of_life_updater` — mise à jour section Proof-of-Life
3. `feat(scripts): add cross_ref_validator` — validation références croisées

### Phase 2 — P1 (atomic, 3 commits)

4. `docs(skill): add proof-of-life-automation` — skill documentation
5. `feat(hooks): add pre-commit-proof-of-life` — hook bloquant
6. `feat(scripts): add proof_staleness_scanner` — détection preuves stale

### Phase 3 — P2 (atomic, 3 commits)

7. `feat(scripts): add proof_of_life_aggregator` — agrégation multi-repos
8. `docs(channels): add proof-of-life WAZAA channel` — canal WAZAA
9. `docs(adr): add proof-of-life automation ADR` — ADR backing

## Critères d'acceptation globaux

- [ ] `proof_of_life_capture.py --strict` : capture pytest avec horodatage UTC, commande et résultat
- [ ] `proof_of_life_updater.py --prd <path>` : section Proof-of-Life mise à jour sans erreur
- [ ] `cross_ref_validator.py --root <path>` : 0 incohérence entre PRD parent et enfants
- [ ] Hook pre-commit bloque commit si preuve manquante ou timestamp > 24h
- [ ] `proof_staleness_scanner.py --scan unified-design/PRD-MOC/` : 0 preuve stale
- [ ] >= 95% des PRD/MOC avec statut `approved` ont une preuve de vie valide
- [ ] Aucun [x] dans un PRD/MOC sans preuve d'exécution horodatée vérifiable

## États du cycle de vie

| État | Nature | Transition |
|---|---|---|
| IDLE | Preuve non nécessaire | → CAPTURE_RESULTS si implémentation validée |
| CAPTURE_RESULTS | Capture pytest avec horodatage | → FORMAT_PROOF |
| FORMAT_PROOF | Formatage markdown avec horodatage ISO | → UPDATE_PRD |
| UPDATE_PRD | Mise à jour section Proof-of-Life | → VALIDATE_CROSS_REFS |
| VALIDATE_CROSS_REFS | Validation références croisées | → COMPLETE |
| COMPLETE | Preuve enregistrée | — |
| BLOCK | Preuve bloquée (manquante/stale) | → CAPTURE_RESULTS après correction |

## Gènes obligatoires

| Gène | Description |
|---|---|
| timestamp_utc | Toute preuve horodatée en UTC (ISO8601) |
| command_traceability | Commande exacte exécutée |
| result_verifiable | Résultat vérifiable (passed/failed/skipped) |
| cross_ref_consistency | Preuves cohérentes entre documents liés |

## Anti-patterns bloquants

| Anti-pattern | Pathologie |
|---|---|
| missing_gene: timestamp_utc | Preuve sans horodatage -> impossibilité d'auditer la fraîcheur |
| missing_gene: command_traceability | Preuve sans commande -> impossibilité de reproduire |
| missing_gene: result_verifiable | Preuve sans résultat -> [x] invérifiable |
| missing_gene: cross_ref_consistency | Preuves incohérentes -> confusion entre documents |
| stale_proof (> 24h) | Preuve obsolète -> [x] invalide |
| missing_proof | [x] sans preuve -> violation DESIGN-E |

## Références

- **Design** : `designs/loopx-proof-of-life-automation/design.yaml`
- **Gouvernance** : `DESIGNS_GOVERNANCE.md`
- **Règles** : `.kilocode/rules/pr-lifecycle-gate.md`, `.kilocode/rules/session-boot-sequence.md`
- **INTENT** : `INTENTS/INTENT-LOOPX-PROOF-OF-LIFE-AUTOMATION-20260921.md`
- **Skill** : `proof-of-life-automation` (P1-1)
- **WAZAA** : `channels/proof-of-life.yaml` (P2-2)

## Proof-of-Life

- [ ] 2026-10-01T01:49:00+02:00 — PRD-MOC créé : loopx-proof-of-life-automation
- [ ] P0-1 : proof_of_life_capture.py créé et testé
- [ ] P0-2 : proof_of_life_updater.py créé et testé
- [ ] P0-3 : cross_ref_validator.py créé et testé
- [ ] P1-1 : Skill proof-of-life-automation créé
- [ ] P1-2 : Hook pre-commit créé et testé
- [ ] P1-3 : proof_staleness_scanner.py créé et testé
