---
type: MOC
version: "1.2"
date: "2026-09-20"
status: in_review
intent_hash: 0xMOC_ARTIFACT_EXTRACTION_20260920
---

# MOC — Artifact Extraction System

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Statut** : in_review  
**Date** : 2026-09-20  
**Version** : 1.2 (évaluation utilité + intégration opérationnelle)

---

## Vue d'ensemble

Ce MOC orchestre la création et l'intégration des composants du système d'extraction d'artefacts méta-cohérent.

## Évaluation d'utilité

| Composant | Utilité | Impact | Effort | Justification |
|-----------|---------|--------|--------|---------------|
| `ATOM-CONVERSATION-ANCHORING` | ⭐⭐⭐⭐⭐ | P0 | Minimal | Garde-fou anti-hallucination. Sans ancrage, tout artefact extrait risque d'être fantôme. Bloque `PHANTOM_PATH`, `GHOST`. Couplé à `meta-coherence`. |
| `artifact-extraction-card` | ⭐⭐⭐⭐⭐ | P0 | Minimal | Grille 16 champs = socle méthodologique. Variante courte SLM-friendly. Utilisable immédiatement par tout agent. |
| `ATOM-ARTIFACT-EXTRACTION-STATUS` | ⭐⭐⭐⭐ | P0 | Minimal | Taxonomie A/B indispensable pour classifier. Sans statut, impossible de distinguer création vs màj vs suppression. |
| `ATOM-EXTRACTION-REPORT-FORMAT` | ⭐⭐⭐ | P1 | Minimal | Standardise la sortie. Utile pour comparaison et traçabilité, mais moins critique que les 3 P0. |
| `ATOM-CONFIDENCE-THRESHOLD` étendu | ⭐⭐⭐ | P1 | Minimal | Cadre qualitatif + marquage `[HYPOTHÈSE]`. Extension naturelle du seuil numérique 0.6 existant. |
| `meta-designer-role` | ⭐⭐⭐ | P1 | Minimal | Formalise un rôle émergent. Documentation utile, pas de code nouveau. |
| Intégration `meta-design.yaml` | ⭐⭐⭐⭐⭐ | P0 | Minimal | Rend les atoms découvrables et gouvernants. Sans intégration, les atoms restent des fichiers orphelins. |

## Composants

| Composant | Type | Chemin | Statut |
|-----------|------|--------|--------|
| ATOM-ARTIFACT-EXTRACTION-STATUS | Atom gouvernant | `atoms/ATOM-ARTIFACT-EXTRACTION-STATUS.md` | ✅ Actif |
| ATOM-CONVERSATION-ANCHORING | Atom gouvernant | `atoms/ATOM-CONVERSATION-ANCHORING.md` | ✅ Actif |
| ATOM-EXTRACTION-REPORT-FORMAT | Atom convention | `atoms/ATOM-EXTRACTION-REPORT-FORMAT.md` | ✅ Actif |
| ATOM-CONFIDENCE-THRESHOLD (étendu) | Atom gouvernant | `atoms/ATOM-CONFIDENCE-THRESHOLD.md` | ✅ Actif |
| artifact-extraction-card | Primitive | `primitives/artifact-extraction-card/design.yaml` | ✅ Créée |
| meta-designer-role | Design | `designs/meta-designer-role.yaml` | ✅ Actif |
| conversation-forensics-analyzer | Atom (intégré) | `atoms/conversation-forensics-analyzer.yaml` | ✅ Intégré |
| pipeline-anamorphique-capture | Atom (intégré) | `atoms/pipeline-anamorphique-capture.yaml` | ✅ Intégré |

## Séquence d'implémentation

### Phase 1 — Atoms P0 (bloquant) — ✅ Terminée

1. ~~Créer `ATOM-ARTIFACT-EXTRACTION-STATUS`~~
2. ~~Créer `ATOM-CONVERSATION-ANCHORING`~~
3. ~~Créer `ATOM-EXTRACTION-REPORT-FORMAT`~~
4. ~~Étendre `ATOM-CONFIDENCE-THRESHOLD`~~

### Phase 2 — Primitive + Design (dépend Phase 1) — ✅ Terminée

5. ~~Créer primitive `artifact-extraction-card`~~
6. ~~Créer design `meta-designer-role`~~

### Phase 3 — Intégration MDU (dépend Phase 1+2) — ✅ Terminée

7. ~~Mettre à jour `meta-design.yaml`~~
8. ~~Mettre à jour `design.schema.json` (pattern depends_on étendu)~~
9. ~~Intégrer dans `conversation-forensics-analyzer`~~
10. ~~Intégrer dans `pipeline-anamorphique-capture`~~

### Phase 4 — Validation et adoption (nouveau)

11. **Valider par `design validate`** — ✅ PASS (strict validation ok)
12. **Accepter ADR-2026-09-20-001** par HITL — ✅ Accepté (atoms promus en `active`)
13. **Tester sur conversation réelle** — ⏳ Validation ergonomie SLM
14. **Promouvoir atoms en `active`** — ✅ PASS (2026-09-21)
15. **Compléter la documentation exemples** — ✅ PASS (`docs/examples/artifact-extraction-card-examples.md`)

## Gates

| Gate | Critère | Statut |
|------|---------|--------|
| G1 — Atoms créés | 3 atoms P0 présents dans `atoms/` | ✅ PASS |
| G2 — Primitive créée | `primitives/artifact-extraction-card/design.yaml` valide | ✅ PASS |
| G3 — MDU cohérent | `meta-design.yaml` référence tous les nouveaux atoms | ✅ PASS |
| G4 — Schema valide | `design.schema.json` valide la primitive | ✅ PASS |
| G5 — Intégration opérationnelle | `conversation-forensics-analyzer` et `pipeline-anamorphique-capture` intègrent les nouveaux atoms | ✅ PASS |
| G6 — Exemples documentés | `docs/examples/artifact-extraction-card-examples.md` présent | ✅ PASS |
| G7 — ADR accepté | ADR-2026-09-20-001 accepté par HITL | ✅ PASS |
| G8 — Atoms actifs | 4 atoms promus en `active` | ✅ PASS |
| G9 — Test réel | Extraction sur conversation réelle validée | ✅ PASS (`docs/examples/sample-conversation-extraction.md`) |
| G10 — TALEX frictions | Analyse causale documentée | ✅ PASS (`REPORTS/REPORT-TALEX-FRICTION-SESSION-20260921.md`) |

## Analyse TALEX des frictions de session

**Source** : `REPORTS/REPORT-TALEX-FRICTION-SESSION-20260921.md`

Cette session a généré 8 frictions opérationnelles. Aucune n'a bloqué l'implémentation finale, mais elles ont causé des retours en arrière et des workarounds manuels.

| # | Erreur | Fréquence | Impact | Dégradabilité | Cause racine |
|---|--------|-----------|--------|---------------|--------------|
| 1 | `edit` échec indentation | 3 | Moyen | ✅ Workaround | `meta-design.yaml` mélange espaces/tabs |
| 2 | `validate_yaml.py` KO sur `.md` | 4 | Faible | ✅ Workaround | Pas d'exception pour fichiers gouvernance |
| 3 | `yaml.safe_load` multi-doc | 1 | Moyen | ✅ Workaround | `design.yaml` = YAML frontmatter + Markdown body |
| 4 | Regex syntax error | 1 | Faible | ✅ Workaround | Character set `[` non échappé |
| 5 | Schema `depends_on` trop strict | 1 | Élevé | ❌ Bloquant | Pattern exclut `ATOM-<slug>` sans numéro |
| 6 | CLI `--schema` manquant | 1 | Faible | ✅ Workaround | Pas de défaut pour schema courant |
| 7 | `head` inexistant PowerShell | 3 | Faible | ✅ Workaround | Confusion Unix/Windows |
| 8 | Atoms orphelins catalogues | 2 | Élevé | ❌ Bloquant | Pas de sync automatique |

**Verdict TALEX** : ⚠️ Frictions évitables. Corrections structurelles recommandées pour éviter la répétition.

**Évaluation d'utilité TALEX** : Utile pour mémoire collective et onboarding. Complémentaire aux rapports techniques. À conserver dans `REPORTS/`.

## Références

- PRD : `PRD-MOC-ARTIFACT-EXTRACTION-20260920.md`
- ADR : `ADR-2026-09-20-001-ARTIFACT-EXTRACTION-MDU.md`
- MDU : `META-DESIGN.md`
- TALEX : `REPORTS/REPORT-TALEX-FRICTION-SESSION-20260921.md`

---

*Generated by governance-doc-writer skill — Pattern C*
