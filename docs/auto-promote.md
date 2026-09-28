# Auto-Promote — Documentation

## Objectif

Automatiser la promotion des documents de gouvernance (ADR, Designs, INTENTS) quand les critères métier sont remplis.

## Usage

### Dry-run (simulation)

```bash
python scripts/auto_promote.py --dry-run
```

### Apply (appliquer les promotions)

```bash
python scripts/auto_promote.py --apply
```

### Générer un rapport

```bash
python scripts/auto_promote.py --apply --report reports/auto-promote-report.json
```

### Promouvoir seulement les ADR

```bash
python scripts/auto_promote.py --adr --apply
```

### Promouvoir seulement les Designs

```bash
python scripts/auto_promote.py --design --apply
```

### Promouvoir seulement les INTENTS

```bash
python scripts/auto_promote.py --intent --apply
```

## Critères de promotion

### ADR

- Status actuel : `proposed`
- Design associé : intégré dans ≥1 consumer (module + tests passants)
- Action : `proposed` → `accepted`

### Designs

- Status actuel : `proposed` ou `draft`
- Intégration : ≥1 consumer a un module d'intégration fonctionnel
- Tests : tests d'intégration passants
- Action : `proposed`/`draft` → `active`

### INTENTS

- Status actuel : `proposed`
- Proof-of-Life : ≥1 item `[x]` horodaté
- Livrables : tous les livrables listés sont réalisés
- Action : `proposed` → `approved`

## Politique

La politique de promotion est définie dans `policies/auto-promotion.yaml`.

## Intégration CI

```bash
# Dans le pipeline CI
python scripts/auto_promote.py --dry-run

# Si OK, appliquer
python scripts/auto_promote.py --apply
```

## Références

- **PRD-MOC** : `PRD/PRD-MOC-AUTO-PROMOTE-20260928.md`
- **MOC** : `MOC/MOC-AUTO-PROMOTE-20260928.md`
- **Framework** : `PRD/PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
