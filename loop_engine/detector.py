"""Detect cycles in the design dependency graph using DFS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Cycle:
    nodes: tuple[str, ...]

    @property
    def length(self) -> int:
        return len(self.nodes)

    def __str__(self) -> str:
        return " -> ".join(self.nodes)


class CycleDetectionError(Exception):
    """Raised when an unrecoverable cycle is found."""


def detect_cycles(
    graph: object,
    *,
    max_cycle_length: int = 5,
) -> list[Cycle]:
    """Return all simple cycles within the configured max length."""
    edges: dict[str, list[str]] = getattr(graph, "edges_from", {})
    cycles: list[Cycle] = []
    visited: set[str] = set()
    rec_stack: set[str] = set()
    path: list[str] = []

    def dfs(node: str) -> None:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        for neighbor in edges.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in rec_stack:
                start = path.index(neighbor)
                cycle_nodes = tuple(path[start:] + [neighbor])
                if len(cycle_nodes) - 1 <= max_cycle_length:
                    cycles.append(Cycle(nodes=cycle_nodes))
        path.pop()
        rec_stack.remove(node)

    for node in edges:
        if node not in visited:
            dfs(node)

    unique: list[Cycle] = []
    seen: set[tuple[str, ...]] = set()
    for cycle in cycles:
        normalized = tuple(_normalize_cycle(cycle.nodes))
        if normalized not in seen:
            seen.add(normalized)
            unique.append(Cycle(nodes=normalized))
    return unique


def _normalize_cycle(nodes: tuple[str, ...]) -> tuple[str, ...]:
    if not nodes:
        return nodes
    start = min(range(len(nodes) - 1), key=lambda idx: nodes[idx])
    return nodes[start:-1] + nodes[:start]
