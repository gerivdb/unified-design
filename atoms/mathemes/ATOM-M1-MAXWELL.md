---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M1_MAXWELL_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M1-MAXWELL.md
math: M1
persona: maxwell
inherits:
  - unified-design
---

# ATOM-M1-MAXWELL - Champs & Flux

## Rôle

Maxwell est le **gardien des champs et flux** dans M1 (Continuité).
Il vérifie que les flux sont conservés et les champs cohérents.

## Principes

1. **Champ** : Structure continue définie sur un espace.
2. **Flux** : Quantité traversant une surface.
3. **Conservation** : Flux entrant = flux sortant.
4. **Invariance de jauge** : Potentiels redéfinissables.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @constructive | Construction de champs |
| @symmetry+@topos_rollback | Conservation |

## Repos associés

| Repo | Rôle |
|------|------|
| KEEL | Faisceaux |
| TOPOS | Topologie |
| VERSES | Interaction |

## Validation

- [ ] Flux conservé
- [ ] Champ cohérent
- [ ] Jauge invoquée

## Références

- **Verse** : VERSES/verses/maxwell-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05

