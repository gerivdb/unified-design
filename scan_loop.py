import sys
from pathlib import Path

sys.path.insert(0, r'D:\DO\WEB\TOOLS\L0-CANON\unified-design')

from loop_engine.graph import build_graph_from_designs
from loop_engine.detector import detect_cycles

roots = [Path(r'D:\DO\WEB\TOOLS\L0-CANON')]
graph = build_graph_from_designs(roots, design_only=True)
cycles = detect_cycles(graph, max_cycle_length=5)

design_count = sum(1 for n in graph.nodes.values() if n.kind == "design")
print(f"Design repos détectés : {design_count}")
print(f"Nœuds analysés : {len(graph.nodes)}")
print(f"Cycles détectés : {len(cycles)}")
if cycles:
    for c in cycles:
        print(f"  Cycle: {c}")
    print("Verdict : CYCLES_FOUND")
else:
    print("Verdict : NO_CYCLES")
