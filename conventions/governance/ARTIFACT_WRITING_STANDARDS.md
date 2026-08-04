---
type: CONVENTION
version: "1.0.0"
status: active
date: "2026-08-05"
intent_hash: 0xCONVENTION_ARTIFACT_WRITING_STANDARDS_20260805
citizen: "L2-PLATFORM"
layer: "L4"
author: gerivdb
source_repo: gerivdb/unified-design
source_path: conventions/governance/ARTIFACT_WRITING_STANDARDS.md
---

# ARTIFACT WRITING STANDARDS - Conventions de redaction

## Objectif

Traduire les principes conceptuels `unified-design` en normes de redaction concretes pour tous les artefacts de gouvernance : `PRD`, `ADR`, `EPIC`, `INTENT`, `SPEC`, `REPORT`, `RPT`, `GUI`, `RUN`.

## Principes operationnalises

| Principe conceptuel | Norme de redaction |
|---------------------|--------------------|
| SRP | 1 artefact = 1 sujet |
| OCP | Sections extensibles sans rupture |
| LSP | Sous-typages conformes au template parent |
| ISP | Sections optionnelles explicites |
| DIP | References explicites, pas de couplage implicite |
| DRY | 1 information = 1 occurrence |
| KISS | Sections courtes, vocabulaire simple |
| YAGNI | Pas de section "futur" non justifiee |
| LoD | References ciblees, pas de digressions |
| Least Astonishment | Ordre des sections conforme au template |
| Convention over Configuration | Structure standard prioritaire sur variations |
| Stratified Abstraction | Detail croissant par strate L0..L4 |

## Structure obligatoire

Tout artefact de gouvernance doit contenir :

| Section | Contenu obligatoire | Critere mesurable |
|---------|---------------------|-------------------|
| Frontmatter | YAML valide | Schema `intent_frontmatter.json` |
| Objectif | 1 phrase + 1 liste | <= 3 lignes + <= 5 items |
| Contexte | Probleme + etat actuel | <= 10 lignes |
| Perimetre | In/Out explicites | >= 1 IN, >= 1 OUT |
| Architecture | DAG ASCII ou diagramme | Present, lisible en terminal |
| Regles | Numerotees ou ASCII | Chaque regle = 1 cause/effet |
| Roles | 1 section par acteur | Chaque acteur = 1 responsabilite |
| Processus | Etapes numerotees | >= 2 etapes, <= 10 etapes |
| Probes | Table ASCII P-xxx | Chaque probe = condition -> comportement |
| Criteres | Table ASCII | Tous les items verifiables |
| Rollback | Etapes numerotees | >= 1 etape |
| References | Liens explicites | >= 1 reference par artefact cite |

## Regles de clarte

1. Phrases courtes : <= 20 mots par phrase.
2. Sections courtes : <= 15 lignes par section hors tableaux.
3. Un sujet par section : pas de section "Divers" ou "Autres".
4. Listes numerotees pour les sequences : ordre, etapes, flux.
5. Listes a puces pour les enumerations : items independants.
6. Tableaux ASCII obligatoires pour les mappings, matrices, probes, criteres.
7. Pas de paragraphe > 5 lignes sans sous-section.
8. Pas de digression : toute information non liee au sujet de l'artefact est rejetee par `MOX`.
9. Vocabulaire simple : eviter le jargon non defini dans `ONTOLOGY/`.
10. References croisees explicites : pas de "voir ADR" sans numero ni chemin.

## Anti-patterns bloquants

| Anti-pattern | Norme a appliquer |
|--------------|-------------------|
| Section "Divers" / "Autres" | Supprimer ou creer un artefact dedie |
| Paragraphe > 10 lignes | Decouper en sous-sections |
| Phrase > 30 mots | Reformuler en 2 phrases |
| Pas de tableau pour les probes | Table ASCII P-xxx obligatoire |
| Reference sans chemin | Chemin absolu ou IntentHash |
| Digression cross-artefact sans lien | `MOX` rejette, `ARGUS` signale |
| Duplication d'information | Reference unique + lien |
| Liste a puces > 8 items | Decouper en 2 tableaux ou sections |
| Pas de frontmatter | Rejet par RSS-v2.3 |
| Pas de section Rollback | Rejet par `MOX` |

## Probes de redaction

| Probe | Condition -> Comportement attendu |
|-------|----------------------------------|
| P-101 | Longueur moyenne phrase <= 20 mots |
| P-102 | Longueur max section <= 15 lignes |
| P-103 | Items par liste a puces <= 8 items |
| P-104 | >= 1 tableau ASCII par section donnees/processus |
| P-105 | >= 1 reference explicite par section reference |
| P-106 | Frontmatter valide selon `intent_frontmatter.json` |
| P-107 | Toutes les sections obligatoires presentes |
| P-108 | 0 digression cross-artefact sans lien detectee |
| P-109 | 0 duplication d'information detectee |

## References

- `unified-design/atoms/kiss.yaml`
- `unified-design/atoms/srp.yaml`
- `unified-design/atoms/dip.yaml`
- `unified-design/atoms/yagni.yaml`
- `unified-design/atoms/law-of-demeter.yaml`
- `unified-design/atoms/principle-of-least-astonishment.yaml`
- `unified-design/atoms/stratified-abstraction.yaml`
- `unified-design/atoms/convention-over-configuration.yaml`
- `REPO-STANDARDS/docs/RSS-v2.md`
- `REPO-STANDARDS/schemas/intent_frontmatter.json`
- `PRD MOC N243 - Artifact Writing Standards : act-protocol/PRD/PRD-MOC-N243-ARTIFACT-WRITING-STANDARDS-2026-08-05.md`
