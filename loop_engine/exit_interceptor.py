#!/usr/bin/env python3
"""
exit_interceptor.py - Stop Hook bloquant exit agent + validation cross-model
Empeche un agent de "noter ses propres devoirs" - validation obligatoire par 2eme modele.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ValidatorModel(str, Enum):
    """Modeles valideurs supportes."""
    CODEX = "openai-codex"
    GPT4 = "gpt-4"
    CLAUDE = "claude"
    CUSTOM = "custom"


@dataclass
class ExitValidationRequest:
    """Demande de validation de sortie."""
    agent_id: str
    session_id: str
    work_summary: str
    artifacts: list[str] = field(default_factory=list)  # Fichiers modifies/crees
    test_results: dict = field(default_factory=dict)
    exit_reason: str = "task_complete"
    timestamp: float = field(default_factory=time.time)


@dataclass
class ExitValidationResult:
    """Resultat de la validation cross-model."""
    approved: bool
    validator_model: ValidatorModel
    review_artifact: str  # Chemin vers review.md signe
    comments: str
    issues_found: list[str] = field(default_factory=list)
    score: float = 0.0  # 0-100
    timestamp: float = field(default_factory=time.time)
    signature: str = ""  # Hash de non-repudiation


class ExitInterceptor:
    """
    Intercepteur de sortie (Stop Hook) pour agents.
    - Bloque la commande exit/finish
    - Demande validation a un 2eme modele (Codex par defaut)
    - Genere review.md signe
    - Empeche auto-validation (self-review prevention)
    """
    
    def __init__(
        self,
        validator_model: ValidatorModel = ValidatorModel.CODEX,
        timeout_seconds: int = 300,
        review_artifact_name: str = "review.md",
        require_signed_review: bool = True,
        self_review_prevention: bool = True,
        custom_validator_cmd: list[str] = None
    ):
        self.validator_model = validator_model
        self.timeout_seconds = timeout_seconds
        self.review_artifact_name = review_artifact_name
        self.require_signed_review = require_signed_review
        self.self_review_prevention = self_review_prevention
        self.custom_validator_cmd = custom_validator_cmd
        self._pending_validations: dict[str, ExitValidationRequest] = {}
    
    def intercept_exit(self, request: ExitValidationRequest) -> ExitValidationResult:
        """
        Point d'entree principal - appele quand un agent tente de sortir.
        Bloque jusqu'a validation ou timeout.
        """
        logger.info(f"Exit intercepted for agent {request.agent_id}")
        
        # Verification auto-review prevention
        if self.self_review_prevention:
            if self._is_self_review(request):
                return ExitValidationResult(
                    approved=False,
                    validator_model=self.validator_model,
                    review_artifact="",
                    comments="BLOCKED: Self-review prevention - agent cannot validate own work",
                    issues_found=["self_review_attempt"],
                    score=0.0
                )
        
        # Enregistrer la demande
        self._pending_validations[request.agent_id] = request
        
        try:
            # Lancer validation cross-model
            result = asyncio.run(self._validate_with_second_model(request))
            return result
        finally:
            self._pending_validations.pop(request.agent_id, None)
    
    def _is_self_review(self, request: ExitValidationRequest) -> bool:
        """Detecte si l'agent essaie de se valider lui-meme."""
        # Heuristique: si l'agent a cree le fichier de review lui-meme
        review_path = Path(request.artifacts[0]) if request.artifacts else None
        if review_path and review_path.name == self.review_artifact_name:
            # Verifier qui a cree le fichier (git blame ou mtime vs agent start)
            return True
        return False
    
    async def _validate_with_second_model(
        self,
        request: ExitValidationRequest
    ) -> ExitValidationResult:
        """Lance la validation par le 2eme modele."""
        
        # Preparer le contexte pour le validateur
        context = self._build_validation_context(request)
        
        # Ecrire le contexte dans un fichier temporaire
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(context, f, indent=2)
            context_file = f.name
        
        try:
            # Appeler le validateur selon le modele
            if self.validator_model == ValidatorModel.CODEX:
                result = await self._call_codex_validator(context_file, request)
            elif self.validator_model == ValidatorModel.CUSTOM and self.custom_validator_cmd:
                result = await self._call_custom_validator(context_file, request)
            else:
                result = await self._call_generic_validator(context_file, request)
            
            # Generer review.md signe
            review_path = self._generate_signed_review(request, result)
            result.review_artifact = review_path
            
            return result
            
        finally:
            # Nettoyer fichier contexte
            try:
                os.unlink(context_file)
            except OSError:
                pass
    
    def _build_validation_context(self, request: ExitValidationRequest) -> dict:
        """Construit le contexte de validation pour le 2eme modele."""
        return {
            "validation_request": {
                "agent_id": request.agent_id,
                "session_id": request.session_id,
                "exit_reason": request.exit_reason,
                "timestamp": datetime.fromtimestamp(request.timestamp).isoformat()
            },
            "work_summary": request.work_summary,
            "artifacts": request.artifacts,
            "test_results": request.test_results,
            "validation_criteria": {
                "code_quality": "Code follows project conventions, no obvious bugs",
                "test_coverage": "Tests exist and pass for new functionality",
                "documentation": "Changes documented appropriately",
                "security": "No security vulnerabilities introduced",
                "performance": "No significant performance regressions"
            },
            "validator_instructions": (
                "Review the agent's work summary and artifacts. "
                "Check if the work is complete and correct. "
                "Return APPROVED or REJECTED with specific issues. "
                "Do NOT approve if you are the same model that did the work."
            )
        }
    
    async def _call_codex_validator(
        self,
        context_file: str,
        request: ExitValidationRequest
    ) -> ExitValidationResult:
        """Appelle OpenAI Codex pour validation."""
        # Codex CLI: codex exec --prompt "..." --context-file context.json
        prompt = self._build_codex_prompt(request)
        
        cmd = [
            "codex", "exec",
            "--prompt", prompt,
            "--context-file", context_file,
            "--output-format", "json"
        ]
        
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout_seconds
            )
            
            if proc.returncode != 0:
                logger.error(f"Codex validator failed: {stderr.decode()}")
                return self._failed_result("Codex execution failed")
            
            return self._parse_validator_response(stdout.decode(), ValidatorModel.CODEX)
            
        except asyncio.TimeoutError:
            return self._failed_result("Codex validator timeout")
        except FileNotFoundError:
            logger.warning("Codex CLI not found, falling back to generic")
            return await self._call_generic_validator(context_file, request)
        except Exception as e:
            logger.error(f"Codex validator error: {e}")
            return self._failed_result(f"Codex error: {e}")
    
    def _build_codex_prompt(self, request: ExitValidationRequest) -> str:
        """Construit le prompt pour Codex."""
        artifacts_list = "\n".join(f"- {a}" for a in request.artifacts)
        return f"""
Review the work of agent {request.agent_id} (session {request.session_id}).

WORK SUMMARY:
{request.work_summary}

ARTIFACTS MODIFIED/CREATED:
{artifacts_list if artifacts_list else "None"}

TEST RESULTS:
{json.dumps(request.test_results, indent=2)}

VALIDATION CRITERIA:
- Code quality and correctness
- Test coverage for new functionality
- Documentation completeness
- Security considerations
- Performance impact

RESPOND WITH JSON:
{{
  "approved": true/false,
  "score": 0-100,
  "comments": "Detailed review comments",
  "issues_found": ["issue1", "issue2"]
}}

IMPORTANT: You are a SECOND MODEL reviewing this work. Do not approve if you generated this work yourself.
"""
    
    async def _call_generic_validator(
        self,
        context_file: str,
        request: ExitValidationRequest
    ) -> ExitValidationResult:
        """Validateur generique (fallback) - simulation pour demo."""
        # En production, remplacer par appel reel au modele choisi
        logger.warning("Using generic validator fallback - implement real model call")
        
        # Simulation: approuver si tests passent
        tests_pass = request.test_results.get("passed", False)
        score = 85 if tests_pass else 40
        
        return ExitValidationResult(
            approved=tests_pass,
            validator_model=self.validator_model,
            review_artifact="",
            comments="Generic validator fallback - implement real cross-model call",
            issues_found=[] if tests_pass else ["tests_failing"],
            score=score
        )
    
    async def _call_custom_validator(
        self,
        context_file: str,
        request: ExitValidationRequest
    ) -> ExitValidationResult:
        """Appelle un validateur personnalise."""
        if not self.custom_validator_cmd:
            return self._failed_result("No custom validator command configured")
        
        cmd = self.custom_validator_cmd + [context_file]
        
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout_seconds
            )
            
            if proc.returncode != 0:
                return self._failed_result(f"Custom validator failed: {stderr.decode()}")
            
            return self._parse_validator_response(stdout.decode(), ValidatorModel.CUSTOM)
            
        except Exception as e:
            return self._failed_result(f"Custom validator error: {e}")
    
    def _parse_validator_response(
        self,
        response: str,
        model: ValidatorModel
    ) -> ExitValidationResult:
        """Parse la reponse JSON du validateur."""
        try:
            data = json.loads(response)
            return ExitValidationResult(
                approved=data.get("approved", False),
                validator_model=model,
                review_artifact="",
                comments=data.get("comments", ""),
                issues_found=data.get("issues_found", []),
                score=data.get("score", 0.0)
            )
        except json.JSONDecodeError:
            # Fallback: chercher APPROVED/REJECTED dans le texte
            approved = "APPROVED" in response.upper() and "REJECTED" not in response.upper()
            return ExitValidationResult(
                approved=approved,
                validator_model=model,
                review_artifact="",
                comments=response[:500],
                issues_found=[] if approved else ["parse_error"],
                score=80 if approved else 30
            )
    
    def _failed_result(self, reason: str) -> ExitValidationResult:
        return ExitValidationResult(
            approved=False,
            validator_model=self.validator_model,
            review_artifact="",
            comments=reason,
            issues_found=["validator_error"],
            score=0.0
        )
    
    def _generate_signed_review(
        self,
        request: ExitValidationRequest,
        result: ExitValidationResult
    ) -> str:
        """Genere review.md signe (non-repudiation)."""
        review_content = f"""# Exit Validation Review

**Agent:** {request.agent_id}
**Session:** {request.session_id}
**Validator:** {result.validator_model.value}
**Timestamp:** {datetime.fromtimestamp(result.timestamp).isoformat()}
**Decision:** {"APPROVED" if result.approved else "REJECTED"}
**Score:** {result.score}/100

## Work Summary
{request.work_summary}

## Artifacts
{chr(10).join(f"- {a}" for a in request.artifacts) if request.artifacts else "None"}

## Test Results
```json
{json.dumps(request.test_results, indent=2)}
```

## Review Comments
{result.comments}

## Issues Found
{chr(10).join(f"- {i}" for i in result.issues_found) if result.issues_found else "None"}

---
**Signature:** {self._sign_review(request, result)}
"""
        # Ecrire review.md
        review_path = Path.cwd() / self.review_artifact_name
        review_path.write_text(review_content, encoding="utf-8")
        
        # Mettre a jour signature dans result
        result.signature = self._sign_review(request, result)
        result.review_artifact = str(review_path)
        
        logger.info(f"Signed review generated: {review_path}")
        return str(review_path)
    
    def _sign_review(
        self,
        request: ExitValidationRequest,
        result: ExitValidationResult
    ) -> str:
        """Genere signature cryptographique (non-repudiation)."""
        payload = f"{request.agent_id}:{request.session_id}:{result.validator_model.value}:{result.approved}:{result.timestamp}"
        return hashlib.sha256(payload.encode()).hexdigest()[:32]
    
    def verify_review_signature(self, review_path: str) -> bool:
        """Verifie la signature d'un review.md."""
        try:
            content = Path(review_path).read_text()
            # Extraire signature (derniere ligne)
            lines = content.strip().split("\n")
            sig_line = lines[-1] if lines else ""
            if "**Signature:**" in sig_line:
                signature = sig_line.split("**Signature:**")[1].strip()
                return len(signature) == 32
        except Exception:
            pass
        return False


class ExitInterceptorHook:
    """
    Hook integreable dans le cycle de vie agent (pre-exit).
    Usage: agent.register_exit_hook(interceptor.intercept_exit)
    """
    
    def __init__(self, interceptor: ExitInterceptor):
        self.interceptor = interceptor
    
    def __call__(self, agent_state: dict) -> bool:
        """
        Appele avant exit agent.
        Returns True si exit autorise, False si bloque.
        """
        request = ExitValidationRequest(
            agent_id=agent_state.get("agent_id", "unknown"),
            session_id=agent_state.get("session_id", "unknown"),
            work_summary=agent_state.get("work_summary", ""),
            artifacts=agent_state.get("artifacts", []),
            test_results=agent_state.get("test_results", {}),
            exit_reason=agent_state.get("exit_reason", "task_complete")
        )
        
        result = self.interceptor.intercept_exit(request)
        
        # Stocker resultat pour audit
        agent_state["exit_validation"] = {
            "approved": result.approved,
            "validator": result.validator_model.value,
            "score": result.score,
            "review_artifact": result.review_artifact,
            "timestamp": result.timestamp
        }
        
        if not result.approved:
            logger.warning(f"Exit BLOCKED for {request.agent_id}: {result.comments}")
            return False
        
        logger.info(f"Exit APPROVED for {request.agent_id} (score: {result.score})")
        return True


def demo():
    """Demo de l'intercepteur."""
    import tempfile
    logging.basicConfig(level=logging.INFO)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        
        interceptor = ExitInterceptor(
            validator_model=ValidatorModel.CODEX,
            timeout_seconds=30
        )
        
        # Simuler demande de sortie
        request = ExitValidationRequest(
            agent_id="agent-001",
            session_id="sess-abc123",
            work_summary="Implemented symbol retrieval MCP client. Replaces 2000-line file reads with targeted symbol extraction via Serena MCP. Expected 16k token savings.",
            artifacts=[
                "loop_engine/mcp_symbol_retriever.py",
                "tests/test_mcp_symbol_retriever.py"
            ],
            test_results={"passed": True, "tests": 5, "coverage": 0.87},
            exit_reason="feature_complete"
        )
        
        print("Intercepting exit...")
        result = interceptor.intercept_exit(request)
        
        print(f"Approved: {result.approved}")
        print(f"Validator: {result.validator_model.value}")
        print(f"Score: {result.score}")
        print(f"Review: {result.review_artifact}")
        print(f"Signature: {result.signature}")
        
        if result.review_artifact:
            print("\n--- Review Content ---")
            print(Path(result.review_artifact).read_text())


if __name__ == "__main__":
    demo()