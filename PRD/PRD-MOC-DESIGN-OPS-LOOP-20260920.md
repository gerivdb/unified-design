---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-20"
status: proposed
intent_hash: 0xPRD_MOC_DESIGN_OPS_LOOP_20260920
author: gerivdb
source_repo: gerivdb/unified-design
source_path: PRD/PRD-MOC-DESIGN-OPS-LOOP-20260920.md
parent_doc: PRD-MOC-ECOSYSTEM-META-COHERENCE-EXTENSION-20260920.md
related_adr: ADR-2026-09-19-SAFE-ACTION-PATTERN.md
related_intent: INTENT-2026-09-19-SAFE-ACTION-PATTERN.md
related_moc: PRD-MOC-ECOSYSTEM-META-COHERENCE-20260920.md
governance:
  strate: L0-CANON
  profil: master
  rss_depth: 0
---

# PRD-MOC — DESIGN-OPS-LOOP : boucle THINK/DO/CHECK opérationnelle

> **Parent** : PRD-MOC-ECOSYSTEM-META-COHERENCE-EXTENSION-20260920.md
> **Périmètre** : design `design-ops-loop`, primitive `design-ops-loop-primitive`, skill `design-ops-loop-skill`, citizen `design-ops-loop-citizen`, workflow `workflow-design-ops-loop`.

---

## 1. Objectif

Orchestrer la boucle THINK → DO → CHECK du MDU : perception des besoins, exécution des corrections, validation du réel. Ce design est le **père opérationnel** de `ecosystem-meta-coherence` : il ne détecte pas les frictions, il les orchestre.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type |
|---|---|---|---|
| L1 | Design `design-ops-loop` | `designs/design-ops-loop/design.yaml` | Créer |
| L2 | Primitive `design-ops-loop-primitive` | `primitives/design-ops-loop-primitive.yaml` | Créer |
| L3 | Skill `design-ops-loop-skill` | `skills/design-ops-loop-skill/SKILL.md` | Créer |
| L4 | Citizen `design-ops-loop-citizen` | `citizens/design-ops-loop-citizen/citizen.yaml` | Créer |
| L5 | Workflow `workflow-design-ops-loop` | `workflows/workflow-design-ops-loop.md` | Créer |

## 3. Tâches

### Phase A — Design et primitive
1. `designs/design-ops-loop/design.yaml` : states THINK/DO/CHECK, functions F1-F9, invariant, genes, anti_patterns, depends_on, inherits, cross_references
2. `primitives/design-ops-loop-primitive.yaml` : primitive réutilisable pour tout design voulant s’inscrire dans THINK/DO/CHECK

### Phase B — Skill et citizen
3. `skills/design-ops-loop-skill/SKILL.md` : skill d’orchestration THINK/DO/CHECK
4. `citizens/design-ops-loop-citizen/citizen.yaml` : citizen pilote de boucle

### Phase C — Workflow et enregistrement
5. `workflows/workflow-design-ops-loop.md` : workflow déclaré
6. Mise à jour `META-DESIGN.md`, `meta-design.yaml`, catalogues

## 4. Contraintes

- Encodage UTF-8 strict
- Chaque YAML suit le template MDU
- Commits atomiques <= 3 fichiers
- Hérite de `ecosystem-meta-coherence` et `chain-fluidity`
- Pas de doublon avec `meta-coherence` (draft) : `design-ops-loop` est la version opérationnelle

## 5. Critères d’acceptation

1. `design.yaml` parse YAML valide et passe `validate_designs.py --strict`.
2. Primitive créée et référencée dans `primitives.index.yaml`.
3. Skill créé et référencé dans `skills.index.yaml`.
4. Citizen créé et référencé dans `citizens.index.yaml`.
5. Workflow créé.
6. `META-DESIGN.md` et `meta-design.yaml` mis à jour.
7. Aucune violation DAG.

## 6. Proof-of-Life

- [ ] 2026-09-20T22:21:00Z — Création design `design-ops-loop`
- [ ] 2026-09-20T22:21:00Z — Création primitive `design-ops-loop-primitive`
- [ ] 2026-09-20T22:21:00Z — Création skill `design-ops-loop-skill`
- [ ] 2026-09-20T22:21:00Z — Création citizen `design-ops-loop-citizen`
- [ ] 2026-09-20T22:21:00Z — Création workflow `workflow-design-ops-loop`
- [ ] 2026-09-20T22:21:00Z — Mise à jour MDU et catalogues
- [ ] 2026-09-20T22:21:00Z — Validation YAML + hooks PASS

## 7. Références

- **Parent MDU** : `ecosystem-meta-coherence`, `chain-fluidity`, `safe-action-pattern`
- **Designs MDU** : `designs/ecosystem-meta-coherence/design.yaml`, `designs/chain-fluidity/design.yaml`
