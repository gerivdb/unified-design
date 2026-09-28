---
type: INTENT
version: "1.0.0"
date: "2026-09-27"
status: approved
intent_hash: 0xINTENT_UNIFIED_DESIGN_METACOHERENCE_AUTOMATION_20260927
parent_prd: PRD-MOC-VEX-HTTP-SERVER-20260927.md
repo: "gerivdb/unified-design"
layer: "L0"
author: gerivdb
source_repo: gerivdb/unified-design
source_path: INTENTS/INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md
---

# INTENT — Unified-Design Métacohérence Automatisée et Gap-Comblé-ification

> **Contexte** : Cet intent synthétise l'analyse causale/structurale du repo `unified-design` et propose un système d'automatisation de la métacoherence des designs, leur application effective, et leur vérification fonctionnelle. Il documente les lacunes identifiées, les causes racines, la mécanique proposée, et le plan de gap-comblé-ification pour transformer le catalogue passif de designs en système actif vérifiable.

---

## 1. Contexte & Motivation

### 1.1 État observé — unified-design est un catalogue passif

Le repo `unified-design` (L0-CANON) est le **dépositaire unique** de tous les designs architecturaux de l'écosystème gerivdb. Il contient :

- **148 designs** actifs dans `designs/`
- **392 atoms** dans `atoms/`
- **5053 fichiers** au total
- **Scripts de validation** : `validate_designs.py`, `design_coverage_scanner.py`, `compliance_scanner.py`, `engine/validator.py`

**Problème fondamental** : tous ces validateurs vérifient uniquement la **syntaxe et la présence** des fichiers, jamais l'**implémentation effective** dans les repos cibles.

### 1.2 Gouvernance violée — designs orphelins

| Violation | Constat | Impact |
|-----------|---------|--------|
| **Designs locaux interdits** | VEX possède 9 designs dans `design/` local (`http-server-design.md`, `client-architecture.md`, etc.) qui n'existent pas dans unified-design | Duplication de canonicalité, drift, impossible à vérifier |
| **ADR manquantes** | 123/133 designs sans ADR backing (audit 2026-09-23) | Décisions non tracées, impossibilité d'auditer |
| **intent_hash manquant** | 7 designs sans `intent_hash` valide | Impossible de référencer mécaniquement |
| **Status draft non résolus** | 8 designs en `draft` sans chemin de promotion | Blocage structurel |
| **Bridges déclarés mais non vérifiés** | Les designs déclarent des `bridges` vers des repos cibles, mais aucun script ne valide l'implémentation | Designs orphelins, jamais appliqués |

### 1.3 Métacoherence déclarée mais non mécanisée

Les designs `ecosystem-meta-coherence` et `ecosystem-meta-coherence-gate` existent et formalisent les états THINK/DO/CHECK, mais :

- Aucune primitive Python n'existe pour les appliquer
- Aucun hook pre-commit ne les invoque
- Aucun skill ne les implémente
- Aucune vérification automatique ne confirme que les invariants sont respectés

**Résultat** : la métacoherence est un **document statique**, pas un mécanisme actif.

### 1.4 Application réelle des designs — zone blanche

Les designs déclarent des `capabilities` et `functions` mais sans :

- **Contrat d'implémentation vérifiable** : pas de `implementation_contract` avec chemins de fichiers, patterns obligatoires, tests associés
- **Métrique de couverture design→code** : impossible de savoir quel % du design est implémenté
- **Vérification automatique** : aucun script ne compare le design déclaré au code réel

**Exemple concret** : le design `strata-orchestrator-assignment` (L0) déclare un contrat d'interface pour les orchestrateurs de strate (L0→L4) avec endpoints `/health`, `/status`, `/start`, `/stop`, `/deploy`, `/metrics`, `/load`. Aucun script ne vérifie que VEX, KIX, N243, etc. exposent bien ces endpoints.

---

## 2. Lacunes causales/structurales identifiées

### 2.1 CR-1 — Validation syntaxique ≠ vérification sémantique

**Cause racine** : les validateurs actuels vérifient la structure des fichiers YAML, pas l'existence des artefacts concrets dans les repos cibles.

**Preuve** :
- `validate_designs.py` : vérifie `name`, `version`, `status`, `intent_hash` — ne lit pas le code
- `engine/validator.py` : valide `depends_on`, `inherits`, `bridges` — ne vérifie pas l'implémentation
- `design_coverage_scanner.py` : vérifie la présence des designs dans `designs/` — ne vérifie pas qu'ils sont codés

### 2.2 CR-2 — Catalogue auto-généré sans boucle de retour

**Cause racine** : `catalog/designs.index.yaml` est auto-généré mais ne contient aucune métrique d'implémentation.

**Preuve** : pas de champs `implemented`, `coverage_pct`, `last_verified_commit`, `impl_paths`.

### 2.3 CR-3 — Designs orphelins entre unified-design et les repos

**Cause racine** : les repos créent leurs designs localement au lieu de les déclarer dans unified-design.

**Preuve** : VEX a 9 designs dans `VEX/design/` qui violent `DESIGNS_GOVERNANCE.md`.

### 2.4 CR-4 — Absence de contrat d'implémentation vérifiable

**Cause racine** : les designs déclarent des capabilities sans pattern de nommage obligatoire, tests d'acceptation, ou métrique de couverture.

**Preuve** : aucun design ne contient de section `implementation_contract`.

### 2.5 CR-5 — Métacoherence déclarée mais pas mécanique

**Cause racine** : le design `ecosystem-meta-coherence-gate` existe mais n'a pas de primitive, de skill, ou de hook pre-commit actif.

**Preuve** : `grep -r "ecosystem-meta-coherence-gate" scripts/ skills/ .kilocode/` dans unified-design → aucun résultat.

---

## 3. Décision — Système d'automatisation métacoherence + gap-comblé-ification

### 3.1 Objectif

Transformer `unified-design` d'un **catalogue passif** en **système actif vérifiable** où :
- Tout design `active` a un contrat d'implémentation vérifiable
- Tout écart design→code est automatiquement détecté
- Toute correction est tracée causalement (friction → root cause → fix → preuve)
- La métacoherence est enforced mécaniquement, pas seulement déclarée

### 3.2 Architecture cible

```
unified-design/
├── designs/<name>/
│   ├── design.yaml              # + champ OBLIGATOIRE `implementation_contract`
│   └── implementation_contract:
│       repo: gerivdb/VEX
│       artifacts:
│         - path: src/vex/http_server.py
│           must_contain:
│             - "class VEXHealthHandler"
│             - "def do_GET"
│           tests:
│             - tests/test_http_server.py::test_http_server_health_endpoint
│       verification:
│         - command: python -m pytest tests/test_http_server.py -q
│         - expected: "3 passed"
│
├── scripts/
│   ├── design_impl_verifier.py   # NOUVEAU — vérifie l'implémentation
│   ├── metacoherence_gate.py     # NOUVEAU — applique ecosystem-meta-coherence-gate
│   ├── gap_combleur.py           # NOUVEAU — automatise le gap-comblé-ification
│   └── validate_designs.py       # EXISTANT — étendre avec vérification impl
│
├── .kilocode/
│   └── hooks/
│       └── pre-commit-design-verifier.py  # NOUVEAU — bloque si impl manquante
│
└── catalog/
    └── designs.index.yaml        # + champs `implemented`, `coverage_pct`, `last_verified`
```

### 3.3 Primitive 1 — `design_impl_verifier.py`

**Responsabilité** : vérifier qu'un design est effectivement implémenté dans le(s) repo(s) cibles.

**Mécanisme** :
1. Charger `design.yaml` + `implementation_contract`
2. Pour chaque artifact listé :
   - Vérifier que le fichier existe dans le repo cible
   - Vérifier qu'il contient les patterns/mots-clés obligatoires (`must_contain`)
   - Vérifier que les tests associés existent et passent
3. Générer un rapport JSON avec `implemented`, `coverage_pct`, `artifacts_verified`, `artifacts_missing`, `tests_passing`

**Intégration** :
- Hook pre-commit : bloque le commit si `implemented: false` sur un design `active`
- CI locale : `python scripts/design_impl_verifier.py --strict`
- PRD-MOC proof-of-life : lecture automatique du rapport

### 3.4 Primitive 2 — `metacoherence_gate.py`

**Responsabilité** : appliquer le design `ecosystem-meta-coherence-gate` mécaniquement.

**Mécanisme** :
```
IDLE → AUDIT → PASS → PROGRESS → BILAN → ENREGISTRER
```

- **IDLE** : détecter si une mutation du MDU est nécessaire
- **AUDIT** : vérifier les invariants Think/Do/Check
  - THINK : les besoins écosystémiques sont-ils documentés ?
  - DO : les mutations sont-elles tracées ?
  - CHECK : les preuves horodatées sont-elles présentes ?
- **PASS/FAIL** : autoriser ou bloquer la mutation
- **ENREGISTRER** : horodater la décision dans VOLTX + KG-CAUSAL

**Intégration** :
- Hook pre-commit sur unified-design : bloque tout commit qui passe AUDIT sans preuve
- Skill `mdu-integrity-checker` : invoqué avant toute mutation du MDU
- Workflow `mdu-validation` : étape obligatoire dans tout PR touchant unified-design

### 3.5 Primitive 3 — `gap_combleur.py`

**Responsabilité** : automatiser le gap-comblé-ification = transformer un gap design→code en implémentation atomique.

**Mécanisme** :
1. Exécuter `design_impl_verifier.py` sur tous les designs `active`
2. Identifier les gaps :
   - Design sans `implementation_contract` → générer contrat minimal
   - Artifact manquant → générer squelette de fichier
   - Test manquant → générer test pytest minimal
   - Design local hors unified-design → proposer migration vers unified-design
3. Pour chaque gap, classifier :
   - **AUTO** : gap comblable automatiquement (squelette, import, test minimal)
   - **SEMI-AUTO** : gap nécessitant une validation HITL
   - **MANUAL** : gap nécessitant une décision architecturale

**Pipeline** :
```
python scripts/gap_combleur.py --source unified-design --target VEX
→ Détecte: design http-server-design absent de unified-design, présent dans VEX/design/
→ Propose: AUTO — migrer VEX/design/http-server-design.md → unified-design/designs/http-server-design/
→ Propose: AUTO — ajouter implementation_contract dans design.yaml
→ Propose: SEMI-AUTO — valider que src/vex/http_server.py implémente bien le design
→ Exécute: migration + contrat + vérification
→ Résultat: gap comblé, métacoherence restaurée
```

---

## 4. Livrables Atomiques

| ID | Livrable | Chemin cible | Type | Critère d'acceptation |
|---|---|---|---|---|
| L1 | `design_impl_verifier.py` | `scripts/design_impl_verifier.py` | Nouveau | Vérifie 5 designs test, sortie JSON valide |
| L2 | `implementation_contract` pour tous les designs `active` | `designs/<name>/implementation_contract.yaml` | Nouveau | 148 designs mis à jour |
| L3 | `metacoherence_gate.py` | `scripts/metacoherence_gate.py` | Nouveau | Audit 30j = 0 mutation sans preuve |
| L4 | Hook pre-commit design-verifier | `.kilocode/hooks/pre-commit-design-verifier.py` | Nouveau | Bloque commit si impl manquante |
| L5 | `gap_combleur.py` | `scripts/gap_combleur.py` | Nouveau | Dry-run détecte 0 gap après exécution |
| L6 | Migration designs VEX vers unified-design | `designs/http-server-design/`, `designs/client-architecture/`, etc. | Migration | VEX n'a plus de dossier `design/` local |
| L7 | Mise à jour `catalog/designs.index.yaml` | `catalog/designs.index.yaml` | Modification | Champs `implemented`, `coverage_pct`, `last_verified` présents |
| L8 | Skill `mdu-integrity-checker` | `skills/mdu-integrity-checker/SKILL.md` | Nouveau | Skill documenté et testé |
| L9 | ADR backing | `ADR/ADR-2026-09-27-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION.md` | Nouveau | ADR créé et approuvé |

---

## 5. Plan de Commits (Atomic)

| Commit | Fichiers | Description |
|---|---|---|
| `feat(scripts): add design_impl_verifier` | `scripts/design_impl_verifier.py` | Vérifie l'implémentation des designs dans les repos cibles |
| `feat(scripts): add metacoherence_gate` | `scripts/metacoherence_gate.py` | Applique ecosystem-meta-coherence-gate mécaniquement |
| `feat(scripts): add gap_combleur` | `scripts/gap_combleur.py` | Automatise le gap-comblé-ification |
| `feat(hooks): add pre-commit-design-verifier` | `.kilocode/hooks/pre-commit-design-verifier.py` | Bloque commit si design non implémenté |
| `feat(designs): migrate VEX designs to unified-design` | `designs/http-server-design/`, `designs/client-architecture/`, etc. | Migre 9 designs de VEX/design/ vers unified-design |
| `feat(catalog): add implementation fields` | `catalog/designs.index.yaml` | Ajoute champs `implemented`, `coverage_pct`, `last_verified` |
| `docs(skill): add mdu-integrity-checker` | `skills/mdu-integrity-checker/SKILL.md` | Skill de vérification d'intégrité MDU |
| `docs(adr): add metacohérence automation ADR` | `ADR/ADR-2026-09-27-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION.md` | ADR backing |

---

## 6. Critères d'Acceptation

1. **Design → Code** : `design_impl_verifier.py --strict unified-design/designs/` passe pour 100% des designs `active` avec `coverage_pct >= 80%`
2. **Métacoherence** : `metacoherence_gate.py --audit-period 30d` retourne 0 mutation du MDU sans preuve horodatée
3. **Gap-comblé-ification** : `gap_combleur.py --dry-run unified-design --target VEX` retourne `gaps_detected: 0` après exécution
4. **Gouvernance** : aucun repo n'a de dossier `designs/` ou `design/` local hors unified-design
5. **Couverture ADR** : >= 95% des designs `active` ont un ADR backing
6. **IntentHash** : 100% des designs `active` ont un `intent_hash` valide
7. **Hook pre-commit** : tentative de commit d'un design `active` sans `implementation_contract` → bloquée
8. **Skill opérationnel** : `mdu-integrity-checker` invoqué dans tout PR touchant unified-design

---

## 7. Références

- **Analyse** : `REPORTS/metacoherence-gericode-unified-design-2026-09-20.md` (si créé)
- **Audit** : `reports/mdu-loopx-audit-20260923.md`
- **Validation** : `reports/mdu-loopx-validation-20260923.md`
- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Design** : `designs/ecosystem-meta-coherence-gate/design.yaml`
- **Meta-design** : `META-DESIGN.md`
- **Gouvernance** : `DESIGNS_GOVERNANCE.md`
- **Scripts existants** : `scripts/validate_designs.py`, `scripts/design_coverage_scanner.py`, `scripts/compliance_scanner.py`
- **PRD-MOC VEX** : `PRD-MOC-VEX-HTTP-SERVER-20260927.md`
- **ADR** : `ADR/ADR-2026-09-27-001-strata-orchestrator-assignment.md`

---

## 8. Proof-of-Life (à compléter)

- [x] 2026-09-27T22:56:39+02:00 — INTENT créé, analyse causale/structurale documentée
- [x] 2026-09-28T23:44:00+02:00 — `design_impl_verifier.py` — premier test sur 5 designs exécuté
- [ ] `implementation_contract` — 10 designs migrés
- [ ] `metacoherence_gate.py` — audit 30j exécuté
- [ ] `gap_combleur.py` — dry-run sur VEX
- [ ] Hook pre-commit — testé et validé
- [ ] ADR backing — créé et approuvé
