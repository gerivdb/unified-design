---
type: ATOM
status: active
date: "2026-08-05"
intent_hash: 0xATOM_MATHEME_M2_VAPNIK_20260805
strate: L0-CANON
author: gerivdb
source_repo: gerivdb/unified-design
source_path: atoms/mathemes/ATOM-M2-VAPNIK.md
math: M2
persona: vapnik
inherits:
  - unified-design
---

# ATOM-M2-VAPNIK - VC Dimension & Généralisation

## Rôle

Vapnik est le **gardien de la généralisation** dans M2 (Information).
Il vérifie que les modèles généralisent et ne surapprennent pas.

## Principes

1. **VC dimension** : Capacité du modèle à séparer.
2. **Généralisation** : Performance sur données non vues.
3. **Séparabilité** : Existence d'un hyperplan séparateur.
4. **Marge** : Distance à l'hyperplan.

## Patterns associés

| Pattern | Action |
|---------|--------|
| @vapnik_vc | Généralisation |
| @learning | Apprentissage |

## Repos associés

| Repo | Rôle |
|------|------|
| BRAIN | Mémoire cognitive |
| LLM-REPO | Boot protocol |
| VERSES | Interaction |

## Validation

- [ ] VC dimension bornée
- [ ] Généralisation vérifiée
- [ ] Surapprentissage évité

## Références

- **Verse** : VERSES/verses/vapnik-verse.md
- **ADR** : ADR-MATHEMES-PERSONAS-ORCHESTRATION-2026-08-05

