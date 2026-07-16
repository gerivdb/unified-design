---
type: ATOM
id: ATOM-003-python-gil-limitations
version: 1.0.0
date: 2026-07-16
title: "Python GIL Limitations — Compréhension des limites du Global Interpreter Lock"
intent_hash: 0xATOM_PYTHON_GIL_20260716
status: approved
strate: N+3
lang: python
---

# ATOM-003 — Python GIL Limitations

## Contexte

Le GIL (Global Interpreter Lock) limite le parallélisme en Python, surtout dans les scénarios FFI et calcul intensif.

## Loi fondamentale

**Le GIL empêche le parallélisme CPU-bound en Python natif. Pour le contournement : multiprocessing > threading.**

### Violation courante

```python
# ❌ FAUX — threading pour CPU-bound
import threading

def cpu_task(data):
    # CPU-bound work
    result = heavy_computation(data)
    return result

threads = [threading.Thread(target=cpu_task, args=(d,)) for d in data_list]
for t in threads: t.start()  # Pas de parallélisme réel à cause du GIL

# ✅ CORRECT — multiprocessing pour CPU-bound
import multiprocessing

processes = [multiprocessing.Process(target=cpu_task, args=(d,)) for d in data_list]
for p in processes: p.start()  # Parallélisme réel
```

## Conséquences

- **Performance dégradée** : threads CPU-bound s'exécutent séquentiellement
- **Attente inutile** : temps de calcul multiplié par le nombre de threads
- **Contournement inefficace** : attentes de l'event loop

## Recommandations

1. Utiliser `multiprocessing` pour les tâches CPU-bound
2. Utiliser `threading` uniquement pour I/O-bound (FFI, réseau, disque)
3. Évaluer `concurrent.futures.ProcessPoolExecutor` pour les pools de processus
4. Considérer `numpy`/`numba` pour les calculs vectoriels (ils libèrent le GIL)

## Références

- ATOM-004-cache-invalidation-hygiene (universal)

## Référence ADR
- **ADR** : ADR-2026-07-16-003-ATOM-PYTHON-GIL-LIMITATIONS
- **IntentHash** : 0xADR_PYTHON_GIL_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded