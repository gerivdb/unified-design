---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-22"
status: approved
intent_hash: 0xPRD_MOC_ECOSYSTEM_META_COHERENCE_EXTENSION_20260920
author: gerivdb
source_repo: gerivdb/unified-design
source_path: PRD/PRD-MOC-ECOSYSTEM-META-COHERENCE-EXTENSION-20260920.md
parent_doc: PRD-MOC-ECOSYSTEM-META-COHERENCE-20260920.md
related_adr: ADR-2026-09-19-SAFE-ACTION-PATTERN.md
related_intent: INTENT-2026-09-19-SAFE-ACTION-PATTERN.md
related_moc: PRD-MOC-ECOSYSTEM-META-COHERENCE-20260920.md, PRD-MOC-GENERAL-MASTER.md
governance:
  strate: L0-CANON
  profil: master
  rss_depth: 0
---

# PRD-MOC — ECOSYSTEM-META-COHERENCE EXTENSION : pipelines, workflows, primitives, skills, citizens

> **Parent** : PRD-MOC-ECOSYSTEM-META-COHERENCE-20260920.md
> **Périmètre** : extension du design `ecosystem-meta-coherence` vers des pipelines/workflows/primitives/skills/citizens réutilisables et métacohérents.
> **Coordination transverse** : voir PRD-MOC-GENERAL-MASTER.md §3.

---

## 1. Objectif

Compléter l’écosystème `ecosystem-meta-coherence` par des **pipelines**, **workflows**, **primitives**, **skills** et **citizens** déclarés, réutilisables et traçables, pour transformer les scripts existants en capacités écosystémiques standardisées.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type |
|---|---|---|---|
| E1 | Pipeline `pipeline-sot-completeness` | `pipelines/pipeline-sot-completeness.yaml` | Créer |
| E2 | Pipeline `pipeline-yaml-structure-validation` | `pipelines/pipeline-yaml-structure-validation.yaml` | Créer |
| E3 | Pipeline `pipeline-dryrun-causal-audit` | `pipelines/pipeline-dryrun-causal-audit.yaml` | Créer |
| E4 | Pipeline `pipeline-session-boot-closeout` | `pipelines/pipeline-session-boot-closeout.yaml` | Créer |
| E5 | Pipeline `pipeline-friction-analysis-to-fix` | `pipelines/pipeline-friction-analysis-to-fix.yaml` | Créer |
| E6 | Workflow `workflow-dryrun-causal-audit` | `workflows/dryrun-causal-audit.md` | Créer |
| E7 | Workflow `workflow-structural-fix-pipeline` | `workflows/structural-fix-pipeline.md` | Créer |
| E8 | Workflow `workflow-session-boot-closeout` | `workflows/session-boot-closeout.md` | Créer |
| E9 | Workflow `workflow-pre-push-validation` | `workflows/pre-push-validation.md` | Créer |
| E10 | Workflow `workflow-friction-to-fix` | `workflows/friction-to-fix.md` | Créer |
| E11 | Primitive `design-ops-loop-primitive` | `primitives/design-ops-loop-primitive.yaml` | Créer |
| E12 | Primitive `artifact-layers-primitive` | `primitives/artifact-layers-primitive.yaml` | Créer |
| E13 | Primitive `session-boot-primitive` | `primitives/session-boot-primitive.yaml` | Créer |
| E14 | Primitive `causal-traceability-primitive` | `primitives/causal-traceability-primitive.yaml` | Créer |
| E15 | Skill `design-ops-loop-skill` | `skills/design-ops-loop-skill/SKILL.md` | Créer |
| E16 | Skill `artifact-layers-validator` | `skills/artifact-layers-validator/SKILL.md` | Créer |
| E17 | Skill `registry-sync-checker-skill` | `skills/registry-sync-checker-skill/SKILL.md` | Créer |
| E18 | Skill `ontology-term-gate-skill` | `skills/ontology-term-gate-skill/SKILL.md` | Créer |
| E19 | Skill `inventory-reconciler-interpreter-skill` | `skills/inventory-reconciler-interpreter-skill/SKILL.md` | Créer |
| E20 | Skill `session-boot-skill` | `skills/session-boot-skill/SKILL.md` | Créer |
| E21 | Citizen `design-ops-loop-citizen` | `citizens/design-ops-loop-citizen/citizen.yaml` | Créer |
| E22 | Citizen `artifact-layers-auditor` | `citizens/artifact-layers-auditor/citizen.yaml` | Créer |
| E23 | Citizen `session-boot-citizen` | `citizens/session-boot-citizen/citizen.yaml` | Créer |
| E24 | Design `workflow-sot-completeness` | `designs/workflow-sot-completeness/design.yaml` | Créer |
| E25 | Design `workflow-yaml-structure-validator` | `designs/workflow-yaml-structure-validator/design.yaml` | Créer |
| E26 | Design `design-ops-loop` | `designs/design-ops-loop/design.yaml` | Créer |
| E27 | Design `artifact-layers-design` | `designs/artifact-layers-design/design.yaml` | Créer |
| E28 | Design `session-boot-design` | `designs/session-boot-design/design.yaml` | Créer |
| E29 | Mise à jour `META-DESIGN.md` | `META-DESIGN.md` | Modifier |
| E30 | Mise à jour `meta-design.yaml` | `meta-design.yaml` | Modifier |
| E31 | Mise à jour catalogues | `catalog/*.yaml` | Modifier |

## 3. Tâches

### Phase A — Pipelines
1. `pipeline-sot-completeness.yaml` : détection champs manquants → auto-fix → validate → commit
2. `pipeline-yaml-structure-validation.yaml` : backup → parse → validate → fix → re-validate
3. `pipeline-dryrun-causal-audit.yaml` : présence → YAML → frontmatter → MDU → hooks → crossref → merge
4. `pipeline-session-boot-closeout.yaml` : boot_checks → talex → wazaa → 5sexter → closeout → auto_commit → push
5. `pipeline-friction-analysis-to-fix.yaml` : detect_frictions → classify → prioritize → implement_atomic_tasks → validate → record_proof

### Phase B — Workflows
6. `workflows/dryrun-causal-audit.md` : workflow déclaré pour dryrun-causal-auditor
7. `workflows/structural-fix-pipeline.md` : workflow déclaré pour ecosystem-meta-coherence-analyzer
8. `workflows/session-boot-closeout.md` : workflow déclaré pour session_boot.py
9. `workflows/pre-push-validation.md` : workflow déclaré pour pre-push-auditor
10. `workflows/friction-to-fix.md` : workflow déclaré pour friction_analyzer_session.py

### Phase C — Primitives
11. `primitives/design-ops-loop-primitive.yaml` : boucle THINK/DO/CHECK réutilisable
12. `primitives/artifact-layers-primitive.yaml` : 7 layers standards d’un repo
13. `primitives/session-boot-primitive.yaml` : checks BOOT obligatoires
14. `primitives/causal-traceability-primitive.yaml` : format friction → root cause → fix → proof

### Phase D — Skills
15. `skills/design-ops-loop-skill/SKILL.md` : orchestration THINK/DO/CHECK
16. `skills/artifact-layers-validator/SKILL.md` : validation structure repo
17. `skills/registry-sync-checker-skill/SKILL.md` : version skill de registry-sync-checker.py
18. `skills/ontology-term-gate-skill/SKILL.md` : version skill de ontology_term_gate.py
19. `skills/inventory-reconciler-interpreter-skill/SKILL.md` : version skill unifiée
20. `skills/session-boot-skill/SKILL.md` : version skill de session_boot.py

### Phase E — Citizens
21. `citizens/design-ops-loop-citizen/citizen.yaml` : citizen pilote boucle THINK/DO/CHECK
22. `citizens/artifact-layers-auditor/citizen.yaml` : citizen audit structure repos
23. `citizens/session-boot-citizen/citizen.yaml` : citizen exécution BOOT/CLOSEOUT

### Phase F — Designs
24. `designs/workflow-sot-completeness/design.yaml` : workflow SOT completeness
25. `designs/workflow-yaml-structure-validator/design.yaml` : workflow YAML validation
26. `designs/design-ops-loop/design.yaml` : design boucle THINK/DO/CHECK opérationnelle
27. `designs/artifact-layers-design/design.yaml` : design 7 layers repo
28. `designs/session-boot-design/design.yaml` : design checks BOOT

### Phase G — Enregistrement MDU
29. `META-DESIGN.md` : enregistrement nouveaux designs + workflows + skills + citizens
30. `meta-design.yaml` : ajout entrées
31. Catalogues : mise à jour `catalog/skills.index.yaml`, `catalog/primitives.index.yaml`, `catalog/citizens.index.yaml`, `catalog/pipelines.index.yaml`, `catalog/workflows.index.yaml`

## 4. Contraintes

- Encodage UTF-8 strict
- Chaque YAML suit le template MDU
- Commits atomiques <= 3 fichiers
- Pas de doublon avec `ecosystem-meta-coherence` : extension uniquement
- Toute primitive/workflow/pipeline doit être référencée dans un design ou un PRD-MOC

## 5. Plan de commits proposé

| Commit | Fichiers |
|---|---|
| `feat(pipeline): add sot-completeness and yaml-validation pipelines` | E1, E2 |
| `feat(pipeline): add dryrun-causal-audit and session-boot pipelines` | E3, E4 |
| `feat(pipeline): add friction-analysis-to-fix pipeline` | E5 |
| `feat(workflows): add dryrun, structural-fix, session-boot, pre-push, friction workflows` | E6, E7, E8, E9, E10 |
| `feat(primitives): add design-ops-loop, artifact-layers, session-boot, causal-traceability primitives` | E11, E12, E13, E14 |
| `feat(skills): add design-ops-loop, artifact-layers, registry-sync, ontology-term-gate, inventory-reconciler, session-boot skills` | E15, E16, E17, E18, E19, E20 |
| `feat(citizens): add design-ops-loop, artifact-layers, session-boot citizens` | E21, E22, E23 |
| `feat(designs): add workflow-sot-completeness, workflow-yaml-structure-validator, design-ops-loop, artifact-layers, session-boot designs` | E24, E25, E26, E27, E28 |
| `feat(mdu): register new pipelines, workflows, primitives, skills, citizens, designs` | E29, E30, E31 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : `validate_designs.py --strict` ; hooks pre-commit
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. Tous les pipelines E1-E5 sont créés et référencés dans `catalog/pipelines.index.yaml`.
2. Tous les workflows E6-E10 sont créés et référencés dans `catalog/workflows.index.yaml`.
3. Toutes les primitives E11-E14 sont créées et référencées dans `catalog/primitives.index.yaml`.
4. Tous les skills E15-E20 sont créés et référencés dans `catalog/skills.index.yaml`.
5. Tous les citizens E21-E23 sont créés et référencés dans `catalog/citizens.index.yaml`.
6. Tous les designs E24-E28 sont créés, valides YAML, et référencés dans `META-DESIGN.md` et `meta-design.yaml`.
7. `META-DESIGN.md` et `meta-design.yaml` sont mis à jour.
8. Aucune violation DAG n’est introduite.
9. Les pre-commit hooks passent sans blocage encoding.
10. Le mapping extension → MDU est documenté dans `cross_references`.

## 8. Proof-of-Life

- [x] 2026-09-22T21:47:00Z — Création PRD-MOC ECOSYSTEM-META-COHERENCE EXTENSION
- [x] 2026-09-22T21:47:00Z — Création pipelines E1-E5
- [x] 2026-09-22T21:47:00Z — Création workflows E6-E10
- [x] 2026-09-22T21:47:00Z — Création primitives E11-E14
- [x] 2026-09-22T21:47:00Z — Création skills E15-E20
- [x] 2026-09-22T21:47:00Z — Création citizens E21-E23
- [x] 2026-09-22T21:47:00Z — Création designs E24-E28
- [x] 2026-09-22T21:47:00Z — Mise à jour META-DESIGN.md, meta-design.yaml, catalogues
- [x] 2026-09-22T21:47:00Z — Dryrun causal : tous les livrables présents, YAML valide, frontmatter valide, hooks PASS
- [x] 2026-09-22T21:47:00Z — Push origin/main réussi

## 9. Évaluation finale

| Critère d'acceptation | État | Preuve |
|---|---|---|
| 1. Pipelines E1-E5 créés et référencés | ⬜ | |
| 2. Workflows E6-E10 créés et référencés | ⬜ | |
| 3. Primitives E11-E14 créées et référencées | ⬜ | |
| 4. Skills E15-E20 créés et référencés | ⬜ | |
| 5. Citizens E21-E23 créés et référencés | ⬜ | |
| 6. Designs E24-E28 créés et référencés | ⬜ | |
| 7. META-DESIGN.md et meta-design.yaml mis à jour | ⬜ | |
| 8. Aucune violation DAG | ⬜ | |
| 9. Pre-commit hooks passent | ⬜ | |
| 10. Mapping documenté | ⬜ | |

**Verdict** : ⬜ **En attente d’implémentation**

## 10. Références

- **Parent** : PRD-MOC-ECOSYSTEM-META-COHERENCE-20260920.md
- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Atom** : `atoms/ecosystem-meta-coherence-gate.md`
- **Primitive** : `primitives/ecosystem-meta-coherence.yaml`
- **Skills** : `skills/ecosystem-meta-coherence-analyzer/SKILL.md`, `skills/dryrun-causal-auditor/SKILL.md`
- **Workflows** : `workflows/dryrun-causal-audit.md`, `workflows/structural-fix-pipeline.md`
- **Citizen** : `citizens/meta-coherence-auditor/citizen.yaml`
- **Pipeline** : `pipelines/mdu-validation.yaml`
- **MDU** : `META-DESIGN.md`, `meta-design.yaml`
- **Parent MDU** : `meta-coherence`, `chain-fluidity`, `safe-action-pattern`
