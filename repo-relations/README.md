# Repo Relations — Cartographie inter-dépôts de l'écosystème gerivdb

## Vue d'ensemble

Ce répertoire contient la **cartographie formelle des relations inter-dépôts** de l'écosystème `gerivdb`, instanciée à partir des atomes MDU définis dans `unified-design/atoms/`.

## Structure

```
repo-relations/
├── registry.yaml              # Vue d'ensemble : tous les flows par repo
├── layers/                    # Relations par strate L*
│   ├── L0-CANON.yaml
│   ├── L0-CONSTITUTIONAL.yaml
│   ├── L1-INFRA.yaml
│   ├── L2-PLATFORM.yaml
│   ├── L3-CITIZENS.yaml
│   ├── L4-TOOLS.yaml
│   ├── L5-ARCHIVE.yaml
│   └── L6-WORK.yaml
├── flows/                     # Un fichier par flux significatif
│   ├── govhub-unified-design.yaml
│   ├── govhub-nexus.yaml
│   ├── govhub-topos.yaml
│   ├── govhub-ecos-cli.yaml
│   ├── govhub-kiva-cli.yaml
│   ├── nexus-argus.yaml
│   ├── ontology-verses.yaml
│   ├── ontology-kgl.yaml
│   ├── unified-design-repo-standards.yaml
│   ├── brain-fluence.yaml
│   ├── brain-wazaa.yaml
│   ├── kiva-kiva-cli.yaml
│   ├── kiva-trix.yaml
│   └── batmcp-skills.yaml
└── README.md
```

## Concepts

### cross_repo_flow

Un `cross_repo_flow` est un flux orienté `provider -> consumers` avec :
- **Provider** : repo source du flux
- **Consumers** : repos consommateurs
- **Contrat** : interface, format, chemins, version
- **Validation** : checks à exécuter (`provider_registered`, `no_cycle`, etc.)
- **WAL logging** : traçabilité obligatoire

### structural_relations

Les relations horizontales entre repos, modélisées avec 8 kinds :
- `requires` / `blocks` / `inherits` / `supersedes` / `evolves_to` (asymétriques, strictes)
- `opposes` / `complements` / `stabilizes` (symétriques ou tolérées)

### Repos structurants

12 repos identifiés comme structurants (SOT, `memory_role`, rôle canonique) :
`GOVERNANCE-HUB`, `NEXUS`, `ONTOLOGY`, `unified-design`, `HERMES`, `VOLTX`, `BRAIN`, `TOPOS`, `N243`, `WAZAA`, `VERSES`, `INFX`, `ARGUS`.

## Validation

```bash
# Valider tous les flows
gerivdb design validate repo-relations/

# Valider en mode strict
gerivdb design validate repo-relations/ --strict
```

## Références

- `unified-design/atoms/cross-repo-flow.yaml` — pattern de base
- `unified-design/atoms/structural-relations.yaml` — kinds de relations
- `INTENT-REPO-RELATIONS-CARTOGRAPHY.md` — intent détaillé
