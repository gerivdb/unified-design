---
type: ATOM
id: ATOM-001-ffi-abi-boundary
version: 1.0.0
date: 2026-07-16
title: "FFI ABI Boundary — Loi fondamentale des interfaces entre langages compilés"
intent_hash: 0xATOM_FFI_ABI_BOUNDARY_20260716
status: approved
strate: L1b
---

# ATOM-001 — FFI ABI Boundary

## Contexte

Lors de l'intégration entre langages compilés (Zig, C, Python via FFI), les frontières d'interface sont des espaces critiques où les conventions d'appel (ABI) doivent être strictement respectées. Les violations d'ABI provoquent des crashes silencieux, des corruptions mémoire, ou des erreurs de compilation.

## Loi fondamentale

**Toujours placer les types scalaires (usize, u32, i64) AVANT les pointeurs dans les signatures d'export C.**

L'ABI Microsoft x64 définit les registres de passage des arguments :
- RCX, RDX, R8, R9 pour les 4 premiers arguments
- Les types scalaires de 64 bits tiennent dans un registre
- Les pointeurs tiennent dans un registre
- Mais l'ordre affecte l'attribution des registres

### Violation courante

```zig
// ❌ FAUX — usize après pointeur
export fn callback(data: *const u8, len: usize) void { ... }

// ✅ CORRECT — usize avant pointeur
export fn callback(len: usize, data: *const u8) void { ... }
```

## Conséquences

- **Crash systématique** : L'appel peut passer les arguments dans les mauvais registres
- **Debugging difficile** : Erreur apparaît à l'appelant, pas à l'appelé
- **Non-portabilité** : Le bug apparaît sous Windows, pas sous Linux (ABI différent)

## Recommandations

1. Utiliser `u32` pour les tailles de buffers (compatible avec la plupart des ABI)
2. Utiliser `u64` pour les pointeurs si nécessaire
3. Documenter explicitement l'ordre des paramètres dans les commentaires
4. Tester en mode library (pas seulement en mode exe)

## Références

- ADR-20260621-001-zig-015-api-compatibility
- EPIC-312: Générateur automatique de wrappers FFI

## Référence ADR
- **ADR** : ADR-2026-07-16-001-ATOM-FFI-ABI-BOUNDARY
- **IntentHash** : 0xADR_FFI_ABI_BOUNDARY_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded