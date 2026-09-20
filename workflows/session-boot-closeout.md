# Workflow — Session Boot Closeout

**IntentHash** : `0xWORKFLOW_SESSION_BOOT_CLOSEOUT_20260920`
**Pipeline** : `pipeline-session-boot-closeout`
**Skill** : `session-boot-skill`

---

## Déclencheur

Début et fin de toute session multi-repo.

## Étapes

### ÉTAPE-1 — Boot checks
Exécuter les checks BOOT :
- TALEX checklist
- WAZAA realtime snapshot
- BOOT-5sexter auto-discovery quick scan

### ÉTAPE-2 — Travail
Travail de session (implémentation, corrections, etc.).

### ÉTAPE-3 — Closeout
- Vérifier le statut git
- Auto-commit des changements valides
- Push optionnel vers origin/main

## Sortie

- JSON de résultat des checks
- Commit message horodaté
- Push status

## Anti-patterns

- Session sans boot
- Session sans closeout
- Auto-commit sans vérification des changements
