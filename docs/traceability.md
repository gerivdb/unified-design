# ADR-Design-Integration Traceability — Documentation

## Objectif

Garantir la traçabilité complète ADR → Design → Consumer → Integration pour tous les designs intégrés.

## Usage

### Vérifier la traçabilité pour tous les consumers/designs

```bash
python scripts/adr_design_traceability.py --check-all
```

### Vérifier un consumer spécifique

```bash
python scripts/adr_design_traceability.py --consumer KIVA-CLI
```

### Vérifier un design spécifique

```bash
python scripts/adr_design_traceability.py --design safe-action-pattern
```

### Générer un rapport JSON

```bash
python scripts/adr_design_traceability.py --check-all --json-out reports/adr-traceability-report.json
```

## Format de traçabilité

Chaque PRD-MOC consumer DOIT contenir :

```yaml
---
related_adr: ADR-2026-09-19-SAFE-ACTION-PATTERN.md
related_intent: INTENT-2026-09-19-SAFE-ACTION-PATTERN.md
related_moc: MOC-SAFE-ACTION-PATTERN-20260919.md
parent_doc: PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md
governance:
  adr_status: accepted  # ou proposed
  design_status: active  # ou standard, proposed
  integration_status: functional  # ou stub, missing
---
```

## Promotion ADR

Tout design intégré avec `integration_status: functional` DOIT avoir son ADR promu de `proposed` à `accepted` dans un délai de 7 jours.

## Références

- **PRD-MOC** : `PRD/PRD-MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY-20260928.md`
- **MOC** : `MOC/MOC-ADR-DESIGN-INTEGRATION-TRACEABILITY-20260928.md`
- **Registry** : `PRD/PRD-MOC-UNIFIED-DESIGN-CONSUMERS-REGISTRY-20260928.md`
