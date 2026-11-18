# Workflow — Doc Sync Full Pipeline

**IntentHash** : `0xWORKFLOW_DOC_FULL_PIPELINE_20261117`
**Skills** : doc-metadata-auditor, doc-structure-creator, ki-injector, doc-sync-gate-skill
**Citizens** : doc-metadata-auditor, ki-sync, doc-univ-auditor, doc-tech-auditor
**Pipelines** : pipeline-doc-completeness, pipeline-ragx-completeness

---

## Déclencheur

Déclenché :
- À chaque nouveau fichier .md créé dans un repo de documentation
- À chaque nouveau bundle KI dans docs/ki-bundles/
- Manuellement sur demande pour un repo donné

## Étapes

### ÉTAPE-1 — Auditer les métadonnées (doc-metadata-auditor)
Vérifier que chaque fichier .md possède : intent_hash, profil, source_repo.
Si un fichier manque des métadonnées, les ajouter automatiquement.

### ÉTAPE-2 — Créer la structure manquante (doc-structure-creator)
Si le repo n'a pas de dossier docs/ complet, créer les 7 dossiers :
docs/api, docs/guides, docs/runbooks, docs/adr, docs/changelog,
docs/ki-bundles, docs/ki-context avec leurs README.md respectifs.

### ÉTAPE-3 — Injecter les KI dans RAGX (ki-injector)
Pour chaque nouveau bundle KI dans docs/ki-bundles/, injecter via
POST http://127.0.0.1:8853/context et vérifier le hash Merkle de retour.

### ÉTAPE-4 — Vérifier la version du navigateur (browser-version-gate)
Vérifier que la version Chromium/ungoogled-chromium installée est dans
la politique autorisée (tested_versions, allowed_versions). Si hors
politique, bloquer l'injection et alerter.

### ÉTAPE-5 — Pousser les changements (repo-push-manager)
Pousser tous les changements vers le remote du repo avec vérification
que le remote et la branche sont corrects.

## Sortie

- Rapport JSON complet : rapports/audit-full-pipeline-*.json
- État : COMPLETÉ si toutes les étapes ont réussi, ÉCHEC sinon

## Anti-patterns

- Injecter un KI sans avoir vérifié les métadonnées du fichier source
- Pousser sans avoir vérifié que le remote est correct
- Injecter un KI sans avoir vérifié la version du navigateur

## Références

- **Design** : `designs/documentation-technique/design.yaml`
- **Design** : `designs/documentation-universitaire/design.yaml`
- **Design** : `designs/documentation-ragx-integration/design.yaml`
- **Design** : `designs/documentation-sync-gate/design.yaml`
- **Skills** : doc-metadata-auditor, doc-structure-creator, ki-injector, browser-version-gate, repo-push-manager
- **Citizens** : doc-metadata-auditor, ki-sync, browser-version-gate
