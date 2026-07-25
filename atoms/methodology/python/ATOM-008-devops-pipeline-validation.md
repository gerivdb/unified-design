---
type: ATOM
id: ATOM-008-devops-pipeline-validation
version: 1.0.0
date: 2026-07-17
title: "DevOps Pipeline Validation — Validation des pipelines CI/CD cross-repo"
intent_hash: 0xATOM_DEVOPS_PIPELINE_VALIDATION_20260717
status: proposed
strate: L1b
lang: yaml
---

# ATOM-008 — DevOps Pipeline Validation

## Contexte

Les pipelines CI/CD cross-repo dans l'écosystème gerivdb (NEXUS, BRAIN, WAZAA, TRIX) partagent des patterns communs de validation, de drift detection et de rollback.

## Loi fondamentale

**Tout pipeline CI/CD cross-repo doit inclure :**
1. **Drift detection** — Vérifier que les workflows n'ont pas changé de manière non autorisée
2. **Rollback automatique** — En cas d'échec, revenir à la dernière version stable
3. **Timeout de sécurité** — Limiter la durée d'exécution pour éviter les jobs bloqués

### Violation courante

```yaml
# ❌ FAUX — Pipeline sans validation
name: build-and-deploy
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: ./build.sh  # Pas de validation du contenu
```

### ✅ CORRECT — Pipeline avec ATOM-008

```yaml
# ✅ CORRECT — Pipeline validé par ATOM-008
name: build-and-deploy
on: [push, schedule, workflow_dispatch]
concurrency: build-cluster  # Évite les runs parallèles
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Drift detection
        run: scripts/drift-check.sh
      - name: Security scan
        run: trivy fs .
  build:
    needs: validate
    runs-on: ubuntu-latest
    timeout-minutes: 120  # max_runtime_hours = 2
    steps:
      - uses: actions/checkout@v3
      - run: ./build.sh
  deploy:
    needs: build
    if: success()
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: ./deploy.sh
```

## Paramètres

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `triggers` | list | `[push]` | Événements déclencheurs autorisés |
| `drift_detection` | bool | `true` | Activer la détection de drift |
| `rollback_on_failure` | bool | `true` | Rollback automatique en cas d'échec |
| `max_runtime_hours` | int | `2` | Timeout maximum en heures |

## Invariants

- **Drift detection obligatoire** pour tout pipeline touchant plusieurs repos
- **Rollback automatique** requis pour les pipelines de production
- **Timeout de sécurité** doit être inférieur à 24h

## Application

### NEXUS Pipeline

```yaml
# .github/workflows/nexus-sync.yaml
name: Nexus Cross-Repo Sync
on:
  schedule:
    - cron: '0 */6 * * *'  # Toutes les 6 heures
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps:
      - uses: actions/checkout@v3
      - name: Validate drift
        run: python scripts/drift_validator.py --max-age 6h
      - name: Sync repos
        run: ./scripts/sync-all.sh
      - name: Health check
        run: ./scripts/health-check.sh
```

### WAZAA Pipeline

```yaml
# .github/workflows/wazaa-deploy.yaml
name: WAZAA Deploy
on: [push, workflow_dispatch]
concurrency: wazaa-deploy

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 120
    steps:
      - uses: actions/checkout@v3
      - name: Drift detection
        run: ./scripts/detect-drift.sh
      - name: Deploy
        run: ./scripts/deploy.sh
```

## Références

- registry-sync.yaml
- git-remote-safety.yaml
- INTENTS: 303, 308
- ADR-2026-07-16-007: CI Pipeline Patterns

## Référence ADR
- **ADR** : ADR-2026-07-17-008-DEVOPS-PIPELINE-VALIDATION
- **IntentHash** : 0xADR_DEVOPS_PIPELINE_20260717
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded