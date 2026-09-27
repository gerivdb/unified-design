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

# PRD-MOC — Structural Fix Pipeline Update (JEVX Patterns)

> **Parent** : INTENT-JEVX-SOVEREIGN-OVERLAY.md (`0xINTENT_JEVX_SOVEREIGN_OVERLAY_20260919`)
> **Périmètre** : ce dépôt uniquement — mise à jour du workflow `structural-fix-pipeline.md` avec les patterns JEVX.
> **Coordination transverse** : voir MOC JEVX §3 (livrables, dépendances).

---

## 1. Objectif

Mettre à jour le workflow `structural-fix-pipeline.md` pour intégrer les patterns JEVX spécifiques :
- Détection automatique des patterns JEVX (ÉTAPE-1bis)
- Sélection backend via skill `jevx-backend-selector` (ÉTAPE-2bis)
- Application des primitives `constrained-parallel-decoding` et `sovereign-adapter-pattern`

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Workflow `structural-fix-pipeline` | `workflows/structural-fix-pipeline.md` | Modifier | ✅ |
| L2 | Enregistrement MDU | `META-DESIGN.md`, `meta-design.yaml` | Modifier | ✅ |
| L3 | Index catalog | `catalog/designs.index.yaml` | Modifier | ✅ |
| L4 | Mise à jour PRD-MOC JEVX | `PRD/PRD-MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md` | Modifier | ✅ |

## 3. Tâches

### Phase A — Mise à jour workflow
1. `structural-fix-pipeline.md` : ajout ÉTAPE-1bis (détection patterns JEVX) et ÉTAPE-2bis (sélection backend)
2. Validation : lint Markdown

### Phase B — Enregistrement MDU
3. `META-DESIGN.md` : ajout section workflows JEVX
4. `meta-design.yaml` : ajout entrée workflow
5. `catalog/designs.index.yaml` : ajout entrée workflow

### Phase C — Intégration
6. Mise à jour PRD-MOC JEVX : ajout livrable L9
7. Validation pre-commit PASS

## 4. Contraintes

- **SLM** : tâche atomique, un fichier par modification
- **UTF-8** : strict
- **Commits** : atomiques <= 3 fichiers
- **Références** : lier vers skills/primitive/pipeline JEVX correspondants

## 5. Plan de commits

| Commit | Fichiers | Description |
|---|---|---|
| `feat(jevx): update structural-fix-pipeline with JEVX patterns` | `workflows/structural-fix-pipeline.md` | Mise à jour workflow |
| `docs(jevx): register workflow update in MDU` | `META-DESIGN.md`, `meta-design.yaml` | Enregistrement MDU |
| `docs(jevx): update catalog and PRD-MOC` | `catalog/designs.index.yaml`, `PRD/PRD-MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md` | Index + PRD-MOC |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : lint Markdown + validation frontmatter
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. Le workflow `structural-fix-pipeline.md` est mis à jour avec les patterns JEVX.
2. Le workflow est enregistré dans `META-DESIGN.md` et `meta-design.yaml`.
3. Le workflow est référencé dans `catalog/designs.index.yaml`.
4. Le PRD-MOC JEVX est mis à jour avec le nouveau livrable.
5. Les pre-commit hooks passent.

## 8. Proof-of-Life

- [x] 2026-09-20T21:06:00+02:00 — Mise à jour workflow `structural-fix-pipeline.md`
- [x] 2026-09-20T21:06:00+02:00 — Enregistrement MDU
- [x] 2026-09-20T21:06:00+02:00 — Mise à jour catalog et PRD-MOC
- [x] 2026-09-20T21:06:00+02:00 — Validation pre-commit PASS

## 9. Évaluation

| Critère d'acceptation | État | Preuve |
|---|---|---|
| 1. Workflow mis à jour | ✅ | `workflows/structural-fix-pipeline.md` |
| 2. Enregistré MDU | ✅ | `META-DESIGN.md` + `meta-design.yaml` |
| 3. Référencé catalog | ✅ | `catalog/designs.index.yaml` |
| 4. PRD-MOC JEVX mis à jour | ✅ | Section 3 + Proof-of-Life |
| 5. Pre-commit PASS | ✅ | PASS sur commits atomiques |

**Verdict** : ✅ **Prod-ready opérationnel 100%**

## 10. Références

- **ADR** : ADR-0111-JEVX-SOVEREIGN-OVERLAY
- **Intent** : INTENT-JEVX-SOVEREIGN-OVERLAY
- **Skill** : jevx-backend-selector
- **Primitives** : constrained-parallel-decoding, sovereign-adapter-pattern
- **MDU** : META-DESIGN.md, meta-design.yaml
