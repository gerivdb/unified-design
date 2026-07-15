---
status: proposed
date: "2026-07-15"
intent_hash: 0xADR_0016_LOOP_ENGINE
---

# ADR-016 — Unified Design Loop Detection Engine

## Contexte

`unified-design` v2 promet une `loop_detection` capable d'analyser le graphe de dépendances entre designs et de détecter les cycles sémantiques. Jusqu'à présent, cette capacité n'existe qu'à l'état déclaratif dans `meta-design.yaml`. Aucun moteur interne ne l'implémente.

Par ailleurs, l'étude de `loopany-platform` montre que ce citizen L1-INFRA/N3 implémente des **loops d'exécution** (cron, run lifecycle, artifacts), mais pas de graphe de contraintes sémantiques ni de détection de cycles de design.

Il y a donc un chaînon manquant entre la promesse du méta-design et l'outil opérationnel.

## Décision

Créer un module `loop_engine/` dans `unified-design` avec :

1. `graph.py` : construction du graphe orienté à partir des `design.yaml`, `atoms/*.yaml`, `loops/*.yaml`.
2. `detector.py` : détection de cycles par DFS avec marquage, limitée par `max_cycle_length`.
3. `classifier.py` : classification heuristique des cycles en `virtuous_cycle`, `deadlock_pattern`, ou `unknown`.
4. `reporter.py` : export console/JSON/DOT.

Ce moteur sera référencé dans `meta-design.yaml` via `loop_detection.engine: loop_engine`.

Il sera également intégré dans `connard-validator` pour bloquer les PRs introduisant des deadlocks non documentés.

## Rationale

- **Cohérence** : le module vit dans le même repo que le méta-design qu'il valide ; pas de drift possible.
- **Extensibilité** : la classification peut évoluer de heuristique vers un petit classifieur ML sans casser l'API.
- **Performance** : < 2s sur l'écosystème complet grâce au cache et à l'analyse incrémentale.

## Alternatives considérées

| Alternative | Raison du rejet |
|-------------|-----------------|
| Externaliser le moteur dans `loopany-platform` | Couplage fort citizen ↔ méta-design ; drift de SOT |
| Utiliser un outil générique (NetworkX, etc.) | Dépendance lourde pour un besoin restreint |
| Laisser `connard-validator` faire la détection seul | Pas de source de vérité partagée ; duplication |

## Conséquences

- **Ajout de fichiers** : `loop_engine/*.py`.
- **Mise à jour** : `meta-design.yaml` référence `loop_engine`.
- **Intégration** : `connard-validator` devra appeler `loop-check`.
- **Documentation** : ADR-016 traite cette décision.

## Références

- ADR-015-unified-design-v2
- ADR-013-meta-design-validation-protocol
- loopany-platform (citizen L1-INFRA/N3) — source des atomes d'exécution

## Statut

proposed — en attente de validation par les architectes N+1.
