---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-22"
status: approved
intent_hash: 0xPRD_MOC_SESSION_BOOT_20260920
author: gerivdb
source_repo: gerivdb/GOVERNANCE-HUB
source_path: PRD-MOC/PRD-MOC-SESSION-BOOT-20260920.md
parent_doc: PRD-MOC-ECOSYSTEM-META-COHERENCE-EXTENSION-20260920.md
related_adr: ADR-2026-09-19-SAFE-ACTION-PATTERN.md
related_intent: INTENT-2026-09-19-SAFE-ACTION-PATTERN.md
related_moc: PRD-MOC-ECOSYSTEM-META-COHERENCE-20260920.md
governance:
  strate: L0-CANON
  profil: master
  rss_depth: 0
---

# PRD-MOC — SESSION-BOOT : checks BOOT/CLOSEOUT standardisés

> **Parent** : PRD-MOC-ECOSYSTEM-META-COHERENCE-EXTENSION-20260920.md
> **Périmètre** : design `session-boot-design`, primitive `session-boot-primitive`, skill `session-boot-skill`, citizen `session-boot-citizen`, workflow `workflow-session-boot-closeout`, pipeline `pipeline-session-boot-closeout`.

---

## 1. Objectif

Standardiser les checks BOOT (démarrage) et CLOSEOUT (fin) de session multi-repo via un design, une primitive, un skill, un citizen et un workflow déclarés. Ce design apporte la fluidité : une session = un boot vérifié + un closeout automatique.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type |
|---|---|---|---|
| L1 | Design `session-boot-design` | `designs/session-boot-design/design.yaml` | Créer |
| L2 | Primitive `session-boot-primitive` | `primitives/session-boot-primitive.yaml` | Créer |
| L3 | Skill `session-boot-skill` | `skills/session-boot-skill/SKILL.md` | Créer |
| L4 | Citizen `session-boot-citizen` | `citizens/session-boot-citizen/citizen.yaml` | Créer |
| L5 | Workflow `workflow-session-boot-closeout` | `workflows/workflow-session-boot-closeout.md` | Créer |

## 3. Tâches

### Phase A — Design et primitive
1. `designs/session-boot-design/design.yaml` : states IDLE/BOOT/CLOSEOUT, functions, invariant, genes, anti_patterns, depends_on, inherits, cross_references
2. `primitives/session-boot-primitive.yaml` : primitive réutilisable pour checks BOOT/CLOSEOUT

### Phase B — Skill et citizen
3. `skills/session-boot-skill/SKILL.md` : skill d’exécution BOOT/CLOSEOUT
4. `citizens/session-boot-citizen/citizen.yaml` : citizen exécution BOOT/CLOSEOUT

### Phase C — Workflow et enregistrement
5. `workflows/workflow-session-boot-closeout.md` : workflow déclaré
6. Mise à jour `META-DESIGN.md`, `meta-design.yaml`, catalogues

## 4. Contraintes

- Encodage UTF-8 strict
- Chaque YAML suit le template MDU
- Commits atomiques <= 3 fichiers
- Hérite de `ecosystem-meta-coherence` et `session-boot-sequence` (GOVERNANCE-HUB)
- Pas de doublon avec `session_boot.py` : ce dernier est l’implémentation, ce design est la spécification

## 5. Critères d’acceptation

1. `design.yaml` parse YAML valide et passe `validate_designs.py --strict`.
2. Primitive créée et référencée dans `primitives.index.yaml`.
3. Skill créé et référencé dans `skills.index.yaml`.
4. Citizen créé et référencé dans `citizens.index.yaml`.
5. Workflow créé.
6. `META-DESIGN.md` et `meta-design.yaml` mis à jour.
7. Aucune violation DAG.

## 6. Proof-of-Life

- [ ] 2026-09-20T22:21:00Z — Création design `session-boot-design`
- [ ] 2026-09-20T22:21:00Z — Création primitive `session-boot-primitive`
- [ ] 2026-09-20T22:21:00Z — Création skill `session-boot-skill`
- [ ] 2026-09-20T22:21:00Z — Création citizen `session-boot-citizen`
- [ ] 2026-09-20T22:21:00Z — Création workflow `workflow-session-boot-closeout`
- [ ] 2026-09-20T22:21:00Z — Mise à jour MDU et catalogues
- [ ] 2026-09-20T22:21:00Z — Validation YAML + hooks PASS

## 7. Références

- **Parent MDU** : `ecosystem-meta-coherence`, `session-boot-sequence` (GOVERNANCE-HUB)
- **Designs MDU** : `designs/ecosystem-meta-coherence/design.yaml`
- **Scripts** : `scripts/session_boot.py`
