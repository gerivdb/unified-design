#!/bin/bash

# Validation locale du meta-design

# 1. Installer les dependances
pip install pyyaml jsonschema

# 2. Verifier les fichiers
if [ ! -f meta-design.yaml ]; then
    echo "[ERREUR] meta-design.yaml absent"
    exit 1
fi
if [ ! -f schemas/meta-design.schema.json ]; then
    echo "[ERREUR] meta-design.schema.json absent"
    exit 1
fi

# 3. Executer la validation
python scripts/validate_meta_design.py \
    --schema schemas/meta-design.schema.json \
    meta-design.yaml

# 4. Retourner le resultat
if [ $? -eq 0 ]; then
    echo "[OK] Validation reussie"
    exit 0
else
    echo "[ERREUR] Validation echoue"
    exit 1
fi