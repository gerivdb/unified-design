---
type: DESIGN
version: "1.0.0"
status: proposed
date: "2026-09-21"
intent_hash: 0xDESIGN_MEMORY_CHANNEL_MULTIPLEX_20260921
repo: gerivdb/unified-design
layer: L0-CANON
---

# Design — Memory Channel Multiplexing

## Contexte
WAZAA expose 4 channels mémoire distincts :
- `L0-CANON/HERMES/memory/swap`
- `L0-CANON/HERMES/memory/tier`
- `L0-CANON/HERMES/memory/quantum`
- `VERSES/evolution/*`

Ces channels sont éparpillés et nécessitent 4 abonnés distincts.

## Problème
- Overhead d'abonnement × 4
- Pas de vue unifiée du flux mémoire
- Duplication potentielle de messages
- Pas de garantie d'ordre entre channels

## Solution

### 1. Bus mémoire unifié

```
L0-CANON/HERMES/memory/*
  ├── swap     → pression, swap_in, swap_out
  ├── tier     → promote, demote, rollback
  ├── quantum  → pending, committed, aborted
  └── evolution → concept_id, evolution_type
```

Un seul abonné `hermes_memory_bus` écoute le wildcard `L0-CANON/HERMES/memory/*`.

### 2. Format de message unifié

```json
{
  "event": "HERMES_MEMORY_EVENT",
  "channel": "swap|tier|quantum|evolution",
  "action": "swap_in|promote|commit|evolve",
  "payload": {
    "key": "string",
    "value": "any",
    "tier": "cold|warm|hot|swap",
    "mode": "glace|plasma|hybride",
    "invariant_valid": true,
    "timestamp": "2026-09-21T00:00:00Z"
  },
  "metadata": {
    "source": "HERMES",
    "session_id": "kilo-xxx-xxxxxx",
    "trace_id": "trace-xxx"
  }
}
```

### 3. Multiplexeur WAZAA

```python
class MemoryChannelMultiplexer:
    def __init__(self):
        self.subscribers = {
            "swap": SwapHandler(),
            "tier": TierHandler(),
            "quantum": QuantumHandler(),
            "evolution": EvolutionHandler(),
        }
    
    def route(self, message: WazaaMessage) -> None:
        channel = message.topic.split("/")[-2]
        handler = self.subscribers.get(channel)
        if handler:
            handler.handle(message)
```

### 4. Optimisations

1. **Wildcard unique** : un seul abonné au lieu de 4
2. **Batching** : regrouper les messages par channel avant traitement
3. **Backpressure** : queue par channel avec limite de taille
4. **Metrics unifiées** : un seul dashboard pour tous les channels

### 5. Fluidité

- Messages routés en < 100µs
- Pas de blocking I/O dans le multiplexeur
- Ordering garantie par channel
- Dead-letter queue pour messages invalides

## Implémentations

| Composant | Rôle | Fichier |
|-----------|------|---------|
| WAZAA | Multiplexeur | `src/wazaa_bus_citizens/memory_multiplexer_citizen.py` |
| WAZAA | Wildcard topic | `channels/channels.index.yaml` |
| HERMES | Handlers | `src/memory_core/memory_event_handlers.py` |
| FLEX | États toroïdaux | `src/core/toroidal/pipeline.zig` |
| INFX | VLD des messages | `src/infx/vld/` |

## Critères d'acceptation
- [ ] Wildcard `L0-CANON/HERMES/memory/*` déclaré
- [ ] Multiplexeur implémenté
- [ ] 4 handlers fonctionnels
- [ ] Format de message unifié
- [ ] Batching et backpressure implémentés
- [ ] Tests de routage passent

## Références
- `WAZAA/channels/channels.index.yaml` — registre channels
- `WAZAA/src/bus/channel_registry.py` — validation soft
- `PRD-MOC-MEMORY-WAZAA-CHANNELS-2026-09-20.md` — PRD-MOC channels
