# ATOM-ENV-GUARD

## Règle
Détection automatique de l'environnement d'exécution (PowerShell vs bash) et imposition d'appels atomiques PowerShell.

## Mécanisme
- Présence de variables `isPowerShell`, `isBash` diffusées via `KILOCONFIG.sh`
- Redirection automatique des commandes Unix vers leurs équivalents PowerShell atomiques via `break_uix.sh` ou `power_tools.ps1`
- Prévention des erreurs `head`, `grep`, `awk` non reconnues

## Application
```powershell
# Exemple de remboîrage automatique
if ($isBash) {
  $command = ConvertTo-AtomShell -Bash "$Environment:Command"
  .\break_uix.ps1 -Command $command
}
```