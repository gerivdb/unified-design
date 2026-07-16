---
type: ATOM
id: ATOM-006-error-diagnostic-tree
version: 1.0.0
date: 2026-07-16
title: "Error Diagnostic Tree — Transformation des bugs en arbre de décision pour diagnostic"
intent_hash: 0xATOM_ERROR_DIAGNOSTIC_TREE_20260716
status: approved
strate: L1b
---

# ATOM-006 — Error Diagnostic Tree

## Contexte

Les erreurs de compilation ou d'exécution sont souvent le fruit de plusieurs causes possibles. Un arbre de diagnostic permet de guider le développeur à travers les hypothèses jusqu'à la solution.

## Loi fondamentale

**Chaque bug résolu doit être transformé en un nœud dans un arbre de diagnostic, avec les questions à poser et les solutions possibles.**

### Exemple : Erreur de compilation Zig FFI

```
Erreur: "expected struct" ou "expected 1 argument"
├── Vérifier l'ordre des paramètres FFI
│   ├── usize/*const u8 → inverser l'ordre ✅
│   └── u32/*const u8 → utiliser u32 au lieu de usize
├── Vérifier si le symbole est défini
│   ├── Bibliothèque non recompilée → purger zig-cache/
│   └── Fonction mal nommée → vérifier le préfixe
└── Vérifier la version Zig
    ├── Zig 0.15 buggé → utiliser workaround u64
    └── Zig 0.14 fonctionnel → recompiler en mode exe
```

## Conséquences

- **Temps de debugmultiplié** : Chaque développeur doit rouper à travers les mêmes hypothèses
- **Connaissance non partagée** : Les solutions restent dans la tête du développeur
- **Rétro-apprentissage** : Les nouveaux membres prennent du temps pour les mêmes bugs

## Recommandations

1. Documenter chaque bug résolu dans un format arbre
2. Créer un index des arbres de diagnostic par type d'erreur
3. Intégrer les arbres dans les messages d'erreur (suggestions)
4. Maintenir les arbres à jour avec les nouvelles versions

## Références

- ADR-20260621-001-zig-015-api-compatibility
- EPIC-312: Générateur automatique de wrappers FFI

## Référence ADR
- **ADR** : ADR-2026-07-16-006-ATOM-ERROR-DIAGNOSTIC-TREE
- **IntentHash** : 0xADR_ERROR_DIAGNOSTIC_TREE_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded