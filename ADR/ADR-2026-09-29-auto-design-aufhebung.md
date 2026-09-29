---
type: ADR
version: "1.0.0"
date: "2026-09-29"
status: proposed
intent_hash: 0xADR_AUTO_DESIGN_AUFHEBUNG_20260929
---

# ADR — Auto-Design comme Aufhebung et Autonomie de l'Écosystème

## Contexte

L'écosystème `gerivdb/*` compte 50+ repos actifs. Chaque repo nécessite
un `design.yaml` canonique, des contrats d'implémentation, des bridges
et des runtimes d'exécution. Historiquement, ces artefacts sont créés
manuellement par des agents humains ou IA, ce qui :
1. Crée des inconsistances entre repos
2. Coûte du temps de coordination
3. Empêche l'auto-gouvernance des repos

## Problème

1. Aucune mécanique déclarative pour générer `design.yaml` + contracts + bridges
2. Aucune vérification automatisée de l'adhérence au motif auto-design
3. Aucune industrialisation cross-repo reproductible
4. Les repos citizens (FLUENCE, CANDIDATOR, etc.) restent non auto-designés
5. Pas de promotion automatique des documents de gouvernance (ADR/Design/INTENT)

## Décision

Introduire le motif **auto-design** comme fonction native de `unified-design` :

1. **`engine/auto_design/analyzer.py`** : score de maturité 0-100
2. **`engine/auto_design/generator.py`** : génère `design.yaml` + contracts + bridges
3. **`engine/auto_design/industrializer.py`** : copie templates runtimes
4. **`engine/auto_design/verifier.py`** : vérifie adhérence + score
5. **`engine/auto_design/reporter.py`** : rapport global
6. **`engine/auto_design/auto_promote.py`** : promotion automatique governance
7. **`scripts/auto_design_cli.py`** : CLI `analyze|generate|deploy|verify|report|promote`
8. **`templates/auto_design/*.py`** : `cycle_runner`, `bridge_executor`, `pr_factory`
9. **`skills/auto-design-readiness/SKILL.md`** : guide d'usage
10. **Hooks pre-commit** : bloquent si `design.yaml` absent ou promotion manquée

## Conséquences

### Positives
- Auto-gouvernance déclarative des repos
- Réduction du travail manuel de coordination
- Vérification continue de l'adhérence
- Promotion automatique des documents de gouvernance
- Extension cross-repo reproductible (Phase 2/3)

### Négatives
- Surcoût initial : 6 repos industrialisés (Phase 2)
- Complexité : nouveaux modules à maintenir
- Risque de blocage : hooks pre-commit stricts
- Chemins manquants pour 7 repos (Phase 3 en attente)

## Alternatives considérées

| Alternative | Raison du rejet |
|---|---|
| Création manuelle par repo | Non scalable, 50+ repos |
| Script ad-hoc par repo | Duplication, pas de motif canonique |
| CI/CD uniquement | Pas de feedback immédiat, pas de dry-run |
| Documentation seulement | Pas de enforcement mécanique |

## Références

- **PRD** : `PRD/PRD-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **MOC** : `MOC/MOC-AUTO-DESIGN-AUFHEBUNG-20260929.md`
- **Design** : `designs/auto-design/design.yaml`
- **Repo PoC** : `gerivdb/AUTO-DEV` (100% opérationnel)

## Statut

Proposé — Phase 1 implémentée et testée (8 tests passants), Phase 2 en cours (6/7 repos industrialisés).
