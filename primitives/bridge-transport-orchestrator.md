# Primitive: bridge-transport-orchestrator

## IntentHash
0xPRIMITIVE_BRIDGE_TRANSPORT_ORCHESTRATOR_20260930

## Contexte
PRD-027/MOC-028 : activation des transports optionnels WAZAA et BOINC-LLM-P2P
pour les bridges auto-dev. La racine est la nécessité d'orchestrer plusieurs transports
avec fallback WAL automatique.

## Règle
Tout bridge avec `transport: wazaa` ou `transport: boinc-p2p` DOIT être orchestré
par `BridgeExecutor` qui gère :
1. Publication vers le transport déclaré
2. Fallback WAL local si transport injoignable
3. Retry asynchrone pour les transports disponibles
4. Traçabilité IntentHash dans chaque événement

## Check-list

### 1. Validation bridge YAML
```powershell
# Vérifier la présence de transport_topic (wazaa) ou transport_endpoint (boinc-p2p)
Select-String -Path "<bridge.yaml>" -Pattern "transport_(topic|endpoint)"
```
- Si `transport: wazaa` → `transport_topic` obligatoire
- Si `transport: boinc-p2p` → `transport_endpoint` obligatoire
- Si `transport` absent → local only, pas de publication

### 2. Publication transport
```python
# WAZAA : POST /events avec header X-WAZAA-Token
# BOINC : POST /internal/* avec payload JSON
# Les deux acceptent 200/202 comme succès
```

### 3. Fallback WAL
```python
# Si transport retourne None (down/timeout/5xx) :
# Écrire dans WAL local pour retry ultérieur
# Format : {timestamp, bridge_name, payload, transport}
```

### 4. Traçabilité
- Chaque événement publié → `event_id: auto-dev-<hex8>`
- Chaque événement WAL → `intent_hash` du bridge
- drift_alerter → `BridgeExecutor._publish_wazaa` avec topic `drift.critical`

## Anti-patterns
- Publier sans vérifier le retour HTTP (200/202)
- Ignorer le fallback WAL si transport down
- Oublier `X-WAZAA-Token` pour WAZAA
- Utiliser `transport: wazaa` sans `transport_topic`

## Sortie attendue
- 100% des bridges avec transport publiés ou WALés
- 0 perte d'événement (WAZAA down → WAL local)
- drift_alerter connecté et testé
