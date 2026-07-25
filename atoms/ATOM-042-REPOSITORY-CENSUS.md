---
type: ADR
status: proposed
date: "2026-07-18"
intent_hash: 0xATOM_042_REPOSITORY_CENSUS_20260718
---

# ATOM-042 : Repository Census & Discovery

## Contexte

Le Design-Seeker MVP et le Dashboard MDU ne possédaient pas de composant dédié à la Source de Vérité (SoT) de la liste des dépôts. Ils s'appuyaient sur des scans partiels ou des configurations statiques (9 repos dans `ecosystem.yaml`), alors que la base autoritaire (`known_repositories.yaml` du GOVERNANCE-HUB) en recense 225.

### Problème identifié
- **225 repos** dans `known_repositories.yaml` (source autoritaire)
- **9 repos** dans `ecosystem.yaml` (scan partiel)
- **Coverage: 4%** - lacune critique de connaissance de l'écosystème

### Impact
- Design-Seeker aveugle à 96% des dépôts
- Dashboard affichant des statistiques inexactes
- UAE scoring incomplet
- Risque de duplication ou d'ouverture de repos non synchronisés

## Décision

Implémenter un **Registre des Dépôts** unique et consommable par tous les modules MDU:

1. **Source de Vérité** : `GOVERNANCE-HUB/known_repositories.yaml`
2. **Lecture obligatoire** : Tous les outils MDU doivent lire ce fichier
3. **Coverage reporting** : Dashboard doit afficher le % de repos scannés
4. **TQL Endpoint** : Interrogation `SELECT repo FROM registry`

## Conséquences

### Positives
- Couverture réelle de l'écosystème (225 repos)
- Statistiques fiables dans le Dashboard
- Détection de patterns transversaux complète
- Prévention des ouvertures de dépôts dupliqués

### Négatives
- Temps de scan initial plus long
- Dépendance à GOVERNANCE-HUB pour la liste des repos
- Nécessité de maintenir la cohérence du fichier source

## Implémentation

### Composants modifiés
1. `TOPOS/ecosystem.yaml` - Ajout de la source autoritaire
2. `scripts/design_seeker_mvp.py` - Lecture de known_repositories.yaml
3. `scripts/mdu_dashboard.py` - Affichage de la couverture

### Nouveaux fichiers
1. `scripts/update_repo_registry.py` - Synchronisation automatique
2. `TQL/tql.yaml` - Endpoint de requête registry

## Références

- ADR-041 : FLUENCE Deployment Hook anti-friction pattern
- GOVERNANCE-HUB/known_repositories.yaml
- TOPOS/topology.yaml
- ECOS-CLI/manifest.json