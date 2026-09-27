# ATOM-TALEX-FRICTION-ANALYZER

## Description

Atome de gouvernance pour l'analyse des frictions TALEX. Encode les règles de détection, classification, analyse causale et résolution des frictions de session.

## États obligatoires

| État | Nature | Gate |
|---|---|---|
| IDLE | En attente de détection | DETECT |
| DETECT | Collecte des frictions | CLASSIFY |
| CLASSIFY | Classification par type/impact | ANALYZE |
| ANALYZE | Analyse des causes racines | PROPOSE |
| PROPOSE | Proposition de corrections | APPLY |
| APPLY | Application des corrections (HITL) | VERIFY |
| VERIFY | Vérification post-correction | IDLE |

## Fonctions obligatoires

1. **DÉTECTER_FRICTIONS** — collecte des frictions de session
2. **CLASSIFIER_ERREURS** — classification par type/impact
3. **ANALYSER_CAUSES** — identification des causes racines
4. **PROPOSER_CORRECTIONS** — génération d'actions correctives atomiques
5. **APPLIQUER_CORRECTIONS** — application des corrections validées
6. **VÉRIFIER_CORRECTIONS** — vérification post-correction

## Règles

1. Toute friction de session est détectée et tracée.
2. Toute friction est classifiée par type et impact.
3. Toute friction est analysée causalement (cause racine identifiée).
4. Toute friction génère une action corrective atomique.
5. Toute correction est vérifiée avant clôture.

## Anti-patterns

| Gène manquant | Pathologie |
|---|---|
| systematic-detection | Frictions silencieuses → accumulation de dettes |
| causal-tracing | Corrections superficielles → récidives |
| auto-correction | Corrections manuelles répétitives → perte de temps |
| traceability | Impossibilité d'auditer les corrections |

## Invariant central

Toute friction de session est détectée, classifiée, analysée causalement, et résolue par des actions correctives atomiques vérifiées.

## Références

- **Design** : `designs/talex-friction-analyzer/design.yaml`
- **Primitive** : `primitives/talex-friction-analyzer-primitive.yaml`
- **IntentHash** : `0xDESIGN_TALEX_FRICTION_ANALYZER_20260922`
- **Dépôt** : gerivdb/unified-design
