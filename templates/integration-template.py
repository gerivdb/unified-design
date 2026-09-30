#!/usr/bin/env python3
"""
Integration template for unified-design consumers.
This template is used by the integration framework to generate integration modules.
"""

import sys
from pathlib import Path

# Add the unified-design PRD directory to the path
prd_dir = Path(__file__).parent.parent / "PRD"
sys.path.insert(0, str(prd_dir))

from {{DESIGN_SLUG}} import {{CLASS_NAME}}


class {{CLASS_NAME}}Integration:
    """Integration wrapper for {{DESIGN_NAME}}."""

    def __init__(self):
        self.{{DESIGN_SLUG}} = {{CLASS_NAME}}()

    def validate(self, context: dict) -> dict:
        """Validate using {{DESIGN_NAME}}."""
        return self.{{DESIGN_SLUG}}.{{INSTANCE_METHOD}}(context)

    def check_and_execute(self, context: dict, action_func) -> dict:
        """Check {{DESIGN_NAME}} then execute action if allowed."""
        validation = self.validate(context)
        if validation.get("{{RESPONSE_FIELD}}") == "{{ALLOW_VALUE}}":
            result = action_func(context)
            return {"validation": validation, "execution": result}
        else:
            return {"validation": validation, "execution": None}


_{{DESIGN_SLUG}}_integration = None


def get_{{DESIGN_SLUG}}_integration() -> {{CLASS_NAME}}Integration:
    """Get or create singleton instance."""
    global _{{DESIGN_SLUG}}_integration
    if _{{DESIGN_SLUG}}_integration is None:
        _{{DESIGN_SLUG}}_integration = {{CLASS_NAME}}Integration()
    return _{{DESIGN_SLUG}}_integration


if __name__ == "__main__":
    # Quick smoke test
    integration = get_{{DESIGN_SLUG}}_integration()
    test_context = {
        "intent_hash": "0xTEST_{{DESIGN_SLUG.upper()}}",
        "consumer": "{{CONSUMER_NAME}}",
    }
    result = integration.validate(test_context)
    print(f"[{{DESIGN_NAME}}] Validation result: {result}")
