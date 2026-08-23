---
type: DESIGN
version: "1.0.0"
date: 2026-08-23
status: accepted
intent_hash: 0xDESIGN_COHERENCE_TRANSVERSE_20260823
design_id: U-C1
layer: L0
source: 5 occurrences documentees (MOX, ADR-028, TRIX-Arbiter, ARGUS EPIC-002/004, bootstrap)
---

# COHERENCE_TRANSVERSE.md — Le pattern contrat-adossement

## Principe fondateur

> **Tout contrat déclare son adossement. Un contrat sans implémentation datée, sans
> vérificateur et sans propriétaire n'est pas un contrat : c'est une intention.**

Le pattern « contrat écrit, adossement absent » a produit cinq défaillances documentées
en une seule session (2026-08-23). Ce design interdit la sixième.

## Les règles

| # | Règle |
|---|-------|
| CT1 | Tout contrat (hook, endpoint, route, EPIC stub, principe MDU) déclare dans le même document : l'implémentation attendue, son vérificateur mécanique, son propriétaire |
| CT2 | Toute migration de repo met à jour ses références de démarrage/hooks **dans le même commit** que le déplacement |
| CT3 | Un EPIC/TODO de plus de 30 jours sans adossement est remonté au registre de gaps (ARGUS) comme `missing_implementation` |
| CT4 | La vérification croise : contrats déclarés × code existant × hooks actifs. Incohérence = échec bruyant |

## Détection (implémentation)

- `check-services-coherence.py --pre-launch` : services.yaml ↔ binaires
- `check-prdmoc-coherence` MC6 : références fantômes entre artefacts
- Extension prévue : scan des IntentHash de hooks ↔ code source correspondant

## Historique des occurrences (preuves)

| Date | Contrat | Adossement manquant | Coût |
|------|---------|---------------------|------|
| ~2026-06 | Rôle MOX engine | Jamais déclaré | Productions stockées dans l'usine |
| 2026-07-16 | ADR-028 principles→gate | Adoption + mécanisation | Principes inertes 5 mois |
| ~2026-07 | `/git/locks/status` (KIX, GT-017) | Route jamais codée dans trixd | Hooks bloqués semaines |
| 2026-06 | EPIC-ARGUS-002/004 scanners | Stubs TODO | Métacohérence absente |
| ~2026-07 | Bootstrap → ECOS-CLI migré | .bat non mis à jour | Daemons morts silencieusement |

**La sixième occurrence n'aura pas lieu : ce design est lui-même adossé**
(vérificateurs cités ci-dessus, propriétaires nommés dans les INTENTs porteurs).
