---
type: DESIGN
version: "1.0.0"
status: proposed
date: "2026-09-21"
intent_hash: 0xDESIGN_MEMORY_FACTUAL_MEMORY_INTEGRATION_20260921
repo: gerivdb/unified-design
layer: L0-CANON
---

# Design — factual_memory L3 Integration

## Contexte
`factual_memory` (L3-CITIZENS) est un composant mémoire factuelle orphelin.
Il possède un PRD-MOC (`PRD-MOC-FACTUAL-MEMORY-INTEGRATION-2026-09-20.md`) mais aucune implémentation technique n'a été démarrée.

## Problème
- factual_memory est isolé de l'écosystème mémoire
- Pas de bus WAZAA vers/from factual_memory
- Pas de provider HERMES pour factual_memory
- Pas de channel WAZAA dédié

## Solution proposée

### Option A — Bridge WAZAA (recommandé)
Créer un bridge WAZAA qui expose factual_memory comme un citizen:
```
L0-CANON/HERMES/memory/fact
  └── factual_memory_bridge_citizen
      ├── subscribe(factual_memory_topic)
      ├── transform(fact → memory_entry)
      └── publish(L0-CANON/HERMES/memory/swap)
```

### Option B — Migration facts.db
Migrer facts.db vers Mnemo cache:
```
factual_memory (L3)
  └── facts.db (SQLite)
      └── Mnemo (L4) via import script
```

### Option C — Provider HERMES
Ajouter un provider factual_memory à HERMES:
```python
class FactualMemoryProvider(MemoryProviderPrimitive):
    def prefetch(self, query: str) -> Optional[MemoryEntry]:
        return query_factual_memory(query)
    
    def sync_turn(self, user: str, assistant: str) -> None:
        store_factual_memory(user, assistant)
```

## Architecture cible

```
HERMES (orchestrator)
  ├── Mnemo (cache hot)
  ├── FLEX (toroidal provider)
  ├── factual_memory (L3) [NOUVEAU]
  │   └── facts.db
  └── WAZAA (event bus)
      └── factual_memory_bridge
```

## Implémentations

| Composant | Rôle | Fichier |
|-----------|------|---------|
| WAZAA | Bridge citizen | `src/wazaa_bus_citizens/factual_memory_bridge_citizen.py` |
| WAZAA | Channel | `channels/L0-CANON/HERMES/memory/fact` |
| HERMES | Provider | `src/memory_providers/factual_memory.py` |
| factual_memory | Adapter | `src/adapters/factual_memory_adapter.py` |

## Critères d'acceptation
- [ ] factual_memory accessible via WAZAA
- [ ] HERMES peut interroger factual_memory
- [ ] Migration facts.db → Mnemo testée
- [ ] Tests d'intégration passants

## Références
- `PRD-MOC-FACTUAL-MEMORY-INTEGRATION-2026-09-20.md` — PRD-MOC parent
- `PRD-MOC-MEMORY-ECOSYSTEM-MASTER-2026-09-21.md` — master PRD-MOC
- `WAZAA/src/wazaa_bus_citizens/` — citizens existants
