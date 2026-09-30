# Primitive: transport-fallback-wal

## IntentHash
0xPRIMITIVE_TRANSPORT_FALLBACK_WAL_20260930

## Contexte
PRD-027/MOC-028 : fallback WAL local quand WAZAA ou BOINC-LLM-P2P est injoignable.
La racine est la garantie de non-perte d'événements même en cas de panne transport.

## Règle
Tout échec de publication transport (down, timeout, 5xx) DOIT déclencher une écriture
WAL locale avec rejeu asynchrone dès que le transport est disponible.

## Check-list

### 1. Détection d'échec
```python
# _publish_wazaa retourne None si :
# - ConnectionError (transport down)
# - Timeout (> 2s)
# - HTTP 5xx
# _publish_boinc_p2p retourne None si :
# - Mêmes conditions ci-dessus
```

### 2. Écriture WAL
```python
# Format WAL :
wal_entry = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "bridge_name": bridge_name,
    "transport": transport_type,
    "payload": payload,
    "intent_hash": data.get("intent_hash", ""),
    "retry_count": 0
}
# Append dans <auto-dev-root>/wal/transport-fallback.jsonl
```

### 3. Rejeu asynchrone
```python
# Au démarrage de BridgeExecutor :
# 1. Lire WAL
# 2. Trier par timestamp
# 3. Réessayer chaque entrée (max 3 retries)
# 4. Supprimer les entrées rejouées avec succès
```

### 4. Protection concurrence
```python
# Utiliser un fichier lock pour éviter les écritures concurrentes :
# <wal_path>.lock
# Avec timeout de 5s max pour éviter les deadlocks
```

## Anti-patterns
- Écrire None dans WAL (valeur vide)
- Ignorer les retry_count (boucle infinie)
- Oublier de supprimer les entrées rejouées
- WAL sans limite de taille (croissance illimitée)

## Sortie attendue
- 0 événement perdu même si WAZAA/BOINC down pendant 24h
- WAL max 1000 entrées (rotation automatique)
- Rejeu dans les 5min suivant la restauration du transport
