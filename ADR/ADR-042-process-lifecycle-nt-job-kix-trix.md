---
type: ADR
version: "1.0.0"
status: proposed
date: "2026-08-16"
intent_hash: 0xADR_042_PROCESS_LIFECYCLE_NT_JOB_KIX_TRIX_20260816
---

# ADR-042: Couplage NT Job Objects + REST KIX pour le cycle de vie des processus

## Context
Sur Windows, la gestion du cycle de vie des processus fils (creation, suivi, terminaison) repose actuellement sur des scripts ad-hoc sans isolation ni garantie de nettoyage. En cas de crash ou d'abandon, les processus orphelins consomment des ressources et peuvent bloquer des ports ou des handles.

NT Job Objects (ADR-106) offrent un mecanisme natif de groupe de processus avec limite de ressources et notification de terminaison. KIX (ADR-2026-07-27-016-kix-orchestrator) expose un controleur REST pour orchestrer des operations systemes. Les coupler permet de centraliser le cycle de vie via une API REST tout en utilisant les garanties du noyau Windows.

## Decision
Adopter le couplage suivant :
- Creation de NT Job Objects pour chaque operation TRIX/KIX necessitant un groupe de processus.
- Exposition de routes REST dans KIX pour creer, interroger et terminer ces Job Objects.
- Utilisation de ces routes comme interface unique pour le cycle de vie des processus lances par TRIX.

Ce choix preserve l'isolation entre les composants tout en exploitant les primitives natives Windows pour la fiabilite.

## Consequences
- Positif : Nettoyage automatique des processus fils via le Job Object.
- Positif : API REST unifiee pour le monitoring et le controle.
- Negatif : Couplage supplementaire entre TRIX et KIX.
- Negatif : Necessite des privileges administrateur pour creer des Job Objects (ADR-092).

## References
- ADR-106: NT Job Objects
- ADR-2026-07-27-016-kix-orchestrator: KIX Orchestrator
- ADR-092: Windows Admin Privilege