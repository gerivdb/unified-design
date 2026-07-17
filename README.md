---
type: README
version: 1.1.0
status: active
intent_hash: 0xATOM_SOTA_CONVENTIONS
---

# Unified Design – Conventions SOTA du développement MDU

Ce dépôt contient les conventions de développement standardisées pour l'écosystème MDU.

## ATOM codifiés

| ATOM | Nom | Description |
|------|-----|-------------|
| 001 | FFI Convention | Convention d'interface C |
| 002 | Definition Order | Ordre des définitions |
| 003 | Namespace Convention | Convention de nommage |
| 004 | Cache Convention | Gestion du cache |
| 005 | Interface Contract | Contrat d'interface |
| 006 | Error Diagnostic Tree | Arborescence d'erreurs |
| 007-013 | Conventions par domaine | Langages, DevOps, Sécurité |
| 014 | Self-modification | Méta-atome |
| 015 | Semantic Drift | Détecteur de dérive |
| 016 | ADR Quorum | Vote sur ADR |
| 017 | Working Mode | Contexte solo/team |
| 018 | Auto-ancrage | Ancrage implicite |
| 019 | Git Branch | Convention de branche |
| 020 | Conventional Commits | Format de commit structuré |
| 021 | SemVer + Changelog | Versionnement sémantique |
| 022 | Code Quality | Formatage et linting |
| 023 | Minimal CI | Pipeline CI automatisé |
| 024 | Templates | Templates PR/Issue |
| 025 | Loop Engineering | Pile à 4 couches (Prompt/Context/Harness/Loop) |
| 026 | Maker-Checker | Double validation |
| 027 | Default-FAIL | Sécurité par défaut |
| 028 | Evidence Required | Évidence tangible requise |
| 029 | TRIX Architecture | Architecture TRIX |
| 030 | Bilevel Autoresearch | Recherche automatique bicouche |
| 031 | Five Movements | Cinq mouvements de débat |
| 032 | Six Organes | Six organes de gouvernance |
| 033 | TOPOS Merge | Fusion souveraine TOPOS |
| 034 | Anti-Patterns | Anti-patterns interdits |
| 035 | Ontology Anchoring | Ancrage ontologique requis |
| 036 | VERSES Mapping | Modèles d'interaction double canal |
| 037 | TINA Specification | Langage machine interne |
| 038 | TQL Interface Contract | Interface de requête ontologique |

## Structure des dossiers

```
unified-design/
├── README.md                    # Ce fichier
├── ONTOLOGY_MAP.md              # Cartographie ONTOLOGY ↔ ATOMs
├── docs/                        # Documentation principale
│   └── GIT_BRANCH_CONVENTION.md
├── conventions/                 # Conventions SOTA
│   ├── README.md
│   ├── commit/
│   │   ├── CONVENTIONAL_COMMITS.md
│   │   └── .commitlintrc.yml
│   ├── versioning/
│   │   └── SEMVER_AND_CHANGELOG.md
│   ├── lint/
│   │   └── CODE_QUALITY.md
│   ├── ci/
│   │   └── MINIMAL_CI.md
│   ├── loop/
│   │   └── LOOP_ENGINEERING.md
│   ├── maker-checker/
│   │   └── MAKER_CHECKER.md
│   ├── default-fail/
│   │   └── DEFAULT_FAIL.md
│   ├── evidence/
│   │   └── EVIDENCE_REQUIRED.md
│   ├── trix/
│   │   └── TRIX_ARCHITECTURE.md
│   ├── autoresearch/
│   │   └── BILEVEL_AUTORESEARCH.md
│   ├── movements/
│   │   └── FIVE_MOVEMENTS.md
│   ├── organs/
│   │   └── SIX_ORGANS.md
│   ├── topos/
│   │   └── TOPOS_MERGE.md
│   ├── anti-patterns/
│   │   └── ANTI_PATTERNS.md
│   ├── ontology/
│   │   └── ATOM-035-ONTOLOGY_ANCHORING.md
│   ├── verses/
│   │   └── ATOM-036-VERSES_MAPPING.md
│   ├── tina/
│   │   └── ATOM-037-TINA_SPECIFICATION.md
│   └── tql/
│       └── ATOM-038-TQL_INTERFACE_CONTRACT.md
├── workflows/                   # Templates CI/CD
│   └── ci-template.yml
└── templates/                   # Templates génériques
    ├── CONTRIBUTING.md
    ├── PULL_REQUEST_TEMPLATE.md
    └── ISSUE_TEMPLATE.md
```

## Adoption dans un nouveau repo

1. Copier les conventions depuis ce répertoire
2. Ajouter les fichiers de configuration (ruff, eslint, etc.)
3. Installer les hooks pre-commit
4. Configurer le CI GitHub Actions
5. Ajouter les templates dans `.github/`

## Références

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Pre-commit](https://pre-commit.com/)