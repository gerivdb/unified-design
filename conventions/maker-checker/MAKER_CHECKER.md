---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_026_MAKER_CHECKER
---

# ATOM-026 : Séparation Maker-Checker

## Principe

L'agent qui écrit (Analyst) ne valide jamais son propre travail.
Un second agent (Critic) ou un humain (HOTL) doit valider.

## Implémentation MDU

- L'Avocat du Diable (rôle tournant) est le Critic natif du MDU.
- Tout livrable de session doit être relu par le Gardien + un autre expert.
- En solo : le développeur endosse le rôle Critic après une pause (cold review).
- Futur : automate Critic (test runner, linter, drift detector) comme gate.

## Workflow recommandé

```
1. Maker (Agent principal) crée le livrable
2. Pause / changement de contexte
3. Checker (Avocat du Diable ou autre expert) relit
4. Si OK → merge, sinon → itération
```

## Exemple

```yaml
# Dans design.context
roles:
  maker: "Agent principal - crée le code"
  checker: "Avocat du Diable - valide les changements"
```

## Anti-pattern évité

- **Nodding Loop** : l'agent s'approuve lui-même → interdit