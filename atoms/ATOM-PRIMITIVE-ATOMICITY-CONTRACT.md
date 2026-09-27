# ATOM-PRIMITIVE-ATOMICITY-CONTRACT

## Description

Primitive d'atomicité contractuelle pour le MDU. Formalise la règle `max_nesting_depth <= 3` et la rend enforceable par les workflows MDU.

## États obligatoires

| État | Nature | Gate |
|---|---|---|
| IDLE | En attente de vérification | AUDIT |
| AUDIT | Vérification de la profondeur de dépendance | PASS / FAIL |
| PASS | Conforme | Enregistrer |
| FAIL | Non conforme | Documenter dérogation |

## Fonctions obligatoires

1. **AUDITER_DEPENDANCES** — audit de la profondeur de dépendance du design
2. **VÉRIFIER_MAX_NESTING** — vérification `max_nesting_depth <= 3`
3. **DÉROGATION** — gestion des dérogations documentées
4. **VALIDER_PREUVE** — validation de la preuve horodatée
5. **BLOQUER_SI_VIOLATION** — blocage si `max_nesting_depth > 3` sans dérogation
6. **ENREGISTRER_TRACE** — enregistrement horodaté

## Règles

1. Tout design MDU respecte `max_nesting_depth <= 3`, sauf dérogation documentée.
2. Toute dérogation est documentée dans `design.schema.json`.
3. Tout design est vérifié avant intégration.
4. Toute vérification est tracée et horodatée.

## Anti-patterns

| Gène manquant | Pathologie |
|---|---|
| max-nesting-depth | Dépendances profondes → complexité cognitive ingérable |
| documented-derogation | Dérogations implicites → dettes techniques invisibles |
| verification-systematic | Designs non vérifiés → violations silencieuses |
| traceability | Vérifications sans traçabilité → impossibilité d'auditer |

## Invariant central

Tout design MDU respecte `max_nesting_depth <= 3`, sauf dérogation documentée.

## Références

- **Primitive** : `primitives/primitive-atomicity-contract.yaml`
- **IntentHash** : `0xPRIMITIVE_ATOMICITY_CONTRACT_20260921`
- **Dépôt** : gerivdb/unified-design
- **Parent** : `design-ops-loop`, `safe-action-pattern`, `ecosystem-meta-coherence`
