# Skill — Auto-Design Readiness

## Quand l'utiliser

- Évaluer la maturité auto-design d'un repo cible
- Générer un `design.yaml` + `implementation_contract` + `bridges` pour un repo non encore auto-designé
- Déployer les runtimes auto-design (`cycle_runner.py`, `bridge_executor.py`, `pr_factory.py`)
- Vérifier l'adhérence au motif auto-design
- Produire un rapport de couverture global

## Prérequis

- `unified-design` cloné dans `D:\DO\WEB\TOOLS\L0-CANON\unified-design`
- Python 3.9+ sur le PATH
- Repo cible accessible localement

## Commandes

```powershell
# Analyser un repo
python scripts/auto_design_cli.py analyze D:\DO\WEB\TOOLS\L4-TOOLS\VEX

# Générer design.yaml + contracts + bridges (dry-run)
python scripts/auto_design_cli.py generate D:\DO\WEB\TOOLS\L4-TOOLS\VEX

# Générer et appliquer
python scripts/auto_design_cli.py generate D:\DO\WEB\TOOLS\L4-TOOLS\VEX --apply

# Déployer les runtimes
python scripts/auto_design_cli.py deploy D:\DO\WEB\TOOLS\L4-TOOLS\VEX

# Vérifier l'adhérence
python scripts/auto_design_cli.py verify D:\DO\WEB\TOOLS\L4-TOOLS\VEX

# Rapport global
python scripts/auto_design_cli.py report
```

## Sortie

- `analyze` : JSON avec `auto_design_readiness` (0-100) + recommandations
- `generate` : JSON avec `design_yaml`, `contracts`, `bridges`
- `deploy` : JSON avec `deployed` chemins
- `verify` : JSON avec `auto_design_score` + breakdown
- `report` : JSON agrégé sur tous les repos connus

## Seuils

- `auto_design_readiness >= 80` : mature, prêt pour industrialisation
- `auto_design_score >= 80` : conforme au motif auto-design

## Référence

- INTENT : `INTENTS/INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- Design : `designs/auto-design/design.yaml`
- Engine : `engine/auto_design/`
