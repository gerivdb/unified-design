---
type: ATOM
id: ATOM-007-error-tree-diagnostics
version: 1.0.0
date: 2026-07-17
title: "Error Diagnostic Tree — Transformation des bugs en arbre de décision pour diagnostic"
intent_hash: 0xATOM_ERROR_TREE_DIAGNOSTICS_20260717
status: proposed
strate: L1b
---

# ATOM-007 — Error Diagnostic Tree

## Contexte

Lors du développement de systèmes GPU/CPU multi-threadés, les erreurs peuvent être difficiles à diagnostiquer car elles traversent plusieurs couches (GPU driver, FFI, queue, threading).

## Loi fondamentale

**Transformer chaque exception en un arbre de diagnostic avec :**
1. **Code d'erreur numérique** (pour tracing)
2. **Message catégorisé** (GPU, MEMORY, TIMEOUT, etc.)
3. **Stack de contexte** (chemin d'exécution)

### Violation courante

```python
# ❌ FAUX — Exception non catégorisée
except Exception as e:
    logger.error("[Decoder] Decode loop error: %s", e)
```

### ✅ CORRECT — Arbre de diagnostic

```python
class DecodeError(Exception):
    """Base error for decode operations."""
    error_code: int = 1000
    
class GPUDecodeError(DecodeError):
    """GPU decode specific errors."""
    error_code: int = 1001
    
class NVDECDllError(GPUDecodeError):
    """NVDEC DLL specific errors."""
    error_code: int = 1002
```

## Structure de l'arbre

```
DecodeError (1000)
├── GPUDecodeError (1001)
│   ├── NVDECDllError (1002)
│   ├── ContextCreationError (1003)
│   └── FrameCallbackError (1004)
├── MemoryError (2000)
│   ├── QueueFullError (2001)
│   └── BufferAllocationError (2002)
└── TimeoutError (3000)
    ├── FrameTimeout (3001)
    └── CallbackTimeout (3002)
```

## Paramètres

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `error_code` | int | auto | Code numérique unique de l'erreur |
| `category` | string | auto | Catégorie (GPU, MEMORY, TIMEOUT, etc.) |
| `context_stack` | list | [] | Pile de contexte pour tracing |

## Références

- ATOM-006-error-diagnostic-tree
- INTENT-303: Pipeline Sync GPU→CPU
- ADR-0013: Short-circuit NEUTRE

## Référence ADR
- **ADR** : ADR-2026-07-17-007-ERROR-TREE-DIAGNOSTICS
- **IntentHash** : 0xADR_ERROR_TREE_DIAGNOSTICS_20260717
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded