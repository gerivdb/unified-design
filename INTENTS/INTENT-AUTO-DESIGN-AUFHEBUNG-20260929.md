---
intent_hash: 0xINTENT_AUTO_DESIGN_AUFHEBUNG_20260929
status: exploratory
priority: P1
---

# INTENT — Auto-Design comme Aufhebung et Autonomie de l'Écosystème

> **Contexte** : Cet intent formalise le chemin architectural par lequel `unified-design`, via le concept d'`auto-design` matérialisé par `AUTO-DEV`, établit un motif réplicable d'industrialisation et d'autonomie pour l'ensemble des repos `gerivdb/*`. Il décrit l'Aufhebung comme mécanisme d'annulation de la dépendance humaine centralisée, de conservation des intentions métier, et d'élévation vers l'auto-gouvernance écosystémique.

---

## 1. Conception du Chemin

### 1.1 unified-design = matrice de méta-conception

`unified-design` n'est pas un repo de production. C'est le **dépôt de la méta-conception** :

- Il définit le concept **auto-design** (ONTOLOGY + `design.yaml` + cycle_runner)
- Il matérialise l'**industrialisation** (AUTO-DEV comme premier citoyen)
- Il contient la **recette réplicable** : bridges déclaratifs + agents + tests + docs

C'est un **design pattern rendu exécutable**, pas un document statique.

### 1.2 AUTO-DEV = preuve de concept opérationnelle

AUTO-DEV est le **premier repo à avoir été "aufgehoben"** :

- **Annulation** de la dépendance à une main-d'œuvre humaine centralisée
- **Conservation** de l'intention métier et des bridges déclaratifs existants
- **Élévation** vers un mode où le repo s'industrialise lui-même via `design.yaml` + cycles auto-dev

**Résultat** : 100% opérationnel (51 bridges, 5/5 Scientific Reflection Protocols, 3/3 auto-debug pathways, 2/2 Research Directions actives).

### 1.3 Aufhebung comme mécanisme architectural

L'Aufhebung ici n'est pas seulement philosophique. C'est un mécanisme technique où chaque repo :

1. **Annule** sa dépendance à une intervention humaine centralisée pour rester cohérent
2. **Conserve** son identité métier (PRD, MOC, bridges, citizens)
3. **S'élève** vers un régime auto-gouverné : `design.yaml` déclare l'intention, `cycle_runner.py` exécute la médiation, `bridge_executor.py` vérifie la synchronisation

### 1.4 Réplication = autonomie émergente

La réplication du motif auto-design sur tous les repos produit une **autonomie émergente** :

| Niveau | Rôle |
|--------|------|
| **N+1** (unifié) | `unified-design` définit le motif |
| **N+3** (industrialisé) | `AUTO-DEV` implémente le motif |
| **N+4** (écosystème) | Tous les repos `gerivdb/*` peuvent adopter le motif |

Chaque repo devient alors :
- **Auto-conçu** via son propre `design.yaml`
- **Auto-médiatisé** via ses bridges déclaratifs
- **Auto-validé** via ses tests et preuves d'exécution
- **Auto-synchronisé** via les cycles `cycle_runner.py`

---

## 2. Décision — Fonction Auto-Design

### 2.1 Objectif

Établir `auto-design` comme **fonction native** de l'écosystème, accessible depuis `unified-design`, capable de :

1. **Analyser** un repo cible et détecter sa maturité auto-design
2. **Générer** un `design.yaml` + `implementation_contract` + bridges déclaratifs
3. **Industrialiser** le repo en activant les cycles `cycle_runner.py` + `bridge_executor.py`
4. **Vérifier** l'adhérence au motif et produire un rapport de couverture

### 2.2 Architecture cible

```
unified-design/
├── engine/
│   └── auto_design/
│       ├── __init__.py
│       ├── analyzer.py          # Analyse un repo, score auto-design readiness
│       ├── generator.py         # Génère design.yaml + contracts + bridges
│       ├── industrializer.py    # Déploie cycle_runner.py + bridge_executor.py
│       ├── verifier.py          # Vérifie l'adhérence au motif
│       └── reporter.py          # Rapport de couverture auto-design
├── designs/
│   └── auto-design/
│       ├── design.yaml          # Définition canonique du motif
│       └── implementation_contract.yaml
└── scripts/
    └── auto_design_cli.py       # CLI: auto-design analyze|generate|deploy|verify <repo>
```

### 2.3 Primitives

#### Primitive 1 — `analyzer.py`

**Responsabilité** : évaluer la maturité auto-design d'un repo.

**Mécanisme** :
1. Charger `known_repositories.yaml` pour obtenir le repo cible
2. Vérifier la présence de :
   - `design.yaml` (ou `designs/*/design.yaml`)
   - `bridges/*.yaml`
   - `cycle_runner.py` / `bridge_executor.py`
   - Tests d'intégration (`tests/test_*.py`)
   - Docs (`docs/*.md`, `PRD/*.md`, `MOC/*.md`)
3. Scorer chaque dimension (0-100) :
   - `design_coverage` : % de composants avec `design.yaml`
   - `bridge_density` : nombre de bridges actifs / nombre de composants
   - `test_coverage` : tests présents et passants
   - `doc_coverage` : docs PRESENCE + preuves d'exécution
   - `auto_debug_maturity` : presence de `auto_debug_integrator` + pathways
4. Retourner un score global + recommandations

**Intégration** :
- `powershell -File "C:\DevTools\bin\ecos.ps1" status` peut invoquer `auto_design_cli.py analyze`
- Skill `auto-design-readiness` : wrapper pour l'analyse

#### Primitive 2 — `generator.py`

**Responsabilité** : générer le `design.yaml` + `implementation_contract` + bridges pour un repo non encore auto-designé.

**Mécanisme** :
1. Scanner le repo pour identifier les composants (agents, src, scripts, tests, docs)
2. Pour chaque composant, générer un `design.yaml` minimal avec :
   - `name`, `version`, `status`, `intent_hash`
   - `implementation_contract` (chemins, must_contain, tests)
   - `bridges` (déclaratifs vers les composants partenaires)
3. Générer le `design.yaml` racine du repo avec :
   - `components:` liste des composants
   - `auto_debug_pathways:` (si applicable)
   - `scientific_reflection_protocols:` (si applicable)
4. Générer les `bridges/*.yaml` déclaratifs

**Intégration** :
- `auto_design_cli.py generate <repo>` — dry-run par défaut
- `auto_design_cli.py generate <repo> --apply` — écriture effective

#### Primitive 3 — `industrializer.py`

**Responsabilité** : déployer les runtimes auto-design (`cycle_runner.py`, `bridge_executor.py`, `pr_factory.py`) dans un repo.

**Mécanisme** :
1. Vérifier que `generator.py` a préalablement créé les `design.yaml` + `bridges`
2. Copier les runtimes depuis `unified-design/templates/` vers le repo cible
3. Configurer les chemins dans `design.yaml` (`cycle_runner_path`, `bridge_executor_path`)
4. Ajouter les hooks pre-commit si nécessaire
5. Exécuter un dry-run du cycle pour valider la médiation

**Intégration** :
- `auto_design_cli.py deploy <repo>`
- Après déploiement, exécuter `auto_design_cli.py verify <repo>` pour valider

#### Primitive 4 — `verifier.py`

**Responsabilité** : vérifier l'adhérence d'un repo au motif auto-design.

**Mécanisme** :
1. Charger le `design.yaml` racine du repo
2. Pour chaque `implementation_contract` :
   - Vérifier l'existence des artifacts
   - Vérifier la présence des patterns `must_contain`
   - Vérifier que les tests passent
3. Vérifier que les bridges déclaratifs sont actifs (via `bridge_executor.py --status`)
4. Vérifier que les preuves d'exécution (Proof-of-Life) sont à jour
5. Générer un rapport JSON avec :
   - `auto_design_score` (0-100)
   - `components_verified`, `components_missing`
   - `bridges_active`, `bridges_inactive`
   - `tests_passing`, `tests_failing`
   - `proofs_up_to_date`, `proofs_stale`

**Intégration** :
- `auto_design_cli.py verify <repo>`
- Hook pre-commit : bloque si `auto_design_score < 80` sur un repo `active`

#### Primitive 5 — `reporter.py`

**Responsabilité** : produire un rapport de couverture auto-design pour l'écosystème.

**Mécanisme** :
1. Charger `known_repositories.yaml`
2. Pour chaque repo `active` :
   - Exécuter `verifier.py` (ou lire le cache)
   - Agréger les scores
3. Générer un rapport global :
   - `% repos auto-designés`
   - `% bridges actifs`
   - `% tests passants`
   - `% preuves à jour`
4. Identifier les gaps et proposer des actions (AUTO / SEMI-AUTO / MANUAL)

**Intégration** :
- `auto_design_cli.py report --global`
- Intégré à `ecos.ps1 health` pour afficher le score auto-design par repo

---

## 3. Livrables Atomiques

| ID | Livrable | Chemin cible | Type | Critère d'acceptation |
|---|---|---|---|---|
| L1 | `analyzer.py` | `engine/auto_design/analyzer.py` | Nouveau | Score 5/5 repos test avec rating OK |
| L2 | `generator.py` | `engine/auto_design/generator.py` | Nouveau | Dry-run génère design.yaml + bridges valides |
| L3 | `industrializer.py` | `engine/auto_design/industrializer.py` | Nouveau | Deploy + verify sur repo test = score >= 80 |
| L4 | `verifier.py` | `engine/auto_design/verifier.py` | Nouveau | Verify retourne JSON valide avec scores |
| L5 | `reporter.py` | `engine/auto_design/reporter.py` | Nouveau | Rapport global avec % couverture |
| L6 | `auto_design_cli.py` | `scripts/auto_design_cli.py` | Nouveau | CLI fonctionnelle (analyze, generate, deploy, verify, report) |
| L7 | Templates runtimes | `templates/auto_design/` | Nouveau | cycle_runner.py + bridge_executor.py + pr_factory.py |
| L8 | `design.yaml` canonique | `designs/auto-design/design.yaml` | Modification | Définit le motif avec contracts + bridges |
| L9 | Skill `auto-design-readiness` | `skills/auto-design-readiness/SKILL.md` | Nouveau | Skill documenté et testé |

---

## 4. Plan de Commits (Atomic)

| Commit | Fichiers | Description |
|---|---|---|
| `feat(engine): add auto_design analyzer` | `engine/auto_design/analyzer.py` | Évalue la maturité auto-design d'un repo |
| `feat(engine): add auto_design generator` | `engine/auto_design/generator.py` | Génère design.yaml + contracts + bridges |
| `feat(engine): add auto_design industrializer` | `engine/auto_design/industrializer.py` | Déploie les runtimes auto-design |
| `feat(engine): add auto_design verifier` | `engine/auto_design/verifier.py` | Vérifie l'adhérence au motif |
| `feat(engine): add auto_design reporter` | `engine/auto_design/reporter.py` | Rapport de couverture global |
| `feat(scripts): add auto_design_cli` | `scripts/auto_design_cli.py` | CLI unifiée pour auto-design |
| `feat(templates): add auto_design runtimes` | `templates/auto_design/*.py` | Templates cycle_runner + bridge_executor + pr_factory |
| `docs(design): update auto-design design.yaml` | `designs/auto-design/design.yaml` | Définit le motif canonique |
| `docs(skill): add auto-design-readiness` | `skills/auto-design-readiness/SKILL.md` | Skill d'analyse de maturité auto-design |

---

## 5. Critères d'Acceptation

1. **Analyse** : `auto_design_cli.py analyze <repo>` retourne un score 0-100 avec breakdown par dimension
2. **Génération** : `auto_design_cli.py generate <repo> --dry-run` génère un `design.yaml` valide + bridges pour 100% des composants détectés
3. **Déploiement** : `auto_design_cli.py deploy <repo>` copie les runtimes et configure le repo sans erreur
4. **Vérification** : `auto_design_cli.py verify <repo>` retourne `auto_design_score >= 80` pour AUTO-DEV (repo déjà industrialisé)
5. **Rapport** : `auto_design_cli.py report --global` couvre 100% des repos `active` de `known_repositories.yaml`
6. **Ontologie** : les termes `auto-design`, `auto-industrialisation`, `Aufhebung`, `design.yaml`, `cycle_runner` sont présents dans `ONTOLOGY/`
7. **Preuve d'exécution** : dry-run complet sur AUTO-DEV + un repo L4 (ex: VEX) horodaté dans Proof-of-Life

---

## 6. Références

- **Repo source** : `gerivdb/unified-design`
- **Repo PoC** : `gerivdb/AUTO-DEV` (100% opérationnel)
- **Concept** : `ONTOLOGY/concepts/core/auto-design.md`
- **Déclaration** : `ONTOLOGY_DECLARATION.yaml`
- **Design canonique** : `designs/auto-design/design.yaml`
- **PRD backing** : `PRD/PRD-020-auto-dev-ecosystem-full-integration.md`
- **MOC backing** : `MOC/MOC-020-auto-dev-ecosystem-full-integration.md`
- **ADR backing** : `ADR/ADR-2026-09-29-auto-design-aufhebung.md` (à créer)

---

## 8. Référence ADR

- **ADR** : `ADR/ADR-2026-09-29-auto-design-aufhebung.md` (à créer)
- **IntentHash** : `0xADR_AUTO_DESIGN_AUFHEBUNG_20260929`
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded

---

## 9. Proof-of-Life

- [x] 2026-09-29T03:12:37+02:00 — INTENT créé, chemin architectural formalisé
- [x] 2026-09-29T03:16:00+02:00 — 19 stubs ONTOLOGY créés, gate ontologique --strict passée (0 ABSENT)
- [ ] `analyzer.py` — test sur AUTO-DEV + VEX
- [ ] `generator.py` — dry-run sur repo L4
- [ ] `industrializer.py` — déploiement sur repo test
- [ ] `verifier.py` — vérification AUTO-DEV score >= 80
- [ ] `reporter.py` — rapport global exécuté
- [ ] ADR backing — créé et approuvé
