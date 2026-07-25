---
type: ATOM
id: ATOM-051-repo-locator-validator
version: 1.0.0
date: 2026-07-19
title: "Repo Locator Validator — Vérification systématique de l'existence et du chemin des dépôts"
intent_hash: 0xATOM_051_REPO_LOCATOR_VALIDATOR_20260719
status: proposed
strate: L4-TOOLS
tags:
  - repo
  - localization
  - validation
  - governance
  - clone
---

# ATOM-051 — Repo Locator Validator

## Contexte

Les agents et outils KI créent régulièrement des clones illégitimes parce qu'ils confondent "je ne trouve pas dans le contexte actuel" avec "n'existe pas localement". Cette règle force une vérification systématique de l'existence et du chemin des dépôts avant toute opération.

## Design

Le **Repo Locator Validator** est un module qui vérifie, avant toute opération sur un dépôt, que :
1. Le dépôt est référencé dans `known_repositories.yaml`
2. Le champ `local_path` est présent
3. Le dossier local existe
4. Le chemin est sous une strate L* valide
5. Aucun clone illégitime hors strate n'existe

## Règle / Invariant

**"Je ne trouve pas" ne signifie JAMAIS "n'existe pas". Avant de conclure qu'un repo/document n'existe pas localement, l'agent DOIT consulter la source de vérité.**

### Contraintes formelles

```python
# Contrat de validation en 5 étapes
def validate_repo_location(repo_name: str, proposed_path: str = None) -> LocationResult:
    """
    Valide l'existence et le chemin d'un dépôt.
    Retourne LocationResult(ok=True/False, action="use_existing|create|hitl")
    """
    # ÉTAPE-1 : repo dans known_repositories.yaml ?
    entry = get_repo_entry(repo_name)
    if not entry:
        return LocationResult(ok=False, action="hitl", reason="not_in_yaml")
    
    # ÉTAPE-2 : local_path présent ?
    local_path = entry.get("local_path")
    if not local_path:
        return LocationResult(ok=False, action="hitl", reason="no_local_path")
    
    # ÉTAPE-3 : dossier existe ?
    if Path(local_path).exists():
        return LocationResult(ok=True, action="use_existing", path=local_path)
    
    # ÉTAPE-4 : chemin sous strate L* valide ?
    if not is_valid_stratum(local_path):
        return LocationResult(ok=False, action="hitl", reason="invalid_stratum")
    
    # ÉTAPE-5 : clone illégitime hors strate ?
    illegitimate = find_illegitimate_clone(repo_name)
    if illegitimate:
        return LocationResult(ok=False, action="audit", illegitimate=illegitimate)
    
    return LocationResult(ok=True, action="create", path=local_path)
```

### Règles de décision

| ÉTAPE-1 | ÉTAPE-2 | ÉTAPE-3 | ÉTAPE-4 | ÉTAPE-5 | Action |
|---|---|---|---|---|---|
| Non dans YAML | — | — | — | — | STOP — HITL creation |
| Dans YAML | Pas de `local_path` | — | — | — | STOP — HITL chemin |
| Dans YAML | Présent | Existe | — | — | STOP — utiliser existant |
| Dans YAML | Présent | N'existe pas | Invalide | — | STOP — HITL correction |
| Dans YAML | Présent | N'existe pas | Valide | Illégitime | SIGNALER — auditer |
| Dans YAML | Présent | N'existe pas | Valide | Pas d'illégitime | HITL confirmation clone |

## Condition de validation

1. Vérifier que `known_repositories.yaml` est la source de vérité
2. Vérifier que tous les outils d'analyse utilisent `validate_repo_location()`
3. Tester avec un repo existant : `use_existing`
4. Tester avec un repo hors YAML : `hitl`
5. Tester avec un chemin hors strate : `hitl`
6. Vérifier qu'aucun clone n'est créé dans `D:\DO\WEB\TOOLS\<NOM>` sans préfixe L*

## Parents

- ATOM-041 (OperatorT) : base de l'infrastructure ternaire
- ATOM-042 (DAG-3 Runtime) : runtime du méta-graphe
- ATOM-043 (DAG-3 Validator) : validation sémantique
- ATOM-044 (Janus Involution) : symétrie CPT

## Tags

`#repo` `#localization` `#validation` `#governance` `#clone` `#L4-TOOLS`
