---
type: INTENT
version: "1.0.0"
date: "2026-09-27"
status: proposed
intent_hash: 0xINTENT_UNIFIED_DESIGN_METACOHERENCE_STRUCTURAL_CHECKER_20260927
parent_intent: INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md
repo: "gerivdb/unified-design"
layer: "L0"
author: gerivdb
source_repo: gerivdb/unified-design
source_path: .kilo/check_meta_coherence.py
---

# INTENT — Unified-Design Structural Metacoherence Checker & Auto-Heal

> **Contexte** : Complète `INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md`.
> Cet intent couvre specifically le vérificateur structurel de métacohérence des `designs/**/*.yaml`
> et son mode de correction automatique limitée, livré par `.kilo/check_meta_coherence.py`.

---

## 1. Contexte & Motivation

### 1.1 État observé — la structure déclarée des designs n’est pas vérifiée mécaniquement

Les designs `unified-design` utilisent massivement :
- `inherits:` pour l’héritage déclaratif entre designs
- `depends_on:` pour les dépendances fonctionnelles
- `bridges:` pour les délégations cross-repo

Aucun script ne valide aujourd’hui **structurellement** que ces graphes sont :
- résolvables localement,
- conformes à la règle de profondeur `max_inheritance_depth: 3`,
- exempts de YAML invalides bloquant le parse.

### 1.2 Dette identifiée le 2026-09-27

| Indicateur | Valeur observée |
|---|---|
| Designs YAML analysés | 283 |
| YAML invalides | 5 |
| Parents `inherits:` introuvables | 35 |
| Dépendances `depends_on:` introuvables | 185 |
| Violations profondeur `> 3` | 52 |

## 2. Décision

### 2.1 Objectif

Industrialiser `.kilo/check_meta_coherence.py` en **outil de gouvernance à correction automatique limitée** :
- `--check` : vérification seule, aucun fichier modifié
- `--plan` : vérification + plan de correctifs, aucun fichier modifié
- `--apply` : application des fixes **auto-approuvées** seulement
- `--strict` : mode CI/pre-commit, exit 1 si warnings ou errors

### 2.2 Architecture cible

```
unified-design/
├── .kilo/
│   └── check_meta_coherence.py        # ← vérificateur + fix-plan + auto-heal limité
├── reports/
│   └── meta-coherence/
│       ├── latest.json                 # snapshot courant
│       ├── latest-fix-plan.json        # plan de fix
│       └── backups/                    # sauvegardes avant modification
└── integration points:
    ├── pre-commit hook                 # --strict
    ├── CI step                         # --check
    └── maintainer workflow             # --plan / --apply
```

### 2.3 Mécanisme

1. **Chargement** : tous les `designs/**/*.yaml`, résolution par slug `name`
2. **Vérification** :
   - `inherits:` → parent existe dans l’atlas local ?
   - `depends_on:` → dépendance résoluble ?
   - `bridges:` → cible cohérente ?
   - profondeur d’héritage ≤ 3 ?
   - YAML valide ?
3. **Planification** : classer chaque écart en `auto_fix` ou `manual_fix`
4. **Auto-heal limité** :
   - `cap_depth` : plafonner la profondeur à 3
   - `remove_missing_parent` : supprimer les parents orphelins
   - **exclure** L0/constitutional des suppressions sans HITL
5. **Traçabilité** : rapport horodaté + backups avant écriture

## 3. Livrables Atomiques

| ID | Livrable | Chemin cible | Type | Critère d'acceptation |
|---|---|---|---|---|
| L1 | `check_meta_coherence.py` | `.kilo/check_meta_coherence.py` | Modification | Modes `--check/--plan/--apply/--strict` fonctionnels |
| L2 | Rapport JSON horodaté | `reports/meta-coherence/latest.json` | Nouveau | Présent après exécution |
| L3 | Plan de fix JSON | `reports/meta-coherence/latest-fix-plan.json` | Nouveau | Présent après exécution |
| L4 | Backups pré-fix | `reports/meta-coherence/backups/` | Nouveau | Tout fichier modifié est backupé avant écriture |
| L5 | Intégration pre-commit | `.pre-commit-config.yaml` | Modification | Hook `meta-coherence` en `--strict` |
| L6 | CI step | `.github/workflows/` ou workflow local | Nouveau | `python .kilo/check_meta_coherence.py --strict` |
| L7 | README d'usage | `.kilo/CHECK_METACOHERENCE.md` | Nouveau | Documenté et testé |
| L8 | Tests unitaires | `.kilo/tests/test_check_meta_coherence.py` | Nouveau | Couvre missing_parent, depth, bad_yaml |
| L9 | Alias registry optionnelle | `.kilo/meta_coherence_aliases.yaml` | Nouveau | Traduit `design-principle` → slug réel si applicable |

## 4. Critères d'Acceptation

1. **Vérification** : `python .kilo/check_meta_coherence.py --check` retourne un JSON valide sur 283 designs
2. **Plan** : `python .kilo/check_meta_coherence.py --plan` génère un fix-plan cohérent
3. **Auto-heal** : `python .kilo/check_meta_coherence.py --apply` ne touche pas aux designs L0/constitutional sans HITL explicite
4. **CI** : `python .kilo/check_meta_coherence.py --strict` exit 0 quand la dette est résorbée
5. **Backups** : tout fichier modifié par `--apply` a un backup dans `reports/meta-coherence/backups/`
6. **Traçabilité** : le rapport inclut `timestamp`, `issues_total`, `auto_fixes`, `manual_fixes`

## 5. Proof-of-Life

- [x] 2026-09-27T23:24:48+02:00 — INTENT créé, vérificateur `.kilo/check_meta_coherence.py` déjà opérationnel en mode check
- [ ] 2026-09-27 — Rapport `reports/meta-coherence/latest.json` généré et validé
- [ ] 2026-09-27 — Plan de fix `latest-fix-plan.json` généré
- [ ] 2026-09-28 — Modes `--plan` et `--strict` validés
- [ ] 2026-09-28 — Mode `--apply` testé sur un design non L0
- [ ] 2026-09-28 — Alias registry peuplée si applicable
 - [ ] 2026-09-29 — Pre-commit hook intégré et testé
 - [x] 2026-09-29 — CI step validé
 - [x] 2026-09-28T00:48:21+02:00 — PR #81 mergée, merge commit `3e19ef3`
 - [x] 2026-09-28T01:15:42+02:00 — PR #83 mergée, merge commit `aa855f0`
 - [x] 2026-09-28T01:34:30+02:00 — PR #85 mergée, merge commit `3d70bfe`
 - [x] 2026-09-28T01:38:30+02:00 — PR #86 mergée, merge commit `8d73450`
 - [x] 2026-09-28T01:42:04+02:00 — PR #87 mergée, merge commit `1a70f10`
 - [x] 2026-09-28T01:45:50+02:00 — PR #88 mergée, merge commit `d095f61`

## 6. Références

- **Intent parent** : `INTENT-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md`
- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Design** : `designs/ecosystem-meta-coherence-gate/design.yaml`
- **Design** : `designs/incremental-growth.yaml`
- **Script** : `.kilo/check_meta_coherence.py`
- **Règle** : `DESIGNS_GOVERNANCE.md`
- **ADR** : `ADR-013-meta-design-validation-protocol`
- **ADR** : `ADR-015-unified-design-v2`
- **MDU** : `META-DESIGN.md`
