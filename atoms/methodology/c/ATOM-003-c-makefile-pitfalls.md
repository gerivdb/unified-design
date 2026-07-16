---
type: ATOM
id: ATOM-003-c-makefile-pitfalls
version: 1.0.0
date: 2026-07-16
title: "C Makefile Pitfalls — Implicit dependencies, PHONY, environment variables"
intent_hash: 0xATOM_C_MAKEFILE_PITFALLS_20260716
status: approved
strate: N+3
lang: c
---

# ATOM-003 — C Makefile Pitfalls

## Contexte

Les Makefiles C sont source de bugs de build, surtout avec les dépendances implicites et les variables d'environnement.

## Loi fondamentale

**Toujours déclarer explicitement les dépendances et utiliser `.PHONY` pour les cibles non-fichiers.**

### Violation courante

```makefile
# ❌ FAUX — dépendance implicite
program: main.o utils.o
	gcc main.o utils.o -o program

main.o: main.c
	gcc -c main.c -o main.o
# Manque: header.h comme dépendance explicite

# ❌ FAUX — cible phony non déclarée
clean:
	rm -f *.o program
# Si fichier "clean" existe, make ne l'exécutera pas
```

## Conséquences

- **Builds incohérents** : Fichiers non recompilés après changement d'header
- **Échecs de clean** : `make clean` ne fonctionne pas si fichier "clean" existe
- **Variables d'environnement** : Comportement différent selon l'environnement

## Recommandations

1. Toujours utiliser `.PHONY: clean all install`
2. Déclarer les headers comme dépendances : `main.o: main.c utils.h`
3. Utiliser des variables pour les outils : `CC ?= gcc`, `CFLAGS ?= -Wall`
4. Utiliser `make -d` pour le debug des règles
5. Ajouter `.DELETE_ON_ERROR` pour nettoyer en cas d'échec

## Références

- ATOM-004-cache-invalidation-hygiene (universal)

## Référence ADR
- **ADR** : ADR-2026-07-16-003-ATOM-C-MAKEFILE-PITFALLS
- **IntentHash** : 0xADR_C_MAKEFILE_PITFALLS_20260716
- **Dépôt** : gerivdb/LLM-REPO
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded