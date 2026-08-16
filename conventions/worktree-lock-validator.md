---
type: GUI
version: "1.0.0"
intent_hash: 0xCONNARD_VALIDATOR_WORKTREE_LOCK_20260816
---

# Worktree Lock Validator (connard-validator)

## Objectif
Verifier qu'un worktree peut etre purge sans risque avant toute operation de nettoyage.

## Protocole obligatoire — 4 Checks sequentiels

### CHECK-1 — Le worktree est-il reference dans .kilo/worktrees/*/config.json ?
```
-> Lire .kilo/worktrees/*/config.json
-> Chercher le chemin du worktree
-> Si NON trouve : STOP — worktree non gere par Kilo, demander HITL
-> Si trouve : continuer CHECK-2
```

### CHECK-2 — Le processus associe (node/electron/Code) est-il termine ?
```
-> Verifier les processus node, electron, Code
-> Si un processus utilise le worktree : STOP — attendre la fin de la session
-> Si aucun processus : continuer CHECK-3
```

### CHECK-3 — Les handles Windows sont-ils liberes (via TRIX port 8742 /git/locks/status) ?
```
-> Interroger http://localhost:8742/git/locks/status
-> Verifier qu'aucun handle ne reference le worktree
-> Si handles presents : STOP — liberer les handles avant purge
-> Si handles libres : continuer CHECK-4
```

### CHECK-4 — Le vote ternaire KIX est-il a 2 (Safe Purge) ?
```
-> Interroger KIX pour le vote ternaire du worktree
-> Si vote != 2 : STOP — demande HITL pour override
-> Si vote == 2 : autoriser la purge
```

## Table de decision

| CHECK-1 | CHECK-2 | CHECK-3 | CHECK-4 | Action |
|---|---|---|---|---|
| Non trouve | — | — | — | STOP — HITL creation/verification |
| Trouve | En cours | — | — | STOP — attendre fin session |
| Trouve | Termine | Handles presents | — | STOP — liberer handles |
| Trouve | Termine | Handles libres | Vote != 2 | STOP — HITL override |
| Trouve | Termine | Handles libres | Vote == 2 | Autoriser purge |

## Exceptions
- Purge manuelle explicite de l'utilisateur avec confirmation HITL
- Mode recovery ou emergency (ADR specifique)

## Anti-patterns bloquants
- Purger un worktree sans verifier les handles Windows
- Ignorer le vote ternaire KIX
- Considerer un worktree comme libre simplement parce qu'aucun processus n'est visible

