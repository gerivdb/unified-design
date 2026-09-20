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
---

# PRD-MOC — JEVX Sovereign Adapter Pattern Primitive

> **Parent** : INTENT-JEVX-SOVEREIGN-OVERLAY.md (`0xINTENT_JEVX_SOVEREIGN_OVERLAY_20260919`)
> **Périmètre** : ce dépôt uniquement — création de la primitive `sovereign-adapter-pattern` et intégration dans le MDU.
> **Coordination transverse** : voir MOC JEVX §3 (livrables, dépendances).

---

## 1. Objectif

Créer une primitive MDU pour le pattern d'adaptateur souverain JEVX. Traduit l'état Jev en prompt de classification, valide JSON, normalise probabilités. Transposition Python de l'adaptateur TypeScript `localjev` pour WSL1/ENV2.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Primitive `sovereign-adapter-pattern` | `primitives/sovereign-adapter-pattern/design.yaml` | Créer | ✅ |
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
6. Mise à jour PRD-MOC JEVX : ajout livrable L6
7. Validation pre-commit PASS

## 4. Contraintes

- **WSL1** : compatible via Python 3.12 + llama.cpp AVX1
- **JSON strict** : response_format = json_schema
- **Temperature** : 0
- **Retry** : max 2 avec context_injection
- **SLM** : tâche atomique, un fichier par modification
- **UTF-8** : strict
- **Commits** : atomiques <= 3 fichiers

## 5. Plan de commits

| Commit | Fichiers | Description |
|---|---|---|
| `feat(jevx): add sovereign-adapter-pattern primitive` | `primitives/sovereign-adapter-pattern/design.yaml` | Création primitive |
| `docs(jevx): register primitive in MDU` | `META-DESIGN.md`, `meta-design.yaml` | Enregistrement MDU |
| `docs(jevx): update catalog and PRD-MOC` | `catalog/designs.index.yaml`, `PRD/PRD-MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md` | Index + PRD-MOC |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : `python scripts/validate_designs.py --strict primitives/sovereign-adapter-pattern/design.yaml`
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. La primitive `sovereign-adapter-pattern` est créée et valide YAML.
2. La primitive est enregistrée dans `META-DESIGN.md` et `meta-design.yaml`.
3. La primitive est référencée dans `catalog/designs.index.yaml`.
4. Le PRD-MOC JEVX est mis à jour avec le nouveau livrable.
5. Les pre-commit hooks passent.

## 8. Proof-of-Life

- [x] 2026-09-20T21:06:00+02:00 — Création primitive `sovereign-adapter-pattern`
- [x] 2026-09-20T21:06:00+02:00 — Enregistrement MDU
- [x] 2026-09-20T21:06:00+02:00 — Mise à jour catalog et PRD-MOC
- [x] 2026-09-20T21:06:00+02:00 — Validation pre-commit PASS

## 9. Évaluation

| Critère d'acceptation | État | Preuve |
|---|---|---|
| 1. Primitive créée | ✅ | `primitives/sovereign-adapter-pattern/design.yaml` |
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
- **Référence externe** : `githubnext/localjev` (adaptateur TypeScript)
