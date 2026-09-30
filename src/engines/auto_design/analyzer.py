"""Re-export AutoDesignAnalyzer from engine.auto_design.analyzer for src/ compatibility."""

from engine.auto_design.analyzer import AutoDesignAnalyzer, analyze_repo

__all__ = ["AutoDesignAnalyzer", "analyze_repo"]
