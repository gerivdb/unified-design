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

# PRD-MOC — JEVX Backend Selector Skill

> **Parent** : INTENT-JEVX-SOVEREIGN-OVERLAY.md (`0xINTENT_JEVX_SOVEREIGN_OVERLAY_20260919`)
> **Périmètre** : ce dépôt uniquement — création du skill `jevx-backend-selector` et intégration dans le MDU.
> **Coordination transverse** : voir MOC JEVX §3 (livrables, dépendances).

---

## 1. Objectif

Créer un skill KiloCode capable de sélectionner le backend JEVX optimal selon les contraintes matérielles (Z600/ENV2), la latence cible et le cas d'usage. Le skill s'appuie sur `designs/jevx-backend-matrix.yaml` et les profils `hardware_profile` du MDU.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Skill `jevx-backend-selector` | `skills/jevx-backend-selector/SKILL.md` | Créer | ✅ |
| L2 | Enregistrement MDU | `META-DESIGN.md`, `meta-design.yaml` | Modifier | ✅ |
| L3 | Index catalog | `catalog/designs.index.yaml` | Modifier | ✅ |
| L4 | Mise à jour PRD-MOC JEVX | `PRD/PRD-MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md` | Modifier | ✅ |

## 3. Tâches

### Phase A — Création skill
1. `SKILL.md` : triggers, inputs/outputs, processus de sélection, exemples
2. Validation : lint Markdown + vérification frontmatter

### Phase B — Enregistrement MDU
3. `META-DESIGN.md` : ajout section skills JEVX
4. `meta-design.yaml` : ajout entrée skill
5. `catalog/designs.index.yaml` : ajout entrée skill

### Phase C — Intégration
6. Mise à jour PRD-MOC JEVX : ajout livrable L7
7. Validation pre-commit PASS

## 4. Contraintes

- **SLM** : tâche atomique, un fichier par modification
- **UTF-8** : strict (hook pre-commit bloque non-ASCII)
- **Commits** : atomiques <= 3 fichiers
- **BDCP** : pas de sortie réseau non médiée

## 5. Plan de commits

| Commit | Fichiers | Description |
|---|---|---|
| `feat(jevx): add backend selector skill` | `skills/jevx-backend-selector/SKILL.md` | Création skill |
| `docs(jevx): register skill in MDU` | `META-DESIGN.md`, `meta-design.yaml` | Enregistrement MDU |
| `docs(jevx): update catalog and PRD-MOC` | `catalog/designs.index.yaml`, `PRD/PRD-MOC-JEVX-SOVEREIGN-OVERLAY-20260920.md` | Index + PRD-MOC |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : `gerivdb design validate --strict` ; hooks pre-commit
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. Le skill `jevx-backend-selector` est créé avec frontmatter valide.
2. Le skill est enregistré dans `META-DESIGN.md` et `meta-design.yaml`.
3. Le skill est référencé dans `catalog/designs.index.yaml`.
4. Le PRD-MOC JEVX est mis à jour avec le nouveau livrable.
5. Les pre-commit hooks passent.

## 8. Proof-of-Life

- [x] 2026-09-20T21:06:00+02:00 — Création skill `jevx-backend-selector`
- [x] 2026-09-20T21:06:00+02:00 — Enregistrement MDU
- [x] 2026-09-20T21:06:00+02:00 — Mise à jour catalog et PRD-MOC
- [x] 2026-09-20T21:06:00+02:00 — Validation pre-commit PASS

## 9. Évaluation

| Critère d'acceptation | État | Preuve |
|---|---|---|
| 1. Skill créé | ✅ | `skills/jevx-backend-selector/SKILL.md` |
| 2. Enregistré MDU | ✅ | `META-DESIGN.md` + `meta-design.yaml` |
| 3. Référencé catalog | ✅ | `catalog/designs.index.yaml` |
| 4. PRD-MOC JEVX mis à jour | ✅ | Section 3 + Proof-of-Life |
| 5. Pre-commit PASS | ✅ | PASS sur commits atomiques |

**Verdict** : ✅ **Prod-ready opérationnel 100%**

## 10. Références

- **ADR** : ADR-0111-JEVX-SOVEREIGN-OVERLAY
- **Intent** : INTENT-JEVX-SOVEREIGN-OVERLAY
- **Design** : jevx-backend-matrix
- **Atom** : typed-decision-api
- **MDU** : META-DESIGN.md, meta-design.yaml
