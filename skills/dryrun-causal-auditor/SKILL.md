---
name: dryrun-causal-auditor
description: >
  Vérifie qu'un livrable ou un ensemble de livrables est prod-ready opérationnel à 100%
  avant toute implémentation ou merge. Exécute les 7 étapes du dryrun causal :
  présence, validité YAML, frontmatter, validation MDU, hooks, cross-references, merge.
version: "1.0.0"
status: active
intent_hash: 0xSKILL_DRYRUN_CAUSAL_AUDITOR_20260920
layer: L0
triggers:
  - "dryrun causal"
  - "vérifier prod-ready"
  - "avant implémentation"
  - "avant merge"
inputs:
  - type: design_path
    description: "Chemin vers le design YAML à valider"
  - type: repo_root
    description: "Racine du repo"
outputs:
  - type: audit_report
    description: "Rapport d'audit dryrun (JSON/Markdown)"
  - type: verdict
    description: "PASS / WARN / STOP"
tools:
  - yaml_parser
  - validate_designs.py
  - git
  - pre-commit
artifacts:
  - path: reports/dryrun-causal-audit-*.md
    format: markdown
governance:
  adr: ADR-2026-09-19-SAFE-ACTION-PATTERN
  design: ecosystem-meta-coherence
  atom: ecosystem-meta-coherence-gate
---

# Skill : Dryrun Causal Auditor

## Description
Vérifie qu'un livrable est prod-ready opérationnel à 100% avant toute implémentation ou merge.

## When to use
- Avant toute implémentation de design/atom/ADR
- Avant tout merge vers `main`
- Après toute session de correction structurelle

## Process

### ÉTAPE-1 — Présence
Vérifier que tous les fichiers attendus existent physiquement.

### ÉTAPE-2 — Validité YAML
Parser chaque YAML avec `yaml.safe_load()`.

### ÉTAPE-3 — Frontmatter
Vérifier le frontmatter de chaque document de gouvernance.

### ÉTAPE-4 — Validation MDU
Exécuter `validate_designs.py --strict` sur le design cible.

### ÉTAPE-5 — Hooks
Vérifier que les pre-commit hooks passent.

### ÉTAPE-6 — Cross-references
Vérifier que les références croisées sont cohérentes.

### ÉTAPE-7 — Merge
Vérifier que le merge sur `main` est possible.

## Anti-patterns
- Skip dryrun pour gagner du temps
- Valider sans vérifier les chemins
- Ignorer les warnings

## References
- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Atom** : `atoms/ecosystem-meta-coherence-gate.md`
- **Workflow** : `workflows/dryrun-causal-audit.md`
