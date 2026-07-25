---
type: ATOM
id: ATOM-004-cache-invalidation-hygiene
version: 1.0.0
date: 2026-07-16
title: "Cache Invalidation Hygiene — Purge systématique du cache après changements structurels"
intent_hash: 0xATOM_CACHE_INVALIDATION_HYGIENE_20260716
status: approved
strate: L1b
---

# ATOM-004 — Cache Invalidation Hygiene

## Contexte

Les compilateurs modernes utilisent des caches d'objets pour accélérer la compilation. Cependant, ces caches peuvent devenir obsolètes après des changements structurels (nouveaux fichiers, signatures modifiées, changements d'ABI), causant des erreurs cryptiques ou des comportements imprévisibles.

## Loi fondamentale

**Après tout changement structurel majeur (nouvelle fonction exportée, modification de signature FFI, ajout de fichiers), purger systématiquement le cache de compilation.**

### Commande de purge

```bash
# Zig
rm -rf zig-cache/

# Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Node.js
rm -rf node_modules/.cache/
```

## Conséquences

- **Erreurs de compilation cryptiques** : "expected struct" au lieu de "function not found"
- **Temps perdu** : heures de debugging pour un problème de cache
- **Frustration de développement** : le code fonctionne en theory, pas en practice

## Recommandations

1. Ajouter une commande de purge dans le Makefile ou package.json
2. Exécuter `rm -rf zig-cache/` après chaque modification FFI
3. Utiliser des scripts de build qui purgent automatiquement
4. Documenter la procédure de purge dans le README

## Références

- ADR-20260621-001-zig-015-api-compatibility
- EPIC-312: Générateur automatique de wrappers FFI

## Référence ADR
- **ADR** : ADR-2026-07-16-004-ATOM-CACHE-INVALIDATION-HYGIENE
- **IntentHash** : 0xADR_CACHE_INVALIDATION_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded