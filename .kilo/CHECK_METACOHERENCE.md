# CHECK_METACOHERENCE.md — Unified-Design Structural Metacoherence Checker

> **Intent** : `INTENT-UNIFIED-DESIGN-METACOHERENCE-STRUCTURAL-CHECKER-20260927.md`
> **Script** : `.kilo/check_meta_coherence.py`
> **Aliases** : `.kilo/meta_coherence_aliases.yaml`

## 1. Objectif

Vérifier la **métacohérence structurelle** des `designs/**/*.yaml` de `unified-design` et produire un plan de correctifs traçable.

**Pas** de vérification sémantique du code implémenté : ce checker valide uniquement la résolvabilité du graphe `inherits` / `depends_on` / `bridges` dans l’atlas local.

## 2. Installation / pré-requis

- Python 3.10+
- `PyYAML` installé dans l’environnement utilisé par le repo
- Fichier d’alias optionnel : `.kilo/meta_coherence_aliases.yaml`

## 3. Modes d’exécution

```powershell
# Vérification seule, aucun fichier modifié
python .kilo/check_meta_coherence.py --mode check

# Rapport + plan de correctifs, aucun fichier modifié
python .kilo/check_meta_coherence.py --mode plan

# Application des fixes auto-approuvées seulement
python .kilo/check_meta_coherence.py --mode apply

# Mode CI/pre-commit : exit 1 si problème
python .kilo/check_meta_coherence.py --mode strict
python .kilo/check_meta_coherence.py --strict
```

### 3.1 Mode `check`

- Génère `reports/meta-coherence/latest.json`
- Génère `reports/meta-coherence/latest-fix-plan.json`
- Affiche un résumé JSON sur stdout
- Ne modifie aucun fichier

### 3.2 Mode `plan`

- Identique à `check` pour le rapport
- Ajoute la classification `auto_fixes` / `manual_fixes`
- Ne modifie aucun fichier

### 3.3 Mode `apply`

- Applique uniquement les `auto_fixes` :
  - `cap_depth` : plafonnement de la profondeur d’héritage à 3
- Ne touche pas aux `manual_fixes` :
  - `remove_missing_parent`
  - `remove_missing_dependency`
- Sauvegarde chaque fichier modifié dans `reports/meta-coherence/backups/`
- Génère `reports/meta-coherence/apply-report-<ts>.json`

### 3.4 Mode `strict`

- Bloque si :
  - `issues_total > 0`
  - `bad_yaml > 0`
- Exit 0 uniquement si 0 problème détecté

## 4. Aliases

Le fichier `.kilo/meta_coherence_aliases.yaml` permet de résoudre des références courantes vers des designs dont le slug diffère du nom attendu.

Exemple :

```yaml
aliases:
  plix: plix
  llux: llux
  meta-coherence: meta-coherence
```

Toute référence non résolue et sans alias est comptée en `missing_parent` ou `missing_dependency`.

## 5. Intégration

### 5.1 Pre-commit

```yaml
- repo: local
  hooks:
    - id: meta-coherence-checker
      name: Unified-Design structural metacoherence checker
      entry: python .kilo/check_meta_coherence.py --strict
      language: system
      pass_filenames: false
      types: [yaml]
      files: ^designs/.*\.yaml$
```

### 5.2 CI step local

```powershell
python .kilo/check_meta_coherence.py --check
if ($LASTEXITCODE -ne 0) { exit 1 }
```

## 6. Dette connue et limites

| Limite | Raison | Traitement |
|--------|--------|-----------|
| `depends_on:` orphelins non résolubles | Références vers ATOM/PRD/MOC hors `designs/` | Comptés, mais non corrigés en auto |
| YAML invalides | Parsing impossible | Rapportés, correction manuelle |
| Alias incomplets | Nombreux slugs manquants | Enrichir `.kilo/meta_coherence_aliases.yaml` |

## 7. Références

- **Intent** : `INTENTS/INTENT-UNIFIED-DESIGN-METACOHERENCE-STRUCTURAL-CHECKER-20260927.md`
- **Intent parent** : `INTENTS/INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md`
- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Design** : `designs/ecosystem-meta-coherence-gate/design.yaml`
- **Design** : `designs/incremental-growth.yaml`
