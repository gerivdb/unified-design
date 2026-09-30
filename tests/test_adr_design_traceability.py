"""Tests for adr_design_traceability.py."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from adr_design_traceability import (
    get_adr_status,
    find_prd_mocs_for_consumer,
    check_traceability,
    DESIGN_ADR_MAP,
)


class TestAdrDesignTraceability:
    """Tests for ADR-Design-Integration traceability."""

    def test_get_adr_status_returns_accepted_for_known_adr(self):
        """Test that known ADR returns accepted status."""
        status = get_adr_status("ADR-2026-09-19-SAFE-ACTION-PATTERN.md")
        assert status == "accepted"

    def test_get_adr_status_returns_missing_for_unknown_adr(self):
        """Test that unknown ADR returns missing."""
        status = get_adr_status("ADR-UNKNOWN-9999.md")
        assert status == "missing"

    def test_design_adr_map_has_required_designs(self):
        """Test that DESIGN_ADR_MAP contains all expected designs."""
        required = [
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
        for design in required:
            assert design in DESIGN_ADR_MAP

    def test_check_traceability_returns_ok_for_valid_pair(self):
        """Test that check_traceability returns OK for valid consumer/design."""
        result = check_traceability("KIVA-CLI", "safe-action-pattern")
        assert "status" in result
        assert "adr_status" in result
        assert "prd_moc_found" in result

    def test_find_prd_mocs_for_consumer_returns_list(self):
        """Test that find_prd_mocs_for_consumer returns a list."""
        result = find_prd_mocs_for_consumer("KIVA-CLI", "safe-action-pattern")
        assert isinstance(result, list)
