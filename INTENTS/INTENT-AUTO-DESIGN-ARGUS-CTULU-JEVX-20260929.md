---
type: INTENT
status: proposed
date: "2026-09-29"
intent_hash: 0xINTENT_AUTO_DESIGN_ARGUS_CTULU_JEVX_20260929
---

# INTENT — Auto-Design : exploitation d'ARGUS, CTULU et JEVX pour la gestion automatique des commits et la validation cross-repo

> **Contexte** : `auto-design` dispose d'une architecture complète (analyzer, generator, industrializer, verifier, auto_promote, CLI, hooks). Cependant, il raisonne en autonomie locale et n'exploite pas les capacités existantes d'**ARGUS** (couche N+2 de détection), **CTULU** (couche N+3 d'orchestration et traçabilité) et **JEVX** (couche de projection/synchronisation). Cet intent formalise l'intégration de ces trois composants pour transformer le scoring de `auto-design` en validation sémantique écosystémique et pour automatiser la gestion des commits.

---

## 1. Conception du Chemin

### 1.1 auto-design = orchestrateur de l'auto-industrialisation

`auto-design` est le **moteur d'auto-industrialisation** de l'écosystème :

- Il analyse, génère, déploie et vérifie des designs atomiques
- Il promeut automatiquement les governance docs
- Il manque de **validation sémantique** (bridges, cross-refs, meta-coherence)
- Il manque de **traçabilité** (graphe INTENT→PRD→EPIC→TASK)
- Il manque de **gestion automatique des commits** (conventional commits, atomic commits, auto-commit)

### 1.2 ARGUS = validateur sémantique N+2

ARGUS apporte la **détection de pathologies cross-repo** :

| Scanner | Pathologie | Bénéfice auto-design |
|---|---|---|
| `bridge_check.py` | GAP, VOID, DRIFT, UNPROVEN | Valide les bridges déclaratifs générés par `generator.py` |
| `crossref_check.py` | ORPHAN, GAP, STALE, BROKEN | Vérifie que les cross-refs dans `design.yaml` et `implementation_contracts` sont vivantes |
| `catalog_sync_scanner.py` | SOURCE_MISSING, DUPLICATE_ID, HAND_EDIT_DETECTED, STALE_INDEX, ORPHAN_ARTIFACT | S'assure que le catalogue `unified-design/catalog/` reflète les designs déployés |
| `meta_cycle_feedback.py` | RECURRING_GAP, PERSISTENT_DRIFT, UNRESOLVED_CROSSREF | Agrége les findings et détecte les patterns récurrents |
| `gaps_sot_scanner.py` | gaps SOT ouverts, décisions pending | Vérifie que le repo industrialisé est bien dans `known_repositories.yaml` |
| `ecosystem_meta_coherence.py` | gaps/drifts écosystémiques | Gate pré-déploiement : bloque si contradictions existent |
| `nodex.py` | classification sémantique des composants | Enrichit `_detect_components()` avec KG-L et ontologie |

### 1.3 CTULU = moteur d'exécution N+3

CTULU apporte l'**exécution, la traçabilité et la gouvernance synthétique** :

| Outil | Responsabilité | Bénéfice auto-design |
|---|---|---|
| `trace_graph.py` | Graphe de traçabilité cross-repo | Vérifie qu'un design déployé correspond à un PRD/EPIC existant |
| `trace_validator.py` | Validation du graphe | Détecte orphelins, liens cassés, status mismatch, collisions d'hash |
| `trace_drift.py` | Détection de dérives | Scan les designs industrialisés pour frontmatter decay, schema violation, terminal modification |
| `trace_cli.py` | CLI unifiée | Interface build/validate/drift/rollback pour `cycle_runner.py` |
| `trix-commit-monitor.py` | Auto-commit multi-repo | Commit et push automatiques des changements de design |
| `trix-git-workflow.py` | Commit atomique + push sécurisé | Conventional commits, ≤3 fichiers, génération IntentHash, sync multi-repo |
| `trix-pre-commit-guard.py` | Garde pré-commit | Valide JSON, détecte résidus, vérifie required dirs |
| `vibe-governance-synthesizer/` | Génération 6 artifacts | Complète `auto_promote.py` : génère INTENT, EPIC, PRD, ADR, ISSUE, IMPENSE + commit |
| `tool_ir/` | Format intermédiaire standardisé | Décrit les composants auto-design en YAML → Zig généré |
| `tools-inventory-scanner/` | Inventaire des outils | Améliore `_detect_components()` |
| `tools-stub-detector/` | Détection de stubs | Complète `_score_auto_debug_maturity()` |

### 1.4 JEVX = couche de projection/synchronisation

JEVX complète CTULU comme **mécanisme de projection et de synchronisation** des designs :

- **Projection** : JEVX projette les designs auto-design vers des formats de consommation (TALEX, CURX, narratives)
- **Synchronisation** : JEVX assure la cohérence entre `unified-design/designs/` et les repos cibles
- **Validation** : JEVX valide que les designs projetés sont conformes aux attentes des consommateurs

### 1.5 Architecture cible intégrée

```
unified-design/
├── engine/
│   └── auto_design/
│       ├── analyzer.py          # + ARGUS nodex.py + CTULU tools-inventory-scanner
│       ├── generator.py         # + JEVX projection templates
│       ├── industrializer.py    # + CTULU trix-commit-monitor + trix-git-workflow
│       ├── verifier.py          # + ARGUS bridge_check + crossref_check + CTULU trace_validator
│       ├── reporter.py          # + ARGUS meta_cycle_feedback + CTULU trace_graph
│       └── auto_promote.py      # + CTULU vibe-governance-synthesizer
├── templates/
│   └── auto_design/
│       ├── cycle_runner.py
│       ├── bridge_executor.py
│       ├── pr_factory.py
│       ├── commit_validator.py   # Conventional commits + atomic check
│       ├── commit_monitor.py     # Auto-commit via CTULU
│       └── trace_gate.py         # Traceability gate via CTULU
└── INTENTS/
    └── INTENT-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md
```

---

## 2. Décisions architecturales

### 2.1 Conventional Commit Validation (P1)

**Responsable** : `analyzer.py` + CTULU `trix-git-workflow.py`

```python
def _score_conventional_commit_adherence(self) -> int:
    """Vérifie si le repo suit les conventional commits via CTULU."""
    from trix_git_workflow import get_recent_commits
    commits = get_recent_commits(self.repo_root, count=20)
    pattern = re.compile(r'^(feat|fix|docs|test|refactor|chore|ci|build|revert|style|perf)')
    compliant = sum(1 for c in commits if pattern.match(c.get("message", "")))
    return int((compliant / len(commits)) * 100) if commits else 0
```

**Bénéfice** : Score de conformité commit dans `auto_design_readiness`.

### 2.2 Atomic Commit Checking (P1)

**Responsable** : `verifier.py` + CTULU `trix-git-workflow.py`

```python
def _check_atomic_commits(self) -> dict:
    """Vérifie que les commits sont atomiques (≤3 fichiers) via CTULU."""
    from trix_git_workflow import get_recent_commits, run_git
    result = run_git(["log", "--format=%H", "-20"], cwd=str(self.repo_root))
    shas = result.stdout.strip().split("\n") if result.stdout.strip() else []
    violations = []
    max_files = 0
    for sha in shas:
        diff = run_git(["diff-tree", "--no-commit-id", "-r", "--name-only", sha], cwd=str(self.repo_root))
        files = [f for f in diff.stdout.strip().split("\n") if f]
        max_files = max(max_files, len(files))
        if len(files) > 3:
            violations.append({"sha": sha[:8], "files": len(files)})
    return {"atomic": len(violations) == 0, "max_files": max_files, "violations": violations}
```

**Bénéfice** : Bloque si commits non atomiques détectés.

### 2.3 Bridge Validation via ARGUS (P1)

**Responsable** : `verifier.py` + ARGUS `bridge_check.py`

```python
def _validate_bridges_argus(self) -> dict:
    """Valide les bridges via ARGUS bridge_check."""
    import subprocess, json
    script = Path(r"D:\DO\WEB\TOOLS\L1-INFRA\ARGUS\scanners\bridge_check.py")
    result = subprocess.run(
        [sys.executable, str(script), "--repo", str(self.repo_root), "--json"],
        capture_output=True, text=True, timeout=120
    )
    return json.loads(result.stdout) if result.stdout else {"error": "bridge_check failed"}
```

**Bénéfice** : Transforme le comptage de fichiers en validation sémantique (GAP/DRIFT/VOID/UNPROVEN).

### 2.4 Crossref Validation via ARGUS (P1)

**Responsable** : `verifier.py` + ARGUS `crossref_check.py`

```python
def _validate_crossrefs_argus(self) -> dict:
    """Valide les cross-refs via ARGUS crossref_check."""
    import subprocess, json
    script = Path(r"D:\DO\WEB\TOOLS\L1-INFRA\ARGUS\scanners\crossref_check.py")
    result = subprocess.run(
        [sys.executable, str(script), "--repo", str(self.repo_root), "--json"],
        capture_output=True, text=True, timeout=120
    )
    return json.loads(result.stdout) if result.stdout else {"error": "crossref_check failed"}
```

**Bénéfice** : Détecte les liens cassés que le scoring actuel ignore.

### 2.5 Auto-Commit on Design Changes (P2)

**Responsable** : `industrializer.py` + CTULU `trix-commit-monitor.py`

```python
def deploy_with_auto_commit(self) -> dict:
    """Déploie et commit automatiquement les changements."""
    deploy_result = self.deploy()
    if deploy_result["status"] == "ok":
        from trix_commit_monitor import git_status, git_add, git_commit, git_push
        changes = git_status(str(self.repo_root))
        if changes:
            git_add(str(self.repo_root), changes)
            msg = f"feat(auto_design): industrialize {self.repo_root.name}"
            git_commit(str(self.repo_root), msg)
            git_push(str(self.repo_root))
    return deploy_result
```

**Bénéfice** : Traçabilité automatique des changements de design.

### 2.6 Commit Templates Deployment (P2)

**Responsable** : `industrializer.py`

Nouveaux templates déployés :
- `templates/auto_design/commit_validator.py` — valide conventional commits + atomicité
- `templates/auto_design/commit_monitor.py` — auto-commit avec message standardisé

**Bénéfice** : Repos industrialisés héritent des conventions de commit.

### 2.7 Branch/Commit Coupling (P2)

**Responsable** : `pr_factory.py` (à créer) + CTULU `trix-git-workflow.py`

```python
def create_pr(repo_root: Path, branch_name: str, title: str, body: str) -> dict:
    """Crée une PR avec couplage branch/commit."""
    from trix_git_workflow import get_current_branch, commit_atomic
    current = get_current_branch(str(repo_root))
    if current != branch_name:
        return {"success": False, "error": f"Branch mismatch: {current} != {branch_name}"}
    # Commit atomique avant PR
    ...
```

**Bénéfice** : Cohérence branch → commit → PR.

### 2.8 Meta-Coherence Gate (long terme)

**Responsable** : `generator.py` + ARGUS `ecosystem_meta_coherence.py`

```python
def _check_meta_coherence(self) -> dict:
    """Vérifie la méta-cohérence écosystémique avant déploiement."""
    from ecosystem_meta_coherence import verify_meta_coherence
    context = {
        "repo": str(self.repo_root),
        "design": self._build_design_yaml(self._detect_components()),
        "bridges": self._build_bridges(self._detect_components()),
    }
    return verify_meta_coherence(context)
```

**Bénéfice** : Bloque le déploiement si des gaps/drifts écosystémiques existent.

### 2.9 Traceability Integration (long terme)

**Responsable** : `verifier.py` + CTULU `trace_graph.py` + `trace_validator.py` + `trace_drift.py`

```python
def _validate_traceability(self) -> dict:
    """Valide la traçabilité du repo via CTULU."""
    from traceability.trace_graph import build_and_save
    from traceability.trace_validator import TraceabilityValidator
    graph = build_and_save([self.repo_root], ".traceability/graph.json", "json")
    validator = TraceabilityValidator(graph)
    return validator.validate(strict=True).summary()
```

**Bénéfice** : +90% visibilité sur la cohérence des designs.

### 2.10 Component Classification via ARGUS NODEX (long terme)

**Responsable** : `generator.py` + ARGUS `nodex.py`

```python
def _detect_components(self) -> list[str]:
    """Détecte les composants avec classification sémantique ARGUS."""
    raw = self._detect_components_raw()
    from nodex import NodexRunnerEffective
    runner = NodexRunnerEffective()
    classified = []
    for comp in raw:
        result = runner._execute({"entity_id": comp, "query_type": "classify"})
        if result.get("ontology_alignment", {}).get("type_valid"):
            classified.append(comp)
    return classified
```

**Bénéfice** : Réduit les faux négatifs de détection de composants.

---

## 3. Livrables Atomiques

| ID | Livrable | Module source | Effort | Priorité |
|---|---|---|---|---|
| L1 | `_score_conventional_commit_adherence()` | `analyzer.py` + CTULU | 1h | P1 |
| L2 | `_check_atomic_commits()` | `verifier.py` + CTULU | 30min | P1 |
| L3 | `generate_commit_message()` | `generator.py` | 30min | P1 |
| L4 | `_validate_bridges_argus()` | `verifier.py` + ARGUS | 1h | P1 |
| L5 | `_validate_crossrefs_argus()` | `verifier.py` + ARGUS | 1h | P1 |
| L6 | Templates `commit_validator.py` + `commit_monitor.py` | `templates/auto_design/` | 1h | P2 |
| L7 | Auto-commit on deploy | `industrializer.py` + CTULU | 1h | P2 |
| L8 | Branch/commit coupling | `pr_factory.py` + CTULU | 30min | P2 |
| L9 | `_check_meta_coherence()` | `generator.py` + ARGUS | 2h | P3 |
| L10 | `_validate_traceability()` | `verifier.py` + CTULU | 3h | P3 |
| L11 | `_classify_components_noded()` | `generator.py` + ARGUS | 2h | P3 |

**Effort total estimé** : ~13h de développement SLM.

---

## 4. Plan de Commits (Atomic)

| Commit | Fichiers | Description |
|---|---|---|
| `feat(analyzer): add conventional commit scoring` | `engine/auto_design/analyzer.py` | Score de conformité conventional commits via CTULU |
| `feat(verifier): add atomic commit checking` | `engine/auto_design/verifier.py` | Vérifie atomicité ≤3 fichiers via CTULU |
| `feat(generator): add commit message generation` | `engine/auto_design/generator.py` | Génère messages de commit conventionnels |
| `feat(verifier): add ARGUS bridge validation` | `engine/auto_design/verifier.py` | Valide bridges via ARGUS `bridge_check.py` |
| `feat(verifier): add ARGUS crossref validation` | `engine/auto_design/verifier.py` | Valide cross-refs via ARGUS `crossref_check.py` |
| `feat(templates): add commit templates` | `templates/auto_design/commit_validator.py`, `templates/auto_design/commit_monitor.py` | Templates de commit management |
| `feat(industrializer): add auto-commit on deploy` | `engine/auto_design/industrializer.py` | Commit automatique après déploiement |
| `feat(pr_factory): add branch/commit coupling` | `engine/auto_design/pr_factory.py` | Couplage branch → commit → PR |
| `feat(verifier): add meta-coherence gate` | `engine/auto_design/verifier.py` | Gate pré-déploiement via ARGUS |
| `feat(verifier): add traceability validation` | `engine/auto_design/verifier.py` | Validation graphe via CTULU |
| `feat(generator): add NODEX component classification` | `engine/auto_design/generator.py` | Classification sémantique via ARGUS NODEX |

---

## 5. Critères d'Acceptation

1. **Conventional commits** : `_score_conventional_commit_adherence()` retourne un score 0-100 cohérent avec `git log --oneline`
2. **Atomic commits** : `_check_atomic_commits()` détecte les commits >3 fichiers et retourne les violations
3. **Bridge validation** : `_validate_bridges_argus()` retourne un rapport JSON avec findings GAP/DRIFT/VOID/UNPROVEN
4. **Crossref validation** : `_validate_crossrefs_argus()` retourne un rapport JSON avec findings ORPHAN/GAP/STALE/BROKEN
5. **Auto-commit** : `industrializer.deploy_with_auto_commit()` commit et push automatiquement après déploiement
6. **Templates** : `industrializer.py` déploie `commit_validator.py` et `commit_monitor.py` dans `scripts/`
7. **Branch coupling** : `pr_factory.create_pr()` vérifie que la branche courante correspond à la branche cible
8. **Meta-coherence** : `_check_meta_coherence()` bloque le déploiement si `status != OK`
9. **Traceability** : `_validate_traceability()` retourne un rapport de violations (orphelins, liens cassés, status mismatch)
10. **NODEX** : `_detect_components()` utilise NODEX pour classifier les composants avec KG-L

---

## 6. Intégration ARGUS/CTULU/JEVX

### 6.1 ARGUS — Ponts d'intégration

| Point d'intégration | Fichier ARGUS | Méthode |
|---|---|---|
| Bridge validation | `scanners/bridge_check.py` | `scan_repo(repo_root, sot_path)` → JSON |
| Crossref validation | `scanners/crossref_check.py` | `scan_repo(repo_root, sot_path)` → JSON |
| Catalog sync | `scanners/catalog_sync_scanner.py` | `collect_designs(ud)` + `collect_adrs(govhub)` |
| Meta-cycle feedback | `scanners/meta_cycle_feedback.py` | `_detect_patterns(findings)` |
| Gaps SOT | `scanners/gaps_sot_scanner.py` | `scan_gaps_sot()` |
| Meta-coherence | `PRD/ecosystem_meta_coherence.py` | `verify_meta_coherence(context)` |
| NODEX classification | `runners/nodex.py` | `NodexRunnerEffective()._execute(input_data)` |

### 6.2 CTULU — Ponts d'intégration

| Point d'intégration | Fichier CTULU | Méthode |
|---|---|---|
| Trace graph | `tools/traceability/trace_graph.py` | `build_and_save(roots, output, fmt)` |
| Trace validator | `tools/traceability/trace_validator.py` | `TraceabilityValidator(graph).validate(strict)` |
| Trace drift | `tools/traceability/trace_drift.py` | `DriftDetector(graph).scan()` |
| Trace CLI | `tools/traceability/trace_cli.py` | `cmd_build`, `cmd_validate`, `cmd_drift` |
| Commit monitor | `tools/trix-box/trix-commit-monitor.py` | `--commit`, `--status`, `--check` |
| Git workflow | `tools/trix-box/trix-git-workflow.py` | `commit_atomic()`, `push_safe()`, `sync_repo()`, `get_recent_commits()` |
| Pre-commit guard | `tools/trix-box/trix-pre-commit-guard.py` | `check_staged_json()`, `check_untracked()` |
| Governance synthesizer | `tools/vibe-governance-synthesizer/` | `PromptParser.parse()`, `ArtifactSet`, `synthesizer.py` |
| Tool IR | `tools/tool_ir/` | `propagator.py`, schemas YAML |
| Tools inventory | `tools/tools-inventory-scanner/` | `inventory_scanner.py` |
| Tools stub detector | `tools/tools-stub-detector/` | `detector.py` |

### 6.3 JEVX — Ponts d'intégration

| Point d'intégration | Rôle | Mécanisme |
|---|---|---|
| Projection de designs | Transformer `design.yaml` en formats TALEX/CURX/narratives | Templates Jinja2 dans `templates/auto_design/jevi_projection/` |
| Synchronisation | Assurer cohérence entre `unified-design/designs/` et repos cibles | Hook post-deploy qui invoque JEVX sync |
| Validation | Vérifier que les designs projetés sont conformes aux attentes consommateurs | JEVX validation gate dans `verifier.py` |

---

## 7. Bénéfices attendus

| Bénéfice | Mesure | Source |
|---|---|---|
| Conventional commit compliance | 100% des commits scannés | CTULU `trix-git-workflow.py` |
| Atomic commit enforcement | 100% des commits vérifiés | CTULU `trix-git-workflow.py` |
| Bridge validation sémantique | 100% des bridges vérifiés | ARGUS `bridge_check.py` |
| Cross-ref validation | 100% des cross-refs vérifiées | ARGUS `crossref_check.py` |
| Auto-commit traçabilité | 100% des déploiements commités | CTULU `trix-commit-monitor.py` |
| Governance promotion avancée | 6 artifacts générés + commit | CTULU `vibe-governance-synthesizer` |
| Traceability cross-repo | 100% des designs tracés | CTULU `trace_graph.py` |
| Meta-coherence gate | 0 déploiement à risque | ARGUS `ecosystem_meta_coherence.py` |
| Component classification | +30% précision détection | ARGUS `nodex.py` + KG-L |
| JEVX projection | Designs consommables par TALEX/CURX | JEVX templates |

---

## 8. Références

- **Repo source** : `gerivdb/unified-design`
- **Repo ARGUS** : `gerivdb/ARGUS`
- **Repo CTULU** : `gerivdb/CTULU`
- **Repo JEVX** : mécanisme intégré à CTULU/TALEX
- **Repo KG-L** : `gerivdb/KG-L`
- **Ontologie** : `ONTOLOGY/concepts/core/auto-design.md`
- **Design canonique** : `designs/auto-design/design.yaml`
- **PRD backing** : `PRD/PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **MOC backing** : `MOC/MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **ADR backing** : `ADR/ADR-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **EPIC backing** : `EPICS/EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **TASKs** : `TASKS/TASK-AUTO-DESIGN-*-20260929.md` (14 tâches)

---

## 9. Référence ADR

- **ADR** : `ADR/ADR-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- **IntentHash** : `0xADR_AUTO_DESIGN_ARGUS_CTULU_JEVX_20260929`
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded

---

## 10. Proof-of-Life

- [x] 2026-09-29T18:36:10+02:00 — INTENT créé, intégration ARGUS/CTULU/JEVX formalisée
- [x] 2026-09-29T18:38:00+02:00 — PRD créé : `PRD-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- [x] 2026-09-29T18:39:00+02:00 — MOC créé : `MOC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- [x] 2026-09-29T18:40:00+02:00 — ADR créé : `ADR-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- [x] 2026-09-29T18:41:00+02:00 — EPIC créé : `EPIC-AUTO-DESIGN-ARGUS-CTULU-JEVX-20260929.md`
- [x] 2026-09-29T18:42:00+02:00 — 14 TASKs créés dans `TASKS/`
- [x] 2026-09-29T18:43:00+02:00 — Évaluation enrichie avec capacités ARGUS/CTULU/JEVX documentée
- [x] 2026-09-29T18:44:00+02:00 — Plan d'intégration écosystémique complet défini
