# Unified-Design Automation Scripts

Scripts d'automatisation pour l'écosystème unified-design.

## Scripts

| Script | Usage | Description |
|--------|-------|-------------|
| `auto_promote.py` | `python scripts/auto_promote.py --apply` | Promotion automatique ADR/Designs/INTENTS |
| `cross_repo_ci.py` | `python scripts/cross_repo_ci.py --consumer KIVA-CLI` | Pipeline CI cross-repo |
| `adr_design_traceability.py` | `python scripts/adr_design_traceability.py --check-all` | Vérification traçabilité ADR/Design/Integration |
| `verify_integration_usage.py` | `python scripts/verify_integration_usage.py --all` | Vérification usage dans le code métier |

## Usage

### Auto-Promote

```bash
# Dry-run
python scripts/auto_promote.py --dry-run

# Apply
python scripts/auto_promote.py --apply

# Avec rapport
python scripts/auto_promote.py --apply --report reports/auto-promote-report.json
```

### Cross-Repo CI

```bash
# Un consumer
python scripts/cross_repo_ci.py --consumer KIVA-CLI

# Plusieurs consumers
python scripts/cross_repo_ci.py --consumer KIVA-CLI ECOS-CLI

# Un design
python scripts/cross_repo_ci.py --design safe-action-pattern

# Tous
python scripts/cross_repo_ci.py --all
```

### ADR Traceability

```bash
# Tous
python scripts/adr_design_traceability.py --check-all

# Un consumer
python scripts/adr_design_traceability.py --consumer KIVA-CLI

# Un design
python scripts/adr_design_traceability.py --design safe-action-pattern
```

### Verify Integration Usage

```bash
# Tous
python scripts/verify_integration_usage.py --all

# Un consumer
python scripts/verify_integration_usage.py --consumer KIVA-CLI
```

## Tests

```bash
# Tous les tests
pytest tests/test_auto_promote.py tests/test_cross_repo_ci.py tests/test_adr_design_traceability.py tests/test_verify_integration_usage.py -v

# Un script
pytest tests/test_auto_promote.py -v
```

## Références

- **PRD-MOC Framework** : `PRD/PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- **PRD-MOC CI** : `PRD/PRD-MOC-CROSS-REPO-CI-PIPELINE-20260928.md`
- **PRD-MOC Traceability** : `PRD/PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY-20260928.md`
- **PRD-MOC Usage** : `PRD/PRD-MOC-CONSUMER-INTEGRATION-USAGE-20260928.md`
- **PRD-MOC Auto-Promote** : `PRD/PRD-MOC-AUTO-PROMOTE-20260928.md`
