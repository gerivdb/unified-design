---
type: ATOM
id: ATOM-003-rust-cargo-build-pitfalls
version: 1.0.0
date: 2026-07-16
title: "Rust Cargo Build Pitfalls — Cache, features et linking"
intent_hash: 0xATOM_RUST_CARGO_20260716
status: approved
strate: N+3
lang: rust
---

# ATOM-003 — Rust Cargo Build Pitfalls

## Contexte

Cargo est puissant mais son cache et ses features peuvent causer des bugs subtils de construction.

## Loi fondamentale

**Les problèmes de linking FFI symptômes souvent d'un cache Cargo corrompu ou de features mal configurées.**

### Violation courante

```toml
# ❌ FAUX — features qui changent le comportement sans le dire
[features]
default = ["std"]
ffi = []  # active des bindings C

# Le code compile mais le comportement change selon les features activées
```

```bash
# ❌ FAUX — pas de nettoyage du cache
cargo build  # peut utiliser un cache obsolète
```

## Conséquences

- **Binaries différents** : Même commit → binaires différents selon le cache
- **Linking échoué** : Erreurs "cannot find -lfoo" malgré la librairie installée
- **Features conflictuelles** : Code qui compile mais ne fonctionne pas

## Recommandations

1. Utiliser `cargo clean` après les changements de configuration FFI
2. Vérifier les features avec `cargo tree -f "{p} {f}"`
3. Utiliser `CARGO_TARGET_DIR` pour isoler les builds
4. Documenter les features critiques dans le README
5. Utiliser `pkg-config` pour trouver les bibliothèques C

## Références

- ATOM-004-cache-invalidation-hygiene (universal)

## Référence ADR
- **ADR** : ADR-2026-07-16-003-ATOM-RUST-CARGO-PITFALLS
- **IntentHash** : 0xADR_RUST_CARGO_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded