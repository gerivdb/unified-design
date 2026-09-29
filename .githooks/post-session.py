#!/usr/bin/env python3
# .githooks/post-session.py
# Hook post-session pour auto-commit/push automatique LOOPX.
# IntentHash: 0xPRD_MOC_LOOPX_AUTO_COMMIT_20260929
#
# Déclencheur : fin de session agentique LOOPX.
# Action : git status → git add (max 3 fichiers/commit) → git commit → git push.
# Si échec : log + HITL immédiat.

from __future__ import annotations

import subprocess
import sys
import os
import json
import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
MAX_FILES_PER_COMMIT = 3
MAX_MINUTES_WITHOUT_COMMIT = 30
GITIGNORE_PATH = REPO_ROOT / ".gitignore"
HOOK_LOG_PATH = REPO_ROOT / "reports" / "post-session-hook.log"

# Protections: ces chemins/dossiers ne doivent JAMAIS être ajoutés à .gitignore
PROTECTED_PATTERNS = [
    ".githooks",
    "PRD-MOC",
    "PRD-MOC/",
    "src/",
    "tests/",
    "docs/",
    "scripts/",
    "*.md",
    "*.py",
    "*.yaml",
    "*.yml",
    "*.json",
    "*.toml",
]


def run_git(args: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Exécute une commande git dans le repo root."""
    return subprocess.run(
        ["git"] + args,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=check,
    )


def log(message: str) -> None:
    """Log dans un fichier dédié + stdout."""
    timestamp = datetime.datetime.now().isoformat()
    line = f"[POST-SESSION] {timestamp} {message}"
    print(line)
    try:
        HOOK_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(HOOK_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def get_git_status() -> Dict[str, Any]:
    """Retourne status, modified, untracked, deleted."""
    status_proc = run_git(["status", "--short"], check=False)
    modified = []
    untracked = []
    deleted = []
    for line in status_proc.stdout.splitlines():
        if not line.strip():
            continue
        code = line[:2]
        path = line[3:]
        if code == "M ":
            modified.append(path)
        elif code == "??":
            untracked.append(path)
        elif code == "D ":
            deleted.append(path)
    return {
        "modified": modified,
        "untracked": untracked,
        "deleted": deleted,
        "total": len(modified) + len(untracked) + len(deleted),
    }


def is_protected(candidate: str) -> bool:
    """Retourne True si le candidat ne doit pas être ajouté à .gitignore."""
    for pattern in PROTECTED_PATTERNS:
        if candidate == pattern or candidate.startswith(pattern.rstrip("/")):
            return True
    return False


def sync_gitignore(candidates: List[str]) -> List[str]:
    """Ajoute les candidates à .gitignore si manquants et non protégés. Retourne la liste ajoutée."""
    if not GITIGNORE_PATH.exists():
        return []
    current = GITIGNORE_PATH.read_text(encoding="utf-8").splitlines()
    added = []
    for candidate in candidates:
        if candidate in current:
            continue
        if is_protected(candidate):
            log(f"gitignore SKIP protected: {candidate}")
            continue
        current.append(candidate)
        added.append(candidate)
    if added:
        GITIGNORE_PATH.write_text("\n".join(current) + "\n", encoding="utf-8")
        log(f"gitignore updated: {added}")
    return added


def atomic_commit(files: List[str], message: str) -> Optional[str]:
    """Commit atomique (max 3 fichiers). Retourne le hash ou None."""
    if not files:
        return None
    if len(files) > MAX_FILES_PER_COMMIT:
        log(f"BLOCKED: too many files for atomic commit: {len(files)} > {MAX_FILES_PER_COMMIT}")
        return None
    try:
        for f in files:
            run_git(["add", f], check=True)
        run_git(["commit", "-m", message], check=True)
        hash_proc = run_git(["rev-parse", "HEAD"], check=True)
        return hash_proc.stdout.strip()[:8]
    except subprocess.CalledProcessError as e:
        log(f"COMMIT FAILED: {e.stderr}")
        return None


def safe_push(branch: str = "main") -> bool:
    """Push sécurisé sans force. Retourne True si OK."""
    try:
        remote_proc = run_git(["remote", "-v"], check=False)
        if "origin" not in remote_proc.stdout:
            log("PUSH SKIPPED: no origin remote")
            return False
        run_git(["push", "origin", branch], check=True)
        return True
    except subprocess.CalledProcessError as e:
        log(f"PUSH FAILED: {e.stderr}")
        return False


def hitl_on_failure(reason: str) -> None:
    """Log HITL et écrit un fichier d'alerte."""
    alert_path = REPO_ROOT / "reports" / "post-session-hitl-alert.md"
    try:
        alert_path.parent.mkdir(parents=True, exist_ok=True)
        alert_path.write_text(
            f"# HITL Alert — {datetime.datetime.now().isoformat()}\n\n"
            f"**Reason**: {reason}\n\n"
            "Action requise : vérifier git status + résoudre manuellement.\n",
            encoding="utf-8",
        )
    except Exception:
        pass
    log(f"HITL REQUIRED: {reason}")


def main() -> int:
    log("post-session hook started")
    status = get_git_status()

    if status["total"] == 0:
        log("working tree clean, nothing to do")
        return 0

    log(f"changes detected: {status['total']} (modified={len(status['modified'])}, untracked={len(status['untracked'])}, deleted={len(status['deleted'])})")

    # Sync .gitignore for untracked candidates
    sync_gitignore(status["untracked"])

    # Re-read status after gitignore sync
    status = get_git_status()
    all_changes = status["modified"] + status["untracked"] + status["deleted"]
    if not all_changes:
        log("no changes after gitignore sync")
        return 0

    # Atomic commits (max 3 files each)
    commit_hashes: List[str] = []
    for i in range(0, len(all_changes), MAX_FILES_PER_COMMIT):
        batch = all_changes[i : i + MAX_FILES_PER_COMMIT]
        message = f"chore(auto-commit): session changes ({len(batch)} files)"
        commit_hash = atomic_commit(batch, message)
        if commit_hash:
            commit_hashes.append(commit_hash)
            log(f"committed {len(batch)} files → {commit_hash}")
        else:
            hitl_on_failure(f"atomic commit failed for batch {i//MAX_FILES_PER_COMMIT + 1}")
            return 1

    # Push
    branch_proc = run_git(["rev-parse", "--abbrev-ref", "HEAD"], check=False)
    branch = branch_proc.stdout.strip() or "main"
    if not safe_push(branch):
        hitl_on_failure("git push failed")
        return 1

    log(f"post-session hook completed: {len(commit_hashes)} commit(s) pushed to {branch}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
