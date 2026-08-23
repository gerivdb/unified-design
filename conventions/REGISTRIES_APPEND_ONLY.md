---
type: CONVENTION
version: "1.0.0"
date: 2026-08-23
status: accepted
intent_hash: 0xCONV_REGISTRIES_APPEND_ONLY_20260823
design_id: U-C4
layer: L0
---

# REGISTRIES_APPEND_ONLY.md — Les deux familles légitimes de registres

## Principe

> **Un état parallèle est un état qui va dévier.** Tout registre appartient à l'une des
> deux familles ci-dessous — tout autre état persistant est un anti-pattern.

## Famille 1 — Dérivés régénérables (index)

| Propriété | Règle |
|-----------|-------|
| Source de vérité | Ailleurs (les fichiers indexés) |
| Écriture | Régénération complète par script idempotent |
| Idempotence | Deux exécutions = résultat identique (critère de test obligatoire) |
| Exemples | `PRD-000-index.md`, `ADR-000-index.md` (update-artifact-index.ps1) |

## Famille 2 — Accumulatifs append-only (registres de faits)

| Propriété | Règle |
|-----------|-------|
| Source de vérité | Le registre lui-même (faits historiques) |
| Écriture | **Ajout uniquement**, dédoublonné par identifiant stable |
| Interdiction | Écraser, retrancher, réécrire l'historique |
| Résolution | Un gap se clôt par changement de `status`, pas par suppression |
| Exemples | ARGUS `gaps/registry.yaml` |

## Anti-patterns rejetés

| Anti-pattern | Pourquoi |
|--------------|----------|
| `state.json` miroir du filesystem | Drift garanti ; la source de vérité = fichiers + git |
| Registre d'inventaire pré-migration persistant | Rapport ponctuel dans l'exécution, jamais un état |
| Index maintenu à la main | Dérive manuelle ; toujours régénérable |

## Test de classification

*« Si je supprime ce registre, puis-je le reconstruire intégralement depuis une autre source ? »*
- OUI → famille 1 (dérivé) : script obligatoire
- NON → famille 2 (accumulatif) : append-only obligatoire
- « Partiellement » → mauvais design, refondre.
