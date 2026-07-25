---
type: ATOM
id: ATOM-045-git-arbiter-health-probe
version: 1.0.0
date: 2026-07-19
title: "Git Arbiter Health Probe — Vérification préventive du service d'arbitrage git"
intent_hash: 0xATOM_045_GIT_ARBITER_HEALTH_PROBE_20260719
status: proposed
strate: L4-TOOLS
tags:
  - git
  - arbiter
  - hook
  - pre-commit
  - governance
---

# ATOM-045 — Git Arbiter Health Probe

## Contexte

Le pré-commit hook TRIX vérifie la disponibilité du Git Arbiter sur `http://localhost:8742/git/locks/status`. Si le service est arrêté, les commits sont bloqués, créant une friction injustifiée pour des opérations non destructives.

## Design

Un **Git Arbiter Health Probe** est une vérification préventive, exécutée avant toute opération git, qui s'assure que le service d'arbitrage est joignable. Si le service est inaccessible, le probe tente un redémarrage automatique avant de conclure à un blocage.

## Règle / Invariant

**Tout pré-commit hook dépendant d'un service local DOIT vérifier sa disponibilité avant de bloquer les commits non destructifs.**

### Contraintes formelles

```python
# Contrat du probe
def ensure_arbiter(timeout_s: float = 2.0) -> ProbeResult:
    """
    Vérifie que GET http://localhost:8742/git/locks/status retourne 200.
    Si non, tente un démarrage automatique si les prérequis sont remplis.
    """
    status_code = curl_get("http://localhost:8742/git/locks/status", timeout_s)
    
    if status_code == 200:
        return ProbeResult(ok=True, action="none")
    
    # Tentative de redémarrage automatique
    started = try_start_arbiter()
    if started:
        return ProbeResult(ok=True, action="restarted")
    
    return ProbeResult(ok=False, action="blocked")
```

### Règles de décision

| État Arbiter | Action Probe | Résultat |
|---|---|---|
| `200 OK` | Aucune | Commit autorisé |
| `000` + redémarrage OK | Redémarrage silencieux | Commit autorisé |
| `000` + redémarrage KO | Blocage avec message | Commit refusé |

## Condition de validation

1. `curl -s -o NUL -w "%{http_code}" http://localhost:8742/git/locks/status` retourne `200`
2. En cas d'arrêt, le probe redémarre l'Arbiter en < 5s
3. Le pré-commit ne bloque PAS les commits non destructifs si le probe a échoué

## Parents

- ATOM-041 (OperatorT) : base de l'infrastructure ternaire
- ATOM-042 (DAG-3 Runtime) : runtime du méta-graphe
- ATOM-043 (DAG-3 Validator) : validation sémantique
- ATOM-044 (Janus Involution) : symétrie CPT

## Tags

`#git` `#arbiter` `#hook` `#pre-commit` `#governance` `#L4-TOOLS`
