"""Re-export AutoDesignVerifier from engine.auto_design.verifier for src/ compatibility."""

from engine.auto_design.verifier import AutoDesignVerifier, verify_repo

__all__ = ["AutoDesignVerifier", "verify_repo"]
