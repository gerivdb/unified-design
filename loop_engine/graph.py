"""Build the oriented dependency graph from design definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


@dataclass(frozen=True)
class DesignNode:
    """A node in the design dependency graph."""

    name: str
    kind: str = "design"  # design | atom | loop
    inherits: tuple[str, ...] = ()
    requires: tuple[str, ...] = ()
    conflicts: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
    path: Path | None = None


@dataclass(frozen=True)
class CapabilityConflict:
    """Declared conflict between two capabilities."""

    a: str
    b: str
    severity: str = "error"
    message: str = ""


class LoopGraph:
    """Oriented graph of design nodes."""

    def __init__(self) -> None:
        self.nodes: dict[str, DesignNode] = {}
        self.edges_from: dict[str, list[str]] = {}
        self.edges_to: dict[str, list[str]] = {}
        self.conflicts: list[CapabilityConflict] = []

    def add_node(self, node: DesignNode) -> None:
        self.nodes.setdefault(node.name, node)
        self.edges_from.setdefault(node.name, [])
        self.edges_to.setdefault(node.name, [])

    def add_edge(self, source: str, target: str) -> None:
        if source not in self.nodes or target not in self.nodes:
            msg = f"Unknown node: {source} or {target}"
            raise KeyError(msg)
        if target not in self.edges_from[source]:
            self.edges_from[source].append(target)
        if source not in self.edges_to[target]:
            self.edges_to[target].append(source)

    def neighbors(self, name: str) -> Sequence[str]:
        return self.edges_from.get(name, [])

    def predecessors(self, name: str) -> Sequence[str]:
        return self.edges_to.get(name, [])

    def all_edges(self) -> Iterable[tuple[str, str]]:
        for source, targets in self.edges_from.items():
            for target in targets:
                yield source, target


def _coerce_node(raw: dict, *, kind: str, path: Path) -> DesignNode:
    return DesignNode(
        name=raw["name"],
        kind=kind,
        inherits=tuple(raw.get("inherits", []) or []),
        requires=tuple(raw.get("requires", []) or []),
        conflicts=tuple(raw.get("conflicts", []) or []),
        capabilities=tuple(raw.get("capabilities", []) or []),
        path=path,
    )


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def build_graph_from_designs(roots: Sequence[Path]) -> LoopGraph:
    """Build a LoopGraph from design/atom/loop YAML files."""
    graph = LoopGraph()

    for root in roots:
        for path in root.rglob("*.yaml"):
            try:
                data = _load_yaml(path)
            except Exception:
                continue

            name = data.get("name")
            if not name:
                continue

            kind = "design"
            if root.name == "atoms":
                kind = "atom"
            elif root.name == "loops":
                kind = "loop"

            node = _coerce_node(data, kind=kind, path=path)
            graph.add_node(node)

    for node in list(graph.nodes.values()):
        for parent in node.inherits:
            if parent in graph.nodes:
                graph.add_edge(parent, node)
        for requirement in node.requires:
            if requirement in graph.nodes:
                graph.add_edge(requirement, node)
        for conflict in node.conflicts:
            graph.conflicts.append(CapabilityConflict(a=node.name, b=conflict))

    return graph
