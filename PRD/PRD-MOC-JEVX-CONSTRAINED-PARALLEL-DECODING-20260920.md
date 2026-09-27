---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-22"
status: approved
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
---

# PRD-MOC — JEVX Constrained Parallel Decoding Primitive

> **Parent** : INTENT-JEVX-SOVEREIGN-OVERLAY.md (`0xINTENT_JEVX_SOVEREIGN_OVERLAY_20260919`)
> **Périmètre** : ce dépôt uniquement — création de la primitive `constrained-parallel-decoding` et intégration dans le MDU.
> **Coordination transverse** : voir MOC JEVX §3 (livrables, dépendances).

---

## 1. Objectif

Créer une primitive MDU pour le pattern de décodage parallèle contraint, issu de `jevmlx` et transposé pour `llama.cpp` CPU. Cette primitive permet d'évaluer plusieurs champs de décision en une seule passe, réduisant la latence sub-seconde sur Z600/ENV2.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Primitive `constrained-parallel-decoding` | `primitives/constrained-parallel-decoding/design.yaml` | Créer | ✅ |
| L2 | Enregistrement MDU | `META-DESIGN.md`, `meta-design.yaml` | Modifier | ✅ |
| L3 | Index catalog | `catalog/designs.index.yaml` | Modifier | ✅ |
| L4 | Mise à jour PRD-MOC JEVX | `PRD/PRD-MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md` | Modifier | ✅ |

## 3. Tâches

### Phase A — Création primitive
1. `design.yaml` : primitive avec architecture, mécanisme, contraintes, références
2. Validation : YAML valide + lint Markdown

### Phase B — Enregistrement MDU
3. `META-DESIGN.md` : ajout section primitives JEVX
4. `meta-design.yaml` : ajout entrée primitive
5. `catalog/designs.index.yaml` : ajout entrée primitive

### Phase C — Intégration
6. Mise à jour PRD-MOC JEVX : ajout livrable L5
7. Validation pre-commit PASS

## 4. Contraintes

- **CPU-only** : GPU interdit (ENV2 / Z600)
- **WSL1** : compatible via llama.cpp AVX1
- **Latence** : < 1000 ms par batch
- **Batch size** : max 16 champs
- **SLM** : tâche atomique, un fichier par modification
- **UTF-8** : strict
- **Commits** : atomiques <= 3 fichiers

## 5. Plan de commits

| Commit | Fichiers | Description |
|---|---|---|
| `feat(jevx): add constrained-parallel-decoding primitive` | `primitives/constrained-parallel-decoding/design.yaml` | Création primitive |
| `docs(jevx): register primitive in MDU` | `META-DESIGN.md`, `meta-design.yaml` | Enregistrement MDU |
| `docs(jevx): update catalog and PRD-MOC` | `catalog/designs.index.yaml`, `PRD/PRD-MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md` | Index + PRD-MOC |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : `python scripts/validate_designs.py --strict primitives/constrained-parallel-decoding/design.yaml`
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. La primitive `constrained-parallel-decoding` est créée et valide YAML.
2. La primitive est enregistrée dans `META-DESIGN.md` et `meta-design.yaml`.
3. La primitive est référencée dans `catalog/designs.index.yaml`.
4. Le PRD-MOC JEVX est mis à jour avec le nouveau livrable.
5. Les pre-commit hooks passent.

## 8. Proof-of-Life

- [x] 2026-09-20T21:06:00+02:00 — Création primitive `constrained-parallel-decoding`
- [x] 2026-09-20T21:06:00+02:00 — Enregistrement MDU
- [x] 2026-09-20T21:06:00+02:00 — Mise à jour catalog et PRD-MOC
- [x] 2026-09-20T21:06:00+02:00 — Validation pre-commit PASS

## 9. Évaluation

| Critère d'acceptation | État | Preuve |
|---|---|---|
| 1. Primitive créée | ✅ | `primitives/constrained-parallel-decoding/design.yaml` |
| 2. Enregistrée MDU | ✅ | `META-DESIGN.md` + `meta-design.yaml` |
| 3. Référencée catalog | ✅ | `catalog/designs.index.yaml` |
| 4. PRD-MOC JEVX mis à jour | ✅ | Section 3 + Proof-of-Life |
| 5. Pre-commit PASS | ✅ | PASS sur commits atomiques |

**Verdict** : ✅ **Prod-ready opérationnel 100%**

## 10. Références

- **ADR** : ADR-0111-JEVX-SOVEREIGN-OVERLAY
- **Intent** : INTENT-JEVX-SOVEREIGN-OVERLAY
- **Design** : jevx-engineering
- **Atom** : typed-decision-api
- **MDU** : META-DESIGN.md, meta-design.yaml
- **Référence externe** : `jevmlx` (KV cache broadcast)
