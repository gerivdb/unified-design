---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-22"
status: proposed
intent_hash: 0xPRD_MOC_JEVX_MDU_INTEGRATION_FIX_20260922
author: gerivdb
source_repo: gerivdb/unified-design
parent_doc: PRD-MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md
related_adr: ADR-0111-JEVX-SOVEREIGN-OVERLAY.md
related_intent: INTENT-JEVX-SOVEREIGN-OVERLAY.md
related_moc: MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md
---

# PRD-MOC — JEVX MDU Integration Fix

> **Parent** : PRD-MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md
> **Périmètre** : corrections d'alignement entre les designs JEVX, le repo JEVX, et les registres de `unified-design` / `GOVERNANCE-HUB`.
> **Coordination transverse** : voir MOC JEVX §3 (livrables, dépendances).

---

## 1. Objectif

Corriger les incohérences d'intégration de JEVX dans le MDU et les registres écosystémiques, après audit du 2026-09-22.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Corriger `do_not_create` JEVX | `GOVERNANCE-HUB/known_repositories.yaml` | Modifier | ⏳ Cross-repo |
| L2 | Corriger `entrypoint` JEVX | `designs/jevx.yaml` | Modifier | ✅ Fait |
| L3 | Clarifier `hardware_profile` JEVX | `designs/jevx.yaml` | Modifier | ✅ Fait |
| L4 | Aligner `depends_on` JEVX sur MDU | `designs/jevx.yaml`, `designs/jevx-engineering.yaml` | Modifier | ✅ Fait |
| L5 | Documenter `consumers` JEVX | `catalog/designs.index.yaml` | Modifier | ✅ Fait |
| L6 | Documenter `consumers` pipeline JEVX | `catalog/pipelines.index.yaml` | Modifier | ✅ Fait |
| L7 | Ajouter JEVX dans CLM pipeline | `designs/clm-pipeline/design.yaml` | Modifier | ✅ Fait |
| L8 | Corriger `SCOPE.yaml` consumer CLM | `JEVX/SCOPE.yaml` | Modifier | ⏳ Cross-repo |
| L9 | Dédupliquer `ONTOLOGY_DECLARATION.yaml` | `JEVX/ONTOLOGY_DECLARATION.yaml` | Modifier | ⏳ Cross-repo |
| L10 | Marquer `security_guardrails` draft | `designs/jevx.yaml` | Modifier | ✅ Fait |
| L11 | Marquer `constrained-parallel-decoding` draft | `designs/jevx-engineering.yaml` | Modifier | ✅ Fait |
| L12 | Aligner `max_queue` sur code | `designs/jevx.yaml` | Modifier | ✅ Fait |

## 3. Tâches

### Phase A — SOT et registres

1. **L1** : `GOVERNANCE-HUB/known_repositories.yaml` — passer `do_not_create: false` → `true` pour JEVX dans `P4_REPOS`. ⏳ Cross-repo (GOVERNANCE-HUB)
2. **L8** : `JEVX/SCOPE.yaml` — remplacer la référence consumer `gerivdb/CLM` par `gerivdb/ROOTX` ou `gerivdb/KG-CAUSAL`, ou supprimer la référence invalide. ⏳ Cross-repo (JEVX)
3. **L9** : `JEVX/ONTOLOGY_DECLARATION.yaml` — supprimer les doublons `jev_variant` et `comparative_study`. ⏳ Cross-repo (JEVX)

### Phase B — Designs JEVX

4. **L2** : `designs/jevx.yaml` — corriger `entrypoint: src/server.ts` → `src/index.ts`. ✅ Fait (commit `cd6b2d1`)
5. **L3** : `designs/jevx.yaml` — clarifier `hardware_profile` :
   - runtime principal = `Bun`
   - runtime alternatif = `Python 3.12 + llama.cpp` pour backends légers
   ✅ Fait (commit `cd6b2d1`)
6. **L4** : `designs/jevx.yaml` et `designs/jevx-engineering.yaml` — aligner `depends_on` sur MDU :
   - `kg-causal` → `kg-causal-engine`
   - `kix`, `rootx`, `talex` → déplacés vers `bridges`/`dependencies`
   ✅ Fait (commit `cd6b2d1`)
7. **L10** : `designs/jevx.yaml` — marquer `security_guardrails` comme `draft`. ✅ Fait (commit `cd6b2d1`)
8. **L11** : `designs/jevx-engineering.yaml` — marquer `constrained-parallel-decoding` comme `draft`. ✅ Fait (commit `cd6b2d1`)
9. **L12** : `designs/jevx.yaml` — aligner `max_queue: 64` sur la sémantique réelle du code. ✅ Fait (commit `cd6b2d1`)

### Phase C — Catalogues MDU

10. **L5** : `catalog/designs.index.yaml` — documenter les consumers pour les designs JEVX (`jevx`, `jevx-engineering`, `jevx-backend-matrix`). ✅ Fait (commit `6e9de0f`)
11. **L6** : `catalog/pipelines.index.yaml` — documenter les consumers pour `jevx-design-validation`. ✅ Fait (commit `6e9de0f`)
12. **L7** : `designs/clm-pipeline/design.yaml` — cohérence JEVX/CLM. ✅ Fait (commit `cd6b2d1`)

## 4. Contraintes

- **CPU-only** : GPU interdit (ENV2 / Z600)
- **WSL1** : runtime prioritaire Python 3.12 + llama.cpp AVX1
- **RAM max** : 24 Go (après OS et services)
- **Backend** : LEGACY_FIT immédiat (NanoJev, jevlike, minojev) ; LEGACY_PATCHABLE (jev_local)
- **Souveraineté** : aucun trafic ne quitte l'ENV sans médiation JEVX
- **Calibration** : probabilités auto-rapportées ; calibration externe requise avant usage décisionnel conséquent
- **Synthetic data** : tous les clones connus sont entraînés sur données 100% synthétiques ; calibration externe obligatoire
- **Encoding** : UTF-8 strict (hook pre-commit bloque non-ASCII)
- **Commits** : atomiques <= 3 fichiers

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `fix(sot): mark JEVX do_not_create true` | `GOVERNANCE-HUB/known_repositories.yaml` | L1 |
| `fix(jevx): align entrypoint and hardware profile` | `designs/jevx.yaml` | L2, L3 |
| `fix(jevx): align depends_on with MDU concepts` | `designs/jevx.yaml`, `designs/jevx-engineering.yaml` | L4 |
| `fix(jevx): mark guardrails and parallel decoding draft` | `designs/jevx.yaml`, `designs/jevx-engineering.yaml` | L10, L11 |
| `fix(jevx): align max_queue with code` | `designs/jevx.yaml` | L12 |
| `docs(catalog): document JEVX consumers` | `catalog/designs.index.yaml`, `catalog/pipelines.index.yaml` | L5, L6 |
| `fix(clm): add JEVX to CLM pipeline or remove ref` | `designs/clm-pipeline/design.yaml`, `designs/jevx.yaml` | L7 |
| `fix(jevx): clean SCOPE and ONTOLOGY_DECLARATION` | `JEVX/SCOPE.yaml`, `JEVX/ONTOLOGY_DECLARATION.yaml` | L8, L9 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : `python scripts/validate_designs.py --strict` ; hooks pre-commit (`design-validate`, `frontmatter-guardian`, `check-yaml`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. `GOVERNANCE-HUB/known_repositories.yaml` : `do_not_create: true` pour JEVX. ⏳ Cross-repo
2. `designs/jevx.yaml` : `entrypoint: src/index.ts`, `hardware_profile` clarifié, `max_queue` aligné. ✅ Fait
3. `designs/jevx.yaml` et `designs/jevx-engineering.yaml` : `depends_on` résolus dans le MDU ou déplacés vers `dependencies`/`bridges`. ✅ Fait
4. `designs/jevx.yaml` : `security_guardrails` marquées `draft` si non implémentées. ✅ Fait
5. `designs/jevx-engineering.yaml` : `constrained-parallel-decoding` marqué `draft` si absent du code. ✅ Fait
6. `catalog/designs.index.yaml` et `catalog/pipelines.index.yaml` : consumers documentés. ✅ Fait
7. `designs/clm-pipeline/design.yaml` et `designs/jevx.yaml` : cohérence sur la présence de JEVX dans CLM. ✅ Fait
8. `JEVX/SCOPE.yaml` : aucune référence invalide à `gerivdb/CLM`. ⏳ Cross-repo
9. `JEVX/ONTOLOGY_DECLARATION.yaml` : aucun doublon. ⏳ Cross-repo
10. Tous les designs passent `python scripts/validate_designs.py --strict`. ✅ Passe

## 8. Proof-of-Life

- [x] 2026-09-22T01:15:20+02:00 — Création PRD-MOC JEVX MDU Integration Fix
- [x] 2026-09-22T01:15:20+02:00 — L2-L4, L7, L10-L12 implémentés dans unified-design (commits `6e9de0f`, `cd6b2d1`)
- [x] 2026-09-22T01:15:20+02:00 — L5-L6 consumers documentés dans catalogues
- [ ] 2026-09-22T01:15:20+02:00 — L1, L8-L9 bloqués cross-repo (GOVERNANCE-HUB, JEVX)
