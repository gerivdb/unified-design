---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_030_BILEVEL_AUTORESEARCH
---

# ATOM-030 : Bilevel Autoresearch (Méta-recherche)

## Définition

Capacité du système à injecter du code Python à chaud pour modifier
ses propres mécanismes de recherche. Gain cible : 5x en efficience.

## Garde-fous obligatoires

### 1. Sandbox
- Exécution isolée (conteneur, VM, ou processus séparé)
- Aucun accès aux fichiers critiques du système
- Timeout par défaut : 30 secondes

### 2. Rollback
- Possibilité de revenir à l'état précédent
- Snapshot du checkpoint avant exécution
- Historique des modifications dans `.mdu/autoresearch.log`

### 3. Approval humaine
- En solo : le développeur valide avant injection
- En équipe : HOTL (Human-in-the-Loop) obligatoire
- Mode automatique : seulement pour code non critique

> Note AXE-0 (PRD-MOC-GEN-009) : l'approval humaine obligatoire ici = niveau
> **A0 (HITL)** de `ONTOLOGY/concepts/autonomy-ladder.md` (validation par action).

### 4. Log
- Toute modification est journalisée
- Format : timestamp, action, résultat, rollback_id
- Conservation : 30 jours

### 5. Timeout
- Limite de temps d'exécution : 30s
- Mémoire max : 512 Mo
- Sortie standardisée : JSON avec `status`, `output`, `error`

## Workflow

```
1. Agent détecte un besoin d'optimisation
2. Génère du code Python à injecter
3. Envoie pour approval (HOTL en solo)
4. Si approuvé → exécution dans sandbox
5. Résultat sauvegardé dans checkpoint
6. Si échec → rollback automatique
```

## Exemple de code injecté

```python
# Code généré par l'agent
def optimize_search(query: str) -> list[str]:
    """Optimisation de recherche sémantique."""
    # Implémentation améliorée
    results = semantic_search(query, top_k=10)
    return rank_by_recency(results)
```

## Risques associés

- **Code malveillant** : injection de code non autorisé
- **Instabilité** : modification du comportement de base
- **Perte de contrôle** : boucle de refinement incontrôlable

## Mitigation

- Signature numérique du code injecté
- Test en isolation avant intégration
- Revue par l'Avocat du Diable