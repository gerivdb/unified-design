"""Tests for cross_repo_ci.py."""

import pytest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from cross_repo_ci import check_consumer, DESIGN_SLUGS, CONSUMER_MAP


class TestCrossRepoCI:
    """Tests for cross-repo CI pipeline."""

    def test_check_consumer_returns_dict(self):
        """Test that check_consumer returns a valid dict."""
        result = check_consumer("KIVA-CLI", "safe-action-pattern")
        assert "consumer" in result
        assert "design" in result
        assert "status" in result

    def test_check_consumer_valid_statuses(self):
        """Test that check_consumer returns valid status."""
        result = check_consumer("KIVA-CLI", "safe-action-pattern")
        assert result["status"] in ("PASS", "FAIL", "MISSING", "ERROR", "TIMEOUT")

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

    def test_ecos_cli_has_valid_path(self):
        """Test that ECOS-CLI path exists."""
        assert CONSUMER_MAP["ECOS-CLI"].exists()
