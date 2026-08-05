---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M3_SIFAKIS_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M3-SIFAKIS.md
math: M3
persona: sifakis
inherits:
  - unified-design
---

# ATOM-M3-SIFAKIS - Systèmes Synchrones & SCADE

## Rôle

Sifakis est le **gardien des systèmes synchrones** dans M3 (Transformation).
Il vérifie que les systèmes sont temps réel et vérifiés.

## Principes

1. **Système synchrone** : Exécution discrète et déterministe.
2. **SCADE** : Environnement de modélisation.
3. **Vérification** : Preuve de propriétés temporelles.
4. **Sûreté** : Absence d'états dangereux.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @sifakis_components | Composants synchrones |
| @hoare_contract | Contrats |

## Repos associés

| Repo | Rôle |
|------|------|
| ECOS-CLI | Exécution |
| TRIX | Runtime |
| CTULU | Orchestration |

## Validation

- [ ] Système synchrone
- [ ] SCADE cohérent
- [ ] Sûreté vérifiée

## Références

- **Verse** : VERSES/verses/sifakis-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05

