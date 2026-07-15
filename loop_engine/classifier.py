"""Classify cycles as virtuous or deadlock-like."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ClassifierRule:
    name: str
    description: str
    matches: Sequence[str]


CLASSIFIER_RULES: list[ClassifierRule] = [
    ClassifierRule(
        name="virtuous_cycle",
        description="Cycle contains a regulation/feedback-positive atom.",
        matches=("latency-bound", "power-capped", "virtuous-cycle"),
    ),
    ClassifierRule(
        name="deadlock_pattern",
        description="Cycle contains conflicting low-limit capabilities.",
        matches=("deadlock-pattern",),
    ),
]


def classify_cycle_type(
    cycle: tuple[str, ...],
    *,
    rules: Sequence[ClassifierRule] = tuple(CLASSIFIER_RULES),
) -> str:
    normalized = {name.lower() for name in cycle}
    for rule in rules:
        if any(match.lower() in normalized for match in rule.matches):
            return rule.name
    return "unknown"


class HeuristicClassifier:
    """Apply simple heuristics over cycle labels."""

    def __init__(self, rules: Sequence[ClassifierRule] | None = None) -> None:
        self.rules = list(rules or CLASSIFIER_RULES)

    def classify(self, cycle: tuple[str, ...]) -> str:
        return classify_cycle_type(cycle, rules=self.rules)
