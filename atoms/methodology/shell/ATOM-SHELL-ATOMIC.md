# ATOM-SHELL-ATOMIC

## Règle
Chaque appel de commande shell doit être atomique : une seule commande par invocation, sans pipeline complexe ni redirection shell.

## Mécanisme
- Fragmentation de toute commande complexe en appels distincts et atomiques
- Pas de chaînage `&&` ou `||` multi-étapes dans un seul appel
- Pas de redirections shell `>`, `2>&1` dans les commandes complexes
- Log : `[SHELL_ATOMIC] command=<cmd> atomic=<bool> steps=<n>`

## Application
```powershell
# [X] Non atomique
git add . && git commit -m "message"

# [OK] Atomique - etapes séparées
git add .
git commit -m "message"
```