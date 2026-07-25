---
type: ATOM
id: ATOM-050-duplicate-commit-detector
version: 1.0.0
date: 2026-07-19
title: "Duplicate Commit Detector — Détection des commits dupliqués dans l'historique git"
intent_hash: 0xATOM_050_DUPLICATE_COMMIT_DETECTOR_20260719
status: proposed
strate: L4-TOOLS
tags:
  - git
  - duplicate
  - forensics
  - archi
  - maintenance
---

# ATOM-050 — Duplicate Commit Detector

## Contexte

Les opérations de rebase, merge ou cherry-pick peuvent introduire des commits dupliqués dans l'historique git. Ces doublons ont le même message et le même contenu mais des SHA différents, créant de la confusion et risquant des conflits lors de futures synchronisations.

## Design

Le **Duplicate Commit Detector** est un module qui analyse le graphe git pour identifier les commits suspects : même message, même diff, mais SHA différent. Il signale ces paires sans les supprimer automatiquement, laissant l'opérateur humain valider la correction.

## Règle / Invariant

**Tout commit dont le message et le diff sont identiques à un commit existant mais avec un SHA différent est une duplication. Il DOIT être signalé avant toute opération de nettoyage.**

### Contraintes formelles

```python
# Contrat de détection
def detect_duplicate_commits(repo_path: str, max_commits: int = 100) -> list[DuplicatePair]:
    """
    Détecte les commits dupliqués dans l'historique.
    Retourne une liste de paires (commit_a, commit_b) avec même message et même diff.
    """
    commits = extract_commits(repo_path, max_commits)
    duplicates = []
    
    for i, a in enumerate(commits):
        for b in commits[i+1:]:
            if a.message == b.message and a.diff == b.diff:
                duplicates.append(DuplicatePair(a.sha, b.sha, a.message))
    
    return duplicates
```

### Règles de décision

| Situation | Action |
|---|---|
| 0 duplication | Aucune action |
| 1 duplication | Signaler, investiguer l'origine |
| Duplication confirmée | Proposer un rebase interactif |
| Duplication sur branche distante | Bloquer le nettoyage automatique, HITL requis |

## Condition de validation

1. Exécuter `detect_duplicate_commits()` sur un repo connu avec duplication
2. Vérifier que la paire `3101c5f` / `db2918b` est détectée
3. Vérifier que les faux positifs sont éliminés (même message, diff différent)
4. Vérifier que le rapport liste les SHA et les messages

## Parents

- ATOM-041 (OperatorT) : base de l'infrastructure ternaire
- ATOM-042 (DAG-3 Runtime) : runtime du méta-graphe
- ATOM-043 (DAG-3 Validator) : validation sémantique
- ATOM-044 (Janus Involution) : symétrie CPT

## Tags

`#git` `#duplicate` `#forensics` `#archi` `#maintenance` `#L4-TOOLS`
