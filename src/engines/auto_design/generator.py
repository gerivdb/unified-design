"""Re-export AutoDesignGenerator from engine.auto_design.generator for src/ compatibility."""

from engine.auto_design.generator import AutoDesignGenerator, generate_repo

__all__ = ["AutoDesignGenerator", "generate_repo"]
