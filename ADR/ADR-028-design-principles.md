---
type: ADR
status: proposed
date: "2026-07-16"
intent_hash: 0xADR_028_DESIGN_PRINCIPLES_20260716
---

# ADR-028 — Intégration des Principes de Conception dans le MDU

## Contexte

L'analyse des conversations KiloCode et des documents WAZAA a révélé la nécessité de formaliser les **principes de conception logicielle** dans le Meta-Design Atlas (MDU). Ces principes (SOLID, DRY, KISS, YAGNI, etc.) sont des invariants universels qui transcendent les langages et les paradigmes.

## Décision

Intégrer les **10 principes de conception** comme atomes MDU avec :

1. **Atome parent** : `design-principle` (catégorie Principle)
2. **Atomes enfants** : SRP, LSP, ISP, DIP, KISS, YAGNI, LoD, POLA, CoC
3. **Index mis à jour** : `L1-INFRA_Atoms_Index.yaml`
4. **Validation CLI** : `gerivdb design validate --principles`

## Principes ajoutés

| Atome | Principe | Description |
|-------|----------|-------------|
| `design-principle` | - | Atome parent pour tous les principes |
| `srp` | Single Responsibility | Une seule responsabilité par entité |
| `lsp` | Liskov Substitution | Les sous-types remplacent les types de base |
| `isp` | Interface Segregation | Interfaces fines et spécifiques |
| `dip` | Dependency Inversion | Dépendre des abstractions |
| `kiss` | Keep It Simple | Éviter la complexité inutile |
| `yagni` | You Aren't Gonna Need It | Implémenter uniquement ce qui est demandé |
| `law-of-demeter` | LoD | Ne pas naviguer profondément |
| `principle-of-least-astonishment` | POLA | Comportement prévisible |
| `convention-over-configuration` | CoC | Conventions par défaut |

## Couverture des principes SOLID

| Principe | Atome existant | Statut |
|----------|----------------|--------|
| SRP | `srp` (nouveau) | ✅ Ajouté |
| OCP | `incremental-growth` | ✅ Couvert |
| LSP | `lsp` (nouveau) | ✅ Ajouté |
| ISP | `isp` (nouveau) | ✅ Ajouté |
| DIP | `dip` (nouveau) | ✅ Ajouté |

## Impact sur le MDU

- **Atomes totaux** : 73 → **84 atomes** (+11 principes)
- **Types d'atomes** : 15 types → **16 types** (+Principle)
- **Validation** : Nouveau flag `--principles` dans le CLI

## Validation des principes

```bash
# Valider qu'un design respecte les principes
gerivdb design validate --principles SRP,KISS,YAGNI

# Vérifier LSP sur un module
ctulu validate-lsp --module src/wazaa_bus_citizens/

# Vérifier CoC dans un projet
ctulu validate-coc --path ./src/
```

## Références

- SOLID Principles (Robert C. Martin)
- DRY, KISS, YAGNI (Andy Hunt, Dave Thomas)
- Law of Demeter (Ian Holland)
- Principle of Least Astonishment (Gerald Weinberg)
- Convention over Configuration (Rails)

## Statut

- **Date** : 2026-07-16
- **Statut** : proposed
- **Prochaine étape** : Revues par l'équipe architecturale