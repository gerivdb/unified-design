---
type: ADR
version: "1.0.0"
status: proposed
date: "2026-08-16"
intent_hash: 0xADR_041_MOC2_OCP_AUTO_DISCOVERY_20260816
---

# ADR-041 - MOC-2 OCP / Auto-Découverte des Atomes par Manifests

## Problem Statement

Le MDU v2.1.0 n'est pas "Open to extension, Closed to modification" (OCP). L'ajout d'un atome, d'un design ou d'un pilier nécessite une édition manuelle de fichiers centraux (`meta-design.yaml`, `META-DESIGN.md`), causant :
- Merge conflicts récurrents sur `meta-design.yaml`.
- Oublis de synchronisation entre `meta-design.yaml` et `META-DESIGN.md`.
- Frictions de contribution pour les nouveaux atomes.

Constat :
- `designs:` est un tableau codé en dur (1 seul design enregistré).
- `piliers:` est un tableau YAML statique.
- L'ajout d'un atome nécessite une édition manuelle dans `meta-design.yaml` ET `META-DESIGN.md`.

Conséquence : le MDU est un goulot d'édition centrale. Toute extension touche à des fichiers canoniques, augmentant le risque d'erreur humaine.

## Decision

### Passer à un mécanisme d'auto-découverte par manifests locaux

**Principe :** Chaque atome, design ou pilier dispose d'un manifest local (`.atom.yaml`, `design.yaml`, `pillar.yaml`). `meta-design.yaml` et `META-DESIGN.md` sont **générés** à partir d'un scan de ces manifests. L'édition manuelle de `meta-design.yaml` est interdite.

### Structure cible

```
L0-CANON/
  atoms/
    constitutional-sot/
      .atom.yaml              # Manifest de l'atome
    stratified-repository-registry/
      .atom.yaml
  designs/
    moc-governance/
      design.yaml             # Manifest du design
  piliers/
    sonar-driven-design/
      pillar.yaml             # Manifest du pilier
  tools/
    meta-design-gen.py         # Générateur (hors scope MDU canonique)
  meta-design.yaml             # AUTO-GENERATED - généré par meta-design-gen.py
  META-DESIGN.md               # AUTO-GENERATED - généré par meta-design-gen.py
```

### Manifest `.atom.yaml` (exemple)

```yaml
atom_id: constitutional-sot
version: "1.0.0"
type: registry
description: "Source de verite constitutionnelle"
profile: CRITICAL
consumers:
  - repo: GOVERNANCE-HUB
    artifact: known_repositories.yaml
  - repo: unified-design
    artifact: meta-design.yaml
last_verified: "2026-08-16"
```

### Header obligatoire dans `meta-design.yaml`

```yaml
# AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY
# Source: atoms/.atom.yaml + designs/*/design.yaml + piliers/*/pillar.yaml
# Generator: tools/meta-design-gen.py
# Regenerate: python tools/meta-design-gen.py
```

### Règles

| Règle | Description |
|-------|-------------|
| **R-OCP-001** | `meta-design.yaml` et `META-DESIGN.md` sont générés, jamais édités manuellement. |
| **R-OCP-002** | Chaque atome/design/pilier possède un manifest local à la racine de son dossier. |
| **R-OCP-003** | L'ajout d'un atome consiste à créer un dossier + manifest, pas à éditer un fichier central. |
| **R-OCP-004** | Un check CI `verify-meta-design-sync` échoue si `meta-design.yaml` commité diffère du résultat de `python tools/meta-design-gen.py`. |
| **R-OCP-005** | Le header `# AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY` est obligatoire en en-tête de `meta-design.yaml`. |

### Breaking change

Ce ADR introduit un **breaking change** sur le schéma `meta-design.yaml` :
- Les tableaux `designs:`, `piliers:`, `agents_par_pilier:` sont supprimés du fichier.
- Ils sont remplacés par des sections générées à partir des manifests.
- Tout outil ou script lisant `meta-design.yaml` doit être migré vers le nouveau format généré.

## Alternatives Considered

1. Garder les tableaux codés en dur + validation stricte -- rejeté : ne résout pas les merge conflicts.
2. Génération uniquement de `META-DESIGN.md`, garder `meta-design.yaml` manuel -- rejeté : divergence persistante.
3. Registre centralisé `atoms_registry.yaml` -- rejeté : même problème de fichier unique.
4. Auto-découverte par manifests + génération automatique (choisi) -- conforme OCP, élimine les edits manuels.

## Consequences

- **Positif** : Ajout d'un atome = création d'un dossier + manifest, pas d'édition de fichier central.
- **Positif** : `meta-design.yaml` et `META-DESIGN.md` ne divergent jamais (générés depuis la même source).
- **Positif** : Merge conflicts sur `meta-design.yaml` éliminés (fichier généré, non édité).
- **Négatif** : Breaking change du schéma `meta-design.yaml` -- migration requise.
- **Négatif** : Courbe d'apprentissage pour les contributeurs (concept de manifest + génération).
- **Négatif** : Dépendance à `tools/meta-design-gen.py` pour toute modification du MDU.

## Validation

- **Preuve** : `meta-design.yaml` v2.1.0 contient 6 tableaux codés en dur (`designs`, `piliers`, `agents_par_pilier`, `governance_atoms`, `capabilities`, `design_rules`).
- **Conformité** : Respecte ADR-2026-06-28-001 (architecture logique N+1/N+2/N+3/N+4).
- **RSS-v2.3** : Conforme.

## Reference ADR

- **ADR** : ADR-041-moc2-ocp-auto-discovery
- **IntentHash** : 0xADR_041_MOC2_OCP_AUTO_DISCOVERY_20260816
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded


