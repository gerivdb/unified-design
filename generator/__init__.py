"""
Compatibility imports for src/generators migration.
Preserves legacy imports from generator.* while code migrates to src/generators/*.
"""

from src.generators.create_design import *
from src.generators.validate_inheritance import *

__all__ = []
