---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-27"
status: approved
intent_hash: 0xPRD_MOC_UNIFIED_DESIGN_METACOHERENCE_AUTOMATION_20260927
parent_prd: INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md
pole_id: POLE-MEMORY-001
owner: L0-CANON
repo: gerivdb/unified-design
---

# PRD-MOC — Unified-Design Métacohérence Automatisée et Gap-Comblé-ification

## Objectif

Transformer `unified-design` d'un catalogue passif en système actif vérifiable :
- Tout design `active` a un contrat d'implémentation vérifiable
- Tout écart design→code est automatiquement détecté
- Toute correction est tracée causalement
- La métacoherence est enforced mécaniquement

## Périmètre

### P0 — Essentiel

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P0-1 | `design_impl_verifier.py` | `scripts/design_impl_verifier.py` | Vérifie 5 designs test, sortie JSON valide |
| P0-2 | Migration designs VEX vers unified-design | `designs/http-server-design/`, `designs/client-architecture/`, etc. | VEX n'a plus de dossier `design/` local |
| P0-3 | Catalog implementation fields | `catalog/designs.index.yaml` | Champs `implemented`, `coverage_pct`, `last_verified` présents |

### P1 — Important

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P1-1 | `implementation_contract` pour 10 designs actifs | `designs/<name>/implementation_contract.yaml` | 10 designs couverts |
| P1-2 | `metacoherence_gate.py` | `scripts/metacoherence_gate.py` | Audit 30j = 0 mutation sans preuve |
| P1-3 | Hook pre-commit design-verifier | `.kilocode/hooks/pre-commit-design-verifier.py` | Bloque commit si impl manquante |

### P2 — Nice-to-have

| ID | Livrable | Chemin cible | Critère d'acceptation |
|---|---|---|---|
| P2-1 | `gap_combleur.py` | `scripts/gap_combleur.py` | Dry-run détecte gaps |
| P2-2 | Skill `mdu-integrity-checker` | `skills/mdu-integrity-checker/SKILL.md` | Skill documenté |
| P2-3 | ADR backing | `ADR/ADR-2026-09-27-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION.md` | ADR créé et approuvé |

## Plan d'exécution SLM

### Phase 1 — P0 (atomic, 3 commits)

1. `feat(scripts): add design_impl_verifier` — script skeleton + test sur 5 designs
2. `feat(designs): migrate VEX designs to unified-design` — migration + `implementation_contract` minimal
3. `feat(catalog): add implementation fields` — mise à jour `designs.index.yaml`

### Phase 2 — P1 (atomic, 3 commits)

4. `feat(designs): add implementation_contract to 10 active designs` — contrat complet
5. `feat(scripts): add metacoherence_gate` — gate THINK/DO/CHECK
6. `feat(hooks): add pre-commit-design-verifier` — hook bloquant

### Phase 3 — P2 (atomic, 3 commits)

7. `feat(scripts): add gap_combleur` — automatisation gap-comblé-ification
8. `docs(skill): add mdu-integrity-checker` — skill documentation
9. `docs(adr): add metacohérence automation ADR` — ADR backing

## Critères d'acceptation globaux

- [ ] `design_impl_verifier.py --strict unified-design/designs/` : `coverage_pct >= 80%` pour 100% des designs `active`
- [ ] `metacoherence_gate.py --audit-period 30d` : 0 mutation sans preuve
- [ ] `gap_combleur.py --dry-run` : `gaps_detected: 0`
- [ ] Aucun repo n'a de dossier `designs/` ou `design/` local hors unified-design
- [ ] >= 95% des designs `active` ont un ADR backing
- [ ] 100% des designs `active` ont un `intent_hash` valide
- [ ] Hook pre-commit bloque commit si `implementation_contract` manquant

## Références

- **INTENT** : `INTENTS/INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md`
- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Design** : `designs/ecosystem-meta-coherence-gate/design.yaml`
- **Meta-design** : `META-DESIGN.md`
- **Gouvernance** : `DESIGNS_GOVERNANCE.md`
- **Scripts existants** : `scripts/validate_designs.py`, `scripts/design_coverage_scanner.py`, `scripts/compliance_scanner.py`

## Proof-of-Life

- [x] 2026-09-27T23:02:31+02:00 — INTENT approuvé, PRD-MOC créé, évaluation P0/P1/P2 effectuée
- [ ] P0-1 : `design_impl_verifier.py` créé et testé
- [ ] P0-2 : Designs VEX migrés vers unified-design
- [ ] P0-3 : Catalog mis à jour avec champs implementation
- [ ] P1-1 : 10 designs ont `implementation_contract`
- [ ] P1-2 : `metacoherence_gate.py` créé et testé
- [ ] P1-3 : Hook pre-commit créé et testé
- [ ] P2-1 : `gap_combleur.py` créé et testé
- [ ] P2-2 : Skill `mdu-integrity-checker` créé
- [ ] P2-3 : ADR backing créé et approuvé
