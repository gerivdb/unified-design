#!/bin/bash
# start_tlm_lang.sh — Démarre le service TLM-LANG Validator
# Dépend de RLM-243 (port 8793) pour la validation ternaire

set -e

TLM_PORT=${TLM_PORT:-8801}
TLM_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[TLM-LANG] Démarrage du service TLM-LANG Validator..."
echo "[TLM-LANG] Port : $TLM_PORT"
echo "[TLM-LANG] Répertoire : $TLM_DIR"

# Vérifier que RLM-243 est accessible
echo "[TLM-LANG] Vérification RLM-243..."
curl -sf http://localhost:8793/health > /dev/null 2>&1 && echo "[TLM-LANG] RLM-243 OK" || echo "[TLM-LANG] Avertissement : RLM-243 inaccessible"

# Démarrer le validator Flask
echo "[TLM-LANG] Lancement du validator sur le port $TLM_PORT..."
cd "$TLM_DIR"
export PYTHONPATH="$TLM_DIR"
python -m src.validator --port "$TLM_PORT" 2>&1 || python src/validator.py 2>&1

echo "[TLM-LANG] Service arrêté."