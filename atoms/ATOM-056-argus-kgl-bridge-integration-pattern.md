---
# ATOM-056: ARGUS-KG-L Bridge Integration Pattern

## Zones définies

| Zone | Chemin | Usage |
|---|---|---|
| Integration | kg_l/integrations/argus_bridge.py | WAL consumption ARGUS → KG-L |
| Entities | src/runtime/models.py | BridgeGap, CrossrefOrphan entities |
| WAL | NEXUS/wal/META_FEEDBACK.jsonl | Causal graph signals |

## Règles

1. Tout bridge_integrity_signal doit créer une entité BridgeGap dans KG-L
2. Tout crossref_integrity_signal doit créer une entité CrossrefOrphan
3. Les entités avec R >= 2 génèrent des recommandations automatiques

## Enforcement

```yaml
# KG-L Integration
argus_bridge_consumer:
  wal_events: [bridge_integrity_signal, crossref_integrity_signal]
  entity_types: [BridgeGap, CrossrefOrphan]

# Pattern detection
recurrence_threshold: 2
action: generate_recommendation
```

## Contexte causal

- **Cause** : Détection de lacunes par ARGUS
- **Effect** : Représentation causale dans KG-L
- **Pattern** : Signal WAL → Entité KG-L → Pattern detection → Recommendation
- **Cycle** : ARGUS scan → WAL event → KG-L entity → Feedback → NEXUS update