---
type: ATOM
id: ATOM-002-c-segfault-debugging
version: 1.0.0
date: 2026-07-16
title: "C Segfault Debugging — gdb, address sanitizer, backtrace analysis"
intent_hash: 0xATOM_C_SEGFAULT_DEBUGGING_20260716
status: approved
strate: N+3
lang: c
---

# ATOM-002 — C Segfault Debugging

## Contexte

Les segmentation faults en C sont souvent difficiles à diagnostiquer sans outils appropriés.

## Loi fondamentale

**Toujours compiler avec `-g -O0` pour le debugging, et utiliser `gdb` ou `addr2line` pour la stack trace.**

### Violation courante

```bash
# ❌ FAUX — compilation release sans debug
gcc -O2 program.c -o program
./program  # segfault, pas de info de debug

# ✅ CORRECT — compilation debug
gcc -g -O0 -fsanitize=address program.c -o program
./program  # segfault + message d'erreur ASan détaillé
```

## Conséquences

- **Debugging blind** : Pas d'information sur l'endroit du crash
- **Heures perdues** : Recherche à l'œil dans un gros fichier
- **Bug non reproduit** : Crash aléatoire sans backtrace

## Recommandations

1. Toujours compiler avec `-g` pour les builds de debug
2. Utiliser `-fsanitize=address,undefined` pour les tests
3. Exécuter `gdb ./program` → `run` → `bt full` au crash
4. Utiliser `addr2line -e program <addr>` pour mapper l'adresse
5. Ajouter des assertions pour les pré-conditions critiques

## Références

- ATOM-004-cache-invalidation-hygiene (universal)

## Référence ADR
- **ADR** : ADR-2026-07-16-002-ATOM-C-SEGFAULT-DEBUGGING
- **IntentHash** : 0xADR_C_SEGFAULT_DEBUGGING_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded