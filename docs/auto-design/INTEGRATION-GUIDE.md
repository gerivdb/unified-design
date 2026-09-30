# Integration Guide — Auto-Design Écosystémique

## Vue d'ensemble

Ce guide explique comment intégrer, utiliser et bénéficier du motif auto-design sur l'ensemble des repos `gerivdb/*`.

## Architecture

```
unified-design/
├── engine/auto_design/
│   ├── analyzer.py          # Score maturité 0-100
│   ├── generator.py         # Génère design.yaml + contracts + bridges
│   ├── industrializer.py    # Copie templates runtimes
│   ├── verifier.py          # Vérifie adhérence + score
│   ├── reporter.py          # Rapport global
│   └── auto_promote.py      # Promotion automatique governance
├── scripts/
│   └── auto_design_cli.py   # CLI unifiée
├── templates/auto_design/
│   ├── cycle_runner.py      # Cycle auto-design
│   ├── bridge_executor.py   # Exécution bridges
│   └── pr_factory.py        # Factory PR
├── designs/auto-design/
│   └── design.yaml          # Motif canonique
├── designs/auto-promote/
│   ├── adr-criteria.yaml    # Critères ADR
│   ├── design-criteria.yaml # Critères Design
│   └── intent-criteria.yaml # Critères INTENT
└── skills/auto-design-readiness/
    └── SKILL.md             # Guide d'usage
```

## Workflow d'intégration

### Étape 1 — Analyser

```powershell
python scripts/auto_design_cli.py analyze <repo_path>
```

Sortie : JSON avec `auto_design_readiness` (0-100) + recommandations

### Étape 2 — Générer

```powershell
python scripts/auto_design_cli.py generate <repo_path> --apply
```

Crée :
- `design.yaml` racine
- `implementation_contracts/*.yaml`
- `bridges/*.yaml`

### Étape 3 — Déployer

```powershell
python scripts/auto_design_cli.py deploy <repo_path>
```

Copie les runtimes :
- `scripts/cycle_runner.py`
- `scripts/bridge_executor.py`
- `scripts/pr_factory.py`

### Étape 4 — Vérifier

```powershell
python scripts/auto_design_cli.py verify <repo_path>
```

Sortie : JSON avec `auto_design_score` (0-100) + `mature` (≥80)

### Étape 5 — Reporter

```powershell
python scripts/auto_design_cli.py report
```

Sortie : JSON agrégé sur tous les repos `active`

## Intégration cross-repo

### Bridge déclaratif

Chaque bridge déclare une médiation entre composants :

```yaml
from: unified-design/auto-design
to: NEXUS/auto-design
type: declarative
status: active
intent_hash: 0xBRIDGE_UNIFIED_DESIGN_NEXUS
```

### Cycle runner

Le `cycle_runner.py` exécute les médiations :

```powershell
python scripts/cycle_runner.py --repo <repo_path> --mode verify
```

### Auto-promote

Promouvoir automatiquement les documents de gouvernance :

```powershell
python scripts/auto_design_cli.py promote --dry-run
python scripts/auto_design_cli.py promote --apply
```

## Hooks pre-commit

### auto-design-verifier

Bloque si `design.yaml` absent sur repo `active` :

```powershell
python .kilocode/hooks/pre-commit-auto-design-verifier.py
```

### auto-promote

Bloque si promotion manquée sur document `proposed` :

```powershell
python .kilocode/hooks/pre-commit-auto-promote.py
```

## CI locale

Script PowerShell pour vérifier auto-design :

```powershell
powershell -File "scripts/run_auto_design_check.ps1" -Command all
```

## Vérification écosystémique

### Scanner tous les repos

```powershell
python scripts/auto_design_cli.py report
```

### Vérifier un repo spécifique

```powershell
python scripts/auto_design_cli.py verify <repo_path>
```

### Valider les bridges

```powershell
python scripts/auto_design_cli.py verify <repo_path> --bridges
```

## Bonnes pratiques

1. **Toujours analyser avant de générer** : connaître l'état du repo
2. **Générer en dry-run d'abord** : vérifier le contenu avant `--apply`
3. **Déployer les runtimes systématiquement** : cycle_runner + bridge_executor
4. **Vérifier après déploiement** : score ≥80 = mature
5. **Promouvoir régulièrement** : éviter l'accumulation de `proposed`

## Dépannage

### Score < 80

- Vérifier que `design.yaml` existe
- Vérifier que `implementation_contract:` est présent
- Vérifier que `bridges/` contient ≥1 fichier
- Vérifier que `tests/` contient des tests

### Hook pre-commit bloque

- Vérifier que `design.yaml` est présent
- Vérifier que les documents `proposed` avec Proof-of-Life sont promus
- Utiliser `git commit --no-verify` en dernier recours (NOT RECOMMENDED)

### Bridge cassé

- Vérifier le `intent_hash` du bridge
- Vérifier que les composants source/cible existent
- Exécuter `bridge_executor.py --status` pour diagnostiquer
