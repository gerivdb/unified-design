---
name: browser-version-gate
description: >
  Skill de gate de version Chromium/browser. Verifie que la version
  Chromium/ungoogled-chromium installee est dans la plage autorisee
  (tested_versions, allowed_versions) et applique la politique
  fail_closed si la version est hors politique.
version: "1.0.0"
status: active
layer: L0-CANON
intent_hash: 0xSKILL_BROWSER_VERSION_GATE_20261117
triggers:
  - "verifier version Chromium"
  - "verifier version ungoogled-chromium"
  - "appliquer politique version-gate"
inputs:
  - type: browser_version
    description: "Version actuelle du navigateur (ex: 147.0.7727.55)"
  - type: version_policy_path
    description: "Chemin vers le fichier version_policy.yaml (defaut: core/browser_abstraction/version_policy.yaml)"
outputs:
  - type: gate_decision
    description: "ALLOW, WARN ou BLOCK"
  - type: reason
    description: "Justification de la decision"
tools:
  - filesystem
  - yaml_parser
artifacts:
  - path: reports/version-gate-*.json
    format: json
governance:
  adr: ADR-2026-11-17-001-STRATE-DOCS-L2-L3
  design: documentation-ragx-integration
  atom: atom-documentation-technique
  atom: atom-documentation-universitaire
---

# Skill : Browser Version Gate

## Description

Skill de gate de version Chromium/browser. Verifie que la version
Chromium/ungoogled-chromium installee est dans la plage autorisee
(tested_versions, allowed_versions) et applique la politique
fail_closed si la version est hors politique.

## Quand utiliser

- Avant toute injection de KI dans RAGX (le navigateur doit etre a jour)
- Avant toute operation dependant de Chromium/CDP
- Verification periodique de la version installee

## Processus

### ETAPE-1 — Lire la version installee
Recuperer la version actuelle de Chromium/ungoogled-chromium.

### ETAPE-2 — Lire la politique de version
Lire le fichier version_policy.yaml avec tested_versions, allowed_versions, forbidden_below, forbidden_above.

### ÉTAPE-3 — Appliquer la politique
- Si version in tested_versions : ALLOW
- Si version in allowed_versions mais pas tested : WARN
- Si version < forbidden_below ou > forbidden_above : BLOCK (fail_closed)

## Anti-patterns

- Injecter un KI sans verifier la version du navigateur
- Ignorer une version hors politique
- Utiliser une version non testee sans avertissement

## References

- **Design** : `designs/documentation-ragx-integration/design.yaml`
- **Design** : `designs/documentation-technique/design.yaml`
