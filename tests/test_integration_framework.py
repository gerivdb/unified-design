"""Tests for integration_framework.py."""

from __future__ import annotations

import pytest

from tools.integration_framework import (
    ActionResult,
    CheckResult,
    DesignGate,
    DesignInjector,
    DesignOpsLoop,
    DesignTestHarness,
    Thought,
    Violation,
)


class TestDesignGate:
    """Tests for DesignGate."""

    def test_verify_returns_true_when_valid(self):
        gate = DesignGate("safe-action-pattern")
        result = gate.verify({
            "command": "run",
            "context": {"preconditions_checked": True},
        })
        assert result is True
        assert len(gate.violations) == 0

    def test_verify_returns_false_when_missing_preconditions(self):
        gate = DesignGate("safe-action-pattern")
        result = gate.verify({
            "command": "run",
            "context": {"preconditions_checked": False},
        })
        assert result is False
        assert any(v.code == "PRECONDITIONS_NOT_CHECKED" for v in gate.violations)

    def test_verify_returns_false_when_missing_proof(self):
        gate = DesignGate("safe-action-gate")
        result = gate.verify({
            "command": "run",
            "context": {"proof_horodatee": False, "invariants_checked": True},
        })
        assert result is False
        assert any(v.code == "MISSING_PROOF" for v in gate.violations)

    def test_get_violations_returns_copy(self):
        gate = DesignGate("safe-action-gate")
        gate.verify({"command": "run", "context": {}})
        v1 = gate.get_violations()
        v2 = gate.get_violations()
        assert v1 == v2
        assert v1 is not v2


class TestDesignOpsLoop:
    """Tests for DesignOpsLoop."""

    def test_think_returns_thought(self):
        loop = DesignOpsLoop("safe-action-pattern")
        thought = loop.think({"command": "run", "context": {"preconditions_checked": True}})
        assert thought.command == "run"
        assert thought.confidence >= 0.0

    def test_do_succeeds_with_high_confidence(self):
        loop = DesignOpsLoop("safe-action-pattern")
        thought = loop.think({"command": "run", "context": {"preconditions_checked": True}})
        result = loop.do(thought)
        assert result.success is True

    def test_do_fails_with_low_confidence(self):
        loop = DesignOpsLoop("safe-action-pattern")
        thought = Thought(command="run", context={}, confidence=0.3)
        result = loop.do(thought)
        assert result.success is False
        assert result.error is not None

    def test_check_passes_when_do_succeeds(self):
        loop = DesignOpsLoop("safe-action-pattern")
        thought = loop.think({"command": "run", "context": {"preconditions_checked": True}})
        result = loop.do(thought)
        check = loop.check(result)
        assert check.passed is True


class TestDesignInjector:
    """Tests for DesignInjector."""

    def test_inject_raises_on_missing_path(self, tmp_path):
        injector = DesignInjector("safe-action-pattern")
        missing = tmp_path / "does_not_exist"
        with pytest.raises(FileNotFoundError):
            injector.inject(missing)

    def test_verify_injection_returns_true_for_existing(self, tmp_path):
        injector = DesignInjector("safe-action-pattern")
        assert injector.verify_injection(tmp_path) is True


class TestDesignTestHarness:
    """Tests for DesignTestHarness."""

    def test_test_design_enforcement(self):
        harness = DesignTestHarness("safe-action-pattern")
        result = harness.test_design_enforcement()
        assert result["design"] == "safe-action-pattern"
        assert result["passed"] is True

    def test_test_design_behavior(self):
        harness = DesignTestHarness("safe-action-pattern")
        result = harness.test_design_behavior({"command": "run"})
        assert result["design"] == "safe-action-pattern"
        assert result["passed"] is True
