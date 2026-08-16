---
type: PRD
version: "1.1"
date: "2026-08-16"
status: draft
intent_hash: 0xPRD_MOC_MDU_GAPS_20260816
---

# PRD MOC -- Meta-Design Gaps Minimum Obligatory Contract

## Contexte

Le **Meta-Design Atlas (MDU v2.1.0)** de `unified-design` couvre bien l'observabilité (SDD), l'orchestration (TCE), l'optimisation matérielle (MAG) et le contrôle qualité (CD).  
Cependant, une analyse au filtre des 11 principes logiciels révèle **4 lacunes structurelles** qui génèrent de l'inflation, du couplage fort et des risques d'over-engineering.

Ce PRD définit le **Minimum Obligatory Contract (MOC)** à intégrer dans le MDU pour combler ces lacunes sans sur-spécification.

---

## Amélioration de l'analyse -- 4 lacunes confirmées et quantifiées

### 1. YAGNI (Principe 4) -- Inflation Méta-Ontologique

**Constat MDU :**
- `meta-design.yaml` ajoute 6 nouvelles capacités "Graph of Loops" (L1-L6) sans traçage de consommation dans `META-DESIGN.md` ni dans `atoms_registry.yaml`.
- `couche_gouvernance` liste 123 entrées réparties en L0-L4, mais aucune colonne `consumers`, `status` ou `last_used` n'existe.
- `META-DESIGN.md` recense 13 atomes L0-CANON et 1 design enregistré (`moc-governance`), sans mécanisme de rétention ou de suppression.

**Angle mort :** Aucun garde-fou ne vérifie qu'un atome/capacité/design est consommé avant d'être maintenu dans le MDU.

**Risque :** Formalisme spéculatif, dette documentaire, divergence MDU vs implémentation.

---

### 2. OCP (Principe 6) -- Registres Centraux Statiques

**Constat MDU :**
- `meta-design.yaml` stocke `designs:` en tableau codé en dur (1 seul design enregistré).
- `piliers:` est un tableau YAML statique dans `meta-design.yaml`.
- `agents_par_pilier:` associe des noms de repos à des piliers sans abstraction d'interface.
- L'ajout d'un atome nécessite une édition manuelle dans `meta-design.yaml` ET `META-DESIGN.md`.

**Angle mort :** Le MDU n'est pas "Open to extension, Closed to modification". Toute extension touche à des fichiers centraux.

**Risque :** Frictions de contribution, merge conflicts sur `meta-design.yaml`, oublis de synchronisation.

---

### 3. DIP (Principe 7) -- Couplage fort Inter-Strates

**Constat MDU :**
- `capabilities` référence des implémentations concrètes : `protocol: "MCP"`, `storage_backend: "sqlite+wal"`, `validator_model: "openai-codex"`.
- `agents_par_pilier:` liste des noms de repos concrets (`NEXUS`, `FLUENCE`, `PIANO`, etc.) sans contrat abstrait.
- `design_rules` contient des checks nommés (ex: `mcp_symbol_access_required`) couplés à un protocole spécifique.

**Angle mort :** Absence de ports/adapters entre L0-CANON et les strates L1-L4. Une couche supérieure ne dépend pas d'abstractions mais d'implémentations.

**Risque :** Impossible de remplacer un composant (ex: passer de `sqlite+wal` à `postgres`) sans toucher au MDU canonique.

---

### 4. KISS (Principe 3) -- Absence de Métrique de Complexité Cognitive

**Constat MDU :**
- `connard-validator` vérifie : `inheritance_depth <= 3`, `latency_p99 <= 45ms`, `power_w <= 12W`.
- Aucun seuil sur la **taille des designs** (nombre de capabilities, nombre de champs).
- Aucun seuil sur la **complexité cyclomatique** des atomes.
- Aucune limite de profondeur d'héritage multiple dans `design_rules`.

**Angle mort :** Un design peut être valide aux tests CD tout en étant cognitivement ingérable (100+ lignes, 10+ capabilities, héritage en cascade).

**Risque :** Designs-monstres, courbe d'apprentissage abrupte, résistance au changement.

---

## Minimum Obligatory Contract (MOC)

### Règle MOC-1 -- YAGNI Gate (Atomes et Capacités)

**Obligation :** Tout atome, capacité ou design ajouté dans `meta-design.yaml` ou `META-DESIGN.md` doit avoir **au moins un consommateur identifié** dans l'écosystème avant d'être promu en `status: active`.

**Application :**
- Ajouter un champ obligatoire `consumers: []` (liste de repo/design IDs) dans chaque entrée d'atome/capacité/design.
- Ajouter un champ `profile: CRITICAL | STANDARD | EXPERIMENTAL` pour qualifier la criticité de l'artefact.
  - `profile: CRITICAL` : l'absence de consommateur déclenche une **alerte HITL**, pas une dépréciation automatique.
  - `profile: STANDARD` : règle par défaut -- dépréciation automatique après 30 jours sans consommateur.
  - `profile: EXPERIMENTAL` : dépréciation automatique après **7 jours** sans consommateur.
- Si `consumers` est vide pendant la durée configurée par `profile`, l'artefact passe en `status: deprecated` (soft-delete).
- `designs:` dans `meta-design.yaml` doit pointer vers un `designs/*.yaml` existant et consommé.

**Impact MDU :**
- `meta-design.yaml` -> ajout champ `consumers` sous chaque capability et design.
- `META-DESIGN.md` -> section "Atoms catalogues" complétée par une colonne `Consommateurs`.
- `atoms_registry.yaml` -> ajout champ `consumers` et `last_verified`.

---

### Règle MOC-2 -- OCP / Auto-Découverte des Atomes

**Obligation :** L'ajout d'un atome ou d'un design ne doit **pas nécessiter d'édition manuelle** de `meta-design.yaml` ou `META-DESIGN.md`.

**Application :**
- Chaque atome dispose d'un manifest local `.atom.yaml` à la racine de son dossier (ou dans `atoms/`).
- `meta-design.yaml` devient **généré** à partir d'un scan de ces manifests (pas de tableau codé en dur).
- `META-DESIGN.md` est régénéré lors du build via un script `tools/meta-design-gen.py`.
- `meta-design.yaml` doit inclure un header explicite en en-tête de fichier :
  ```yaml
  # AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY
  # Source: manifests .atom.yaml + tools/meta-design-gen.py
  # Regenerate: python tools/meta-design-gen.py
  ```
- Ajouter un check CI `verify-meta-design-sync` qui échoue si `meta-design.yaml` commité diffère du résultat produit par `python tools/meta-design-gen.py`.

**Impact MDU :**
- Suppression du tableau `designs:` codé en dur -> remplacé par un scan du répertoire `designs/`.
- Suppression du tableau `piliers:` codé en dur -> chargé depuis `piliers/*.yaml`.
- Ajout d'un script de génération dans `tools/` (hors scope MDU canonique, mais documenté dans ADR dédié).

---

### Règle MOC-3 -- DIP / Ports & Adapters Inter-Strates

**Obligation :** Les strates supérieures (L1-L4) ne doivent pas importer de structures concrètes définies dans `meta-design.yaml` ou `META-DESIGN.md`. Elles dépendent uniquement d'abstractions (ports) définies dans L0-CANON.

**Application :**
- Créer un répertoire `ports/` dans L0-CANON contenant les contrats abstraits (schemas JSON Schema ou interfaces YAML).
- Chaque port doit spécifier un **contrat formel** avec schémas d'entrée/sortie :
  ```yaml
  port_id: symbol-retrieval
  contract:
    input_schema: schemas/ports/symbol_retrieval_input.json
    output_schema: schemas/ports/symbol_retrieval_output.json
  ```
- `capabilities` dans `meta-design.yaml` référence un `port_id` (ex: `port: symbol-retrieval`) au lieu d'une implémentation.
- Les implémentations concrètes (ex: `MCP`, `sqlite+wal`) sont décrites dans des `adapters/*.yaml` par strate, pas dans le MDU canonique.

**Impact MDU :**
- `meta-design.yaml` -> `capabilities` devient une liste de `port_id` + paramètres abstraits.
- Ajout d'un registre `ports/registry.yaml` dans L0-CANON.
- `design_rules` référence des `port_id` au lieu de noms d'implémentation.

---

### Règle MOC-4 -- KISS Gate (Complexité Cognitive)

**Obligation :** Tout design ou atome validé par `gerivdb design validate` doit respecter des seuils de complexité cognitive.

**Application :**
- Ajout de checks dans `connard-validator` :
  - `cognitive_complexity <= 15` (par design/atome)
  - `max_capabilities_per_design <= 8`
  - `max_rules_per_atom <= 10`
  - `max_nesting_depth <= 3` (profondeur d'héritage multiple et imbrication YAML)
- `design_rules` dans `meta-design.yaml` se voit ajouter une section `complexity_gates`.
- **Règle d'interprétation** : les seuils sont sémantiques, pas de limitation artificielle du nombre de lignes. Un design de 210 lignes avec 3 capabilities et 5 règles reste valide si ses métriques de complexité sont conformes.

**Impact MDU :**
- `meta-design.yaml` -> ajout section `complexity_gates`.
- `META-DESIGN.md` -> section "Validation" complétée par les nouveaux checks.
- `connard-validator` -> implémentation des 4 nouveaux checks (hors scope MDU, à adresser dans PRD/PRD dédié).

---

## Plan d'implémentation (MOC -- ordre d'exécution)

| Priorité | Règle | Fichiers MDU modifiés | Effort | Risque |
|----------|-------|----------------------|--------|--------|
| P1 | MOC-1 YAGNI Gate | `meta-design.yaml`, `META-DESIGN.md` | 1h | Faible (ajout de champs + profile) |
| P1 | MOC-4 KISS Gate | `meta-design.yaml`, `META-DESIGN.md` | 1h | Faible (seuils sémantiques) |
| P2 | MOC-3 DIP / Ports | `meta-design.yaml`, nouveau `ports/registry.yaml`, `schemas/ports/*.json` | 2h | Moyen (refactor capabilities + contrats formels) |
| P3 | MOC-2 OCP / Auto-découverte | `meta-design.yaml`, `tools/meta-design-gen.py`, `.atom.yaml` manifests | 3h | Élevé (breaking change schema + header auto-generated + CI check) |

---

## Critères d'acceptation

- [ ] `meta-design.yaml` passe validation YAML + JSON Schema sans erreur.
- [ ] Chaque `capability` et `design` possède un champ `consumers` non vide (ou `status: proposed`) ET un `profile` valide (`CRITICAL | STANDARD | EXPERIMENTAL`).
- [ ] `connard-validator` intègre les 4 checks de complexité cognitive : `cognitive_complexity`, `max_capabilities_per_design`, `max_rules_per_atom`, `max_nesting_depth`.
- [ ] Chaque port dans `ports/` possède un contrat formel avec `input_schema` et `output_schema` référencés.
- [ ] `meta-design.yaml` commence par le header `# AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY` et le check CI `verify-meta-design-sync` passe.
- [ ] Aucune dépendance de L1-L4 vers des structures concrètes de L0-CANON hors `ports/`.
- [ ] `META-DESIGN.md` mentionne les 4 garde-fous MOC dans la section "Validation".

---

## Hors scope

- Implémentation complète du script `tools/meta-design-gen.py` et du header auto-généré (hors scope MDU, voir PRD dédié).
- Migration des 123 entrées de `couche_gouvernance` vers le nouveau format (travail long, à planifier).
- Refactor complet de `atoms_registry.yaml` (hors scope, voir PR existant `PRD-UNIFIED-DESIGN-GOVERNANCE-GAPS-2026-08-16.md`).
- Implémentation des checks `connard-validator` (hors scope MDU, à adresser dans PRD/PRD dédié).
- Création des schemas JSON pour `ports/*` (hors scope MDU, documenté ici comme exigence de contrat).

---

## Documentation de référence

- `META-DESIGN.md` -- Atlas MDU v2.1.0
- `meta-design.yaml` -- Schema de validation YAML
- `PRD-UNIFIED-DESIGN-GOVERNANCE-GAPS-2026-08-16.md` -- PRD existant sur les gaps de gouvernance
- ADR-013 -- Meta-Design Validation Protocol
- ADR-016 -- Unified Design Loop Detection Engine
- ADR-CONNARD-001 -- Connard Design Protocol

---

## Référence ADR

- **ADR** : ADR-2026-07-15-001-MDU-L1-INFRA-EXTENSION
- **IntentHash** : 0xMDU_L1_INFRA_EXT_20260715
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed



