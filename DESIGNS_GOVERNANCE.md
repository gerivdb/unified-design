# Designs — Gouvernance écosystème

> **RÈGLE ABSOLUE** : `gerivdb/unified-design` est le **dépositaire unique**
> de TOUS les designs de l'écosystème gerivdb.

## périmètre

| Couche | Dépôt | Rôle |
|--------|-------|------|
| **L0** | `gerivdb/unified-design` | **Source de vérité unique** — tous les designs, atoms, mathemes, conventions |
| L1-L4 | Repos d'implémentation | Implémentent les designs qui les concernent — **jamais de dossier `designs/` local** |

## Règles

1. **Interdiction stricte** : créer un dossier `designs/` dans tout repo autre que `unified-design`.
2. **Processus normal** : tout nouveau design → `unified-design/designs/<nom>.yaml`, puis référencé depuis les PRD/INTENT des repos d'implémentation.
3. **Implémentations** : chaque repo implémente les designs qui le concernent dans son propre code.
4. **Référence croisée** : tout PRD/INTENT mentionnant un design doit citer son chemin dans `unified-design/designs/`.

## Recette nouveau design

```
1. Créer le YAML dans unified-design/designs/
2. Vérifier conformité schéma : unified-design/schemas/design.schema.json
3. Commit dans unified-design (L0)
4. Référencer depuis le PRD/INTENT du repo d'implémentation
5. Implémenter + tester dans le repo concerné
```

## Référence ADR

- **ADR** : ADR-2026-06-07-001-ADR-GOVERNANCE-GATE
- **IntentHash** : `0xADR_GOVERNANCE_GATE_20260607`
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed

---

*Dernière mise à jour : 2026-08-25 — Corrigé après incident KG35-V10 (designs créés dans KG-L au lieu de unified-design)*
