---
name: prd-status-auto-promoter
description: "Skill qui vérifie les PRD/MOC et propose des transitions de statut quand les livrables sont présents. Automatise la partie évaluation sans toucher à la gouvernance humaine."
version: "1.0.0"
status: active
---

# Skill — PRD Status Auto Promoter

## Usage

```bash
python skills/prd-status-auto-promoter/SKILL.md
```

## Contrat

- Entrée : repo root + glob PRD/MOC
- Sortie : proposition de changement de statut (`proposed` -> `approved`, `draft` -> `implemented`)
- Garantie : ne change pas un statut sans vérification fichiersystem des livrables

## Validation

- `python scripts/verify_prd_status.py --check-all`
- `python scripts/dry_run_causal.py` doit rester `PROD READY 100%`
