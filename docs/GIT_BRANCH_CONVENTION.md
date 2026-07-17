---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_019_GIT_BRANCH_CONVENTION
---

# Convention de branche Git — MDU (ATOM-019)

## Résumé

- **Aucun commit direct sur `main`**
- Branches obligatoires préfixées : `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`, `test/`, `release/`
- Script de vérification local : `scripts/check-branch-name.sh`

## Format des branches

```
<type>(<scope>): <description>
```

### Types autorisés

| Type | Description |
|------|-------------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `chore` | Maintenance, CI, dépendances |
| `docs` | Documentation |
| `refactor` | Refactoring sans changement fonctionnel |
| `test` | Ajout/modification de tests |
| `release` | Préparation de release |

## Exemples

- `feat(simd): add AVX2 kernel`
- `fix(parser): handle empty input`
- `docs(readme): update installation instructions`

## Conventions SOTA associées

Cette convention fait partie des ATOM SOTA suivants :

| ATOM | Nom | Lien |
|------|-----|------|
| 019 | Git Branch | [ `../conventions/commit/CONVENTIONAL_COMMITS.md`](../conventions/commit/CONVENTIONAL_COMMITS.md) |
| 020 | Conventional Commits | [ `../conventions/commit/CONVENTIONAL_COMMITS.md`](../conventions/commit/CONVENTIONAL_COMMITS.md) |
| 021 | SemVer + Changelog | [ `../conventions/versioning/SEMVER_AND_CHANGELOG.md`](../conventions/versioning/SEMVER_AND_CHANGELOG.md) |
| 022 | Code Quality | [ `../conventions/lint/CODE_QUALITY.md`](../conventions/lint/CODE_QUALITY.md) |
| 023 | Minimal CI | [ `../conventions/ci/MINIMAL_CI.md`](../conventions/ci/MINIMAL_CI.md) |
| 024 | Templates | [ `../conventions/templates/CONTRIBUTING.md`](../conventions/templates/CONTRIBUTING.md) |

## Documentation complète

Voir le [README des conventions SOTA](../conventions/README.md) pour une vue d'ensemble.