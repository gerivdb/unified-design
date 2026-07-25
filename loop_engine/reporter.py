"""Reporter: console, JSON, DOT exports for cycle reports."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .detector import Cycle
from .classifier import HeuristicClassifier


@dataclass(frozen=True)
class CycleReport:
    cycles: Sequence[Cycle]
    total_designs: int
    total_loops: int
    max_cycle_length: int


class Reporter:
    def __init__(self, classifier: HeuristicClassifier | None = None) -> None:
        self.classifier = classifier or HeuristicClassifier()

    def render(self, report: CycleReport, fmt: str = "console") -> str:
        if fmt == "console":
            return self._render_console(report)
        if fmt == "json":
            return self._render_json(report)
        if fmt == "dot":
            return self._render_dot(report)
        msg = f"Unsupported format: {fmt}"
        raise ValueError(msg)

    def write(self, report: CycleReport, path: Path, fmt: str) -> None:
        path.write_text(self.render(report, fmt=fmt), encoding="utf-8")

    def _render_console(self, report: CycleReport) -> str:
        lines = [
            f"Cycle report — {len(report.cycles)} cycle(s) found",
            f"Designs: {report.total_designs} | loops: {report.total_loops} | max length: {report.max_cycle_length}",
        ]
        for idx, cycle in enumerate(report.cycles, start=1):
            kind = self.classifier.classify(cycle.nodes)
            lines.append(f"[{idx}] {cycle} -> {kind}")
        return "\n".join(lines)

    def _render_json(self, report: CycleReport) -> str:
        payload = {
            "total_designs": report.total_designs,
            "total_loops": report.total_loops,
            "max_cycle_length": report.max_cycle_length,
            "cycles": [
                {
                    "nodes": list(cycle.nodes),
                    "type": self.classifier.classify(cycle.nodes),
                    "length": cycle.length,
                }
                for cycle in report.cycles
            ],
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def _render_dot(self, report: CycleReport) -> str:
        lines = ["digraph loops {", '  rankdir=LR;']
        seen: set[str] = set()
        for cycle in report.cycles:
            for node in cycle.nodes:
                if node not in seen:
                    seen.add(node)
                    lines.append(f'  "{node}";')
            for i in range(len(cycle.nodes) - 1):
                lines.append(f'  "{cycle.nodes[i]}" -> "{cycle.nodes[i + 1]}";')
        lines.append("}")
        return "\n".join(lines)


def classify_cycle(cycle: tuple[str, ...], classifier: HeuristicClassifier | None = None) -> str:
    return (classifier or HeuristicClassifier()).classify(cycle)


def export_report(report: CycleReport, path: Path, fmt: str = "console") -> None:
    Reporter().write(report, path, fmt)


def print_console_report(report: CycleReport) -> None:
    print(Reporter().render(report, fmt="console"))
