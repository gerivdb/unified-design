---
type: PRD-MOC
version: "1.0.0"
date: "2026-09-22"
status: proposed
intent_hash: 0xPRD_MOC_COMMAND_RESOLUTION_PROTOCOL_20260922
author: gerivdb
source_repo: gerivdb/unified-design
---

# PRD-MOC — Command Resolution Protocol

> **Périmètre** : résolution obligatoire des commandes externes avant invocation dans les scripts PowerShell du governance stack.
> **Coordination transverse** : voir BOOTSTRAP_SOUVERAIN.md règle B2.

---

## 1. Objectif

Éliminer les échecs silencieux causés par des commandes externes non résolues dans les scripts PowerShell.

## 2. Livrables assignés

| ID | Livrable | Chemin cible | Type | Statut |
|---|---|---|---|---|
| L1 | Design `command-resolution-protocol` | `designs/command-resolution-protocol.md` | Créé | ✅ |
| L2 | Guard pré-exécution dans `scripts/run-governance-unit-tests.ps1` | `scripts/run-governance-unit-tests.ps1` | Modifier | ⬜ |
| L3 | Guard pré-exécution dans `.githooks/pre-push.ps1` | `.githooks/pre-push.ps1` | Modifier | ⬜ |
| L4 | MOC orchestration | `MOC/MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` | Créer | ⬜ |

## 3. Tâches

### Phase A — Design

1. **L1** : `designs/command-resolution-protocol.md` — documenter le protocole de résolution.

### Phase B — Implémentation

2. **L2** : `scripts/run-governance-unit-tests.ps1` — résoudre `python` avant `pytest`.
3. **L3** : `.githooks/pre-push.ps1` — résoudre `python` avant `validate_cross_repo.py`.

### Phase C — Orchestration

4. **L4** : `MOC/MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` — créer le MOC d'orchestration.

## 4. Contraintes

- **Pré-vérification** : `Get-Command <cmd> -ErrorAction SilentlyContinue` avant invocation
- **Fallback** : chemins standards (`$env:LOCALAPPDATA\Programs\Python\Python312\python.exe`)
- **Échec bruyant** : `Write-Error` + `exit 1` avec message explicite
- **Documentation** : commandes requises dans l'en-tête du script

## 5. Plan de commits proposé

| Commit | Fichiers | Description |
|---|---|---|
| `feat(protocol): add command resolution protocol design` | `designs/command-resolution-protocol.md` | L1 |
| `feat(scripts): resolve python before pytest` | `scripts/run-governance-unit-tests.ps1` | L2 |
| `feat(hooks): resolve python before validate_cross_repo` | `.githooks/pre-push.ps1` | L3 |
| `feat(moc): add command resolution protocol MOC` | `MOC/MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` | L4 |

## 6. Adossement (PF2)

- **Implémentation** : ce PRD-MOC, exécuté par agent Kilo session suivante
- **Vérificateur** : hooks pre-commit (`check-powershell`, `check-yaml`)
- **Propriétaire** : gerivdb / GOVERNANCE-HUB N+4

## 7. Critères d'acceptation

1. `designs/command-resolution-protocol.md` créé et validé.
2. `scripts/run-governance-unit-tests.ps1` résout `python` avant `pytest`.
3. `.githooks/pre-push.ps1` résout `python` avant `validate_cross_repo.py`.
4. MOC `MOC-COMMAND-RESOLUTION-PROTOCOL-20260922.md` créé.

## 8. Proof-of-Life

- [ ] 2026-09-22T00:56:04+02:00 — Création PRD-MOC Command Resolution Protocol
