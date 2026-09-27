---
type: PRD
version: "1.0"
date: "2026-09-23"
status: draft
intent_hash: 0xPRD_MOC_LOCAL_CI_PIPELINE_20260923
---

# PRD-MOC — Local CI Pipeline

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-23

## Contexte

Le repo n'a pas de CI/CD local fonctionnel :
- `.github/workflows/` n'existe pas ✅ (conforme BDCP)
- `workflows/` contient des docs markdown mais pas de scripts CI exécutables
- `scripts/local_ci.py` et `scripts/local_ci.ps1` existent mais ne sont pas appelés par les hooks
- Le pre-commit appelle `kiva pipeline run unified-design` mais sans vérification préalable

## Mission

Implémenter un pipeline CI local qui valide le MDU avant tout push.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| Pipeline local CI | ⭐⭐⭐⭐⭐ | P0 | Moyen | Valide avant push |
| Intégration pre-push | ⭐⭐⭐⭐ | P1 | Minimal | Bloque les mauvais commits |
| Rapport CI | ⭐⭐⭐ | P1 | Minimal | Traçabilité |

**Verdict** : 1 P0 + 2 P1. Effort moyen, valeur élevée.

## Livrables

1. **`scripts/local_ci.py`** — pipeline CI local
2. **Pre-push hook** — appel à `local_ci.py`
3. **Rapport CI** — sortie JSON + Markdown

## Critères d'acceptation

- [ ] `python scripts/local_ci.py` passe sur `main`
- [ ] Pre-push hook bloque si CI échoue

## Références

- `scripts/local_ci.py`
- `.pre-commit-config.yaml`
- `workflows/ci-template.yml`
