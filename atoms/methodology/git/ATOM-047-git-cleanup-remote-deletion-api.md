---
type: ATOM
id: ATOM-047-git-cleanup-remote-deletion-api
version: 1.0.0
date: 2026-07-19
title: "Git Cleanup Remote Deletion API — Suppression de branches distantes via API quand le hook bloque"
intent_hash: 0xATOM_047_GIT_CLEANUP_REMOTE_DELETION_API_20260719
status: proposed
strate: L4-TOOLS
tags:
  - git
  - cleanup
  - api
  - governance
  - hook
---

# ATOM-047 — Git Cleanup Remote Deletion API

## Contexte

Le hook WIC bloque `git push --delete` sur les branches protégées. Dans un workflow standard, la suppression de branches distantes orphelines nécessite un canal alternatif qui respecte les garde-fous tout en permettant le nettoyage.

## Design

Le **Git Cleanup Remote Deletion API** est un canal de suppression de branches distantes qui contourne le hook git local en utilisant l'API GitHub (`gh api DELETE repos/{owner}/{repo}/git/refs/heads/{branch}`). Ce canal est réservé aux administrateurs et audité.

## Règle / Invariant

**Quand le hook WIC interdit `git push --delete`, la suppression de branches distantes DOIT passer par l'API GitHub avec authentification, et être suivie d'un `git fetch --prune origin`.**

### Contraintes formelles

```python
# Contrat de suppression
def delete_remote_branch(branch: str, repo: str, actor: str) -> DeletionResult:
    """
    Supprime une branche distante via API GitHub.
    Préconditions :
      - actor est administrateur du repo
      - branch n'est pas dans protected_branches
      - branch n'est pas la branche par défaut
    """
    if branch in get_protected_branches(repo):
        return DeletionResult(ok=False, reason="protected_branch")
    
    if not is_admin(actor, repo):
        return DeletionResult(ok=False, reason="not_admin")
    
    response = gh_api(
        method="DELETE",
        path=f"repos/{repo}/git/refs/heads/{branch}"
    )
    
    if response.status_code == 204:
        git_fetch_prune()
        return DeletionResult(ok=True, reason="deleted")
    
    return DeletionResult(ok=False, reason=response.text)
```

### Règles de décision

| Méthode | Résultat |
|---|---|
| `git push --delete` | ❌ bloqué par WIC |
| `gh api DELETE ...` | ✅ autorisé si admin |
| `git fetch --prune` | ✅ obligatoire après suppression |

## Condition de validation

1. Vérifier que `git push --delete` est bien bloqué par le hook
2. Vérifier que `gh api DELETE` supprime la branche
3. Vérifier que `git fetch --prune origin` nettoie les références locales
4. Vérifier que seuls les administrateurs peuvent exécuter la suppression

## Parents

- ATOM-041 (OperatorT) : base de l'infrastructure ternaire
- ATOM-042 (DAG-3 Runtime) : runtime du méta-graphe
- ATOM-043 (DAG-3 Validator) : validation sémantique
- ATOM-044 (Janus Involution) : symétrie CPT
- ATOM-046 (WIC Branch Prefix Validation) : contrat WIC

## Tags

`#git` `#cleanup` `#api` `#governance` `#hook` `#L4-TOOLS`
