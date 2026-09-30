"""Re-export AutoDesignReporter from engine.auto_design.reporter for src/ compatibility."""

from engine.auto_design.reporter import AutoDesignReporter, report_global

__all__ = ["AutoDesignReporter", "report_global"]
