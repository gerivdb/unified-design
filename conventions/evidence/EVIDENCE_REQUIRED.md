---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_028_EVIDENCE_REQUIRED
---

# ATOM-028 : Preuve Tangible Obligatoire (EvidenceType)

## Principe

Toute validation de phase doit être accompagnée d'au moins un EvidenceType.
Le checkpoint `.mdu/checkpoint.json` doit lister les preuves produites.

## Types de preuves acceptés

| Type | Exemple | Format |
|------|---------|--------|
| `log` | Sortie console, benchmark (tok/s, RSS) | Fichier texte |
| `screenshot` | Capture d'écran du résultat | PNG/JPG |
| `video` | Enregistrement PLIX ou équivalent | MP4/WebM |
| `diff` | Diff unifié avant/après | Texte |
| `hash` | Empreinte SHA256 d'un artefact | Hexadécimal |
| `test_output` | Résultat pytest, zig test | JSON/Texte |

## Format du checkpoint

```json
{
  "evidence": [
    {
      "type": "log",
      "path": ".mdu/benchmark_20260717.log",
      "hash": "a1b2c3d4..."
    },
    {
      "type": "test_output",
      "path": ".mdu/pytest_results.json"
    }
  ]
}
```

## Workflow

```
1. Agent exécute une tâche
2. Collecte les preuves (log, test, diff)
3. Écrit dans .mdu/checkpoint.json
4. Hook vérifie la présence d'EvidenceType
5. Si absent → REJECT
```

## Exemple de script

```python
# scripts/collect_evidence.py
import json, hashlib
from pathlib import Path

def collect_evidence(task: str, evidence_type: str, path: str):
    """Collect and record evidence for a task."""
    with open(path, 'rb') as f:
        h = hashlib.sha256(f.read()).hexdigest()
    
    evidence = {
        "task": task,
        "type": evidence_type,
        "path": path,
        "hash": h,
        "timestamp": "2026-07-17T21:10:00Z"
    }
    
    with open('.mdu/checkpoint.json', 'a') as f:
        f.write(json.dumps(evidence) + '\n')
```