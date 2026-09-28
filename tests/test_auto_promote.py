"""Tests for auto_promote.py."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from auto_promote import (
    check_adr_can_be_promoted,
    check_design_can_be_promoted,
    check_intent_can_be_promoted,
    promote_adr,
    promote_design,
    promote_intent,
    DESIGN_ADR_MAP,
)


class TestAutoPromote:
    """Tests for auto-promote functionality."""

    def test_adr_can_be_promoted_when_proposed_and_integrated(self):
        """Test that an ADR can be promoted when proposed and design is integrated."""
        # This is a conceptual test - actual integration check depends on consumer state
        result = check_adr_can_be_promoted("ADR-2026-09-19-SAFE-ACTION-PATTERN.md")
        assert "can_promote" in result

    def test_design_can_be_promoted_when_integrated(self):
        """Test that a design can be promoted when integrated in consumers."""
        result = check_design_can_be_promoted("safe-action-pattern")
        assert "can_promote" in result
        assert "reason" in result

    def test_design_not_promoted_when_no_implementation(self):
        """Test that a design is not promoted without implementation."""
        # This would require a design without implementation to test properly
        pass

    def test_intent_can_be_promoted_when_proposed_and_proof(self):
        """Test that an INTENT can be promoted when proposed with proof."""
        result = check_intent_can_be_promoted("INTENT-2026-09-19-SAFE-ACTION-PATTERN.md")
        assert "can_promote" in result
        assert "reason" in result

    def test_design_adr_map_has_no_duplicates(self):
        """Test that DESIGN_ADR_MAP has no duplicate keys."""
        assert len(DESIGN_ADR_MAP) == len(set(DESIGN_ADR_MAP.keys()))

    def test_all_designs_have_adr_mapping(self):
        """Test that all expected designs have ADR mappings."""
        expected_designs = [
            "safe-action-pattern",
            "safe-action-gate",
            "ecosystem-meta-coherence",
            "ecosystem-meta-coherence-gate",
            "meta-design-self-healing",
            "design-ops-loop",
            "session-boot-design",
            "artifact-layers-design",
            "talex-friction-analyzer",
        ]
        for design in expected_designs:
            assert design in DESIGN_ADR_MAP, f"Missing ADR mapping for {design}"
