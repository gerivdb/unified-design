# ATOM-CHERRY-PICK-STATE

## Règle
Vérification obligatoire de l'état cherry-pick avant toute nouvelle commande Git.

## Mécanisme
- Exécuter `git status` avant toute opération critique
- Si un cherry-pick est en cours (marqueurs REVERT_HEAD ou CHERRY_PICK_HEAD) :
  - Forcer `--continue`, `--skip`, ou `--abort` selon le contexte
  - Ne jamais exécuter une autre commande dans un état cherry-pick incohérent
- Log : `[CHERRY_PICK_STATE] status=<clean|in-progress> resolved=<bool>`

## Application
```powershell
$status = git status --short
if ($status -match "CHERRY_PICK_HEAD|REVERT_HEAD") {
    # Cherry-pick en cours - résoudre d'abord
    git cherry-pick --continue  # ou --skip ou --abort
}
```