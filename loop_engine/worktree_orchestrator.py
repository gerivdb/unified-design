#!/usr/bin/env python3
"""
worktree_orchestrator.py - Orchestration git worktree pour isolation agents
Chaque agent reçoit son worktree privé avec dry-run merge avant fusion.
"""

from __future__ import annotations

import asyncio
import logging
import shutil
import subprocess
import tempfile
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class WorktreeConfig:
    """Configuration worktree agent."""
    base_repo: Path
    max_parallel: int = 8
    dry_run_before_merge: bool = True
    abort_on_conflict: bool = True
    cleanup_on_complete: bool = True
    worktree_prefix: str = "agent-"


@dataclass
class AgentWorktree:
    """Représente un worktree alloué à un agent."""
    agent_id: str
    path: Path
    branch: str
    base_commit: str
    created_at: float
    status: str = "active"  # active | merging | completed | failed


class WorktreeOrchestrator:
    """
    Gère le cycle de vie des worktrees pour isolation parallèle d'agents.
    - Création worktree par agent
    - Dry-run merge (test application propre)
    - Merge réel ou rollback
    - Nettoyage automatique
    """
    
    def __init__(self, config: Optional[WorktreeConfig] = None):
        self.config = config or WorktreeConfig(Path.cwd())
        self.active_worktrees: dict[str, AgentWorktree] = {}
        self._validate_repo()
    
    def _validate_repo(self):
        """Vérifie que le repo de base est valide."""
        if not (self.config.base_repo / ".git").exists():
            raise ValueError(f"Not a git repo: {self.config.base_repo}")
        # Vérifier qu'on est sur une branche (pas detached HEAD)
        result = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            cwd=self.config.base_repo,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise ValueError("Repository in detached HEAD state - checkout a branch first")
    
    def _run_git(self, args: list[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
        """Execute une commande git."""
        return subprocess.run(
            ["git"] + args,
            cwd=cwd or self.config.base_repo,
            capture_output=True,
            text=True
        )
    
    async def create_worktree(self, agent_id: str, base_branch: str = "main") -> AgentWorktree:
        """
        Crée un worktree isolé pour un agent.
        Returns AgentWorktree avec chemin et branche.
        """
        if len(self.active_worktrees) >= self.config.max_parallel:
            raise RuntimeError(f"Max parallel worktrees ({self.config.max_parallel}) reached")
        
        # Générer nom unique
        short_id = str(uuid.uuid4())[:8]
        branch_name = f"{self.config.worktree_prefix}{agent_id}-{short_id}"
        worktree_path = self.config.base_repo.parent / f"{branch_name}"
        
        # Créer la branche depuis base_branch
        result = self._run_git(["branch", branch_name, base_branch])
        if result.returncode != 0:
            raise RuntimeError(f"Failed to create branch: {result.stderr}")
        
        # Créer le worktree
        result = self._run_git(["worktree", "add", str(worktree_path), branch_name])
        if result.returncode != 0:
            # Nettoyer la branche si worktree échoue
            self._run_git(["branch", "-D", branch_name])
            raise RuntimeError(f"Failed to create worktree: {result.stderr}")
        
        # Obtenir commit de base
        base_commit = self._run_git(["rev-parse", base_branch], cwd=worktree_path).stdout.strip()
        
        worktree = AgentWorktree(
            agent_id=agent_id,
            path=worktree_path,
            branch=branch_name,
            base_commit=base_commit,
            created_at=asyncio.get_event_loop().time()
        )
        self.active_worktrees[agent_id] = worktree
        
        logger.info(f"Created worktree for agent {agent_id}: {worktree_path} (branch: {branch_name})")
        return worktree
    
    async def dry_run_merge(self, agent_id: str, target_branch: str = "main") -> tuple[bool, str]:
        """
        Effectue un dry-run de merge (git merge --no-commit --no-ff --dry-run).
        Returns (success, message).
        """
        worktree = self.active_worktrees.get(agent_id)
        if not worktree:
            return False, f"No worktree for agent {agent_id}"
        
        worktree.status = "merging"
        
        # Vérifier que la target branch existe
        result = self._run_git(["rev-parse", "--verify", target_branch], cwd=worktree.path)
        if result.returncode != 0:
            return False, f"Target branch {target_branch} not found"
        
        # Dry-run merge
        result = self._run_git([
            "merge", "--no-commit", "--no-ff", "--dry-run", target_branch
        ], cwd=worktree.path)
        
        if result.returncode != 0:
            worktree.status = "failed"
            msg = f"Dry-run merge failed: {result.stderr}"
            if self.config.abort_on_conflict:
                msg += " (abort_on_conflict=true)"
            return False, msg
        
        worktree.status = "active"
        return True, "Dry-run merge successful - no conflicts"
    
    async def commit_and_merge(self, agent_id: str, message: str, target_branch: str = "main") -> tuple[bool, str]:
        """
        Commit les changements dans le worktree et merge vers target_branch.
        Prérequis: dry_run_merge doit avoir réussi.
        """
        worktree = self.active_worktrees.get(agent_id)
        if not worktree:
            return False, f"No worktree for agent {agent_id}"
        
        # Vérifier qu'il y a des changements
        status = self._run_git(["status", "--porcelain"], cwd=worktree.path)
        if not status.stdout.strip():
            return False, "No changes to commit"
        
        # Commit
        result = self._run_git(["add", "-A"], cwd=worktree.path)
        if result.returncode != 0:
            return False, f"git add failed: {result.stderr}"
        
        result = self._run_git(["commit", "-m", message], cwd=worktree.path)
        if result.returncode != 0:
            return False, f"git commit failed: {result.stderr}"
        
        # Merge vers target (depuis le repo principal pour avoir l'historique)
        result = self._run_git(["merge", "--no-ff", worktree.branch, "-m", f"Merge {worktree.branch}: {message}"])
        if result.returncode != 0:
            return False, f"Merge failed: {result.stderr}"
        
        worktree.status = "completed"
        logger.info(f"Agent {agent_id} merged successfully to {target_branch}")
        return True, f"Merged to {target_branch}"
    
    async def cleanup_worktree(self, agent_id: str, force: bool = False) -> bool:
        """Supprime le worktree et la branche associée."""
        worktree = self.active_worktrees.get(agent_id)
        if not worktree:
            return True
        
        # Vérifier si on peut supprimer (pas de changements non commits sauf si force)
        if not force:
            status = self._run_git(["status", "--porcelain"], cwd=worktree.path)
            if status.stdout.strip():
                logger.warning(f"Worktree {agent_id} has uncommitted changes, use force=True")
                return False
        
        # Supprimer worktree
        result = self._run_git(["worktree", "remove", "--force", str(worktree.path)])
        if result.returncode != 0:
            logger.error(f"Failed to remove worktree: {result.stderr}")
            return False
        
        # Supprimer branche
        result = self._run_git(["branch", "-D", worktree.branch])
        if result.returncode != 0:
            logger.warning(f"Failed to delete branch: {result.stderr}")
        
        del self.active_worktrees[agent_id]
        logger.info(f"Cleaned up worktree for agent {agent_id}")
        return True
    
    async def cleanup_all(self, force: bool = False):
        """Nettoie tous les worktrees actifs."""
        for agent_id in list(self.active_worktrees.keys()):
            await self.cleanup_worktree(agent_id, force=force)
    
    def get_worktree(self, agent_id: str) -> Optional[AgentWorktree]:
        """Retourne le worktree d'un agent."""
        return self.active_worktrees.get(agent_id)
    
    def list_worktrees(self) -> list[AgentWorktree]:
        """Liste tous les worktrees actifs."""
        return list(self.active_worktrees.values())


async def demo():
    """Demo de l'orchestrateur."""
    logging.basicConfig(level=logging.INFO)
    
    # Utiliser un repo temp pour demo
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Path(tmpdir) / "demo_repo"
        repo.mkdir()
        
        # Init repo
        subprocess.run(["git", "init"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, capture_output=True)
        
        # Commit initial
        (repo / "README.md").write_text("# Demo\n")
        subprocess.run(["git", "add", "."], cwd=repo, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial"], cwd=repo, capture_output=True)
        
        config = WorktreeConfig(base_repo=repo, max_parallel=3)
        orchestrator = WorktreeOrchestrator(config)
        
        # Creer worktree agent
        wt = await orchestrator.create_worktree("agent-001")
        print(f"Worktree: {wt.path}")
        print(f"Branch: {wt.branch}")
        
        # Simuler travail
        (wt.path / "agent_work.txt").write_text("Agent output\n")
        
        # Dry-run merge
        ok, msg = await orchestrator.dry_run_merge("agent-001")
        print(f"Dry-run: {ok} - {msg}")
        
        if ok:
            # Commit + merge
            ok, msg = await orchestrator.commit_and_merge("agent-001", "Agent 001 work")
            print(f"Merge: {ok} - {msg}")
        
        # Cleanup
        await orchestrator.cleanup_worktree("agent-001")
        print("Cleanup done")


if __name__ == "__main__":
    asyncio.run(demo())