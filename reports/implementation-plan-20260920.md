# Plan d'implémentation atomique — ECOSYSTEM-META-COHERENCE EXTENSION

## Phase 1 — Pipelines P0 (E1-E5)
- [ ] E1: pipeline-sot-completeness.yaml
- [ ] E2: pipeline-yaml-structure-validation.yaml
- [ ] E3: pipeline-dryrun-causal-audit.yaml
- [ ] E4: pipeline-session-boot-closeout.yaml
- [ ] E5: pipeline-friction-analysis-to-fix.yaml

## Phase 2 — Workflows P0 (E6-E10)
- [ ] E6: workflow-dryrun-causal-audit.md
- [ ] E7: workflow-structural-fix-pipeline.md
- [ ] E8: workflow-session-boot-closeout.md
- [ ] E9: workflow-pre-push-validation.md
- [ ] E10: workflow-friction-to-fix.md

## Phase 3 — Primitives P0 (E11-E14)
- [ ] E11: design-ops-loop-primitive.yaml
- [ ] E12: artifact-layers-primitive.yaml
- [ ] E13: session-boot-primitive.yaml
- [ ] E14: causal-traceability-primitive.yaml

## Phase 4 — Skills P1 (E15-E20)
- [ ] E15: design-ops-loop-skill/SKILL.md
- [ ] E16: artifact-layers-validator/SKILL.md
- [ ] E17: registry-sync-checker-skill/SKILL.md
- [ ] E18: ontology-term-gate-skill/SKILL.md
- [ ] E19: inventory-reconciler-interpreter-skill/SKILL.md
- [ ] E20: session-boot-skill/SKILL.md

## Phase 5 — Citizens P1 (E21-E23)
- [ ] E21: design-ops-loop-citizen/citizen.yaml
- [ ] E22: artifact-layers-auditor/citizen.yaml
- [ ] E23: session-boot-citizen/citizen.yaml

## Phase 6 — Designs P1 (E24-E28)
- [ ] E24: workflow-sot-completeness/design.yaml
- [ ] E25: workflow-yaml-structure-validator/design.yaml
- [ ] E26: design-ops-loop/design.yaml
- [ ] E27: artifact-layers-design/design.yaml
- [ ] E28: session-boot-design/design.yaml

## Phase 7 — MDU et catalogues (E29-E31)
- [ ] E29: META-DESIGN.md
- [ ] E30: meta-design.yaml
- [ ] E31: catalogues

## Validation
- [ ] validate_designs.py --strict sur tous les design.yaml
- [ ] python -c "import yaml; yaml.safe_load(open(...))" sur tous les YAML
- [ ] Pre-commit hooks passent
- [ ] Git push origin/main
