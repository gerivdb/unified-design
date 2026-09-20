---
type: DESIGN
version: "1.0.0"
status: proposed
date: "2026-09-21"
intent_hash: 0xDESIGN_MEMORY_TIER_TRANSITION_20260921
repo: gerivdb/unified-design
layer: L0-CANON
---

# Design — Memory Tier Transitions

## Contexte
Le pôle mémoire HERMES/Mnemo implémente 5 tiers : Glace (cold), Warm, Plasma (hot), Hybride, Swap.
Les transitions entre ces tiers doivent être formelles, vérifiables et optimisées.

## Problème
Actuellement, les transitions sont implicites dans le code :
- `toroidal_memory_mapping.py` contient un mapping statique
- Pas de formalisation des préconditions/postconditions
- Pas de journalisation des transitions
- Pas de rollback automatique en cas d'échec

## Solution

### 1. Matrice de transitions

| From | To | Condition | Action | Rollback |
|------|----|-----------|--------|----------|
| cold | warm | accès > 1h | promote | restore cold |
| warm | hot | accès > 5min | promote | restore warm |
| hot | warm | pression > HOT_MAX_ENTRIES | demote | restore hot |
| warm | cold | inactivité > 24h | demote | restore warm |
| hot | swap | pression critique | swap_out | swap_in |
| swap | hot | accès demandé | swap_in | swap_out |
| any | glace | invariant χ=2 requis | freeze | restore previous |

### 2. Contrat de transition

```python
class TierTransition:
    from_tier: MemoryTier
    to_tier: MemoryTier
    precondition: Callable[[MemoryEntry], bool]
    postcondition: Callable[[MemoryEntry], bool]
    rollback_fn: Callable[[MemoryEntry], None]
    metadata: dict
```

### 3. États du système

```
                    ┌─────────┐
                    │  Swap   │
                    └────┬────┘
                         │ swap_in
                    ┌────┴────┐
          hot ←─────│  Hybride │─────→ cold
                    └────┬────┘
                         │ promote/demote
                    ┌────┴────┐
                    │  Warm   │
                    └────┬────┘
                         │ promote/demote
                    ┌────┴────┐
                    │  Cold   │
                    └─────────┘
```

### 4. Optimisations

1. **Précalcul des mappings** : calculer une table de transition statique au boot
2. **Cache LRU par tier** : éviter les recalculs de précondition
3. **Batch transitions** : regrouper les transitions simultanées
4. **Async rollback** : rollback en arrière-plan sans bloquer

### 5. Fluidité

- Transitions < 1ms via lookup table
- Pas de blocking I/O pendant transition
- Métriques de latence par tier
- Alertes si transition > 10ms

## Implémentations

| Composant | Rôle | Fichier |
|-----------|------|---------|
| HERMES | Moteur de transitions | `src/memory_core/tier_transition_engine.py` |
| Mnemo | Cache physique | `src/memory_core/sram_dram_tier.py` |
| FLEX | Mapping tore ↔ tier | `src/memory_core/toroidal_memory_mapping.py` |
| WAZAA | Events de transition | `channels/L0-CANON/HERMES/memory/tier` |

## Critères d'acceptation
- [ ] Matrice de transitions formalisée
- [ ] Contrat TierTransition implémenté
- [ ] Précalcul des mappings au boot
- [ ] Tests de transition < 1ms
- [ ] Rollback testé pour chaque transition
- [ ] Métriques de latence exposées

## Références
- `HERMES/src/memory_core/sram_dram_tier.py` — implémentation existante
- `HERMES/src/memory_core/toroidal_memory_mapping.py` — mapping tore ↔ tier
- `PRD-MOC-HERMES-MEMORY-POLE-EXTENSION.md` — PRD-MOC parent
