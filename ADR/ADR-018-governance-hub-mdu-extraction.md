---
status: proposed
date: "2026-07-15"
intent_hash: 0xADR_0018_GOVERNANCE_HUB_MDU_EXTRACTION
---

# ADR-018 — Extraction MDU de GOVERNANCE-HUB

## Contexte

`GOVERNANCE-HUB` est la source de vérité constitutionnelle du métacluster `gerivdb` (strate L0-CANON). Il expose des patterns de gouvernance réutilisables :

- Source de vérité constitutionnelle (`constitutional-sot`)
- Registre hiérarchique de dépôts (`stratified-repository-registry`)
- Gouvernance ternaire (`ternary-governance`)
- Séquence de boot canonique (`gated-boot-sequence`)
- Règles absolues et conformité (`absolute-rules-enforcement`)
- Traçabilité ADR/PRD/EPICS/INTENTS (`adr-prd-epics-intents`)

Jusqu'à présent, ces patterns n'existent que sous forme de règles informelles dans `GOVERNANCE-HUB`. Aucun atome MDU ne les capture. Résultat :

- `unified-design` ne peut pas référencer ces patterns comme atomes réutilisables.
- Le `loop_engine` ne peut pas inclure `GOVERNANCE-HUB` dans le graphe de dépendances (pas de `design.yaml`).
- D'autres designs (L1, L2, etc.) ne peuvent pas hériter de ces patterns de gouvernance.

## Décision

1. **Créer 6 atomes MDU** dans `unified-design/atoms/` capturant les patterns de `GOVERNANCE-HUB` :
   - `constitutional-sot.yaml`
   - `stratified-repository-registry.yaml`
   - `ternary-governance.yaml`
   - `gated-boot-sequence.yaml`
   - `absolute-rules-enforcement.yaml`
   - `adr-prd-epics-intents.yaml`

2. **Créer un `design.yaml`** dans `GOVERNANCE-HUB` déclarant l'héritage de ces atomes, permettant au `loop_engine` de l'inclure dans le graphe de dépendances.

3. **Mettre à jour `meta-design.yaml`** avec une section `governance_atoms` listant les nouveaux atomes et ajouter ADR-018 aux références.

## Rationale

- **Réutilisabilité** : tout nouveau dépôt peut hériter de `constitutional-sot` ou `gated-boot-sequence` sans réinventer la couche de boot.
- **Validation automatique** : le `connard-validator` pourra vérifier qu'un design respecte ses atomes déclarés.
- **Traçabilité** : les ADR de `unified-design` pourront référencer ces atomes, liant constitution et méta-design.
- **Extensibilité** : si de nouveaux patterns émergent dans `GOVERNANCE-HUB`, ils seront capturés comme atomes sans refonte.

## Alternatives considérées

| Alternative | Raison du rejet |
|-------------|-----------------|
| Laisser les patterns informels dans GOVERNANCE-HUB | Pas de réutilisabilité, pas de validation croisée |
| Créer un repo séparé `governance-atoms` | Redondance avec `unified-design/atoms/`, complexité cross-repo |
| Héritage direct depuis `unified-design/meta-design.yaml` | `meta-design.yaml` est un schéma, pas un design concret |

## Conséquences

- **Ajout de fichiers** : 6 atomes dans `unified-design/atoms/`, 1 `design.yaml` dans `GOVERNANCE-HUB`.
- **Mise à jour** : `meta-design.yaml` gagne une section `governance_atoms`.
- **Scan loop_engine** : `GOVERNANCE-HUB` sera détecté comme design repo lors des scans ciblés (`design_only=True`).
- **Documentation** : ADR-018 traite cette décision.

## Références

- ADR-015-unified-design-v2
- ADR-016-loop-engine
- GOVERNANCE-HUB (L0-CANON)
- `loop_engine/graph.py` — mode `design_only=True`

## Statut

proposed — en attente de validation par les architectes N+1.
