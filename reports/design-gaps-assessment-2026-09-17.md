# Rapport — Designs absents pour la planification, PRD/MOC, fluidité opérationnelle et assistance HITL

## Date
2026-09-17

## Contexte
Analyse des gaps dans `unified-design/designs/` pour 4 axes opérationnels :
1. Planification des tâches et chainage
2. PRD/MOC et gouvernance des livrables
3. Fluidité opérationnelle
4. Assistance HITL et décharge de dette technique

## Méthode
- Scan de `unified-design/designs/` par mots-clés par axe
- Vérification de l’existence physique des designs attendus
- Évaluation de la couverture par axe

## Résultats

### Axe 1 — Planification des tâches et chainage
| Design attendu | Présent | Commentaire |
|---|---|---|
| `chain-fluidity.yaml` | ❌ | Manquant : fluidité du chainage des tâches |
| `autonomy-fluidity.yaml` | ❌ | Manquant : fluidité d’autonomie des agents |
| `task-planning.yaml` | ❌ | Manquant : planification explicite des tâches |
| `task-chaining.yaml` | ❌ | Manquant : chainage des tâches |

**Couverture existante partielle** :
- `chain-engineering.yaml` : couvre l’ingénierie de chaine, mais pas la fluidité
- `atomic-fragmentation.yaml` : couvre la fragmentation atomique, mais pas la planification
- `delivery-engine.yaml` : couvre le delivery, mais pas le chainage de tâches

**Gap identifié** : Aucun design ne formalise la planification et le chainage des tâches de manière opérationnelle.

### Axe 2 — PRD/MOC et gouvernance des livrables
| Design attendu | Présent | Commentaire |
|---|---|---|
| `conversation-aggregator.yaml` | ❌ | Manquant : agrégation des conversations en livrables |
| `conversation-to-execution-bridge.yaml` | ❌ | Manquant : pont conversation → exécution |

**Couverture existante partielle** :
- `artifact-ownership-routing.yaml` : couvre le routage, mais pas la conversation
- `approval-readiness.yaml` : couvre la préparation, mais pas l’agrégation
- `moc-governance.yaml` : couvre la gouvernance MOC, mais pas le flux conversation

**Gap identifié** : Aucun design ne formalise le flux conversation → PRD/MOC → exécution.

### Axe 3 — Fluidité opérationnelle
| Design attendu | Présent | Commentaire |
|---|---|---|
| `operational-fluidity.yaml` | ❌ | Manquant : fluidité opérationnelle globale |

**Couverture existante partielle** :
- `circuit-breaker-pattern.yaml` : couvre les ruptures
- `graceful-degradation-fallback.yaml` : couvre la dégradation
- `recovery-tooling.yaml` : couvre la récupération
- `chain-engineering.yaml` : couvre les chains

**Gap identifié** : Aucun design ne formalise la fluidité opérationnelle comme principe global.

### Axe 4 — Assistance HITL et décharge de dette technique
| Design attendu | Présent | Commentaire |
|---|---|---|
| `hitl-assistance.yaml` | ❌ | Manquant : assistance HITL formalisée |
| `debt-relief.yaml` | ❌ | Manquant : décharge de dette technique |
| `ergonomics.yaml` | ❌ | Manquant : ergonomie des workflows |
| `elegance.yaml` | ❌ | Manquant : élégance des solutions |
| `assistant-load.yaml` | ❌ | Manquant : charge de l’assistant |

**Couverture existante partielle** :
- `approval-readiness.yaml` : couvre la préparation des approbations
- `artifact-ownership-routing.yaml` : couvre le routage
- `recovery-tooling.yaml` : couvre la récupération

**Gap identifié** : Aucun design ne formalise l’assistance HITL comme décharge de dette technique.

## Conclusion
12 designs manquants identifiés, répartis sur 4 axes opérationnels. Aucun n’est présent dans `unified-design/designs/`.

## Recommandations
1. Créer les 12 designs en mode `draft` avec ADR backing
2. Les lier au PRD-MOC TDC pour traçabilité
3. Les référencer dans `meta-design.yaml` et `META-DESIGN.md`
