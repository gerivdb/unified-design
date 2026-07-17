---
type: README
version: 1.0.0
status: active
intent_hash: 0xATOM_025_LAYER_STRUCTURE
---

# Structure en couches du métacluster MDU

## Couches officielles

| Dossier | Nom complet | Rôle |
|---------|-------------|-------------------------------------------------|
| `L0-CANON` | Canon | Vérité unique, spécifications, conventions |
| `L1-INFRA` | Infrastructure | Gouvernance, hooks, CI, outils de base |
| `L2-PLATFORM` | Plateforme | Services, API, modèles déployés |
| `L3-CITIZENS` | Citoyens | Applications et agents autonomes |
| `L4-TOOLS` | Outils | Scripts, expériences, prototypes |
| `L5-ARCHIVE` | Archive | Projets gelés, historique, documentation |

## Règles de nommage

- **Préfixe `L<numéro>`** obligatoire.
- **Séparateur** : tiret `-` (pas d'underscore).
- **Pas d'espace**.
- **Nom en majuscules**.

## Format de nommage valide

```
L0-CANON
L1-INFRA
L2-PLATFORM
L3-CITIZENS
L4-TOOLS
L5-ARCHIVE
```

## Anomalies corrigées le 17/07/2026

| Dossier | Statut | Action effectuée |
|---------|--------|------------------|
| `L0-CANAN` | ✅ CORRIGÉ | Supprimé - doublon de L0-CANON/ONTOLOGY |
| `L3_EMERGENCE` | ✅ CORRIGÉ | Supprimé - dossier ARGUS vide |
| `L1b` | ⚠️ À OBSERVER | Conservé - utilisé par certains workflows |

**Note sur L1b** : Ce dossier contient `GOVERNANCE-HUB` et est utilisé par certains workflows internes. Il ne respecte pas la nomenclature `L<numéro>-XXX` mais est maintenu temporairement. À surveiller pour éventuelle migration vers L1-GOVERNANCE.

## Utilisation par l'IA

Pour trouver un fichier, l'IA doit :
1. Lire ce fichier `LAYER_STRUCTURE.md` pour comprendre la hiérarchie
2. Identifier la couche correcte (L0-L5)
3. Chercher dans le sous-dossier approprié

### Exemple de recherche

```
✅ Bon : L2-PLATFORM/ECO-CLI/src/...
❌ Mauvais : chercher dans D:\DO\WEB\TOOLS sans filtre

```

## Mise à jour

Ce fichier doit être mis à jour lorsqu'une nouvelle couche est ajoutée ou lorsque la nomenclature évolue.

**Statut** : actif
**Dernière mise à jour** : 2026-07-17