# ATOM-CONFIDENCE-THRESHOLD

> **IntentHash** : `0xATOM_CONFIDENCE_THRESHOLD_20260920`  
> **Statut** : proposed  
> **Dépôt** : `gerivdb/unified-design`  
> **Màj requise si** : statut ADR passe à deprecated ou superseded  

---

## Description

Seuil de confiance 0.6 — Inspiré de D:\GG-knox\engineering ideas\300-kimi-k3\2.md.

Toute décision, vérification ou validation nécessite un seuil de confiance minimum de 0.6 avant d'être acceptée.

## Règles numériques

1. Score de confiance < 0.6 → décision bloquée, demande de vérification supplémentaire
2. Score de confiance ≥ 0.6 et < 0.8 → décision acceptée avec avertissement
3. Score de confiance ≥ 0.8 → décision acceptée sans avertissement
4. Le score de confiance est calculé à partir de sources indépendantes
5. Le score de confiance est documenté dans la preuve d'exécution (PoL)

## Cadre qualitatif (extension 2026-09-20)

| Niveau | Signification | Action |
|--------|---------------|--------|
| `certain` | Élément explicite, multi-sourcé, > 0.8 confiance | Accepter sans réserve |
| `probable` | Élément implicite, logique directe, 0.6-0.8 confiance | Accepter avec avertissement |
| `hypothèse` | Extrapolation au-delà de l'ancrage, < 0.6 confiance | Marquer `[HYPOTHÈSE]` + HITL requis |

## Convention de marquage

- `[HYPOTHÈSE]` : Tout élément `hypothèse` doit être explicitement marqué dans la fiche artefact (champ 15) et dans le rapport d'extraction.
- Interdiction : Présenter comme certain un élément marqué `[HYPOTHÈSE]`.

## Intégration MDU

- Couplé à `ATOM-CONVERSATION-ANCHORING` pour qualifier l'ancrage (explicite / implicite / manquant)
- Couplé à `ATOM-ARTIFACT-EXTRACTION-STATUS` pour classifier le statut (`à confirmer` si < 0.6)
- Couplé à `meta-coherence` pour détecter les écarts de confiance

## Références

- **Source** : `D:\GG-knox\engineering ideas\300-kimi-k3\2.md`
- **Concept** : Seuil de confiance 0.6
- ADR-2026-09-20-001 : Artifact Extraction MDU Extension
- ATOM-CONVERSATION-ANCHORING
