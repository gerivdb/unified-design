# ATOM-ECOSYSTEM-META-COHERENCE-GATE

## Description

Méta-cohérence écosystémique Think/Do/Check : garantit que le MDU reste aligné avec :
- **Think** : les besoins de l'écosystème
- **Do** : l'écosystème lui-même
- **Check** : la vérification de l'écosystème

Fusionne `meta-coherence` (détection d'écarts cross-repo) et `friction-analyzer` (corrections structurelles de session) en un pattern unifié de gouvernance adaptative.

## États obligatoires

| État | Nature | Gate |
|---|---|---|
| THINK | Besoins émergents, signaux faibles | NEEDS_VALIDATED → DO |
| DO | Mutations engagées, irréversibles | EXECUTION_VERIFIED → CHECK |
| CHECK | Constaté, mémorisé, audité | ENREGISTRER → THINK suivant |

## Fonctions obligatoires

1. **PERCEVOIR_BESOINS** — échantillonnage multi-source des besoins écosystémiques
2. **ÉVALUER_BESOINS** — évaluation des besoins vs capacité écosystémique
3. **MODÉLISER_IMPACT** — auto-modèle d'impact : que va changer cette correction ?
4. **RÉSERVER_COHÉRENCE** — marge de cohérence : plan de rollback si correction casse autre chose
5. **VALIDER_BESOINS** — gate : les besoins sont-ils suffisamment fondés pour engager une correction ?
6. **AGIR_CORRECTION** — engagement irréversible : application de la correction structurelle
7. **MONITORER_INVARIANTS** — surveillance des invariants écosystémiques pendant la correction
8. **VALIDER_RÉEL** — succès constaté dans le monde : la correction a-t-elle résolu la friction ?
9. **ENREGISTRER_TRACE** — mémoire : preuve horodatée, traçabilité causale, héritage

## Règles

1. Toute correction structurelle naît d'un besoin écosystémique identifié, pas d'un caprice.
2. Toute correction est tracée : friction → root cause → fix → preuve.
3. Le MDU s'adapte aux besoins de l'écosystème, pas l'inverse.
4. Une correction n'est jamais déclarée réussie sans preuve horodatée.
5. L'agent doit explicitement modéliser l'impact de la correction sur l'écosystème.
6. Toute correction doit avoir un plan de rollback (F4 RÉSERVER_COHÉRENCE).
7. La perception des besoins doit utiliser ≥ 2 sources indépendantes (F1).

## Anti-patterns

| Gène manquant | Pathologie |
|---|---|
| think-first | Correction appliquée sans besoin écosystémique validé → dette technique |
| causal-traceability | Correction sans traçabilité → impossibilité d'auditer, répétition des erreurs |
| adaptive-coherence | MDU figé, besoins écosystémiques ignorés → écosystème frustré |
| verification-real | Correction déclarée réussie sans preuve → échec silencieux |

## Invariant central

Le MDU n'est jamais considéré comme méta-cohérent tant qu'une friction de session non résolue subsiste.

## Références

- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **IntentHash** : `0xDESIGN_ECOSYSTEM_META_COHERENCE_20260920`
- **Dépôt** : gerivdb/unified-design
- **Parent** : `meta-coherence`, `chain-fluidity`, `safe-action-pattern`
