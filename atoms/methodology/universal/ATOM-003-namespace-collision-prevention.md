---
type: ATOM
id: ATOM-003-namespace-collision-prevention
version: 1.0.0
date: 2026-07-16
title: "Namespace Collision Prevention — Stratégie de préfixage pour éviter les collisions de noms"
intent_hash: 0xATOM_NAMESPACE_COLLISION_PREVENTION_20260716
status: approved
strate: L1b
---

# ATOM-003 — Namespace Collision Prevention

## Contexte

Lors de l'évolution d'un langage, les mots-clés réservés peuvent changer ou être ajoutés. Les noms de fonctions ou variables existants peuvent devenir des mots-clés réservés, causant des conflits de compilation.

## Loi fondamentale

**Toujours préfixer les fonctions exposées via FFI avec un préfixe unique (ex: `plix_*`) pour éviter les collisions avec les mots-clés langue.**

### Violation courante

```zig
// ❌ FAUX — nom qui entre en conflit avec un mot-clé futur
export fn unpack(data: []const u8) bool { ... }

// ✅ CORRECT — préfixage explicite
export fn plix_unpack(data: []const u8) bool { ... }
```

## Conséquences

- **Erreur de compilation** : "use of undeclared identifier" ou "unexpected token"
- **Rétro-compatibilité brisée** : Une mise à jour de langue casse le code
- **Migration coûteuse** : Renommage manuel de plusieurs centaines de fonctions

## Recommandations

1. Définir un préfixe de nommage global (ex: `plix_`, `kiva_`, `trix_`)
2. Appliquer le préfixe systématiquement à toutes les fonctions exportées
3. Documenter le préfixe dans le README du module
4. Utiliser des outils de recherche pour vérifier l'absence de mots-clés réservés

## Références

- ADR-20260621-001-zig-015-api-compatibility
- EPIC-312: Générateur automatique de wrappers FFI

## Référence ADR
- **ADR** : ADR-2026-07-16-003-ATOM-NAMESPACE-COLLISION-PREVENTION
- **IntentHash** : 0xADR_NAMESPACE_COLLISION_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded