---
type: ATOM
id: ATOM-002-rust-unsafe-ffi
version: 1.0.0
date: 2026-07-16
title: "Rust unsafe FFI — Bonnes pratiques pour les interfaces non sûres"
intent_hash: 0xATOM_RUST_UNSAFE_FFI_20260716
status: approved
strate: N+3
lang: rust
---

# ATOM-002 — Rust unsafe FFI

## Contexte

Les interfaces FFI en Rust nécessitent du code `unsafe`, qui doit être extrêmement bien maîtrisé.

## Loi fondamentale

**Le code `unsafe` doit être isolé dans des fonctions publiques bien documentées. Toute autre partie du code doit appeler ces fonctions en toute sécurité.**

### Violation courante

```rust
// ❌ FAUX — unsafe dispersé partout
fn main() {
    let ptr = data.as_ptr();
    unsafe {
        libc::free(ptr as *mut libc::c_void);  // risque élevé
    }
}

// ✅ CORRECT — wrapper safe enveloppe unsafe
fn free_buffer(ptr: *mut c_void) {
    unsafe {
        libc::free(ptr as *mut libc::c_void);
    }
}

fn main() {
    free_buffer(ptr);  // appel sûr
}
```

## Conséquences

- **Undefined behavior silencieux** : UB non détecté à la compilation
- **Corruption mémoire** : Données écrasées sans erreur apparente
- **Debugging impossible** : Comportement non reproductible

## Recommandations

1. Toujours encapsuler le `unsafe` dans des fonctions avec contrat clair
2. Documenter les pré-conditions et post-conditions
3. Utiliser `std::ffi::CStr` et `CString` pour les chaînes C
4. Vérifier les pointeurs NULL avant utilisation
5. Utiliser `bindgen` pour générer les bindings FFI automatiquement

## Références

- ATOM-001-ffi-abi-boundary (universal)
- ATOM-005-interface-contract (universal)

## Référence ADR
- **ADR** : ADR-2026-07-16-002-ATOM-RUST-UNSAFE-FFI
- **IntentHash** : 0xADR_RUST_UNSAFE_FFI_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded