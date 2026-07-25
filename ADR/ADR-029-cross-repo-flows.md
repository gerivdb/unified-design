---
type: ADR
status: accepted
date: "2026-07-16"
intent_hash: 0xADR_CROSSREPO_FLOW_EXTENSION_20260716
---

# ADR-029 — Extension Cross-Repo Flows dans unified-design/atoms/

## Contexte

Les atomes MDU actuels sont majoritairement extraits de contenus **internes** aux dépôts (fichiers, scripts, configs). Les liens **inter-dépôts** — pourtant structurants — ne sont pas encore formalisés.

Exemples de flux implicites identifiés :
- PRIMUS → CTULU, SKILLS, NEXUS (primitives exécutables)
- CITIZENS → CTULU, TINA, BRAIN, Kilo Agent (synchronisation registre)
- PHOTON → TRIX, NEXUS, CTULU (pipeline chunking sémantique)
- SKILLS → CTULU, PRIMUS (orchestration skills)
- DevTools → CTULU, ECOS-CLI, BRAIN (outils opérationnels)

Ces flux sont des **invariants structurels** de l'écosystème. Leur absence dans MDU empêche :
- La détection automatique de cycles inter-dépôts
- La validation de cohérence des dépendances
- La documentation automatique des consommateurs

## Décision

Ajouter une nouvelle catégorie d'atomes `cross-repo-flow` dans `unified-design/atoms/`.

### Atomes créés

| Atome | Provider | Consumers | Fichier |
|---|---|---|---|
| `primitive-flow` | PRIMUS | CTULU, SKILLS, NEXUS | `primitive-flow.yaml` |
| `registry-sync` | CITIZENS | CTULU, TINA, BRAIN, Kilo Agent | `registry-sync.yaml` |
| `photon-pipeline` | PHOTON | TRIX, NEXUS, CTULU | `photon-pipeline.yaml` |
| `skill-orchestration` | SKILLS | CTULU, PRIMUS, Kilo Agent | `skill-orchestration.yaml` |
| `infra-tool-layer` | DevTools | CTULU, ECOS-CLI, BRAIN | `infra-tool-layer.yaml` |
| `cross-repo-flow` | Pattern | Tous | `cross-repo-flow.yaml` |

### Structure d'un atome de flux

```yaml
---
name: <flow-name>
description: "Flux de <X> depuis <provider> vers <consumers>"
parameters:
  provider: <repo>
  consumers: [<repo1>, <repo2>, ...]
  contract_validation: required
  cycle_detection: required
inherits: [cross-repo-flow, formal-verification]
---
```

## Conséquences

### Pour le loop engine MDU

Le loop engine DOIT :
1. Vérifier que chaque provider déclaré possède l'atome de flux correspondant
2. Vérifier que chaque consumer déclaré possède le contrat correspondant
3. Exécuter un **DFS sur le graphe de flux** pour détecter les cycles
4. Logger chaque flux dans le WAL

### Pour les dépôts concernés

Les dépôts suivants DOIVENT être mis à jour avec un `design.yaml` référençant les atomes de flux :

| Dépôt | Atome(s) à référencer |
|---|---|
| PRIMUS | `primitive-flow` (en tant que provider) |
| CTULU | `primitive-flow` (consumer), `registry-sync` (mirror), `infra-tool-layer` (consumer), `photon-pipeline` (consumer) |
| SKILLS | `skill-orchestration` (provider), `primitive-flow` (consumer) |
| CITIZENS | `registry-sync` (provider) |
| PHOTON | `photon-pipeline` (provider) |
| DevTools | `infra-tool-layer` (provider) |

### Cycles interdits

Les dépendances cycliques suivantes sont **INTERDITES** :

```
PRIMUS → CTULU → PRIMUS
CITIZENS → CTULU → CITIZENS
PHOTON → NEXUS → PHOTON
```

Toute tentative de créer un tel cycle DOIT être rejetée par le loop engine.

## Validation

- [x] Atomes créés dans `unified-design/atoms/`
- [x] Index `L1-INFRA_Atoms_Index.yaml` mis à jour
- [ ] `design.yaml` créés pour PRIMUS, SKILLS, PHOTON
- [ ] Détection de cycles implémentée dans le loop engine
- [ ] Tests de validation des flux inter-dépôts

## Références

- `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\cross-repo-flow.yaml`
- `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\primitive-flow.yaml`
- `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\registry-sync.yaml`
- `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\photon-pipeline.yaml`
- `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\skill-orchestration.yaml`
- `D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms\infra-tool-layer.yaml`
- `D:\DO\WEB\TOOLS\L4-TOOLS\PRIMUS\README.md`
- `D:\DO\WEB\TOOLS\L4-TOOLS\CTULU\README.md`
- `D:\DO\WEB\TOOLS\L4-TOOLS\SKILLS\README.md`
- `D:\DO\WEB\TOOLS\L3-CITIZENS\CITIZENS\README.md`
- `D:\DO\WEB\TOOLS\L4-TOOLS\PHOTON\README.md`
