---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_021_SEMVER_CHANGELOG
---

# ATOM-021 : Versionnement Sémantique et Changelog

## SemVer (Semantic Versioning)

Format : `MAJOR.MINOR.PATCH`

| Niveau | Description | Exemple |
|--------|-------------|---------|
| MAJOR | Breaking change, incompatible | `2.0.0` |
| MINOR | Nouvelle fonctionnalité, rétrocompatible | `1.1.0` |
| PATCH | Correction de bug, rétrocompatible | `1.0.1` |

## Règles de versionnement

1. **MAJOR** : API brisée, changement de comportement incompatible
2. **MINOR** : Nouvelle fonctionnalité, nouvelle option, amélioration
3. **PATCH** : Bug fix, correction de sécurité, optimisation

## Changelog automatique

Le changelog est généré automatiquement à partir des commits Conventional Commits.

### Outils recommandés

- **Python** : `standard-version` ou `semantic-release`
- **Node.js** : `standard-version`
- **Zig** : génération manuelle ou script dédié

### Workflow solo

```bash
# Générer un nouveau changelog
npx standard-version

# Vérifier les changements
cat CHANGELOG.md

# Commiter les changements
git add CHANGELOG.md
git commit -m "docs: update changelog for v1.2.0"

# Tagger la version
git tag v1.2.0
git push origin v1.2.0
```

### Workflow CI automatisé

```yaml
# GitHub Actions - .github/workflows/release.yml
name: Release
on:
  push:
    branches: [main]
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install -g semantic-release @semantic-release/git @semantic-release/github
      - run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Format du changelog

```markdown
# Changelog

## [1.2.0] - 2026-07-18

### Added
- feat(simd): add AVX2 kernel support for Westmere

### Fixed
- fix(parser): handle empty input gracefully

### Changed
- refactor(cli): extract command handlers to separate modules

## [1.1.0] - 2026-07-17

...
```