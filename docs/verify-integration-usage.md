# Verify Integration Usage — Documentation

## Objectif

Vérifier que les modules d'intégration `unified-design` sont effectivement utilisés dans le code métier des consumer repos.

## Usage

### Vérifier tous les consumers/designs

```bash
python scripts/verify_integration_usage.py --all
```

### Vérifier un consumer spécifique

```bash
python scripts/verify_integration_usage.py --consumer KIVA-CLI
```

### Vérifier un design spécifique

```bash
python scripts/verify_integration_usage.py --design safe-action-pattern
```

### Générer un rapport JSON

```bash
python scripts/verify_integration_usage.py --all --json-out reports/usage-report.json
```

## Critères d'acceptation

- [ ] 126/126 modules d'intégration existent
- [ ] 126/126 modules sont importés dans le code métier
- [ ] Aucun module orphelin (créé mais non utilisé)

## Références

- **PRD-MOC** : `PRD/PRD-MOC-CONSUMER-INTEGRATION-USAGE-20260928.md`
- **MOC** : `MOC/MOC-CONSUMER-INTEGRATION-USAGE-20260928.md`
- **Framework** : `PRD/PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
