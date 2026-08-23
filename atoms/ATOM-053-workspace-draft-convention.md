# ATOM-053: Workspace Draft Convention

> Referencé par atoms_registry.yaml depuis 2026-07 ; fichier cree le 2026-08-24 (correction DESIGN_GHOST, PRD-MOC-GEN-011).
> Zones de workspace normalisees pour fichiers en cours, orphelins et temporaires.

## Zones definies

| Zone | Chemin | Usage |
|------|--------|-------|
| Drafts | `drafts/` | Documents en cours de redaction |
| Limbo | `.LIMBO/` | Fichiers orphelins en transit (routage ARGUS) |
| Trash | `.TRASH/` | Fichiers a supprimer |
| Temp | `.temp/` | Fichiers temporaires |

## Regles

1. Tout fichier orphelin detecte par ARGUS -> `.LIMBO/<strate>/<repo>/`
2. Tout fichier temporaire (`debug_*`, `optimize_*`, `clean_*`, `fix_*`, `rewrite_*`) -> `.LIMBO/temp/`
3. Tout fichier suspect non identifie -> `.LIMBO/quarantine/`
4. Aucun commit de fichier orphelin hors `.LIMBO/`
5. Nettoyage hebdomadaire de `.LIMBO/temp/` et `.TRASH/`

## Enforcement

| Mecanisme | Cible |
|-----------|-------|
| Pre-commit hook | `check_no_orphans_outside_limbo` |
| Scanner ARGUS | `scanners/orphan_file_scanner.py` |
| Commande BALISE | `balise scan --dry-run` |
| Cron routage | `crons/balise_limbo_cron.py` (--apply apres validation HITL) |

## Relations

- **Consomme par** : limbo-transit (design), argus-orphan-scanner, gguf-probe-retention
- **Design parent** : unified-design/designs/limbo-transit.yaml
- **Escalade HOTL** : N validations identiques du meme pattern -> deplacement automatique (PF4/PF6)

## Adossement

- Verificateur : scanner dry-run zero finding sur repo sain
- Proprietaire : GOVERNANCE-HUB N+4
