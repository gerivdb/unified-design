# Workflow — RAGX Sync

**IntentHash** : `0xWORKFLOW_RAGX_SYNC_20261117`
**Pipeline** : `pipeline-ragx-completeness`
**Skill** : `ragx-bridge-skill`

---

## Déclencheur

Avant tout push modifiant une documentation technique ou universelle dans BRAIN-DOCS ou DOC-UNIV-DEV, ou avant toute synchronisation périodique des Knowledge Items vers NotebookLM (ENV3).

## Étapes

### ÉTAPE-1 — Extraire les Knowledge Items
Identifier les documents modifiés dans BRAIN-DOCS (technique) ou DOC-UNIV-DEV (universitaire) et extraire les Knowledge Items pertinents.

### ÉTAPE-2 — Constituer le bundle KI
Pour chaque KI, constituer un bundle avec :
- IntentHash (SHA-256 du contenu)
- TTL (durée de validité)
- Provenance (repo source, fichier d'origine, ligne)

### ÉTAPE-3 — Injecter le contexte dans RAGX
Appeler POST http://127.0.0.1:8853/context avec le payload JSON du bundle KI.

### ÉTAPE-4 — Vérifier le hash Merkle
Vérifier que le hash SHA256 retourné par RAGX correspond au contenu injecté.

### ÉTAPE-5 — Synchroniser vers NotebookLM (mode hors-bande)
Appeler POST http://127.0.0.1:8853/sync pour pousser le bundle vers NotebookLM en mode hors-bande (conforme ADR-0209).

## Sortie

- `reports/ragx-sync-*.json` : rapport de synchronisation
- Verdict : `ALLOW` / `BLOCK`

## Anti-patterns

- Injecter un KI sans IntentHash ni provenance
- Utiliser notebooklm-py sur ENV2 (interdit par ADR-0209)
- Injecter un KI sans cohérence topologique CUBE-A/SPIDX

## References

- **Design** : `designs/documentation-ragx-integration/design.yaml`
- **Skill** : `skills/ragx-bridge-skill/SKILL.md`
- **Repo cible** : `gerivdb/RAGX` (L0-CANON)
