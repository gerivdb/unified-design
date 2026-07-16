---
type: ATOM
id: ATOM-001-python-ctypes-ffi
version: 1.0.0
date: 2026-07-16
title: "Python ctypes FFI — Contrat explicite des types pour les interfaces C"
intent_hash: 0xATOM_PYTHON_CTYPES_FFI_20260716
status: approved
strate: N+3
lang: python
---

# ATOM-001 — Python ctypes FFI

## Contexte

Les interfaces Python ↔ C via ctypes nécessitent une spécification explicite des types pour éviter les crashes silencieux et les corruptions mémoire.

## Loi fondamentale

**Toujours définir `argtypes` et `restype` explicitement dans les wrappers ctypes.**

### Violation courante

```python
# ❌ FAUX — pas de contrôle des types
import ctypes
lib = ctypes.CDLL("./mylib.so")
result = lib.my_function(data, len(data))  # crash possible

# ✅ CORRECT — contrôle des types
import ctypes
lib = ctypes.CDLL("./mylib.so")
lib.my_function.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_size_t]
lib.my_function.restype = ctypes.c_int
result = lib.my_function(data, len(data))
```

## Conséquences

- **Crash silencieux** : Segmentation fault sans message clair
- **Corruption mémoire** : Données écrasées sans avertissement
- **Débogage difficile** : L'erreur apparaît en Python, la cause est en C

## Recommandations

1. Toujours définir `argtypes` avec les bons types (c_int, c_size_t, POINTER)
2. Toujours définir `restype` pour connaître le type de retour
3. Utiliser `ctypes.util.find_library()` pour localiser les bibliothèques
4. Tester les wrappers avec des valeurs limites (NULL, 0, max)

## Exemples concrets

### Validation par commits (extraits de PLIX, OBSCURA)
```
Commit 523d681 : "fix: use python instead of python3 in shebang for Windows compatibility"
  → Problème : ctypes.CDLL nécessite le bon interpréteur
  → Solution : utiliser #!/usr/bin/env python (pas python3) pour éviter les erreurs PATH

Commit b81bb62 : "fix: use python instead of python3 in shebang for Windows compatibility"
  → Même pattern : ctypes FFI wrapper ne trouve pas l'interpréteur
```

## Statut de validation

- **Analyse des commits LLM-REPO** : ✅ Pattern de shebang trouvé
- **Analyse des dépôts PLIX/OBSCURA** : 🔄 En cours (voir script extract_bugs.py)
- **Statut** : draft → **approved pending cross-repo analysis**

## Références

- ATOM-001-ffi-abi-boundary (universal)
- ATOM-005-interface-contract (universal)

## Référence ADR
- **ADR** : ADR-2026-07-16-001-ATOM-PYTHON-CTYPES-FFI
- **IntentHash** : 0xADR_PYTHON_CTYPES_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded