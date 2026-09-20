---
type: DESIGN
version: "1.0.0"
status: proposed
date: "2026-09-21"
intent_hash: 0xDESIGN_MEMORY_PROVIDER_FALLBACK_20260921
repo: gerivdb/unified-design
layer: L0-CANON
---

# Design — Memory Provider Fallback Chain

## Contexte
HERMES implémente 5 providers mémoire : Mnemo, KG-L, VERSES, VOLTX, BRAIN.
Chaque provider a des forces/faiblesses différentes. Aucun fallback explicite n'est formalisé.

## Problème
- Si Mnemo est indisponible, pas de basculement automatique vers KG-L
- Pas de priorité définie entre providers
- Pas de détection de défaillance en temps réel
- Pas de métrique de qualité par provider

## Solution

### 1. Chaîne de fallback explicite

```
PRIMARY: Mnemo (hot cache, low latency)
  ↓ si indisponible
FALLBACK-1: KG-L (causal graph, structured)
  ↓ si indisponible
FALLBACK-2: VERSES (ontological, semantic)
  ↓ si indisponible
FALLBACK-3: VOLTX (conversational, narrative)
  ↓ si indisponible
FALLBACK-4: BRAIN (cognitive, supermemory)
  ↓ si indisponible
LAST_RESORT: N243 (quantum gate, pending decisions)
```

### 2. Contrat de provider

```python
class MemoryProviderContract:
    name: str
    priority: int  # 1=primary, 2=fallback-1, ...
    max_latency_ms: float
    health_check: Callable[[], bool]
    prefetch: Callable[[str], Optional[MemoryEntry]]
    sync_turn: Callable[[str, str], None]
    shutdown: Callable[[], None]
```

### 3. Détection de défaillance

| Signal | Action | Délai |
|--------|--------|-------|
| Health check échoue | Marquer provider comme DOWN | immédiat |
| Latence > max_latency_ms | Dégrader vers fallback | 100ms |
| Erreur consécutive × 3 | Désactiver provider | 1s |
| Recovery détecté | Réintégrer dans chaîne | 5s |

### 4. Optimisations

1. **Circuit breaker** : éviter les appels à un provider DOWN
2. **Cache de santé** : stocker l'état de chaque provider
3. **Prefetch parallèle** : interroger tous les providers disponibles en parallèle
4. **Merge de résultats** : dédoublonner et trier par pertinence

### 5. Élégance

- Pattern Chain of Responsibility
- Un seul point d'entrée : `MemoryProviderRegistry.fallback_chain()`
- Chaque provider autonome, pas de couplage fort
- Métriques unifiées par provider

## Implémentations

| Composant | Rôle | Fichier |
|-----------|------|---------|
| HERMES | Registry + fallback | `src/memory_provider_registry.py` |
| HERMES | Circuit breaker | `src/memory_core/provider_health.py` |
| Mnemo | Primary provider | `src/memory_providers/mnemo.py` |
| KG-L | Fallback-1 | `src/memory_providers/kgl.py` |
| VERSES | Fallback-2 | `src/memory_providers/verses.py` |
| VOLTX | Fallback-3 | `src/memory_providers/voltx.py` |
| BRAIN | Fallback-4 | `src/memory_providers/brain.py` |
| N243 | Last resort | `src/memory_core/n243_client.py` |

## Critères d'acceptation
- [ ] Chaîne de fallback formalisée
- [ ] Circuit breaker implémenté
- [ ] Détection de défaillance < 1s
- [ ] Recovery automatique < 5s
- [ ] Métriques par provider exposées
- [ ] Tests de basculement passent

## Références
- `HERMES/src/memory_provider_registry.py` — registre existant
- `HERMES/src/memory_providers/*.py` — providers existants
- `PRD-MOC-HERMES-MEMORY-PROVIDER-ABC.md` — PRD-MOC provider ABC
