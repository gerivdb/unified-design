---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_023_MINIMAL_CI
---

# ATOM-023 : Pipeline CI minimal

## Objectif

Un pipeline CI minimal qui vérifie la qualité, les tests et la build de manière fiable.

## Jobs obligatoires

| Job | Description | Outils |
|-----|-------------|--------|
| `checkout` | Récupérer le code | actions/checkout |
| `install` | Installer les dépendances | npm, pip, zig build |
| `lint` | Vérifier formatage et lint | ruff, eslint, zig fmt |
| `test` | Exécuter les tests | pytest, cargo test, zig test |
| `build` | Construire le projet | npm run build, cargo build, zig build |

## Template GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.12']
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff pytest

      - name: Lint (ruff)
        run: |
          ruff format --check .
          ruff check .

      - name: Run tests
        run: pytest -v

      - name: Build
        run: |
          # Ajouter les étapes de build ici
          echo "Build OK"
```

## Template pour projets Zig

```yaml
# .github/workflows/ci-zig.yml
name: CI (Zig)

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Zig
        uses: egor-tensin/setup-zig@v1
        with:
          version: '0.15.0'

      - name: Format check
        run: zig fmt --check

      - name: Build
        run: zig build

      - name: Test
        run: zig test

      - name: Run binaries
        run: |
          zig build run-trix || true
```

## Exécution locale

```bash
# Exécuter le pipeline localement
act -j ci

# Ou les étapes individuellement
ruff format . && ruff check .
pytest
zig test
```

## Fail-fast policy

- **Lint échoue** → Arrêt immédiat
- **Tests échouent** → Arrêt immédiat
- **Build échoue** → Arrêt immédiat

## Cache des dépendances

```yaml
- name: Cache pip
  uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

## Notifications

- Échec → Notification Slack/Discord
- Succès → Notification silencieuse (optionnel)