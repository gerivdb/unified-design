---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_034_ANTI_PATTERNS
---

# ANTI-PATTERNS — Ce que le MDU combat

Les anti-patterns sont des schémas de pensée ou de développement qui, s'ils laissés non corrigés, mènent à la dégradation du système.

## Table des anti-patterns

| Anti-pattern | Description | Parade MDU |
|--------------|-------------|------------|
| **Nodding Loop** | L'agent s'approuve lui-même | Avocat du Diable, Maker-Checker, Cold Review |
| **Comprehension Rot** | Perte de compréhension du code par l'humain | ADR, checkpoint, documentation, review externe |
| **Reddition Cognitive** | L'humain abandonne son jugement à l'IA | HOTL, Default-FAIL, Preuve Tangible |
| **Prompt Drift** | Dégradation progressive des résultats | Semantic Drift Detector (ATOM-015), checkpoint |
| **Configuration Decay** | Les hooks/configs deviennent obsolètes | Checkpoint, design.context versionné, revue périodique |
| **Branch Orphan** | Branches sans PR ou travail associé | Branch Lifecycle, Orphan Branch Dispatcher |
| **Silent Failure** | Échec sans signalement visible | Logs obligatoires, Evidence Required (ATOM-028) |
| **Context Bleeding** | Fuite d'état entre sessions | Isolation par worktree, checkpoint nettoyé |

## Détection

### Nodding Loop
- Un seul acteur valide son propre travail
- Absence de review externe
- **Détecteur** : Avocat du Diable (rôle tournant)

### Comprehension Rot
- Documentation obsolète
- Code sans test
- **Détecteur** : ADR, checkpoint, review de pairs

### Reddition Cognitive
- Décisions prises sans justification
- Absence de preuve tangible
- **Détecteur** : Default-FAIL, Evidence Required

### Prompt Drift
- Résultats qui s'écartent du attendu
- **Détecteur** : Semantic Drift Detector (ATOM-015)

## Lutte

### Contre-mesures

1. **Avocat du Diable** : toujours une revue critique
2. **Maker-Checker** : deux acteurs minimum
3. **Default-FAIL** : rejet par défaut
4. **Evidence Required** : preuve avant validation
5. **Checkpoint** : état persistant et vérifiable
6. **ADR** : documentation des décisions

### Règles de combat

- **Règle 1** : Un acteur ne valide jamais son propre travail
- **Règle 2** : Tout succès a besoin d'une preuve
- **Règle 3** : Le système est cassé jusqu'à preuve du contraire
- **Règle 4** : Les décisions sont documentées dans des ADR signés

## Exemple de lutte

```
Scénario : Un agent propose un changement

1. Maker crée le changement
2. Avocat du Diable le critique
3. Si problème → itération
4. Si OK → collecte des preuves (ATOM-028)
5. Signature ADR (ATOM-016)
6. Commit avec Conventional Commits (ATOM-020)
7. Merge sur ENV2 (ATOM-033)
```