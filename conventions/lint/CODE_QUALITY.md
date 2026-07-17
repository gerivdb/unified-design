---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_022_CODE_QUALITY
---

# ATOM-022 : Qualité de code (formatage, linting)

## Règle fondamentale

**Tout commit doit passer le formatage et le lint avant d'être créé.**

## Python

### Formatteur
```bash
ruff format .
```

### Linter
```bash
ruff check --fix .
```

### Configuration (pyproject.toml)
```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.ruff.format]
quote-style = "double"
```

## JavaScript/TypeScript

### Formatteur
```bash
prettier --write .
```

### Linter
```bash
eslint --fix .
```

### Configuration (package.json ou .eslintrc.cjs)
```json
{
  "prettier": {
    "semi": true,
    "trailingComma": "es5"
  },
  "eslint": {
    "env": { "es2021": true },
    "extends": ["eslint:recommended"]
  }
}
```

## Zig

### Formatteur
```bash
zig fmt .
```

### Vérification
```bash
zig fmt --check .
```

## Rust

### Formatteur
```bash
cargo fmt
```

### Linter
```bash
cargo clippy --fix
```

## Hook pre-commit

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.11.1
    hooks:
      - id: eslint
      - id: prettier
```

## Commandes rapides

```bash
# Formatage et lint Python
ruff format . && ruff check --fix .

# Formatage et lint JS/TS
prettier --write . && eslint --fix .

# Formatage Zig
zig fmt . && zig fmt --check .
```