---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_040_DISTRIBUTED_SEEKER_AGENTS
---

# ATOM-040 : Distributed Seeker Agents (Plasticité Locale)

## Principe fondamental

Chaque dépôt peut exécuter un "Seeker Agent" local qui scanne le dépôt et publie ses découvertes. Cette approche distribuée évite le point unique de défaillance et s'adapte à la croissance de l'écosystème.

## Architecture

```
[Dépôt 1] ──.seeker/scan──┐
[Dépôt 2] ──.seeker/scan──┤
[Dépôt 3] ──.seeker/scan──┤  ┌──────────────┐
   ...              ──────┼─▶│  FLUENCE     │
[Dépôt N] ──.seeker/scan──┘  │  Orchestrator│
                              │  Consolidation│
                              └──────┬───────┘
                                     │
                                     ▼
                           [NEXUS/ECOS_ROOT.json]
                           [WAL — design_gaps]
```

## Configuration locale

Chaque dépôt peut activer son seeker avec `.seeker/config.yaml` :

```yaml
# .seeker/config.yaml
enabled: true
phases:
  - scan
  - discovery
  - report
output: .seeker/local_report.json
schedule: "0 */6 * * *"  # Toutes les 6h
```

## Règles associées

### Règle S1 — Activité locale
- Un seeker ne doit jamais dépendre du réseau pour fonctionner
- Les résultats locaux sont toujours persistés
- Pas de requête à distance pendant le scan

### Règle S2 — Consolidation FLUENCE
- FLUENCE consolide les rapports toutes les 24h
- Détection des doublons (même gap dans plusieurs dépôts)
- Score agrégé (moyenne pondérée par taille du dépôt)

### Règle S3 — Fallback automatique
- Si FLUENCE est inaccessible > 24h : les agents continuent localement
- Un fichier `.seeker/pending_sync` stocke les rapports non envoyés
- À la reconnexion, FLUENCE consomme le backlog

### Règle S4 — Redondance
- Chaque gap détecté est attribué à un "owner" (dépôt principal)
- Le gap peut être "shared" si pertinent pour plusieurs dépôts

## Format du rapport local

`.seeker/local_report.json` :

```json
{
  "seeker_version": "1.0.0",
  "repo": "gerivdb/unified-design",
  "scan_timestamp": "2026-07-17T22:00:00Z",
  "gaps": [
    {
      "type": "undocumented_workflow",
      "path": "scripts/example.py",
      "description": "Workflow de génération de design",
      "severity": "medium",
      "suggested_action": "Documenter dans ONTOLOGY"
    }
  ],
  "summary": {
    "total_gaps": 1,
    "critical": 0,
    "high": 0,
    "medium": 1,
    "low": 0
  }
}
```

## Activation

### Activation globale

```bash
# Dans le dépôt cible
ln -s .seeker/config.yaml .git/hooks/post-commit
```

### Activation ponctuelle

```bash
python scripts/design_seeker_mvp.py --repo . --output .seeker/local_report.json
```

## Références

- [ATOM-039](ATOM-039-DESIGN_SEEKER_PIPELINE.md) — Pipeline principal
- [Hassani Pattern](ONTOLOGY_MAP.md) — Plasticité synaptique

## Référence ADR

- **ADR** : ADR-2026-07-17-007-DISTRIBUTED-SEEKER
- **IntentHash** : 0xATOM_040_DISTRIBUTED_SEEKER_AGENTS_20260717
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR → deprecated ou superseded