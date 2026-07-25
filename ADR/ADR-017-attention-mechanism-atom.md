---
status: proposed
date: "2026-07-15"
intent_hash: 0xADR_0017_ATTENTION_MECHANISM_ATOM
---

# ADR-017 — Intégration de l'atome `attention-mechanism` issu d'UAE

## Contexte

Le citoyen `UAE` (L3-CITIZENS/N3) implémente un moteur d'attention universelle
`1/sqrt(d)`, fondation cognitive transverse de l'écosystème gerivdb.

UAE n'est pas un dépôt de design MDU, mais son pattern peut être capitalisé
sous forme d'atome réutilisable pour d'autres designs.

## Décision

Créer un atome `attention-mechanism` dans `unified-design/atoms/` qui capture
les contraintes et paramètres génériques du mécanisme d'attention d'UAE.

L'atome est référencé dans `meta-design.yaml` pour être disponible par héritage.

## Rationale

- **Réutilisation** : Les designs futurs peuvent hériter de cet atome pour exiger
  une capacité d'attention sans dupliquer les contraintes.
- **Abstraction** : L'atome reste une abstraction ; l'implémentation réelle
  demeure dans le citizen UAE.
- **Expressivité** : Le MDU gagne en expressivité sans imposer de dépendance
  lourde à UAE.

## Conséquences

- **Ajout** : `atoms/attention-mechanism.yaml`
- **Mise à jour** : `meta-design.yaml` référence l'atome
- **Documentation** : ADR-017 traite cette décision

## Références

- ADR-015-unified-design-v2
- ADR-016-loop-engine
- ADR-013-meta-design-validation-protocol
- Citizen UAE : `gerivdb/UAE` (L3-CITIZENS/N3)

## Statut

proposed — en attente de validation par les architectes N+1.
