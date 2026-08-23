---
type: CONVENTION
version: "1.0.0"
date: 2026-08-23
status: accepted
intent_hash: 0xENCODING_UTF8_MIGRATION_20260823
design_id: U-C7
decided_by: HITL Linus (Option A) -- review 0xUNIFIED_DESIGNS_MANQUANTS_V1
source_intent: INTENT-2026-08-22-GOVERNANCE-HUB-PRD-MOC-RESTRUCTURING
layer: L0
---

# ENCODAGE_UTF8.md — Norme d'encodage de l'écosystème

## Décision

**UTF-8 partout, sans exception.** CP1252 est un résidu legacy aboli comme contrainte.

## Contexte du conflit résolu

Le hook `pre-commit-encoding-check` v1.0.0 (IntentHash `0xPRE_COMMIT_ENCODING_CHECK_20260603`)
bloquait tout caractère > U+007F dans les fichiers de gouvernance — héritage ENV2/Windows
CP1252. Effet : l'écriture française légitime (em-dash, box-drawing des arbres, flèches,
œ) était rejetée dans les ADR, INTENTs et PRD MOC, pendant que le contenu UTF-8 existait
partout ailleurs. Deux règles contradictoires coexistaient sans arbitrage.

## Règles

| # | Règle |
|---|-------|
| E1 | Tout fichier texte est encodé **UTF-8 sans BOM** (BOM toléré en lecture, à proscrire en écriture) |
| E2 | Les hooks valident la **validité UTF-8**, jamais une plage Unicode maximale |
| E3 | Caractères invisibles toxiques bloqués : zero-width (U+200B-D), word-joiner (U+2060), BOM interne (U+FEFF) |
| E4 | Pictogrammes décoratifs (U+1F300+) : warning non bloquant — usage limité, jamais dans scripts/hooks |
| E5 | Scripts Python déclarent `# -*- coding: utf-8 -*-` ; PowerShell : fichiers sauvegardés UTF-8 sans BOM |
| E6 | Toute migration future de repo vérifie ses hooks d'encodage dans le même commit (pattern contrat-adossement) |

## Anti-régression

- Le hook `pre-commit-encoding-check` **v2.0.0** implémente E1-E4 (GOVERNANCE-HUB)
- `check-prd-structure.ps1 -Mode report` signale tout artefact non décodable UTF-8
- Toute réintroduction d'un blocage par plage Unicode nécessite un nouvel ADR

## Historique

| Version | Date | Changement |
|---------|------|------------|
| 1.0.0 | 2026-06-03 | Blocage U+0100+ (CP1252 legacy) |
| 2.0.0 | 2026-08-23 | **Option A** : UTF-8 partout, validation stricte, invisibles toxiques seuls bloqués |
