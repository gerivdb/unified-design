---
name: ecosystem-meta-coherence-analyzer
description: >
  Analyse les frictions et erreurs ERR de session via TALEX.
  Identifie les causes racines, propose des corrections structurelles,
  et génère des rapports horodatés pour le vault VOLTX.
  Fusionne meta-coherence (détection d'écarts) et friction-analyzer
  (corrections structurelles) en un skill unifié.
version: "1.0.0"
status: active
intent_hash: 0xSKILL_ECOSYSTEM_META_COHERENCE_ANALYZER_20260920
layer: L0
triggers:
  - "analyse via TALEX les friction erreurs ERR"
  - "corriger structurellement"
  - "dryrun causal"
  - "frictions de session"
  - "corrections structurelles"
inputs:
  - type: session_log
    description: "Log de la session KiloCode"
  - type: mdu_state
    description: "État actuel du MDU (META-DESIGN.md, meta-design.yaml)"
  - type: git_state
    description: "État git (branches, commits, remotes)"
outputs:
  - type: friction_report
    description: "Rapport TALEX des frictions (JSON)"
  - type: structural_fixes
    description: "Liste des corrections structurelles à implémenter"
  - type: proof_of_life
    description: "Preuves horodatées pour VOLTX"
tools:
  - talex_friction_analyzer
  - validate_designs.py
  - branch-taxonomy-validator.py
  - git
  - yaml_parser
artifacts:
  - path: reports/talex-friction-analysis-*.json
    format: json
  - path: reports/talex-session-friction-analysis-*.md
    format: markdown
  - path: workflows/dryrun-causal-audit.md
    format: markdown
  - path: workflows/structural-fix-pipeline.md
    format: markdown
governance:
  adr: ADR-2026-09-19-SAFE-ACTION-PATTERN
  design: ecosystem-meta-coherence
  atom: ecosystem-meta-coherence-gate
  intent: INTENT-2026-09-19-SAFE-ACTION-PATTERN
---

# Skill : Ecosystem Meta-Coherence Analyzer

## Description

Analyse les frictions et erreurs ERR de session via TALEX.
Identifie les causes racines, propose des corrections structurelles,
et génère des rapports horodatés pour le vault VOLTX.

## When to use

- Après une session d'implémentation PATRON-0 / safe-action-pattern
- Lorsque des frictions ALFRED/BRGS/VALIDATOR sont détectées
- Avant tout merge vers `main`
- Lorsque le MDU nécessite une mise à jour structurelle

## Process

### 1. Dryrun causal
Vérifier la présence, la validité et la cohérence de tous les livrables.

### 2. Analyse TALEX
Exécuter `talex_friction_analyzer.py` pour générer le rapport des frictions.

### 3. Classification
Classer les frictions par sévérité (critical/high/medium/low/structural).

### 4. Priorisation
Prioriser les corrections (P1/P2/P3).

### 5. Implémentation
Implémenter les corrections via tâches atomiques SLM/ACT auto.

### 6. Mise à jour PRD-MOC
Mettre à jour le PRD-MOC avec les preuves de vie.

## Anti-patterns

- Analyser sans dryrun préalable
- Implémenter sans validation TALEX
- Corrections groupées (> 3 fichiers par commit)
- Oublier la traçabilité causale

## References

- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Atom** : `atoms/ecosystem-meta-coherence-gate.md`
- **Workflow** : `workflows/dryrun-causal-audit.md`
- **Workflow** : `workflows/structural-fix-pipeline.md`
- **TALEX** : `D:\DO\WEB\TOOLS\L4-TOOLS\TALEX\`
