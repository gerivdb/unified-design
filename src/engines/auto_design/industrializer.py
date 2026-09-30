"""Re-export AutoDesignIndustrializer from engine.auto_design.industrializer for src/ compatibility."""

from engine.auto_design.industrializer import AutoDesignIndustrializer, deploy_repo

__all__ = ["AutoDesignIndustrializer", "deploy_repo"]
