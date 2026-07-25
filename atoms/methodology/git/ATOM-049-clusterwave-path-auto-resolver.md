---
type: ATOM
id: ATOM-049-clusterwave-path-auto-resolver
version: 1.0.0
date: 2026-07-19
title: "Clusterwave Path Auto-Resolver — Résolution canonique des chemins de dépôts dans les outils d'analyse"
intent_hash: 0xATOM_049_CLUSTERWAVE_PATH_AUTO_RESOLVER_20260719
status: proposed
strate: L4-TOOLS
tags:
  - path
  - clusterwave
  - repo
  - localization
  - archi
---

# ATOM-049 — Clusterwave Path Auto-Resolver

## Contexte

Les outils d'analyse cross-repo comme Clusterwave codent en dur les chemins des dépôts. Quand un dépôt est déplacé ou renommé, l'outil échoue silencieusement ou signale des chemins erronés, créant des alertes infondées.

## Design

Le **Clusterwave Path Auto-Resolver** est un module qui résout automatiquement les chemins de dépôts en interrogeant la source de vérité (`known_repositories.yaml`) au lieu d'utiliser des chemins codés en dur. Il garantit que tous les outils d'analyse pointent vers les chemins canoniques.

## Règle / Invariant

**Tout outil d'analyse cross-repo DOIT résoudre les chemins via `known_repositories.yaml` avant d'accéder à un dépôt local.**

### Contraintes formelles

```python
# Contrat de résolution
def resolve_canonical_path(repo_name: str, known_repos_path: str) -> Path:
    """
    Résout le chemin canonique d'un dépôt depuis la source de vérité.
    Lève ValueError si le dépôt n'est pas référencé.
    """
    registry = yaml.safe_load(known_repos_path)
    entry = registry.get(repo_name)
    
    if not entry:
        raise ValueError(f"Repo '{repo_name}' not in known_repositories.yaml")
    
    local_path = entry.get("local_path")
    if not local_path:
        raise ValueError(f"Repo '{repo_name}' has no local_path")
    
    return Path(local_path)
```

### Règles de décision

| Situation | Action |
|---|---|
| Dépôt dans `known_repositories.yaml` avec `local_path` | Résoudre et utiliser |
| Dépôt dans YAML sans `local_path` | Erreur : chemin manquant |
| Dépôt hors YAML | Erreur : dépôt non référencé |
| Chemin codé en dur dans outil | Remplacer par appel au resolver |

## Condition de validation

1. Vérifier que tous les outils d'analyse utilisent `resolve_canonical_path()`
2. Vérifier qu'aucun chemin codé en dur ne subsiste
3. Tester avec un dépôt déplacé : l'outil doit suivre le nouveau chemin
4. Vérifier que `known_repositories.yaml` est la seule source de vérité

## Parents

- ATOM-041 (OperatorT) : base de l'infrastructure ternaire
- ATOM-042 (DAG-3 Runtime) : runtime du méta-graphe
- ATOM-043 (DAG-3 Validator) : validation sémantique
- ATOM-044 (Janus Involution) : symétrie CPT

## Tags

`#path` `#clusterwave` `#repo` `#localization` `#archi` `#L4-TOOLS`
