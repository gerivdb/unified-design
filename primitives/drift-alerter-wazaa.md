# Primitive: drift-alerter-wazaa

## IntentHash
0xPRIMITIVE_DRIFT_ALERTER_WAZAA_20260930

## Contexte
PRD-027/MOC-028 : connexion de `drift_alerter.py` à WAZAA bus pour publication
temps réel des alertes drift critiques. La racine est la nécessité de notifier
l'écosystème en temps réel quand un bridge drift critique est détecté.

## Règle
Tout drift critique détecté par `DriftAlerter` DOIT être publié sur WAZAA topic
`drift.critical` via `BridgeExecutor._publish_wazaa`. Les drifts non critiques
sont loggés localement uniquement.

## Check-list

### 1. Détection drift critique
```python
# Dans drift_alerter.py :
# critical_drifts = [d for d in drifts if d.severity == "critical"]
# Pour chaque drift critique :
#   executor._publish_wazaa(
#       data={"transport_topic": "drift.critical", "intent_hash": ""},
#       bridge_name="AUTO-DEV-DRIFT-ALERT",
#       payload=drift_payload
#   )
```

### 2. Format payload WAZAA
```json
{
  "event_type": "drift.AUTO-DEV-DRIFT-ALERT",
  "topic": "drift.critical",
  "payload": {
    "bridge": "<bridge_name>",
    "metric": "<metric_name>",
    "current": <current_value>,
    "threshold": <threshold_value>,
    "severity": "critical",
    "timestamp": "<ISO-UTC>"
  }
}
```

### 3. Fallback local
```python
# Si WAZAA down → log dans drift_alerter_wazaa_wal.jsonl
# Format identique au payload ci-dessus
```

### 4. Tests
```python
# test_drift_alerter_wazaa.py :
# - test_no_critical_drifts : pas de publication
# - test_critical_drifts_published_to_wazaa : publication vérifiée
```

## Anti-patterns
- Publier les drifts non critiques sur WAZAA (spam)
- Oublier `transport_topic: drift.critical`
- Ne pas gérer le fallback WAL si WAZAA down
- Utiliser un bridge_name générique sans préfixe AUTO-DEV

## Sortie attendue
- 100% des drifts critiques publiés sur WAZAA
- 0 drift critique perdu (WAL fallback)
- drift_alerter connecté et testé
