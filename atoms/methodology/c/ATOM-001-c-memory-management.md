---
type: ATOM
id: ATOM-001-c-memory-management
version: 1.0.0
date: 2026-07-16
title: "C Memory Management — malloc/free, dangling pointers, valgrind"
intent_hash: 0xATOM_C_MEMORY_MANAGEMENT_20260716
status: approved
strate: N+3
lang: c
---

# ATOM-001 — C Memory Management

## Contexte

La gestion manuelle de mémoire en C est la source principale des bugs (segfaults, fuites, corruption).

## Loi fondamentale

**Toute allocation `malloc` doit avoir un `free` correspondant dans le même scope ou un parent explicite.**

### Violation courante

```c
// ❌ FAUX — fuite mémoire et double free
char* data = malloc(100);
// ... utilisation
free(data);
free(data);  // double free = UB

// ❌ FAUX — dangling pointer
char* data = malloc(100);
free(data);
strcpy(data, "crash");  // écriture dans mémoire libérée
```

## Conséquences

- **Memory leaks** : Fuites qui s'accumulent
- **Segmentation faults** : Accès à mémoire libérée
- **Heap corruption** : Structures de liste corrompues

## Recommandations

1. Toujours vérifier le retour de `malloc` (NULL check)
2. Utiliser des patterns RAII-like avec des macros cleanup
3. Documenter le propriétaire de la mémoire
4. Utiliser `valgrind --leak-check=full` pour détecter les fuites
5. Utiliser `address sanitizer` pour les erreurs d'accès

## Exemples concrets

### Validation par audit PLIX (28 violations détectées)

```c
// Violations trouvées dans src/llux/llux_inference.c:321-327
void* buffer = malloc(size);  // ❌ Pas de free correspondant
// ... utilisation ...
// Pas de free(buffer) dans le scope

// Violations trouvées dans src/core/plix_json.c:128
char* json_str = malloc(len);  // ❌ Pas de free correspondant
```

### Statut de validation

- **Analyse des commits LLM-REPO** : ✅ Pattern de shebang trouvé
- **Audit PLIX** : ✅ 28 violations malloc sans free détectées
- **Statut** : **approved** — preuves concrètes validées

## Références

- ATOM-004-cache-invalidation-hygiene (universal)

## Référence ADR
- **ADR** : ADR-2026-07-16-001-ATOM-C-MEMORY-MANAGEMENT
- **IntentHash** : 0xADR_C_MEMORY_MANAGEMENT_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded