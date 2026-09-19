---
status: proposed
date: "2026-09-19"
intent_hash: 0xADR_SAFE_ACTION_PATTERN_20260919
---

# ADR-2026-09-19 — Adoption de PATRON-0 comme micro-design d'action universelle dans le MDU

## Contexte

Le Meta-Design Unifié (`unified-design`) contient déjà des concepts dispersés qui formalisent la sécurité des actions en environnement incertain :

- **Think/Do/Check Consciousness** — conscience ternaire macro
- **Gate Layers** — barrière de contrôle à 4 couches
- **External Verification Mandatory** — "l'agent ne se relit pas"
- **Stop Condition** — condition d'arrêt explicite
- **Confidence Threshold** — seuil 0.6
- **Independent Sources Rule** — 2 sources indépendantes
- **U-Model Agent-Ready Data** — modèle de données agent-ready
- **Delta Check** — vérification incrémentale
- **Carry Forward Principle** — travail valide reporté
- **Approval Readiness** — gate de validation avant merge

**Problème** : Ces concepts existent dispersés. Il n'y a pas de **patron d'action universel** qui les agrège en une checklist enforceable, avec une machine d'état explicite (PROJECT → PROGRESS → BILAN), un invariant central, et des anti-patrons documentés.

**Conséquence** : Les agents KiloCode peuvent engager des actions irréversibles sans avoir rempli toutes les conditions de sécurité, car il n'y a pas de gate pré-action unique et vérifiable.

## Décision

Adopter **PATRON-0** comme micro-design `safe-action-pattern` dans le MDU, avec :

1. **Design `safe-action-pattern`** (`designs/safe-action-pattern.yaml`) — 7 fonctions + 3 états + 1 invariant + 4 gènes + anti-patrons
2. **Atom `safe-action-gate`** (`atoms/safe-action-gate.md`) — version enforceable pour CI/hooks
3. **Enregistrement dans `META-DESIGN.md` et `meta-design.yaml`**

## Structure PATRON-0

```
[PROJECT]  1. PERCEVOIR      (multi-source, ordonné, redondant)
           2. ÉVALUER        (multi-axes, indépendants)
           3. SE_MODÉLISER   (capacité propre + incertitude propre)
           4. RÉSERVER       (marge de sûreté / plan de repli)
           5. VALIDER        (gate : les 4 précédents sont-ils suffisants ?)

[PROGRESS] 6. AGIR           (engagement, irréversible)
              + MONITORER    (invariants tenus pendant l'action)

[BILAN]    7. VALIDER_RÉEL   (succès constaté dans le monde, pas prédit)
              + ENREGISTRER  (mémoire → héritage)
```

**Invariant central** : *le succès n'est jamais déclaré avant la fin réelle de l'action.*

**4 gènes universels** :
1. **Pluralité** — une seule source de perception est toujours insuffisante
2. **Auto-modèle** — l'agent doit modéliser sa propre capacité et son incertitude
3. **Réserve** — toute action engage une marge (rollback, budget, plan de repli)
4. **Validation réelle** — le succès n'existe que constaté, jamais prédit

## Alternatives considérées

| Alternative | Raison du rejet |
|---|---|
| Laisser les concepts dispersés | Pas de checklist enforceable, risque d'oubli de fonctions |
| Créer un design par concept | Duplication, pas d'agrégation, complexité accrue |
| Intégrer dans `approval-readiness` uniquement | `approval-readiness` couvre la validation finale, pas la micro-structure d'action |
| Intégrer dans `chain-engineering` uniquement | `chain-engineering` couvre le chaînage, pas la gate pré-action obligatoire |

## Conséquences

### Positives

- **Checklist enforceable** : chaque action peut être vérifiée contre les 7 fonctions
- **Gate pré-action explicite** : F5 VALIDER bloque l'engagement si les 4 premières fonctions ne sont pas remplies
- **Invariant central documenté** : le succès n'est jamais déclaré avant la fin réelle
- **Anti-patrons formalisés** : mapping défaillance → pathologie → correction
- **Compatibilité MDU** : hérite de designs existants, ne duplique pas

### Négatives

- **Complexité apparente** : 7 fonctions + 3 états peuvent sembler lourdes pour des actions simples
- **Risque de bypass** : les agents peuvent ignorer la gate si elle n'est pas enforceable par CI
- **Surcoût cognitif** : chaque action doit maintenant passer par PROJECT → PROGRESS → BILAN

### Mitigations

- La gate F5 VALIDER est **uniquement une vérification**, pas une exécution lourde
- Les hooks CI peuvent vérifier la présence des 7 fonctions dans les preuves d'exécution
- Pour actions simples, PROJECT est quasi-instantané (perception rapide + validation rapide)
- L'atom `safe-action-gate` fournit des règles exploitables par les validators

## Références

- **Intent** : `INTENT-2026-09-19-SAFE-ACTION-PATTERN.md`
- **PRD-MOC** : `PRD/PRD-MOC-SAFE-ACTION-PATTERN-20260919.md`
- **MOC** : `MOC-SAFE-ACTION-PATTERN-20260919.md`
- **Design** : `designs/safe-action-pattern.yaml`
- **Atom** : `atoms/safe-action-gate.md`
- **MDU** : `META-DESIGN.md`, `meta-design.yaml`
- **ADR Think/Do/Check** : `ADR-2026-09-12-001-THINK-DO-CHECK-ARCHITECTURE.md`
- **Parent MDU** : `ATOM-THINK-DO-CHECK-CONSCIOUSNESS`, `ATOM-GATE-LAYERS`, `ATOM-EXTERNAL-VERIFICATION-MANDATORY`, `ATOM-STOP-CONDITION`, `ATOM-CONFIDENCE-THRESHOLD`, `ATOM-INDEPENDENT-SOURCES-RULE`, `ATOM-UMODEL-AGENT-READY-DATA`, `ATOM-DELTA-CHECK`, `ATOM-CARRY-FORWARD-PRINCIPLE`
