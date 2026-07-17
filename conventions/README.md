---
type: README
version: 1.0.0
status: active
intent_hash: 0xATOM_SOTA_CONVENTIONS
---

# Conventions SOTA du développement MDU

Ce répertoire contient les conventions de développement standardisées pour l'écosystème MDU.

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
| 020 | Conventional Commits | Format de commit |
| 021 | SemVer + Changelog | Versionnement |
| 022 | Code Quality | Formatage et lint |
| 023 | Minimal CI | Pipeline CI |
| 024 | Templates | Templates PR/Issue |
| 025 | Loop Engineering | Pile Prompt→Context→Harness→Loop |
| 026 | Maker-Checker | Séparation Analyst/Critic |
| 027 | Default-FAIL | Rejet par défaut |
| 028 | Evidence Required | Preuve tangible obligatoire |
| 029 | TRIX Architecture | Logique ternaire b1.58 |
| 030 | Bilevel Autoresearch | Méta-recherche sécurisée |
| 031 | Five Movements | Disco, Handoff, Verification, Persistence, Scheduling |
| 032 | Six Organes | Automations, Worktrees, Skills, Connectors, Sub-agents, Mémoire |
| 033 | TOPOS Merge Souverain | Merge uniquement sur ENV2 |
| 034 | Anti-Patterns | Nodding Loop, Comprehension Rot, Reddition Cognitive |

## Structure des dossiers

```
conventions/
├── commit/           # ATOM-020 : Conventional Commits
│   └── CONVENTIONAL_COMMITS.md
├── versioning/       # ATOM-021 : SemVer + Changelog
│   └── SEMVER_AND_CHANGELOG.md
├── lint/             # ATOM-022 : Formatage et linting
│   └── CODE_QUALITY.md
├── ci/               # ATOM-023 : Pipeline CI minimal
│   └── MINIMAL_CI.md
└── templates/        # ATOM-024 : Templates de contribution
    ├── CONTRIBUTING.md
    ├── PULL_REQUEST_TEMPLATE.md
    └── ISSUE_TEMPLATE.md

workflows/              # Templates CI/CD
docs/                 # Documentation principale
templates/            # Templates génériques
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