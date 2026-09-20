---
type: PRD
version: "1.0"
date: "2026-09-20"
status: draft
intent_hash: 0xPRD_MOC_ARTIFACT_EXTRACTION_20260920
---

# PRD-MOC — Artifact Extraction System

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : draft  
**Date** : 2026-09-20  

---

## Contexte

Le méta-designer (`pipeline-anamorphique-capture`, `conversation-forensics-analyzer`) extrait aujourd'hui des concepts depuis les conversations, mais sans grille d'extraction standardisée pour les artefacts de design. Il manque :

1. Une **grille 16 champs** reproductible pour fiche tout artefact détecté
2. Une **taxonomie de statut** (nouveau / mise à jour / fusion / suppression / à confirmer)
3. Un **principe d'ancrage conversationnel** pour limiter les hallucinations
4. Un **format de rapport** standardisé (tableau + dépendances + top 5 + roadmap)

## Mission

Implémenter dans `unified-design` un système d'extraction d'artefacts méta-cohérent, utilisable par tout agent opérant sur des conversations pour produire des designs, atoms, skills, pipelines ou workflows.

## Périmètre

| Inclut | Exclut |
|--------|--------|
| Grille 16 champs par artefact | Analyse NLP automatique sans validation HITL |
| Taxonomie A/B (nouveau / màj / fusion / suppression / à confirmer) | Génération libre d'artefacts non ancrés |
| Principe d'ancrage conversationnel + marquage `[HYPOTHÈSE]` | Modification du MDU sans ADR |
| Format de rapport standardisé | Intégration dans un repo hors MDU |

## Livrables

### L0 — Atoms gouvernants (P0)

1. **ATOM-ARTIFACT-EXTRACTION-STATUS** (`atoms/ATOM-ARTIFACT-EXTRACTION-STATUS.md`)
   - Taxonomie : `nouveau | mise à jour | fusion | suppression | à confirmer`
   - Règles de classification
   - Intégration `meta-design.yaml` > `governance_atoms`

2. **ATOM-CONVERSATION-ANCHORING** (`atoms/ATOM-CONVERSATION-ANCHORING.md`)
   - Règle : « Ne fabrique pas d'éléments non ancrés. Si extrapolation → `[HYPOTHÈSE]` »
   - Distinction explicite / implicite / manquant
   - Lien vers `meta-coherence` (détection GAP/GHOST)

3. **ATOM-EXTRACTION-REPORT-FORMAT** (`atoms/ATOM-EXTRACTION-REPORT-FORMAT.md`)
   - Structure : tableau compact + graphe dépendances + Top 5 + Roadmap + Questions ouvertes
   - Intégration `meta-design.yaml` > `governance_atoms`

### L0 — Primitive (P0)

4. **Primitive `artifact-extraction-card`** (`primitives/artifact-extraction-card/design.yaml`)
   - Grille 16 champs : Nom/ID, Type, Statut, Description, Problème résolu, Structure causale, Dépendances, Entrées/Sorties/Invariants/Déclencheurs, Workflow, Bénéfices, Coût/Risques, Indicateurs, Priorité, Ancrage conversationnel, Confiance, Prochaine action
   - Variante courte : 8 champs essentiels

### L1 — Extension (P1)

5. **Extension ATOM-CONFIDENCE-THRESHOLD**
   - Ajout cadre qualitatif : `certain | probable | hypothèse`
   - Convention de marquage : `[HYPOTHÈSE]` pour toute extrapolation
   - Maintien seuil numérique 0.6 minimum

### L1 — Design (P1)

6. **Design `meta-designer-role`** (`designs/meta-designer-role.yaml`)
   - Rôle formalisé : architecte systèmes complexes + méta-designer
   - Contraintes : ancrage, grille 16 champs, rapport standardisé
   - Héritage : `conversation-aggregator`, `design-documentation-generator`

## Architecture cible

```
unified-design/
├── atoms/
│   ├── ATOM-ARTIFACT-EXTRACTION-STATUS.md
│   ├── ATOM-CONFERSATION-ANCHORING.md
│   ├── ATOM-EXTRACTION-REPORT-FORMAT.md
│   └── ATOM-CONFIDENCE-THRESHOLD.md (étendu)
├── primitives/
│   └── artifact-extraction-card/
│       ├── design.yaml
│       └── README.md
├── designs/
│   └── meta-designer-role.yaml
└── meta-design.yaml (mis à jour)
```

## Dépendances

| Dépendance | Type | Raison |
|------------|------|--------|
| `ATOM-CONFIDENCE-THRESHOLD` | amont | Cadre de confiance existant à étendre |
| `meta-coherence` | amont | Détection GAP/GHOST/DRIFT ; ancrage conversationnel |
| `safe-action-pattern` | amont | Patron universel action ; structure causale |
| `conversation-forensics-analyzer` | amont | Base d'analyse forensique conversations |
| `pipeline-anamorphique-capture` | amont | Capture conversations ; extraction concepts |

## Critères d'acceptation

- [ ] 3 atoms P0 créés et référencés dans `meta-design.yaml`
- [ ] Primitive `artifact-extraction-card` créée et validée par `design.schema.json`
- [ ] `ATOM-CONFIDENCE-THRESHOLD` étendu avec cadre qualitatif
- [ ] Design `meta-designer-role` créé et héritage validé
- [ ] Aucun doublon avec atoms existants (`artifact-synced-loop`, `conversation-forensics-analyzer`)
- [ ] Frontmatter YAML valide pour tous les documents de gouvernance

## Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Doublon avec `artifact-synced-loop` | Moyen | Vérification systématique avant création |
| Grille 16 champs trop lourde pour SLM | Moyen | Variante courte prévue |
| Taxonomie A/B non adoptée | Faible | Intégration dans `meta-design.yaml` > `governance_atoms` |

## Références

- `meta-design.yaml` > `governance_atoms`
- `designs/safe-action-pattern.yaml`
- `atoms/ATOM-CONFIDENCE-THRESHOLD.md`
- `atoms/conversation-forensics-analyzer.yaml`
- `atoms/pipeline-anamorphique-capture.yaml`
- `schemas/design.schema.json`

---

*Generated by governance-doc-writer skill — Pattern C*
