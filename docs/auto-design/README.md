# Auto-Design

## Principe

`auto-design` est le motif d'industrialisation déclarative d'un repo :
- `design.yaml` canonique déclare les composants, contrats, bridges, tests
- runtimes (`cycle_runner.py`, `bridge_executor.py`, `pr_factory.py`) exécutent la médiation et la vérification continues
- `analyzer.py` évalue la maturité auto-design
- `generator.py` génère les artefacts pour un repo cible
- `industrializer.py` déploie les runtimes
- `verifier.py` vérifie l'adhérence au motif
- `reporter.py` produit un rapport global

## CLI

```powershell
python scripts/auto_design_cli.py analyze <repo>
python scripts/auto_design_cli.py generate <repo> --apply
python scripts/auto_design_cli.py deploy <repo>
python scripts/auto_design_cli.py verify <repo>
python scripts/auto_design_cli.py report --global
```

## Aufhebung

Mécanisme architectural par lequel un repo annule sa dépendance humaine centralisée, conserve son identité métier, et s'élève vers l'auto-gouvernance via auto-design.

## Références

- INTENT : `INTENTS/INTENT-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- PRD : `PRD/PRD-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- MOC : `MOC/MOC-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- Design : `designs/auto-design/design.yaml`
