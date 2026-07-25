---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_025_LOOP_ENGINEERING
---

# ATOM-025 : Loop Engineering (Pile à 4 couches)

## Définition

Le développement SOTA abandonne le prompting unique au profit de boucles autonomes.
Tout agent ou workflow MDU doit respecter la pile :

1. **Prompt** (L0) : la phrase, l'intention atomique.
2. **Context** (L1) : la fenêtre, les artefacts chargés (design.context, checkpoint).
3. **Harness** (L2) : l'exécution unique, le script, la commande.
4. **Loop** (L3) : l'automatisation, le scheduler, la récurrence.

## Implémentation MDU

- `design.context` = Context (L1)
- `.mdu/checkpoint.json` = Loop state (L3)
- `scripts/mdu_ancrage.sh` (abandonné) → remplacé par sonde implicite (Harness L2)
- Futur : scheduler local (cron/task scheduler) pour relancer les boucles (Loop L3)

## Exemple d'application

```
Prompt : "Analyser le repo LLM-REPO"
Context : design.context chargé, INTENT-XXX lu
Harness : script analyze_repo.py exécuté
Loop : résultat sauvegardé dans .mdu/checkpoint.json, prochain run dans 24h
```

## Règles associées

- **Prompt** doit être atomique (une tâche, une réponse)
- **Context** doit être chargé avant toute exécution
- **Harness** doit être testable isolément
- **Loop** doit être observable et contrôlable