---
type: ATOM
id: ATOM-046-wic-branch-prefix-validation
version: 1.0.0
date: 2026-07-19
title: "WIC Branch Prefix Validation — Contrat de préfixe de branche par workspace"
intent_hash: 0xATOM_046_WIC_BRANCH_PREFIX_VALIDATION_20260719
status: proposed
strate: L4-TOOLS
tags:
  - git
  - wic
  - branch
  - governance
  - hook
---

# ATOM-046 — WIC Branch Prefix Validation

## Contexte

Le Workspace Identity Contract (WIC) définit un préfixe de branche obligatoire pour chaque workspace. La validation du préfixe empêche les collisions de nommage et renforce la séparation des workspaces dans un écosystème multi-branches.

## Design

Le **WIC Branch Prefix Validation** est un contrat qui associe un workspace à un préfixe de branche obligatoire. Toute création de branche hors de ce préfixe est rejetée par le hook de pré-push, sauf pour les branches permanentes (`main`, `staging`, `integration`).

## Règle / Invariant

**Toute branche non permanente d'un workspace DOIT commencer par le préfixe déclaré dans `.workspace-identity.yaml`.**

### Contraintes formelles

```python
# Contrat de validation
def validate_branch_prefix(branch: str, wic: WorkspaceIdentityContract) -> ValidationResult:
    """
    Valide que la branche respecte le contrat WIC.
    """
    if branch in wic.permanent_branches:
        return ValidationResult(ok=True, reason="permanent_branch")
    
    if not branch.startswith(wic.branch_prefix):
        return ValidationResult(
            ok=False,
            reason=f"branch '{branch}' does not start with '{wic.branch_prefix}'"
        )
    
    return ValidationResult(ok=True, reason="prefix_match")
```

### Règles de décision

| Branche | Préfixe WIC | Résultat |
|---|---|---|
| `main` | N'importe lequel | ✅ autorisé (permanent) |
| `trix/foo` | `trix/` | ✅ autorisé |
| `feat/bar` | `trix/` | ❌ rejeté |
| `trix/` | `trix/` | ✅ autorisé |

## Condition de validation

1. Lire `.workspace-identity.yaml`
2. Extraire `branch_prefix` et `permanent_branches`
3. Tester `validate_branch_prefix()` sur un jeu de branches valides/invalides
4. Vérifier que le hook de pré-push retourne le bon code de sortie

## Parents

- ATOM-041 (OperatorT) : base de l'infrastructure ternaire
- ATOM-042 (DAG-3 Runtime) : runtime du méta-graphe
- ATOM-043 (DAG-3 Validator) : validation sémantique
- ATOM-044 (Janus Involution) : symétrie CPT

## Tags

`#git` `#wic` `#branch` `#governance` `#hook` `#L4-TOOLS`
