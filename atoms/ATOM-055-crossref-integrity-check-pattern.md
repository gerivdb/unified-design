---
# ATOM-055: Crossref Integrity Check Pattern

## Zones définies

| Zone | Chemin | Usage |
|---|---|---|
| Scanner | scanners/crossref_check.py | Crossref ORPHAN/GHOST detection |
| Matrix | GOVERNANCE-HUB/NEXUS/ONTOLOGY/crossref_matrix.yaml | Source reference |
| WAL | NEXUS/wal/ARGUS_WAL.jsonl | crossref_integrity_signal events |

## Règles

1. Toute référence croisée doit exister dans crossref_matrix.yaml OU dans le code
2. Les ORPHAN/GHOST doivent être horodatés dans WAL avec severity WARNING
3. R >= 2 ORPHAN sur le meme concept → concept à archiver ou restructurer

## Enforcement

```yaml
# Pre-commit gate
check_crossref_integrity:
  script: scanners/crossref_check.py
  on_failure: hitl_review_required

# Concept lifecycle
orphan_threshold: 2
action: concept_deprecation_proposal
```

## Contexte causal

- **Cause** : Références croisées non synchronisées
- **Effect** : Concepts orphelins dans l'ontologie
- **Pattern** : scan code → compare avec registre → WAL signal
- **Cycle** : ORPHAN R >= 2 → suggestion suppression/archivage