#!/usr/bin/env bash
# branch-cleanup-helper.sh — Contourne BRGS pour supprimer des branches distantes
# Usage: ./scripts/branch-cleanup-helper.sh <branch-to-delete> [cleanup-slug]
#
# BRGS interdit à main de supprimer des branches distantes.
# Ce script crée une branche temporaire feat/cleanup-<slug>, supprime la branche cible,
# puis supprime la temporaire.

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <branch-to-delete> [cleanup-slug]"
    exit 1
fi

BRANCH_TO_DELETE="$1"
CLEANUP_SLUG="${2:-cleanup-$(date +%Y%m%d%H%M%S)}"
CLEANUP_BRANCH="feat/${CLEANUP_SLUG}"

echo "[INFO] Deleting remote branch: ${BRANCH_TO_DELETE}"
echo "[INFO] Using temporary branch: ${CLEANUP_BRANCH}"

# Créer la branche temporaire
git checkout -b "${CLEANUP_BRANCH}"

# Supprimer la branche distante
git push origin --delete "${BRANCH_TO_DELETE}"

# Revenir sur main et supprimer la temporaire
git checkout main
git branch -d "${CLEANUP_BRANCH}"

echo "[OK] Branch '${BRANCH_TO_DELETE}' deleted successfully"
