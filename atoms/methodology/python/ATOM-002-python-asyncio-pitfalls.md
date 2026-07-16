---
type: ATOM
id: ATOM-002-python-asyncio-pitfalls
version: 1.0.0
date: 2026-07-16
title: "Python asyncio Pitfalls — Pièges de l'event loop et concurrence"
intent_hash: 0xATOM_PYTHON_ASYNCIO_20260716
status: approved
strate: N+3
lang: python
---

# ATOM-002 — Python asyncio Pitfalls

## Contexte

L'event loop asyncio est source de bugs subtils, surtout avec les intégrations FFI et les threads.

## Loi fondamentale

**Ne jamais utiliser `await` dans un callback synchronise ou dans un thread sans event loop dédié.**

### Violation courante

```python
# ❌ FAUX — await dans callback synchronise
import asyncio
import threading

def thread_func():
    # Erreur: await dans thread sans event loop
    await some_async_function()  # RuntimeError

# ✅ CORRECT — utiliser asyncio.run() ou loop.call_soon_threadsafe()
def thread_func():
    asyncio.run(some_async_function())
```

## Conséquences

- **RuntimeError** : "no running event loop"
- **Deadlocks** : Event loop bloqué par un appel bloquant
- **Perte de concurrence** : Callbacks synchronisés bloquent l'event loop

## Recommandations

1. Toujours avoir un event loop dédié par thread (ou utiliser `asyncio.run()`)
2. Utiliser `loop.call_soon_threadsafe()` pour communiquer thread → event loop
3. Éviter les appels bloquants dans les coroutines
4. Utiliser `asyncio.to_thread()` pour les fonctions bloquantes

## Références

- ATOM-004-cache-invalidation-hygiene (universal)

## Référence ADR
- **ADR** : ADR-2026-07-16-002-ATOM-PYTHON-ASYNCIO-PITFALLS
- **IntentHash** : 0xADR_PYTHON_ASYNCIO_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded