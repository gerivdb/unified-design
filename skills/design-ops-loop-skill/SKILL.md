---
name: design-ops-loop-skill
description: >
  Orchestre la boucle THINK/DO/CHECK du MDU.
  Appelle dryrun-causal-auditor, ecosystem-meta-coherence-analyzer,
  pre-push-auditor pour garantir que toute correction respecte
  les invariants écosystémiques.
version: "1.0.0"
status: active
layer: L0
intent_hash: 0xSKILL_DESIGN_OPS_LOOP_20260920
triggers:
  - "orchestrer THINK DO CHECK"
  - "boucle opérationnelle MDU"
  - "design-ops-loop"
inputs:
  - type: action
    description: "Action à orchestrer (think/do/check)"
  - type: context
    description: "Contexte écosystémique"
outputs:
  - type: orchestration_result
    description: "Résultat de l'orchestration"
  - type: proof_of_life
    description: "Preuve horodatée"
tools:
  - dryrun-causal-auditor
  - ecosystem-meta-coherence-analyzer
  - pre-push-auditor
artifacts:
  - path: reports/design-ops-loop-*.json
    format: json
governance:
  adr: ADR-2026-09-19-SAFE-ACTION-PATTERN
  design: design-ops-loop
  atom: ecosystem-meta-coherence-gate
---

# Skill : Design Ops Loop

## Description

Orchestre la boucle THINK/DO/CHECK du MDU. Appelle dryrun-causal-auditor, ecosystem-meta-coherence-analyzer, pre-push-auditor pour garantir que toute correction respecte les invariants écosystémiques.

## When to use

- Avant toute implémentation de design/atom/ADR
- Avant tout merge vers `main`
- Après toute session de correction structurelle

## Process

### ÉTAPE-1 — THINK
- dryrun-causal-auditor : vérifier la présence, validité YAML, frontmatter, MDU, hooks, cross-references, merge
- ecosystem-meta-coherence-analyzer : analyser les frictions et erreurs ERR

### ÉTAPE-2 — DO
- Implémenter les corrections via tâches atomiques SLM/ACT auto
- Monitorer les invariants écosystémiques pendant la correction

### ÉTAPE-3 — CHECK
- pre-push-auditor : valider YAML, vérifier champs SOT, exécuter tests
- Enregistrer les preuves dans VOLTX

## Anti-patterns

- Skip dryrun pour gagner du temps
- Implémenter sans validation TALEX
- Corrections groupées (> 3 fichiers par commit)
- Oublier la traçabilité causale

## References

- **Design** : `designs/design-ops-loop/design.yaml`
- **Atom** : `atoms/ecosystem-meta-coherence-gate.md`
- **Workflow** : `workflows/workflow-design-ops-loop.md`
