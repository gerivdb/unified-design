# Workflow — Doc Sync Gate

**IntentHash** : `0xWORKFLOW_DOC_SYNC_20261117`
**Skill** : `doc-sync-gate-skill`

---

## Déclencheur

Avant tout push modifiant une interface publique dans un repo source (ECOS-CLI, KIVA-CLI, TOPOS, BRAIN, etc.), ou avant tout merge vers `main`.

## Étapes

### ÉTAPE-1 — Détecter les changements d'interface publique
Identifier les fichiers modifiés qui exposent une API publique (signature, endpoint, route, contrat).

### ÉTAPE-2 — Identifier le doc cible
Déterminer si la doc cible est dans BRAIN-DOCS (technique) ou DOC-UNIV-DEV (universitaire).

### ÉTAPE-3 — Vérifier la mise à jour de la doc
Vérifier que le document correspondant a été mis à jour pour refléter le changement.

### ÉTAPE-4 — Vérifier l'IntentHash
Vérifier que chaque document possède un IntentHash valide et référençable.

### ÉTAPE-5 — Décision ALLOW ou BLOCK
- **ALLOW** : la doc est à jour, push autorisé
- **BLOCK** : la doc n'est pas à jour, push bloqué avec justification

## Sortie

- Rapport JSON : `reports/doc-sync-gate-*.json`
- Verdict : `ALLOW` / `BLOCK`

## Anti-patterns

- Pousser un changement d'API sans mettre à jour la doc correspondante
- Considérer la doc comme optionnelle lors d'un changement d'interface
- Ignorer l'alignement des versions entre code et doc

## Références

- **Design** : `designs/documentation-sync-gate/design.yaml`
- **Skill** : `skills/doc-sync-gate-skill/SKILL.md`
- **Repo cibles** : `gerivdb/BRAIN-DOCS`, `gerivdb/DOC-UNIV-DEV`
