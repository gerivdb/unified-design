# ARTIFACT WRITING STANDARDS

## Objectif

Traduire les principes conceptuels de conception (SOLID, DRY, KISS, SRP, DIP, YAGNI, LoD, Least Astonishment, Stratified Abstraction, Convention over Configuration) en normes de redaction artefactuelles mesurables pour PRD, ADR, EPIC, INTENT, SPEC, REPORT, RPT, GUI, RUN.

Ce document definit **comment** ecrire les artefacts, pas **quoi** ecrire.

## Principes operationnalises

| PRINCIPE CONCEPTUEL   | NORME DE REDACTION MESURABLE                        |
|----------------------|-----------------------------------------------------|
| SRP                  | 1 artefact = 1 sujet                                |
| OCP                  | Sections extensibles sans rupture                   |
| LSP                  | Sous-typages conformes au template parent           |
| ISP                  | Sections optionnelles explicites                    |
| DIP                  | References explicites, pas de couplage              |
| DRY                  | Une information = 1 occurrence                      |
| KISS                 | Sections courtes, vocabulaire simple               |
| YAGNI                | Pas de section "futur" non justifiee               |
| LoD                  | References ciblees, pas de digressions             |
| Least Astonishment   | Ordre des sections conforme au template             |
| Convention over Config | Structure standard prioritaire sur variations     |
| Stratified Abstraction | Detail croissant par strate (L0..L4)              |

## Standards de redaction mesurables

### Structure obligatoire

Tout artefact de gouvernance doit respecter la structure suivante :

| SECTION       | CONTENU OBLIGATOIRE       | CRITERE MESURABLE                    |
|---------------|---------------------------|--------------------------------------|
| Frontmatter   | YAML valide               | Schema artifact-quality.schema.yaml  |
| Objectif      | 1 phrase + 1 liste        | <= 3 lignes + <= 5 items             |
| Contexte      | Probleme + etat actuel    | <= 10 lignes                         |
| Perimetre     | In/Out explicites         | >= 1 entree IN, >= 1 entree OUT     |
| Architecture  | DAG ASCII ou diagramme    | Present, lisible en terminal         |
| Regles        | Numerotees ou ASCII       | Chaque regle = 1 cause/effet         |
| Roles          | 1 section par acteur      | Chaque acteur = 1 responsabilite     |
| Processus     | Etapes numerotees         | >= 2 etapes, <= 10 etapes           |
| Probes        | Table ASCII P-xxx         | Chaque probe = condition -> comportement|
| Criteres      | Table ASCII               | Tous les items verifiables            |
| Rollback      | Etapes numerotees         | >= 1 etape                           |
| References    | Liens explicites          | >= 1 reference par artefact cite     |

### Regles de clarte

1. Phrases courtes : <= 20 mots par phrase.
2. Sections courtes : <= 15 lignes par section hors tableaux.
3. Un sujet par section : pas de section "Divers" ou "Autres".
4. Listes numerotees pour les sequences : ordre, etapes, flux.
5. Listes a puces pour les enuerations : items independants.
6. Tableaux ASCII obligatoires pour les mappings, matrices, probes, criteres.
7. Pas de paragraphe > 5 lignes sans sous-section.
8. Pas de digression : toute information non liee au sujet de l'artefact est rejetee par MOX.
9. Vocabulaire simple : eviter le jargon non defini dans ONTOLOGY.
10. References croisees explicites : pas de "voir ADR" sans numero ni chemin.

### Anti-patterns bloquants

| ANTI-PATTERN                    | NORME a APPLIQUER                         |
|---------------------------------|-------------------------------------------|
| Section "Divers" / "Autres"     | Supprimer ou creer un artefact dedie       |
| Paragraphe > 10 lignes          | Decouper en sous-sections                  |
| Phrase > 30 mots                | Reformuler en 2 phrases                    |
| Pas de tableau pour les probes  | Table ASCII P-xxx obligatoire              |
| Reference sans chemin           | Chemin absolu ou IntentHash                |
| Digression cross-artefact sans lien | MOX rejette, ARGUS signale           |
| Duplication d'information       | Reference unique + lien                   |
| Liste a puces > 8 items         | Decouper en 2 tableaux ou sections        |
| Pas de frontmatter              | Rejet par RSS-v2.3                        |
| Pas de section Rollback         | Rejet par MOX                             |

### Criteres de clarte mesurables

| CRITeRE                  | SEUIL         | MeTHODE DE VeRIFICATION              |
|--------------------------|---------------|---------------------------------------|
| Longueur moyenne phrase  | <= 20 mots    | Probe P-101 : analyse statique        |
| Longueur max section     | <= 15 lignes  | Probe P-102 : analyse statique        |
| Items par liste a puces  | <= 8 items    | Probe P-103 : analyse statique        |
| Tableaux ASCII obligatoires | >= 1 par section donnees/processus | Probe P-104 : verification presence |
| References explicites    | >= 1 par section reference | Probe P-105 : verification chemins + IntentHash |
| Frontmatter valide       | 100%         | Probe P-106 : schema JSON            |
| Sections obligatoires    | 100%         | Probe P-107 : verification presence  |
| Pas de digression        | 0 detectee   | Probe P-108 : ARGUS cross-check      |
| Duplication information  | 0 detectee   | Probe P-109 : MOX scan               |

## Integration RSS-v2.3

Ce document complete `REPO-STANDARDS/docs/RSS-v2.md` :

| RSS-v2.3 | Ce document |
|----------|-------------|
| Structure des repos | Structure des **artefacts** |
| Nommage des fichiers | Nommage des **sections** |
| Profondeur interne | **Longueur** des sections |
| Dossiers obligatoires | **Sections** obligatoires |
| Schemas YAML/JSON | **Schemas de redaction** |

**Nouvelle regle RSS-v2.3 ?11 ? Redaction artefactuelle** :
> Tout artefact de gouvernance doit respecter les standards definis dans `ARTIFACT_WRITING_STANDARDS`. Toute non-conformite est detectee par MOX et loggee dans WAL.

## Probes de redaction

| PROBE | CONDITION -> COMPORTEMENT ATTENDU |
|-------|----------------------------------|
| P-101 | Longueur moyenne phrase <= 20 mots |
| P-102 | Longueur max section <= 15 lignes |
| P-103 | Items par liste a puces <= 8 items |
| P-104 | >= 1 tableau ASCII par section donnees/processus |
| P-105 | >= 1 reference explicite par section reference |
| P-106 | Frontmatter valide selon artifact-quality.schema.yaml |
| P-107 | Toutes les sections obligatoires presentes |
| P-108 | 0 digression cross-artefact sans lien detectee |
| P-109 | 0 duplication d'information detectee |

## Rollback

1. Revenir aux principes `unified-design/atoms/` existants.
2. Logger le gap dans WAL.
3. Mettre a jour ce document.

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
- `ONTOLOGY/ONTOLOGY.yaml`

## Frontmatter minimal (U-M4 -- 2026-08-23)

Tout artefact de gouvernance porte un frontmatter conforme (Axiome 9) :

```yaml
---
type: <PRD|PRD-MOC|ADR|EPIC|INTENT|SPEC>
category: <general|act-protocol|env2|...>
status: <proposed|active|deprecated|archived|completed|draft|approved>
date: YYYY-MM-DD
intent_hash: 0x...   # recommande, optionnel a la creation
---
```

Le chemin de l'artefact est deduit du frontmatter. Tout ecart est signale par le script
de validation du depot hote (check-prd-structure.ps1 ou equivalent ARGUS).
