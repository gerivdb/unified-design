# ATOM-052: Artifact Lifecycle Zones

> Organisation CRM des artefacts de gouvernance par statut.
> Referencé par atoms_registry.yaml ; fichier materialise le 2026-08-24 (resolution IMP-004, PRD-MOC-GEN-011 P4).
> Compagnon documentaire de ATOM-052-exit-interceptor (meme numero, capacite complementaire) ; prerequis declare de ATOM-053-workspace-draft-convention.

## Principe CRM applique aux artefacts

Chaque artefact de gouvernance est suivi comme une relation client : il possede
un statut de cycle de vie, et ce statut determine sa zone physique dans le
workspace. Le deplacement de zone EST le changement de statut - pas de statut
sans emplacement, pas d'emplacement sans statut.

## Mapping statut -> zone

| Statut cycle | Zone workspace | Signification | Sortie possible |
|--------------|----------------|---------------|-----------------|
| GENESIS      | `drafts/`      | En redaction, non engage          | ACTIVE ou abandon -> `.TRASH/` |
| ACTIVE       | racines canoniques (`PRD/`, `PRD-MOC/`, `ADR/`, `EPICS/`, `designs/`, `atoms/`) | Engage, indexe, consomme | DEPRECATED |
| DEPRECATED   | marqueur frontmatter `status: deprecated` + zone d'origine conservee 30j | Remplace ou obsolete, en attente d'archivage | ARCHIVED |
| ARCHIVED     | `.TRASH/` ou repo L5-ARCHIVE | Froid, historique preserve       | terminal |

Zones transverses (hors cycle mais alimentees par lui) :

| Zone | Alimentation | Regle |
|------|--------------|-------|
| `.LIMBO/<strate>/<repo>/` | ARGUS orphan scanner | transit avant re-affectation (limbo-transit) |
| `.LIMBO/temp/`            | patterns debug_*/optimize_*/... | purge hebdomadaire |
| `.LIMBO/quarantine/`      | fichiers non identifies | audit HITL obligatoire |

## Regles de transition

1. Toute creation d'artefact nait en `drafts/` sauf pattern explicite de generation (templates).
2. Passage GENESIS -> ACTIVE exige : frontmatter complet (type/version/status/intent_hash), index mis a jour, adossement declare (PF2).
3. Un artefact ACTIVE dont l'implementation disparait devient DESIGN_DRIFT -> scan coverage ; s'il reste orphelin 30 jours -> CT3 registre de gaps ARGUS.
4. Interdiction de commiter un artefact situe hors de sa zone de statut (hors drafts pendant redaction).
5. La sortie de session (exit-interceptor) verifie qu'aucun artefact ne reste dans un etat incoherent (drafts non sauvegardes, zones melangees).

## Relations

- **Prerequis de** : ATOM-053-workspace-draft-convention (zones workspace detaillees)
- **Compagnon** : ATOM-052-exit-interceptor (validation en fin de session)
- **Designs consommateurs** : limbo-transit, thought-commit-pipeline (statuts draft/proposed/accepted/executing/done/archived)

## Adossement

- Verificateur : design_coverage_scanner (zero GHOST) + hooks pre-commit encodage/structure
- Proprietaire : GOVERNANCE-HUB N+4
