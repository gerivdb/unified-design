---
type: ATOM
id: ATOM-001-rust-borrow-checker
version: 1.0.0
date: 2026-07-16
title: "Rust Borrow Checker — Stratégies pour surmonter les restrictions d'emprunt"
intent_hash: 0xATOM_RUST_BORROW_CHECKER_20260716
status: approved
strate: N+3
lang: rust
---

# ATOM-001 — Rust Borrow Checker

## Contexte

Le borrow checker est la barrière la plus fréquente pour les nouveaux Rustiens, surtout avec les structures complexes et les traits.

## Loi fondamentale

**Chaque valeur a exactement un propriétaire. Les références empruntées doivent respecter les règles : emprunt mutable exclusive, emprunts immuables multiples autorisés.**

### Violation courante

```rust
// ❌ FAUX — double emprunt mutable
fn main() {
    let mut data = vec![1, 2, 3];
    let first = &mut data[0];
    let second = &mut data[1];  // Erreur: emprunt mutable déjà actif
}

// ✅ CORRECT — scope des emprunts
fn main() {
    let mut data = vec![1, 2, 3];
    {
        let first = &mut data[0];
        *first = 10;
    }  // drop de first
    let second = &mut data[1];  // OK
}
```

## Conséquences

- **Erreurs d'emprunt complexes** : "cannot borrow X as mutable because it is also borrowed as immutable"
- **Code verrouillé** : Difficultés à structurer les données pour satisfaire le borrow checker
- **Temps de développement** : Heures passées à restructurer le code

## Recommandations

1. Utiliser `RefCell<T>` pour les emprunts dynamiques (runtime checked)
2. Utiliser `Rc<RefCell<T>>` pour les structures partagées
3. Séparer les responsabilités dans des structs différents
4. Utiliser `std::mem::drop()` pour libérer les emprunts explicitement
5. Envisager les `async` blocks pour les fonctions longues

## Références

- ATOM-002-definition-order-constraint (universal)

## Référence ADR
- **ADR** : ADR-2026-07-16-001-ATOM-RUST-BORROW-CHECKER
- **IntentHash** : 0xADR_RUST_BORROW_CHECKER_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded