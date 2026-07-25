---
type: ADR
status: proposed
date: "2026-07-16"
intent_hash: 0xADR_027_WAZAA_MDU_INTEGRATION_20260716
---

# ADR-027 — Intégration WAZAA dans le Meta-Design Atlas (MDU)

## Contexte

L'analyse des conversations KiloCode et des documents WAZAA a révélé **10 nouveaux designs atomiques** qui viennent enrichir la couche N+0 du MDU. Ces designs couvrent :

- **Communication distribuée** : cluster-federation, cognitive-bus, event-streaming
- **Mémoire locale** : sovereign-vector-memory
- **Gouvernance de session** : smart-termination, cognitive-bridge
- **Outils CLI unifiés** : anything-cli-unified
- **Capture conversationnelle** : pipeline-anamorphique-capture
- **Sécurité opérationnelle** : git-remote-safety, encoding-batch-fixer
- **Patterns d'implémentation** : pipeline-anamorphique

Ces atomes complètent les 41 atomes canoniques existants et les 32 atomes ajoutés précédemment, portant le total à **83 atomes**.

## Décision

Intégrer les 10 nouveaux atomes dans le catalogue MDU avec :

1. **Fichiers YAML** dans `unified-design/atoms/`
2. **Mise à jour de l'index** `L1-INFRA_Atoms_Index.yaml`
3. **Documentation** des relations avec les atomes existants
4. **Tests de validation** des schémas YAML

## Atomes ajoutés

| # | Nom | Type | Source |
|---|-----|------|--------|
| 1 | cluster-federation | Protocol | EPIC-1221 |
| 2 | sovereign-vector-memory | Architecture | INTENT-005 |
| 3 | cognitive-bus | Integration | INTENT-001 |
| 4 | smart-termination | Protocol | EPIC-1203 |
| 5 | cognitive-bridge | Integration | INTENT-007 |
| 6 | anything-cli-unified | CLI | EPIC-1220 |
| 7 | event-streaming | Pipeline | EPIC-1222 |
| 8 | pipeline-anamorphique | Pipeline | ses_demo_001 |
| 9 | git-remote-safety | Safety | ses_004 |
| 10 | encoding-batch-fixer | Tool | ses_demo_002 |
| 11 | pipeline-anamorphique-capture | Tool | conversations |

## Conséquences

### Positives ✅
- **Couverture MDU** : Passe de 73 à **83 atomes** formalisés
- **Gouvernance prédictive** : Les patterns WAZAA sont maintenant canonisés
- **Interopérabilité** : Les atomes peuvent être réutilisés dans d'autres projets
- **Validation automatique** : Les schémas YAML permettent la validation CI

### Risques ⚠️
- **Complexité accrue** : Le catalogue MDU est plus complet mais plus complexe
- **Maintenance** : Les atomes doivent être maintenus avec les évolutions des citizens

## Relations avec les atomes existants

```
cognitive-bus
├── cluster-federation (hérite)
├── event-streaming (hérite)
└── cognitive-bridge (hérite)

sovereign-vector-memory
├── smart-termination (complémente)
└── pipeline-anamorphique-capture (alimente)

anything-cli-unified
├── cognitive-bus (consomme)
└── git-remote-safety (valide)

pipeline-anamorphique-capture
├── encoding-batch-fixer (détecte)
└── pipeline-anamorphique (analyse)
```

## Validation

- [x] Schémas YAML valides
- [x] Index mis à jour
- [x] Relations documentées
- [ ] Tests CI/CD (à venir)

## Références

- Rapport MDU_MISSING_DESIGNS_20260716.md
- INTENT-001, INTENT-005, INTENT-007
- EPIC-1220, EPIC-1221, EPIC-1222, EPIC-1203
- Sessions KiloCode: ses_demo_001, ses_demo_002, ses_004, ses_005

## Statut

- **Date** : 2026-07-16
- **Statut** : proposed
- **Prochaine étape** : Revues par l'équipe architecturale, merge sur `gerivdb/unified-design`