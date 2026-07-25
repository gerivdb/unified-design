---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_031_FIVE_MOVEMENTS
---

# ATOM-031 : Les Cinq Mouvements

Toute boucle de développement MDU doit implémenter :

## 1. Discovery (Découverte)

Trouver le travail à faire :
- Ticket, INTENT, scan de repo
- Analyse des lacunes (gap)
- Priorisation par impact

## 2. Handoff (Transmission)

Isoler la tâche dans une branche dédiée :
- `git checkout -b feat/<description>`
- Context chargé
- Ressources allouées

## 3. Verification (Vérification)

Exécuter les tests, les benchmarks, le lint :
- `.pre-commit-config.yaml`
- CI GitHub Actions
- Benchmarks (tok/s, RSS)

## 4. Persistence (Persistance)

Écrire le résultat sur disque :
- Commit
- Checkpoint `.mdu/checkpoint.json`
- Rapport de session

## 5. Scheduling (Planification)

Planifier la prochaine exécution :
- Cron / task scheduler
- Rappel manuel
- Trigger événementiel

## Correspondance MDU

| Mouvement | Artefact MDU |
|-----------|--------------|
| Discovery | INTENT, ticket, `design.context` |
| Handoff | `git checkout -b feat/...` |
| Verification | `.pre-commit-config.yaml`, CI, benchmark |
| Persistence | `.mdu/checkpoint.json`, commit, rapport |
| Scheduling | (futur) scheduler local, ou rappel manuel |

## Exemple de flux complet

```
1. Discovery: "Analyser les lacunes dans conventions/"
2. Handoff: git checkout -b feat/atom-031-five-movements
3. Verification: pre-commit + pytest + benchmark
4. Persistence: commit + .mdu/checkpoint.json
5. Scheduling: prochaine analyse dans 24h
```