---
type: ATOM
id: ATOM-002-definition-order-constraint
version: 1.0.0
date: 2026-07-16
title: "Definition Order Constraint — Contrainte d'ordre de déclaration dans les compilateurs stricts"
intent_hash: 0xATOM_DEFINITION_ORDER_CONSTRAINT_20260716
status: approved
strate: L1b
---

# ATOM-002 — Definition Order Constraint

## Contexte

Les compilateurs modernes (Zig 0.15 en mode library) imposent un ordre strict de définition des symboles. Contrairement aux langages interprétés ou aux compilateurs en mode exe, un symbole doit être défini avant d'être utilisé dans certaines configurations.

## Loi fondamentale

**Dans les fichiers Zig 0.15 en mode library, les fonctions utilitaires doivent être définies AVANT les fonctions qui les utilisent.**

### Violation courante

```zig
// ❌ FAUX — dispatch_table utilise handle_kiva_run avant définition
const dispatch_table = [_]DispatchEntry{
    .{ .method = "POST", .path = "/kiva-run", .handler = handle_kiva_run },
};

fn handle_kiva_run(...) void { ... } // Définition après utilisation

// ✅ CORRECT — fonctions utilitaires en premier
fn handle_kiva_run(...) void { ... }

const dispatch_table = [_]DispatchEntry{
    .{ .method = "POST", .path = "/kiva-run", .handler = handle_kiva_run },
};
```

## Conséquences

- **Erreur de compilation** : "use of undeclared identifier" ou "expected struct"
- **Différence comportementale** : Fonctionne en mode exe mais pas en mode library
- **Frustration de développement** : L'erreur apparaît après des heures de travail

## Recommandations

1. Structurer les fichiers Zig avec un ordre explicite :
   - Imports et dépendances
   - Types et structures
   - Fonctions utilitaires (en premier)
   - Fonctions principales
   - Dispatch tables et constantes finales
2. Utiliser un générateur de wrappers (EPIC-312) pour automatiser l'ordre correct
3. Tester immédiatement en mode library après chaque modification

## Références

- ADR-20260621-001-zig-015-api-compatibility
- EPIC-312: Générateur automatique de wrappers FFI

## Référence ADR
- **ADR** : ADR-2026-07-16-002-ATOM-DEFINITION-ORDER-CONSTRAINT
- **IntentHash** : 0xADR_DEFINITION_ORDER_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded