# Workflow — Dryrun Causal Audit

**IntentHash** : `0xWORKFLOW_DRYRUN_CAUSAL_AUDIT_20260920`
**Pipeline** : `pipeline-dryrun-causal-audit`
**Skill** : `dryrun-causal-auditor`

---

## Déclencheur

Avant toute implémentation ou merge vers `main`.

## Étapes

### ÉTAPE-1 — Présence
Vérifier que tous les fichiers attendus existent physiquement.

### ÉTAPE-2 — Validité YAML
Parser chaque YAML avec `yaml.safe_load()`.

### ÉTAPE-3 — Frontmatter
Vérifier le frontmatter de chaque document de gouvernance.

### ÉTAPE-4 — Validation MDU
Exécuter `validate_designs.py --strict` sur le design cible.

### ÉTAPE-5 — Hooks
Vérifier que les pre-commit hooks passent.

### ÉTAPE-6 — Cross-references
Vérifier que les références croisées sont cohérentes.

### ÉTAPE-7 — Merge
Vérifier que le merge sur `main` est possible.

## Sortie

- `reports/dryrun-causal-audit-*.md` : rapport d'audit
- Verdict : `PASS` / `WARN` / `STOP`

## Anti-patterns

- Skip dryrun pour gagner du temps
- Valider sans vérifier les chemins
- Ignorer les warnings
