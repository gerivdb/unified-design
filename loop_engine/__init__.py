"""Loop Detection Engine — Unified Design v2.

Ce module construit le graphe de dépendances entre designs/atomes,
détecte les cycles, les classe, et exporte des rapports.
"""

from __future__ import annotations

from .detector import CycleDetectionError, detect_cycles
from .graph import (
    CapabilityConflict,
    DesignNode,
    LoopGraph,
    build_graph_from_designs,
)
from .reporter import (
    Reporter,
    classify_cycle,
    export_report,
    print_console_report,
)
from .classifier import (
    CLASSIFIER_RULES,
    ClassifierRule,
    HeuristicClassifier,
    classify_cycle_type,
)
