# Workflow — Submodule Sync

**IntentHash** : `0xWORKFLOW_SUBMODULE_SYNC_20260923`  
**Design** : `git-submodule-management`  
**Atom** : `ATOM-SUBMODULE-GOVERNANCE`

---

## Déclencheur

Après tout `git pull` sur un repo contenant des submodules, ou lors d'une demande de synchronisation cross-repo.

## Étapes

### ÉTAPE-1 — Vérification des submodules

1. Lister les submodules : `git submodule status`
2. Vérifier que chaque submodule est enregistré dans `known_repositories.yaml`
3. Vérifier le pinning : `git submodule status | grep '^+'` → doit être vide

### ÉTAPE-2 — Synchronisation

1. Initialiser les submodules manquants : `git submodule init`
2. Mettre à jour tous les submodules : `git submodule update --init --recursive`
3. Vérifier le statut : `git submodule status`

### ÉTAPE-3 — Validation cross-repo

1. Vérifier la cohérence des versions : comparer les SHA entre repos
2. Si divergence : signaler et proposer un alignement via release tag
3. Tracer dans WAL : `Write-WAL "SUBMODULE_SYNC: repo=<name> submodules=<n> status=<synced|divergent>"`

### ÉTAPE-4 — Ajout de submodule (si demandé)

1. Vérifier l'enregistrement dans `known_repositories.yaml`
2. Ajouter le submodule : `git submodule add <url> <path>`
3. Pinner la version : `git submodule update --init --recursive`
4. Commit : `git add <path> .gitmodules && git commit -m "feat(submodule): add <path>"`

### ÉTAPE-5 — Suppression de submodule (si demandé)

1. Vérifier que le submodule n'est plus nécessaire
2. Deinit : `git submodule deinit -f <path>`
3. Supprimer : `git rm -f <path>`
4. Nettoyer : `Remove-Item -Recurse -Force ".git/modules/<path>"`
5. Commit : `git commit -m "feat(submodule): remove <path>"`

## Sortie

- Rapport de synchronisation
- Liste des submodules et leurs SHA
- Divergences détectées (si applicable)
- Actions effectuées (add/remove/sync)

## Anti-patterns

- Oublier git submodule update après git pull
- Submodule non enregistré dans known_repositories.yaml
- Submodule sur branche mobile
- Supprimer submodule sans mettre à jour .gitmodules
- Submodule dans src/, bin/, config/

## Journalisation

```
[SUBMODULE_SYNC] repo=<name> submodules=<n> action=<sync|add|remove> sha=<sha> wal=<logged>
```

## Governance

- **Design** : `designs/git-submodule-management.yaml`
- **Atom** : `ATOM-SUBMODULE-GOVERNANCE`
- **ADR** : ADR-039-clone-topology-watch
