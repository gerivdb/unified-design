---
type: DESIGN
version: "1.0.0"
date: 2026-08-23
status: accepted
intent_hash: 0xDESIGN_BOOTSTRAP_SOUVERAIN_20260823
design_id: U-C3
layer: L0
source: INTENT-2026-08-23-INFRASTRUCTURE-BOOTSTRAP-ARBITER (I2, I4)
---

# BOOTSTRAP_SOUVERAIN.md — Le bootstrap est le point zéro de cohérence

## Principe

> **Si le bootstrap ne vérifie pas ce qu'il lance, il ne peut pas détecter son propre
> échec silencieux. Un daemon mort pendant des semaines est pire qu'un crash au boot.**

## Les règles

| # | Règle |
|---|-------|
| B1 | Tout service est déclaré dans une source unique (`services.yaml`) : binaire, rôle, port, endpoints, `blocking: true/false` |
| B2 | Le bootstrap exécute `check-services-coherence --pre-launch` AVANT tout lancement : binaire absent ou config invalide = échec bruyant |
| B3 | Après lancement : `--verify` teste les ports déclarés ; service `blocking: true` muet = échec ; service `blocking: false` = warning loggé |
| B4 | Le lancement est **idempotent** : un port déjà en écoute n'est pas relancé |
| B5 | Toute migration de chemin met à jour le bootstrap dans le même commit que le déplacement (contrat-adossement) |

## Séquence canonique

```
boot → coherence --pre-launch (échec bruyant si incohérent)
     → start services blocking:true (idempotent)
     → start daemons applicatifs
     → coherence --verify (ports + endpoints)
```

## Implémentation actuelle

- Déclaration : `L1-INFRA/config/services.yaml` (trix-engine 7243, git-arbiter 8742, argus-cron horaire)
- Vérificateur : `L1-INFRA/SCRIPTS/check-services-coherence.py`
- Lanceur idempotent : `L1-INFRA/SCRIPTS/start-infra-services.ps1`
- Point d'entrée boot : `Startup\KIVA-DaemonManager-Bootstrap.bat`
