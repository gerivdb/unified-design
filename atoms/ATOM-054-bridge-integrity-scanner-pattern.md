---
# ATOM-054: Bridge Integrity Scanner Pattern

## Zones définies

| Zone | Chemin | Usage |
|---|---|---|
| Scanner | scanners/bridge_integrity_scanner.py | Bridge GAP/VOID/DRIFT detection |
| WAL | NEXUS/wal/ARGUS_WAL.jsonl | Event storage |
| Report | ARGUS/reports/bridge_integrity_*.json | Scan results |

## Règles

1. Tout pontontologique déclaré dans BRIDGES.yaml doit être vérifié
2. Toute différence GAP/VOID/DRIFT doit être horodatée dans WAL
3. Les ponts critiques (CRITICAL severity) déclenchent un commentaire ARGUS

## Enforcement

```yaml
# Pre-commit gate
check_bridge_integrity:
  script: scanners/bridge_integrity_scanner.py
  on_failure: comment_argus_required

# WAL schema validation
bridge_integrity_signal:
  required_fields: [id, source_repo, field_path, pathology, severity, emitted_at]
```

## Contexte causal

- **Cause** : Pontsontologiques sous-estimés dans BRIDGES.yaml
- **Effect** : Détection tardive des lacunes inter-repo
- **Pattern** : scanner + WAL + feedback loop ARGUS → KG-L → NEXUS
- **Cycle** : R >= 2 → génération automatique pont BridgeGap → NEXUS WAL