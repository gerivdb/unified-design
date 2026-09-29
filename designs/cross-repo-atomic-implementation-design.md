# Design: cross-repo-atomic-implementation

## IntentHash
0xDESIGN_CROSS_REPO_ATOMIC_IMPLEMENTATION_20260930

## Contexte
Implémentation cross-repo de PRD-027 (WAZAA/BOINC transport) nécessite une coordination
atomique entre auto-dev (L2) et BOINC-LLM-P2P (L1). La racine est la nécessité de
décomposer les tâches cross-repo en unités atomiques SLM-compatibles.

## Architecture

```
[auto-dev]                          [BOINC-LLM-P2P]
    │                                    │
    ├── bridge_executor.py              ├── src/health.py
    │   └── _publish_wazaa()            │   └── /internal/*
    │   └── _publish_boinc_p2p()        │
    │                                    │
    └── tests/                          └── tests/
        └── test_wazaa_transport.py        └── test_internal_endpoints.py
        └── test_boinc_transport.py
```

## Protocole atomique

### Tâche 1 : Implémenter publisher (auto-dev)
- Pattern D : edit `agents/bridge_executor.py`
- Validation : `tests/test_wazaa_transport.py` pass
- Commit : `feat(transport): implement WAZAA publisher`

### Tâche 2 : Implémenter endpoints (BOINC-LLM-P2P)
- Pattern C : write `src/health.py` (ajouter endpoints)
- Validation : `tests/test_internal_endpoints.py` pass
- Commit : `feat(internal): add /internal/* endpoints`

### Tâche 3 : Configurer bridges (auto-dev)
- Pattern D : edit 2 bridge YAMLs
- Validation : `bridge_executor.execute_all()` publie
- Commit : `feat(bridges): add transport wazaa`

### Tâche 4 : Connecter drift_alerter (auto-dev)
- Pattern D : edit `agents/drift_alerter.py`
- Validation : `tests/test_drift_alerter_wazaa.py` pass
- Commit : `feat(drift): connect drift_alerter to WAZAA`

### Tâche 5 : Tests e2e + fallback (auto-dev)
- Pattern C : write 4 test files
- Validation : `pytest` 22/22 pass
- Commit : `test(transport): add e2e + fallback tests`

## Garde-fous
- Un commit = un livrable atomique
- Max 3 fichiers modifiés par commit
- Max 30min sans commit
- Tests pass avant chaque commit
- dry-run causal avant push

## Sortie attendue
- 5 commits atomiques
- 26/26 tests pass
- 0 régression
