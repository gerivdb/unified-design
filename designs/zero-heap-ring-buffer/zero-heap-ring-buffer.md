# Zero-Heap Ring Buffer & Synchronous Pipeline

> Pipeline 30 Hz C99/Zig sans allocation dynamique ni locks.

## Vue d'ensemble

**Zero-Heap Ring Buffer** est un pipeline synchrone pour le traitement d'inférence ultra-basse latence. Toutes les mémoires sont allouées au démarrage (stack ou static), aucune allocation dynamique n'est autorisée pendant l'exécution.

## Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   PRODUCER  │───▶│  RING BUF   │───▶│  WORKER 0   │───▶│  CONSUMER  │
│  (HTTP)     │    │  (fixed N)  │    │  (RBF)      │    │  (Response) │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                  │
                          ▼                  ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  WORKER N   │    │  FALLBACK   │
                   │  (LLM)      │    │  (slow)     │
                   └─────────────┘    └─────────────┘

Caractéristiques:
• Ring buffer statique : [N]T où N = puissance de 2
• Sans locks : atomic CAS sur head/tail
• Sans heap : tous les buffers alloués au démarrage
• Sans malloc : utilisation de slab allocator ou arena statique
• Synchronous : pas de async/await, pas de green threads
```

## Composants

| Composant | Technologie | Paramètres |
|:---|:---|:---|
| Ring Buffer | C99/Zig static array | N = 256 (puissance de 2) |
| Synchronization | Atomic CAS | head/tail 32-bit |
| Workers | Thread pool | 16 threads max |
| Memory | Stack / Static | < 64 ko total |
| Frequency | 30 Hz | 33 ms par cycle |

## Budgets

| Resource | Budget |
|----------|--------|
| Mémoire totale | < 64 ko |
| Allocation dynamique | 0 (interdite) |
| Locks | 0 (CAS uniquement) |
| Latence par étape | < 1 ms |
| Débit | 30 Hz (33 ms par cycle) |

## Dépendances

| Dépendance | Type | Rôle |
|:---|:---|:---|
| runner-contract | ONTOLOGY concept | Contrat ACP |
| rbf-cluster | ONTOLOGY concept | Moteur RBF |

## Tests

- [ ] 0 malloc/heap allocation pendant 1h de fonctionnement
- [ ] P99 latence par étape < 1 ms
- [ ] Débit soutenu 30 Hz sur 24h
- [ ] CAS lock-free sur head/tail

## Références

- ADR-2026-08-29-001-neuro-symbolic-rbf-operationalization
- Revue PRD Bellard.md (exécution C99/Zig sans tas)
