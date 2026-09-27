---
type: ADR
version: "1.0.0"
date: "2026-09-27"
status: proposed
intent_hash: 0xADR_UNIFIED_DESIGN_METACOHERENCE_AUTOMATION_20260927
---

# ADR — Unified-Design Métacohérence Automatisée et Gap-Comblé-ification

## Contexte

Le repo `unified-design` contient 148 designs, 392 atoms et 5053 fichiers.
Historiquement, les designs sont des documents passifs sans vérification
d'implémentation. Cela crée des gaps croissants entre design et code,
et empêche toute métacoherence écosystémique.

## Problème

1. Aucune vérification automatique que les designs sont implémentés
2. Aucune traçabilité causale entre design et code
3. Aucune enforcement du pattern THINK/DO/CHECK
4. Les designs VEX étaient dans un dossier local `design/` au lieu de `unified-design`
5. 123/133 designs n'ont pas d'ADR backing

## Décision

Introduire un système de métacohérence automatisée avec :

1. **`implementation_contract`** dans chaque design `active` :
   - `repo` : repo cible
   - `repo_root` : chemin local
   - `artifacts` : fichiers + patterns à vérifier
   - `tests` : tests à exécuter

2. **`design_impl_verifier.py`** : vérifie les artifacts et patterns

3. **`metacoherence_gate.py`** : enforce THINK/DO/CHECK avec audit period

4. **`gap_combleur.py`** : détecte et reporte les gaps d'implémentation

5. **Hook pre-commit** : bloque les commits si impl manquante

6. **Migration designs VEX** : regrouper tous les designs dans unified-design

## Conséquences

### Positives
- Traçabilité causale design→code
- Détection automatique des gaps
- Métacoherence écosystémique enforceable
- Réduction de la dette technique

### Négatives
- Surcoût initial : ajout de contracts pour 148 designs
- Complexité : nouveaux outils à maintenir
- Risque de blocage : hook pre-commit peut bloquer le développement

## Alternatives considérées

| Alternative | Raison du rejet |
|---|---|
| Vérification manuelle | Non scalable, oubli fréquent |
| CI/CD uniquement | Trop tardif, pas de feedback immédiat |
| Documentation seulement | Pas de enforcement mécanique |

## Références

- **PRD-MOC** : `PRD-MOC-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md`
- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **INTENT** : `INTENTS/INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md`

## Statut

Proposé — en attente d'approbation pour implémentation complète.
