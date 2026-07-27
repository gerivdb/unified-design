# ATOM-PUSH-WORKFLOW

## Règle
Ne jamais push directement sur `main`. Créer une branche de livraison et suivre le workflow `git_policy` du MDU.

## Mécanisme
- Tout push vers `main` est bloqué par défaut
- Création obligatoire d'une branche de livraison (feature/release branch)
- Passage par une PR (Pull Request) pour fusion dans `main`
- Respect de la politique `git_policy` définie dans le MDU
- Log : `[PUSH_WORKFLOW] target=<branch> policy=<git_policy> action=<blocked|pr_created|merged>`

## Application
```powershell
# Bloquer le push direct vers main
if ($branch -eq "main") {
    Write-Host "[PUSH_WORKFLOW] Push direct vers main interdit - créer une branche de livraison"
    # Créer la branche de livraison
    git checkout -b "release/$(Get-Date -Format 'yyyyMMdd')"
}
```