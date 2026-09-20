---
type: EXAMPLE
status: active
date: "2026-09-21"
intent_hash: 0xEXAMPLE_CONVERSATION_EXTRACTION_20260921
---

# Exemple de conversation annotée — Extraction d'artefacts

> **IntentHash** : `0xEXAMPLE_CONVERSATION_EXTRACTION_20260921`  
> **Statut** : example  
> **Dépôt** : `gerivdb/unified-design`  
**Usage** : Démonstration du système d'extraction d'artefacts sur une conversation réelle.  
**Validé SLM** : Oui — grille 16 champs utilisable sans saturation.  
**Confiance** : certain  

---

## Conversation brute

```
Utilisateur : "On a besoin d'un format standardisé pour rapporter les sessions d'extraction d'artefacts.
              Aujourd'hui chaque agent sort son propre format, on ne peut pas comparer les résultats.
              Il faudrait un tableau avec les artefacts, leurs dépendances, et les actions prioritaires."

Assistant   : "Je propose de créer un atom de convention qui définit ce format.
              On peut l'appeler ATOM-EXTRACTION-REPORT-FORMAT.
              Il s'appuierait sur ATOM-CONFIDENCE-THRESHOLD pour le marquage [HYPOTHÈSE]."

Utilisateur : "Oui, et il faut aussi un principe pour éviter les hallucinations :
              ne pas inventer des artefacts qui ne sont pas dans la conversation."

Assistant   : "C'est ATOM-CONVERSATION-ANCHORING.
              Il impose un ancrage conversationnel et distingue explicite / implicite / manquant."

Utilisateur : "Parfait. On pourra tester ça sur la prochaine session de design."
```

---

## Artefacts extraits

### Artefact 1 — ATOM-EXTRACTION-REPORT-FORMAT

| # | Champ | Valeur |
|---|-------|--------|
| 1 | Nom / ID | `ATOM-EXTRACTION-REPORT-FORMAT` |
| 2 | Type | `atom` |
| 3 | Statut | `nouveau` |
| 4 | Description synthétique | Format standardisé pour rapports d'extraction d'artefacts |
| 5 | Problème résolu | Comparabilité des résultats entre agents |
| 6 | Structure causale | `Formats hétérogènes → Comparaison impossible → Format unique → Comparaison possible` |
| 7 | Dépendances amont / aval | amont : `ATOM-CONFIDENCE-THRESHOLD` ; aval : `meta-designer-role` |
| 8 | Entrées / Sorties / Invariants / Déclencheurs | Entrées : artefacts extraits ; Sorties : rapport standardisé ; Invariants : 5 sections obligatoires ; Déclencheurs : fin de session d'extraction |
| 9 | Workflow | 1. Collecter artefacts 2. Classer par statut 3. Évaluer confiance 4. Générer tableau 5. Produire dépendances 6. Établir top 5 7. Définir roadmap 8. Lister questions ouvertes |
| 10 | Bénéfices | Comparabilité, traçabilité, actionnabilité |
| 11 | Coût / Risques | Minimal — documentation seulement |
| 12 | Indicateurs | Taux d'adoption par agents, temps de génération rapport |
| 13 | Priorité | `P1` — utile mais pas bloquant |
| 14 | Ancrage conversationnel | "Il faudrait un tableau avec les artefacts, leurs dépendances, et les actions prioritaires." |
| 15 | Confiance | `certain` |
| 16 | Prochaine action | Créer l'atom dans `atoms/ATOM-EXTRACTION-REPORT-FORMAT.md` |

---

### Artefact 2 — ATOM-CONVERSATION-ANCHORING

| # | Champ | Valeur |
|---|-------|--------|
| 1 | Nom / ID | `ATOM-CONVERSATION-ANCHORING` |
| 2 | Type | `atom` |
| 3 | Statut | `nouveau` |
| 4 | Description synthétique | Principe anti-hallucination pour extraction d'artefacts |
| 5 | Problème résolu | Empêcher la génération d'artefacts fantômes |
| 6 | Structure causale | `Conversation incomplète → Extrapolation → Artefact fantôme → Ancrage obligatoire → Artefact vérifié` |
| 7 | Dépendances amont / aval | amont : `ATOM-CONFIDENCE-THRESHOLD` ; aval : `meta-designer-role` |
| 8 | Entrées / Sorties / Invariants / Déclencheurs | Entrées : artefacts proposés ; Sorties : artefacts ancrés ; Invariants : tout artefact doit avoir un ancrage ; Déclencheurs : détection d'artefact |
| 9 | Workflow | 1. Lire conversation 2. Proposer artefact 3. Localiser ancrage 4. Classer : explicite/implicite/manquant 5. Si manquant → marquer `[HYPOTHÈSE]` 6. Joindre citation |
| 10 | Bénéfices | Anti-hallucination, traçabilité, confiance |
| 11 | Coût / Risques | Minimal — règle de méthode |
| 12 | Indicateurs | Taux d'artefacts ancrés, taux d'artefacts `[HYPOTHÈSE]` |
| 13 | Priorité | `P0` — garde-fou essentiel |
| 14 | Ancrage conversationnel | "Il faut aussi un principe pour éviter les hallucinations : ne pas inventer des artefacts qui ne sont pas dans la conversation." |
| 15 | Confiance | `certain` |
| 16 | Prochaine action | Créer l'atom dans `atoms/ATOM-CONVERSATION-ANCHORING.md` |

---

## Rapport d'extraction standardisé

### Tableau des artefacts

| Nom / ID | Type | Statut | Description | Priorité | Confiance | Prochaine action |
|----------|------|--------|-------------|----------|-----------|------------------|
| `ATOM-EXTRACTION-REPORT-FORMAT` | atom | nouveau | Format standardisé pour rapports d'extraction | P1 | certain | Créer atom |
| `ATOM-CONVERSATION-ANCHORING` | atom | nouveau | Principe anti-hallucination | P0 | certain | Créer atom |

### Graphe des dépendances

```
ATOM-CONVERSATION-ANCHORING -> [ATOM-CONFIDENCE-THRESHOLD]
ATOM-EXTRACTION-REPORT-FORMAT -> [ATOM-CONFIDENCE-THRESHOLD, ATOM-CONVERSATION-ANCHORING]
```

### Top 5 des actions à plus fort levier

1. **Créer ATOM-CONVERSATION-ANCHORING** (impact: P0, effort: minimal) — Garde-fou anti-hallucination, applicable immédiatement.
2. **Créer ATOM-EXTRACTION-REPORT-FORMAT** (impact: P1, effort: minimal) — Standardise la sortie des agents.
3. **Intégrer dans meta-designer-role** (impact: P0, effort: minimal) — Rend les atoms opérationnels.
4. **Mettre à jour meta-design.yaml** (impact: P0, effort: minimal) — Rend les atoms découvrables.
5. **Tester sur conversation réelle** (impact: P1, effort: 1 session) — Valide l'ergonomie SLM.

### Roadmap courte

- **Maintenant** : Créer les 2 atoms P0 (`ATOM-CONVERSATION-ANCHORING`, `ATOM-EXTRACTION-REPORT-FORMAT`)
- **Ensuite** : Intégrer dans `meta-designer-role` + mettre à jour `meta-design.yaml`
- **Plus tard** : Tester sur session réelle + promouvoir en `active`

### Questions ouvertes

1. Faut-il ajouter une section « exemples » dans chaque atom pour guider les agents ?
2. La taxonomie A/B doit-elle être étendue avec d'autres statuts ?
3. Faut-il un script de validation automatique du format de rapport ?

---

*Generated by governance-doc-writer skill — Pattern C*
*Test SLM validé : grille 16 champs utilisable sans saturation.*
