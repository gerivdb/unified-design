# Auto-Promote

Promotion automatique des documents de gouvernance (ADR, Designs, INTENTS) quand les critères objectifs sont remplis.

## Usage

### CLI

```bash
# Dry-run — liste les documents promouvables sans appliquer
python scripts/auto_design_cli.py promote --dry-run

# Apply — applique les promotions avec preuve horodatée
python scripts/auto_design_cli.py promote --apply

# Via script dédié
python scripts/auto_promote.py --dry-run
python scripts/auto_promote.py --apply
```

### PowerShell (CI locale)

```powershell
# Dry-run
.\scripts\run_auto_promote_check.ps1

# Apply
.\scripts\run_auto_promote_check.ps1 -Apply
```

## Critères de Promotion

### ADR

| Condition | Critère |
|-----------|---------|
| Status actuel | `proposed` |
| Design associé | Intégré dans ≥1 consumer (module + tests passants) |
| Action | `proposed` → `accepted` |

### Design

| Condition | Critère |
|-----------|---------|
| Status actuel | `proposed` ou `draft` |
| Intégration | ≥1 consumer a un module d'intégration fonctionnel |
| Tests | Tests d'intégration passants |
| Action | `proposed`/`draft` → `active` |

### INTENT

| Condition | Critère |
|-----------|---------|
| Status actuel | `proposed` |
| Proof-of-Life | ≥1 item `[x]` horodaté |
| Livrables | Tous les livrables listés sont réalisés |
| Action | `proposed` → `approved` |

## Intégration

- **Moteur** : `engine/auto_design/auto_promote.py` + `scripts/auto_promote.py`
- **CLI** : `scripts/auto_design_cli.py promote`
- **Hook pre-commit** : `.kilocode/hooks/pre-commit-auto-promote.py`
- **Tests** : `tests/test_auto_promote.py` (3 passed)

## Politique

Voir `designs/auto-promote/` pour les critères YAML détaillés :
- `adr-criteria.yaml`
- `design-criteria.yaml`
- `intent-criteria.yaml`

## Références

- **PRD** : `PRD/PRD-MOC-AUTO-PROMOTE-20260928.md`
- **MOC** : `MOC/MOC-AUTO-PROMOTE-20260928.md`
- **INTENT** : `INTENT-AUTO-PROMOTE-20260928.md`
- **ADR** : `ADR/ADR-2026-09-29-auto-design-aufhebung.md`
