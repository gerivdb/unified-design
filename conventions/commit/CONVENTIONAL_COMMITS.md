---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_020_CONVENTIONAL_COMMITS
---

# ATOM-020 : Conventional Commits

**Inspiré de :** https://www.conventionalcommits.org/en/v1.0.0/

## Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

## Types autorisés

| Type | Description |
|------|-------------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Documentation |
| `style` | Formatage, point-virgule, etc. |
| `refactor` | Refactoring sans changement fonctionnel |
| `perf` | Amélioration de performance |
| `test` | Ajout/modification de tests |
| `chore` | Maintenance, CI, etc. |
| `revert` | Annulation d'un commit précédent |

## Scopes recommandés (contexte CLI/Trix)

- `simd` : optimisations SIMD/AVX
- `parser` : parsing et analyse
- `dispatcher` : table de dispatch
- `handler` : gestionnaires d'API
- `cli` : interface ligne de commande
- `config` : configuration

## Exemples

```
feat(simd): add AVX2 kernel support for Westmere
fix(parser): handle empty input gracefully
docs(readme): update installation instructions
perf(dispatcher): optimize dispatch table lookup
refactor(cli): extract command handlers to separate modules
test(handler): add unit tests for kiva-run endpoint
chore(deps): update Zig to 0.15.0
```

## Configuration commitlint

```yaml
# .commitlintrc.yml
extends: ['@commitlint/config-conventional']
rules:
  body-max-line-length: [2, 'always', 100]
  scope-case: [2, 'always', 'lower-case']
  subject-case: [2, 'never', ['start-case', 'pascal-case', 'upper-case']]
```

## Outil recommandé

```bash
# Installation
npm install -g commitizen cz-conventional-changelog

# Utilisation
git commit -m "$(cz)"
```