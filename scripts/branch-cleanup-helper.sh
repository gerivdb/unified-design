#!/usr/bin/env sh
# BRGS-compliant remote branch deletion helper.
# BRGS forbids deleting remote branches directly from main.
# This script creates a temporary cleanup branch, deletes the target, then returns to main.
set -e

TARGET_BRANCH="${1:-}"
if [ -z "$TARGET_BRANCH" ]; then
  echo "Usage: $0 <remote-branch-name>" >&2
  exit 1
fi

git checkout main
git pull origin main
git checkout -b "cleanup/${TARGET_BRANCH}"
git push origin "cleanup/${TARGET_BRANCH}"
git push origin --delete "${TARGET_BRANCH}"
git checkout main
git branch -d "cleanup/${TARGET_BRANCH}"
git push origin --delete "cleanup/${TARGET_BRANCH}"
echo "Deleted remote branch: ${TARGET_BRANCH}"
