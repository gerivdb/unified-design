---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_033_TOPOS_MERGE_SOVEREIGN
---

# ATOM-033 : TOPOS — Temps Topologique & Merge Souverain

## Définition

Chaque opération doit être routée vers un environnement autorisé.
Le "merge souverain" (fusion dans main) ne peut avoir lieu que sur **ENV2**.

## Règle

- ENV2 (D:\DO\WEB\TOOLS) est l'unique point de merge autorisé.
- Aucun merge dans main depuis un autre environnement (CI, autre machine).
- Le hook local vérifie l'hostname avant d'autoriser un merge.

## Implémentation

### Script de vérification

```bash
#!/bin/bash
# scripts/check-merge-host.sh

HOSTNAME=$(hostname)
ALLOWED_HOST="ENV2"

if [ "$HOSTNAME" != "$ALLOWED_HOST" ]; then
    echo "REJECTED: Merge autorisé uniquement sur $ALLOWED_HOST"
    echo "Hostname détecté: $HOSTNAME"
    exit 1
fi

echo "OK: Merge autorisé sur $ALLOWED_HOST"
exit 0
```

### Hook pre-merge-commit

```powershell
# .githooks/pre-merge-commit.ps1
$host = hostname
if ($host -ne "ENV2") {
    Write-Error "REJECTED: Merge autorisé uniquement sur ENV2"
    Write-Output "Hostname détecté: $host"
    exit 1
}
```

## Exemple d'utilisation

```
1. Développeur travaille sur une machine locale
2. Tentative de merge → hook vérifie hostname
3. Si différent de ENV2 → REJECT
4. Développeur doit utiliser ENV2 pour merge
```

## TOPOS (Temps Topologique)

Le TOPOS est le concept de temps topologique appliqué aux opérations git :
- Chaque commit a une position dans un graphe topologique
- Le merge doit respecter l'ordre topologique
- Les merges concurrents sont résolus par ordre de temps logique

## Référence

- `L1-GOVERNANCE/goVERNANCE-HUB/TOPOS/registry/topos.md` (à créer)