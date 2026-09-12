# ToolAvailabilityVerification

**Type** : N (concept fondamental)  
**Domaine** : environment / tooling / governance  
**Strate** : L0  
**Statut** : accepted  
**IntentHash** : `0xTOOL_AVAILABILITY_VERIFICATION_20260912`

---

## Définition

Principe gouvernant toute affirmation sur la disponibilité d’un élément :
aucune conclusion ne peut être formulée sans preuve issue d’une exécution réelle.

## Forme canonique

- Preuve avant conclusion.
- Commande de vérification avant assertion.
- Citation de la sortie avant toute décision.

## Portée

S’applique à tout type d’éléments :
- Outils (`kiva`, `ecos`, `git`, `python`, etc.)
- Chemins et fichiers (`Test-Path`, `Get-ChildItem`, `Read`)
- Concepts ontologiques (`grep`, `search`, `query`)
- États et métriques (`curl`, `requests`, `benchmark`)
- Promesses et affirmations générales

## Contexte d’application

- Règles KiloCode liées aux outils, chemins, fichiers, concepts.
- Vérifications d’environnement avant implémentation.
- Audit d’état avant toute décision.
- Toute affirmation nécessite une preuve.

## Termes liés

- `ProofOfLife`
- `EnvironmentCapabilityProbe`
- `ToolPresenceAssertion`
- `VerificationBeforeExecution`
- `CausalGapAnalyst`

## Critères de validation

- [ ] Terme présent dans le registre des termes ONTOLOGY.
- [ ] Définition stabilisée, pas de variante synonyme non gouvernée.
- [ ] Référencé par au moins une règle KiloCode.
- [ ] Appliqué à tout l’écosystème, pas seulement DevTools.
