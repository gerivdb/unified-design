---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-20"
status: proposed
intent_hash: 0xINTENT_JEVX_SOVEREIGN_OVERLAY_20260919
author: gerivdb
source_repo: gerivdb/unified-design
parent_doc: INTENT-JEVX-SOVEREIGN-OVERLAY.md
governance:
  strate: L0-CANON
  profil: master
  rss_depth: 0
related_adr: ADR-0111-JEVX-SOVEREIGN-OVERLAY.md
related_intent: INTENT-JEVX-SOVEREIGN-OVERLAY.md
related_moc: MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md
related_prd_moc:
  - PRD-MOC-JEVX-BACKEND-SELECTOR-20260920.md
  - PRD-MOC-JEVX-CONSTRAINED-PARALLEL-DECODING-20260920.md
  - PRD-MOC-JEVX-SOVEREIGN-ADAPTER-PATTERN-20260920.md
  - PRD-MOC-JEVX-DESIGN-VALIDATION-PIPELINE-20260920.md
  - PRD-MOC-JEVX-STRUCTURAL-FIX-PIPELINE-20260920.md
---

# PRD-MOC — JEVX : Decision-Engine Souverain JEVX

> **Parent** : INTENT-JEVX-SOVEREIGN-OVERLAY.md (`0xINTENT_JEVX_SOVEREIGN_OVERLAY_20260919`)
> **Périmètre** : ce dépôt uniquement — création et enregistrement des designs, atoms et patterns JEVX dans le MDU.
> **Coordination transverse** : voir MOC §3 (livrables, dépendances).

---

## 1. Objectif

Intégrer JEVX comme decision-engine souverain dans le Meta-Design Unifié (MDU) de `unified-design`, avec :
- Un design principal (`jevx.yaml`) définissant l'architecture et les contraintes
- Un design de matrice backend (`jevx-backend-matrix.yaml`) documentant les alternatives Z600-compatibles
- Un pattern d'ingénierie (`jevx-engineering.yaml`) réutilisable pour tout wrapper souverain
- Un atom (`typed-decision-api.yaml`) définissant le contrat de décision typée
- Des security guardrails pour les décisions à haut risque

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Design `jevx` | `designs/jevx.yaml` | Créer | ✅ |
| L2 | Design `jevx-engineering` | `designs/jevx-engineering.yaml` | Créer | ✅ |
| L3 | Design `jevx-backend-matrix` | `designs/jevx-backend-matrix.yaml` | Créer | ✅ |
| L4 | Atom `typed-decision-api` | `atoms/typed-decision-api.yaml` | Créer | ✅ |
| L5 | Primitive `constrained-parallel-decoding` | `primitives/constrained-parallel-decoding/design.yaml` | Créer | ✅ |
| L6 | Primitive `sovereign-adapter-pattern` | `primitives/sovereign-adapter-pattern/design.yaml` | Créer | ✅ |
| L7 | Skill `jevx-backend-selector` | `skills/jevx-backend-selector/SKILL.md` | Créer | ✅ |
| L8 | Pipeline `jevx-design-validation` | `pipelines/jevx-design-validation.yaml` | Créer | ✅ |
| L9 | Mise à jour workflow | `workflows/structural-fix-pipeline.md` | Modifier | ✅ |
| L10 | Mise à jour `META-DESIGN.md` | `META-DESIGN.md` | Modifier | ✅ |
| L11 | Mise à jour `meta-design.yaml` | `meta-design.yaml` | Modifier | ✅ |
| L12 | Mise à jour `catalog/designs.index.yaml` | `catalog/designs.index.yaml` | Modifier | ✅ |
| L13 | Intégration KIX | `D:\DO\WEB\TOOLS\L2-PLATFORM\KIX\config\runners.yaml` | Modifier | ✅ |
| L7 | Intégration KIX | `D:\DO\WEB\TOOLS\L2-PLATFORM\KIX\config\runners.yaml` | Modifier | ✅ |

## 3. Tâches

### Phase A — Designs et atom
1. `jevx.yaml` : design principal JEVX avec backend selector, WSL1 deployment, security guardrails
2. `jevx-engineering.yaml` : pattern d'ingénierie avec constrained-parallel-decoding, sovereign-adapter-pattern
3. `jevx-backend-matrix.yaml` : matrice de sélection backend (5 backends, cas d'usage)
4. `typed-decision-api.yaml` : atom avec backends souverains, compromis, WSL1

### Phase A2 — Primitives et skills déduits
5. `primitives/constrained-parallel-decoding/design.yaml` : primitive décodage parallèle contraint
6. `primitives/sovereign-adapter-pattern/design.yaml` : primitive adaptateur souverain
7. `skills/jevx-backend-selector/SKILL.md` : skill sélection backend selon contraintes

### Phase B — Documentation MDU
8. `META-DESIGN.md` : enregistrement des designs, atoms, primitives et skills JEVX
9. `meta-design.yaml` : ajout entrées dans `designs:` et `governance_atoms:`
10. `catalog/designs.index.yaml` : mise à jour index

### Phase C — Validation et intégration
11. Validation YAML : `gerivdb design validate --strict` sur tous les designs
12. Validation design coverage : pre-commit hook
13. Pipeline JEVX : `pipelines/jevx-design-validation.yaml`
14. Workflow structural fix : mise à jour `workflows/structural-fix-pipeline.md`
15. Intégration KIX : enregistrement dans `config/runners.yaml` + vérification `/runners`
16. Intégration KG-CAUSAL : connexion observation/effect channels

## 4. Contraintes

- **CPU-only** : GPU interdit (ENV2 / Z600)
- **WSL1** : runtime prioritaire Python 3.12 + llama.cpp AVX1
- **RAM max** : 24 Go (après OS et services)
- **Backend** : LEGACY_FIT immédiat (NanoJev, jevlike, minojev) ; LEGACY_PATCHABLE (jev_local)
- **Souveraineté** : aucun trafic ne quitte l'ENV sans médiation JEVX
- **Calibration** : probabilités auto-rapportées ; calibration externe requise avant usage décisionnel conséquent
- **Security** : consensus minimum + seuil de confiance + HITL pour actions critiques
- **Encoding** : UTF-8 strict (hook pre-commit bloque non-ASCII)
- **Commits** : atomiques <= 3 fichiers

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `feat(jevx): add backend selector + legacy-fit matrix` | `designs/jevx.yaml`, `designs/jevx-backend-matrix.yaml` | Backend selector, matrice Z600-compatible, WSL1, security guardrails |
| `feat(jevx): add engineering patterns + atom backends` | `designs/jevx-engineering.yaml`, `atoms/typed-decision-api.yaml` | constrained-parallel-decoding, sovereign-adapter, backends |
| `docs(mdu): register jevx designs and atoms` | `META-DESIGN.md`, `meta-design.yaml` | Enregistrement MDU |
| `feat(kix): register jevx service` | `KIX-INTEGRATION.md` | Intégration KIX (si applicable) |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : `gerivdb design validate --strict` sur `designs/jevx*.yaml` ; hooks pre-commit (`design-validate`, `frontmatter-guardian`, `check-yaml`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. Les designs `jevx.yaml`, `jevx-engineering.yaml`, `jevx-backend-matrix.yaml` parse en YAML valide, respectent le schéma `meta-design.yaml`, et passent `gerivdb design validate --strict`.
2. L'atom `typed-decision-api.yaml` est créé et référencé dans `META-DESIGN.md` et `meta-design.yaml`.
3. Le backend selector documente au moins 3 backends Z600-compatibles (NanoJev, jevlike, minojev).
4. Les security guardrails sont définies (consensus minimum, seuil de confiance, HITL, audit trail).
5. Les patterns `constrained-parallel-decoding` et `sovereign-adapter-pattern` sont documentés dans `jevx-engineering.yaml`.
6. Le déploiement WSL1 est documenté avec runtimes préférés et isolation.
7. Aucune violation DAG n'est introduite (vérifier `depends_on` et `inherits`).
8. Les pre-commit hooks passent sans blocage encoding sur tous les fichiers.
9. L'ADr ADR-0111 est référencée et cohérente avec les designs.
10. Les Proof-of-Life sont horodatés et documentés.

## 8. Proof-of-Life

- [x] 2026-09-20T20:11:03+02:00 — Création PRD-MOC JEVX
- [x] 2026-09-20T20:11:03+02:00 — Design `jevx.yaml` avec backend selector, WSL1, security guardrails
- [x] 2026-09-20T20:11:03+02:00 — Design `jevx-backend-matrix.yaml` créé
- [x] 2026-09-20T20:11:03+02:00 — Design `jevx-engineering.yaml` avec patterns
- [x] 2026-09-20T20:11:03+02:00 — Atom `typed-decision-api.yaml` avec backends
- [x] 2026-09-20T20:15:00+02:00 — Mise à jour `META-DESIGN.md` et `meta-design.yaml` (Phase B)
- [x] 2026-09-20T20:15:00+02:00 — Designs et atom enregistrés dans MDU
- [x] 2026-09-20T20:33:14+02:00 — Validation `gerivdb design validate --strict` PASS sur `jevx.yaml`, `jevx-engineering.yaml`, `jevx-backend-matrix.yaml`
- [x] 2026-09-20T20:33:14+02:00 — Correction YAML `jevx-backend-matrix.yaml` (ram_gb scalar)
- [x] 2026-09-20T20:33:14+02:00 — Atom `typed-decision-api.yaml` référencé MDU (validateur designs ne cible pas `atoms/`)
- [x] 2026-09-20T20:54:00+02:00 — Intégration KIX : enregistrement dans `config/runners.yaml` + vérification `/runners` PASS
- [x] 2026-09-20T21:06:00+02:00 — Création primitive `constrained-parallel-decoding`
- [x] 2026-09-20T21:06:00+02:00 — Création primitive `sovereign-adapter-pattern`
- [x] 2026-09-20T21:06:00+02:00 — Création skill `jevx-backend-selector`
- [x] 2026-09-20T21:06:00+02:00 — Création pipeline `jevx-design-validation.yaml`
- [x] 2026-09-20T21:06:00+02:00 — Mise à jour workflow `structural-fix-pipeline.md`
- [x] 2026-09-20T21:06:00+02:00 — Enregistrement primitives/skills dans `meta-design.yaml` et `META-DESIGN.md`
- [x] 2026-09-20T21:06:00+02:00 — Mise à jour `catalog/designs.index.yaml`

## 9. Évaluation

| Critère d'acceptation | État | Preuve |
|---|---|---|
| 1. YAML valide + validation stricte | ✅ | `validate_designs.py --strict` PASS sur 3/3 designs JEVX |
| 2. Atom référencé MDU | ✅ | `META-DESIGN.md` + `meta-design.yaml` |
| 3. 3+ backends Z600 documentés | ✅ | NanoJev, jevlike, minojev, jev_local |
| 4. Security guardrails définies | ✅ | consensus_minimum, confidence_threshold, HITL, audit_trail |
| 5. Patterns documentés | ✅ | constrained-parallel-decoding, sovereign-adapter-pattern |
| 6. WSL1 déployé documenté | ✅ | Python 3.12, llama.cpp AVX1, chroot/proot |
| 7. Pas de violation DAG | ✅ | depends_on cohérent, pas de cycle détecté |
| 8. Pre-commit hooks passent | ✅ | PASS sur commits atomiques |
| 9. ADR-0111 référencée | ✅ | Référencée dans tous les designs |
| 10. Proof-of-Life horodatés | ✅ | Section 8 complétée |
| 11. Intégration KIX | ✅ | `config/runners.yaml` + vérification `/runners` PASS |

**Verdict** : ✅ **Phase A + Phase B + Phase C + Intégration KIX complètes** — Designs, atom, enregistrement MDU, validation ciblée et intégration KIX implémentés.

## 10. Références

- **ADR** : `ADR-0111-JEVX-SOVEREIGN-OVERLAY.md`
- **Intent** : `INTENT-JEVX-SOVEREIGN-OVERLAY.md`
- **Designs** : `designs/jevx.yaml`, `designs/jevx-engineering.yaml`, `designs/jevx-backend-matrix.yaml`
- **Atom** : `atoms/typed-decision-api.yaml`
- **MDU** : `META-DESIGN.md`, `meta-design.yaml`
- **Upstream** : `githubnext/localjev`
- **Backends** : `TianyuCodings/NanoJev`, `vinnylarouge/jevlike`, `zeredy879/minojev`, `Argos1111/jev_local`

## 11. PRD-MOC associés

| PRD-MOC | Description |
|---------|-------------|
| `PRD-MOC-JEVX-BACKEND-SELECTOR-20260920.md` | Skill de sélection backend selon contraintes matérielles |
| `PRD-MOC-JEVX-CONSTRAINED-PARALLEL-DECODING-20260920.md` | Primitive décodage parallèle contraint (KV cache broadcast) |
| `PRD-MOC-JEVX-SOVEREIGN-ADAPTER-PATTERN-20260920.md` | Primitive adaptateur souverain (transposition Python de localjev) |
| `PRD-MOC-JEVX-DESIGN-VALIDATION-PIPELINE-20260920.md` | Pipeline de validation ciblée des designs JEVX |
| `PRD-MOC-JEVX-STRUCTURAL-FIX-PIPELINE-20260920.md` | Mise à jour workflow structural-fix-pipeline avec patterns JEVX |

---

## Annexes

### A. Backend Matrix (extrait)

| Backend | RAM | Latence | WSL1 | Confiance | Usage |
|---------|-----|---------|------|-----------|-------|
| minojev | < 100 Mo | 13–23 ms | ✅ | 90% | Décision minimale |
| NanoJev | ~1.2 Go | 50–200 ms | ✅ | 85% | Décision standard |
| jevlike | < 1 Go | variable | ✅ | 80% | Scorer custom |
| jev_local | ~1.3 Go | 200–500 ms | ⚠️ patch | 70% | API LocalJev |

### B. Security Guardrails

- `decision_safety_filter` : schema_validation + confidence_threshold (0.85) + human_escalation
- `false_negative_prevention` : consensus_minimum (2) + entropy_upper_bound (0.3) + fallback_human
- `audit_trail` : input_hash, backend_id, model_id, seed, probabilities, confidence, retry_count, latency_ms

### C. Patterns

- `constrained-parallel-decoding` : KV cache broadcast, llama_batch, logits biaisés
- `sovereign-adapter-pattern` : Python + llama.cpp + FastAPI minimal
