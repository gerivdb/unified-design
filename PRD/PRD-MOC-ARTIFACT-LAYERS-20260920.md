---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-20"
status: proposed
intent_hash: 0xPRD_MOC_ARTIFACT_LAYERS_20260920
author: gerivdb
source_repo: gerivdb/unified-design
source_path: PRD/PRD-MOC-ARTIFACT-LAYERS-20260920.md
parent_doc: PRD-MOC-ECOSYSTEM-META-COHERENCE-EXTENSION-20260920.md
related_adr: ADR-2026-09-19-SAFE-ACTION-PATTERN.md
related_intent: INTENT-2026-09-19-SAFE-ACTION-PATTERN.md
related_moc: PRD-MOC-ECOSYSTEM-META-COHERENCE-20260920.md
governance:
  strate: L0-CANON
  profil: master
  rss_depth: 0
---

# PRD-MOC — ARTIFACT-LAYERS : structure causale standardisée des repos

> **Parent** : PRD-MOC-ECOSYSTEM-META-COHERENCE-EXTENSION-20260920.md
> **Périmètre** : design `artifact-layers-design`, primitive `artifact-layers-primitive`, skill `artifact-layers-validator`, citizen `artifact-layers-auditor`, workflow `workflow-artifact-layers-validation`.

---

## 1. Objectif

Standardiser la structure causale de chaque repo gerivdb en 7 layers obligatoires : `src/`, `config/`, `tools/`, `scripts/`, `tests/`, `docs/`, `markdown/`. Ce design apporte l’élégance : un repo = une structure prévisible = une validation automatisable.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type |
|---|---|---|---|
| L1 | Design `artifact-layers-design` | `designs/artifact-layers-design/design.yaml` | Créer |
| L2 | Primitive `artifact-layers-primitive` | `primitives/artifact-layers-primitive.yaml` | Créer |
| L3 | Skill `artifact-layers-validator` | `skills/artifact-layers-validator/SKILL.md` | Créer |
| L4 | Citizen `artifact-layers-auditor` | `citizens/artifact-layers-auditor/citizen.yaml` | Créer |
| L5 | Workflow `workflow-artifact-layers-validation` | `workflows/workflow-artifact-layers-validation.md` | Créer |

## 3. Tâches

### Phase A — Design et primitive
1. `designs/artifact-layers-design/design.yaml` : 7 layers, states, functions, invariant, genes, anti_patterns, depends_on, inherits, cross_references
2. `primitives/artifact-layers-primitive.yaml` : primitive réutilisable pour validation structure repo

### Phase B — Skill et citizen
3. `skills/artifact-layers-validator/SKILL.md` : skill de validation structure repo
4. `citizens/artifact-layers-auditor/citizen.yaml` : citizen audit structure repos

### Phase C — Workflow et enregistrement
5. `workflows/workflow-artifact-layers-validation.md` : workflow déclaré
6. Mise à jour `META-DESIGN.md`, `meta-design.yaml`, catalogues

## 4. Contraintes

- Encodage UTF-8 strict
- Chaque YAML suit le template MDU
- Commits atomiques <= 3 fichiers
- Les 7 layers sont obligatoires : `src/`, `config/`, `tools/`, `scripts/`, `tests/`, `docs/`, `markdown/`
- Pas de doublon avec `ecosystem-artifact-layers-design` si existant

## 5. Critères d’acceptation

1. `design.yaml` parse YAML valide et passe `validate_designs.py --strict`.
2. Primitive créée et référencée dans `primitives.index.yaml`.
3. Skill créé et référencé dans `skills.index.yaml`.
4. Citizen créé et référencé dans `citizens.index.yaml`.
5. Workflow créé.
6. `META-DESIGN.md` et `meta-design.yaml` mis à jour.
7. Aucune violation DAG.

## 6. Proof-of-Life

- [ ] 2026-09-20T22:21:00Z — Création design `artifact-layers-design`
- [ ] 2026-09-20T22:21:00Z — Création primitive `artifact-layers-primitive`
- [ ] 2026-09-20T22:21:00Z — Création skill `artifact-layers-validator`
- [ ] 2026-09-20T22:21:00Z — Création citizen `artifact-layers-auditor`
- [ ] 2026-09-20T22:21:00Z — Création workflow `workflow-artifact-layers-validation`
- [ ] 2026-09-20T22:21:00Z — Mise à jour MDU et catalogues
- [ ] 2026-09-20T22:21:00Z — Validation YAML + hooks PASS

## 7. Références

- **Parent MDU** : `ecosystem-meta-coherence`, `artifact-layers-design` (unified-design)
- **Designs MDU** : `designs/ecosystem-artifact-layers-design/design.yaml` (si existant)
