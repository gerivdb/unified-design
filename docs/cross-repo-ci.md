# Cross-Repo CI Pipeline — Documentation

## Objectif

Le `cross_repo_ci.py` valide automatiquement que tous les consumers ont correctement intégré les designs `unified-design` across all 14 consumer repos.

## Usage

### Vérifier tous les consumers/designs

```bash
python scripts/cross_repo_ci.py --all
```

### Vérifier un consumer spécifique

```bash
python scripts/cross_repo_ci.py --consumer KIVA-CLI
```

### Vérifier un design spécifique

```bash
python scripts/cross_repo_ci.py --design safe-action-pattern
```

### Générer un rapport JSON

```bash
python scripts/cross_repo_ci.py --all --json-out reports/cross-repo-ci-report.json
```

## Intégration KIVA-CLI

```bash
# Pipeline KIVA-CLI
kiva pipeline run unified-design-consumers
```

## Références

- **PRD-MOC** : `PRD/PRD-MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
- **MOC** : `MOC/MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
- **Framework** : `PRD/PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- **Registry** : `PRD/PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md`
