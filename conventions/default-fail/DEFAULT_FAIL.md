---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_027_DEFAULT_FAIL
---

# ATOM-027 : Contrat Default-FAIL

## Principe

Aucun succès n'est accepté sans preuve. Le système est "cassé jusqu'à preuve du contraire".

## Règles

- Un push sans signature ADR = REJETÉ (déjà en place via hook).
- Un déploiement sans dry-run = INTERDIT.
- Un benchmark sans résultat mesurable = NON VALIDÉ.
- Un merge sans checklist = BLOQUÉ.

## Implémentation

### Hook pre-push
```powershell
# .githooks/pre-push.ps1
if (-not $env:ADR_SIGNED) {
    Write-Error "REJECTED: Aucune signature ADR détectée"
    Write-Output "Contactez le Gardien MDU pour validation"
    exit 1
}
```

### Vérification de benchmark
```bash
# Avant commit, exécuter
./scripts/benchmark.sh --min-tok-s 30 --max-rss 6500
```

## Exemple de workflow

```
1. Développeur écrit du code
2. Hook vérifie : ADR signée ? → NON → REJECT
3. Développeur signe l'ADR
4. Hook vérifie : benchmark OK ? → NON → REJECT
5. Développeur corrige
6. Push autorisé
```

## Avantages

- **Sécurité** : pas de régression silencieuse
- **Traçabilité** : chaque succès est justifié
- **Fiabilité** : le système reste dans un état valide