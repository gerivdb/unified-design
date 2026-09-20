---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-20"
status: proposed
intent_hash: 0xPRD_MOC_ECOSYSTEM_META_COHERENCE_20260920
author: gerivdb
source_repo: gerivdb/unified-design
parent_doc: INTENT-2026-09-19-SAFE-ACTION-PATTERN.md
governance:
  strate: L0-CANON
  profil: master
  rss_depth: 0
related_adr: ADR-2026-09-19-SAFE-ACTION-PATTERN.md
related_intent: INTENT-2026-09-19-SAFE-ACTION-PATTERN.md
related_moc: MOC-ECOSYSTEM-META-COHERENCE-20260920.md
---

# PRD-MOC — ECOSYSTEM-META-COHERENCE : corrections structurelles et causales Think/Do/Check

> **Parent** : INTENT-2026-09-19-SAFE-ACTION-PATTERN.md
> **Périmètre** : ce dépôt uniquement — création du design `ecosystem-meta-coherence`, de l'atom `ecosystem-meta-coherence-gate`, de la primitive, des skills, workflows, citizen et pipeline associés.
> **Coordination transverse** : voir MOC §3 (livrables, dépendances).

---

## 1. Objectif

Intégrer `ecosystem-meta-coherence` comme design officiel du MDU couvrant les corrections structurelles et causales de l'écosystème, en alignant :
- **Think** : les besoins de l'écosystème
- **Do** : l'écosystème lui-même
- **Check** : la vérification de l'écosystème

Fusionne `meta-coherence` (détection d'écarts cross-repo) et `friction-analyzer` (corrections structurelles de session) en un pattern unifié de gouvernance adaptative.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type |
|---|---|---|---|
| L1 | Design `ecosystem-meta-coherence` | `designs/ecosystem-meta-coherence/design.yaml` | Créer |
| L2 | Atom `ecosystem-meta-coherence-gate` | `atoms/ecosystem-meta-coherence-gate.md` | Créer |
| L3 | Primitive `ecosystem-meta-coherence` | `primitives/ecosystem-meta-coherence.yaml` | Créer |
| L4 | Skill `ecosystem-meta-coherence-analyzer` | `skills/ecosystem-meta-coherence-analyzer/SKILL.md` | Créer |
| L5 | Skill `dryrun-causal-auditor` | `skills/dryrun-causal-auditor/SKILL.md` | Créer |
| L6 | Workflow `dryrun-causal-audit` | `workflows/dryrun-causal-audit.md` | Créer |
| L7 | Workflow `structural-fix-pipeline` | `workflows/structural-fix-pipeline.md` | Créer |
| L8 | Citizen `meta-coherence-auditor` | `citizens/meta-coherence-auditor/citizen.yaml` | Créer |
| L9 | Pipeline `mdu-validation` | `pipelines/mdu-validation.yaml` | Créer |
| L10 | Mise à jour `META-DESIGN.md` | `META-DESIGN.md` | Modifier |
| L11 | Mise à jour `meta-design.yaml` | `meta-design.yaml` | Modifier |
| L12 | Mise à jour catalogues | `catalog/*.yaml` | Modifier |

## 3. Tâches

### Phase A — Design et atom
1. `ecosystem-meta-coherence/design.yaml` : design avec states, functions, invariant, genes, anti_patterns, depends_on, inherits, cross_references
2. `ecosystem-meta-coherence-gate.md` : atom enforceable
3. `ecosystem-meta-coherence.yaml` : primitive réutilisable

### Phase B — Skills et workflows
4. `ecosystem-meta-coherence-analyzer/SKILL.md` : skill d'analyse TALEX
5. `dryrun-causal-auditor/SKILL.md` : skill de vérification prod-ready
6. `dryrun-causal-audit.md` : workflow de dryrun causal
7. `structural-fix-pipeline.md` : workflow de corrections structurelles

### Phase C — Citizen et pipeline
8. `meta-coherence-auditor/citizen.yaml` : citizen auditeur
9. `mdu-validation.yaml` : pipeline CI

### Phase D — Enregistrement MDU
10. `META-DESIGN.md` : enregistrement design + atom + workflows + skills
11. `meta-design.yaml` : ajout entrées dans `designs:`, `governance_atoms:`, etc.
12. Catalogues : mise à jour `skills.index.yaml`, `primitives.index.yaml`, `citizens.index.yaml`

## 4. Contraintes

- Encodage UTF-8 strict
- Chaque YAML suit le template MDU
- Commits atomiques <= 3 fichiers
- Pas de doublon avec `meta-coherence` : `ecosystem-meta-coherence` est la version opérationnelleThink/Do/Check
- Pas de doublon avec `friction-analyzer` : ce dernier est un runner TALEX, pas un design MDU

## 5. Plan de commits proposé

| Commit | Fichiers |
|---|---|
| `feat(design): add ecosystem-meta-coherence` | `designs/ecosystem-meta-coherence/design.yaml` |
| `feat(meta): register ecosystem-meta-coherence design and atom` | `atoms/ecosystem-meta-coherence-gate.md`, `META-DESIGN.md`, `meta-design.yaml` |
| `feat(primitive): add ecosystem-meta-coherence primitive` | `primitives/ecosystem-meta-coherence.yaml` |
| `feat(skills): add ecosystem-meta-coherence-analyzer and dryrun-causal-auditor` | `skills/ecosystem-meta-coherence-analyzer/SKILL.md`, `skills/dryrun-causal-auditor/SKILL.md` |
| `feat(workflows): add dryrun-causal-audit and structural-fix-pipeline` | `workflows/dryrun-causal-audit.md`, `workflows/structural-fix-pipeline.md` |
| `feat(citizen): add meta-coherence-auditor citizen` | `citizens/meta-coherence-auditor/citizen.yaml` |
| `feat(pipeline): add mdu-validation pipeline` | `pipelines/mdu-validation.yaml` |
| `chore(catalog): register new skills, primitives, and citizens` | `catalog/skills.index.yaml`, `catalog/primitives.index.yaml`, `catalog/citizens.index.yaml` |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : `validate_designs.py --strict` ; hooks pre-commit (`design-validate`, `branch-taxonomy-check`, `ascii-fixer`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. Le design `ecosystem-meta-coherence/design.yaml` parse en YAML valide et passe `validate_designs.py --strict`.
2. L'atom `ecosystem-meta-coherence-gate.md` est créé et référencé dans `META-DESIGN.md` et `meta-design.yaml`.
3. La primitive `ecosystem-meta-coherence.yaml` est créée et référencée dans `primitives.index.yaml`.
4. Les skills `ecosystem-meta-coherence-analyzer` et `dryrun-causal-auditor` sont créés et référencés dans `skills.index.yaml`.
5. Les workflows `dryrun-causal-audit` et `structural-fix-pipeline` sont créés.
6. Le citizen `meta-coherence-auditor` est créé et référencé dans `citizens.index.yaml`.
7. Le pipeline `mdu-validation` est créé.
8. Aucune violation DAG n'est introduite.
9. Les pre-commit hooks passent sans blocage encoding.
10. Le mapping `ecosystem-meta-coherence` → MDU est documenté.

## 8. Proof-of-Life

- [x] 2026-09-20T04:00:00+02:00 — Création PRD-MOC ECOSYSTEM-META-COHERENCE
- [x] 2026-09-20T04:00:00+02:00 — Création design `ecosystem-meta-coherence/design.yaml`
- [x] 2026-09-20T04:00:00+02:00 — Création atom `ecosystem-meta-coherence-gate.md`
- [x] 2026-09-20T04:00:00+02:00 — Création primitive `ecosystem-meta-coherence.yaml`
- [x] 2026-09-20T04:00:00+02:00 — Création skills `ecosystem-meta-coherence-analyzer` et `dryrun-causal-auditor`
- [x] 2026-09-20T04:00:00+02:00 — Création workflows `dryrun-causal-audit` et `structural-fix-pipeline`
- [x] 2026-09-20T04:00:00+02:00 — Création citizen `meta-coherence-auditor`
- [x] 2026-09-20T04:00:00+02:00 — Création pipeline `mdu-validation`
- [x] 2026-09-20T04:00:00+02:00 — Mise à jour `META-DESIGN.md` et `meta-design.yaml`
- [x] 2026-09-20T04:00:00+02:00 — Mise à jour catalogues
- [x] 2026-09-20T06:04:17+02:00 — Dryrun causal : tous les livrables présents, YAML valide, frontmatter valide, hooks PASS
- [x] 2026-09-20T06:04:17+02:00 — Analyse TALEX : 7 frictions identifiées, 5 P1/P2 corrigées, 1 P3 warning only

### Résultats d'audit dryrun causal

| Vérification | Résultat |
|---|---|
| `designs/ecosystem-meta-coherence/design.yaml` présent | ✅ |
| `atoms/ecosystem-meta-coherence-gate.md` présent | ✅ |
| `primitives/ecosystem-meta-coherence.yaml` présent | ✅ |
| `skills/ecosystem-meta-coherence-analyzer/SKILL.md` présent | ✅ |
| `skills/dryrun-causal-auditor/SKILL.md` présent | ✅ |
| `workflows/dryrun-causal-audit.md` présent | ✅ |
| `workflows/structural-fix-pipeline.md` présent | ✅ |
| `citizens/meta-coherence-auditor/citizen.yaml` présent | ✅ |
| `pipelines/mdu-validation.yaml` présent | ✅ |
| `META-DESIGN.md` enregistre `ecosystem-meta-coherence` | ✅ |
| `meta-design.yaml` enregistre `ecosystem-meta-coherence` | ✅ |
| `catalog/skills.index.yaml` enregistre les skills | ✅ |
| `catalog/primitives.index.yaml` enregistre la primitive | ✅ |
| `catalog/citizens.index.yaml` enregistre le citizen | ✅ |
| YAML valide (`design.yaml`) | ✅ |
| YAML valide (`meta-design.yaml`) | ✅ |
| `validate_designs.py --strict` ciblé PASS | ✅ |
| Pre-commit PASS | ✅ |
| Merge sur `main` réussi | ✅ |

## 9. Évaluation finale

| Critère d'acceptation | État | Preuve |
|---|---|---|
| 1. `design.yaml` parse YAML valide + passe validation | ✅ | `validate_designs.py --strict` PASS |
| 2. `ecosystem-meta-coherence-gate.md` créé et référencé MDU | ✅ | `META-DESIGN.md` + `meta-design.yaml` |
| 3. Primitive créée et référencée | ✅ | `primitives.index.yaml` |
| 4. Skills créés et référencés | ✅ | `skills.index.yaml` |
| 5. Workflows créés | ✅ | `workflows/dryrun-causal-audit.md`, `workflows/structural-fix-pipeline.md` |
| 6. Citizen créé et référencé | ✅ | `citizens.index.yaml` |
| 7. Pipeline créé | ✅ | `pipelines/mdu-validation.yaml` |
| 8. Aucune violation DAG | ✅ | `depends_on` cohérent, pas de cycle |
| 9. Pre-commit hooks passent | ✅ | PASS sur tous les commits |
| 10. Mapping documenté | ✅ | `cross_references` dans design.yaml |

**Verdict** : ✅ **Prod-ready opérationnel 100%** — tous les livrables sont implémentés, validés et intégrés dans le MDU.

## 10. Références

- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Atom** : `atoms/ecosystem-meta-coherence-gate.md`
- **Primitive** : `primitives/ecosystem-meta-coherence.yaml`
- **Skills** : `skills/ecosystem-meta-coherence-analyzer/SKILL.md`, `skills/dryrun-causal-auditor/SKILL.md`
- **Workflows** : `workflows/dryrun-causal-audit.md`, `workflows/structural-fix-pipeline.md`
- **Citizen** : `citizens/meta-coherence-auditor/citizen.yaml`
- **Pipeline** : `pipelines/mdu-validation.yaml`
- **MDU** : `META-DESIGN.md`, `meta-design.yaml`
- **Parent MDU** : `meta-coherence`, `chain-fluidity`, `safe-action-pattern`
- **Designs MDU** : `designs/meta-coherence.yaml`, `designs/chain-fluidity.yaml`, `designs/safe-action-pattern.yaml`
