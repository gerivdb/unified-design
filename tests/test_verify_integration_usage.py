"""Tests for verify_integration_usage.py."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from verify_integration_usage import (
    verify_consumer_usage,
    DESIGN_SLUGS,
    CONSUMER_MAP,
)


class TestVerifyIntegrationUsage:
    """Tests for verify_integration_usage."""

    def test_verify_consumer_usage_returns_dict(self):
        """Test that verify_consumer_usage returns a valid dict."""
        result = verify_consumer_usage("KIVA-CLI", "safe-action-pattern")
        assert "consumer" in result
        assert "design" in result
        assert "status" in result

    def test_verify_consumer_usage_valid_statuses(self):
        """Test that verify_consumer_usage returns valid status."""
        result = verify_consumer_usage("KIVA-CLI", "safe-action-pattern")
        assert result["status"] in ("OK", "NOT_USED", "MISSING_MODULE", "ERROR")

    def test_all_designs_have_slugs(self):
        """Test that all designs have slugs defined."""
        expected_designs = [
            "safe-action-pattern", "safe-action-gate",
            "ecosystem-meta-coherence", "ecosystem-meta-coherence-gate",
            "meta-design-self-healing", "design-ops-loop",
            "session-boot-design", "artifact-layers-design",
            "talex-friction-analyzer",
        ]
        for design in expected_designs:
            assert design in DESIGN_SLUGS, f"Missing slug for {design}"

    def test_all_consumers_defined(self):
        """Test that all expected consumers are defined."""
        expected_consumers = [
            "KIVA-CLI", "ECOS-CLI", "ARGUS", "CTULU",
            "KG-CAUSAL", "KG-L", "KIX", "LOOPX",
            "NEXUS", "TALEX", "TRIX", "VERSES", "VOLTX", "WAZAA",
        ]
        for consumer in expected_consumers:
            assert consumer in CONSUMER_MAP, f"Missing consumer {consumer}"

    def test_kiva_cli_has_valid_path(self):
        """Test that KIVA-CLI path exists."""
        assert CONSUMER_MAP["KIVA-CLI"].exists()
