#!/usr/bin/env python3
"""Fix indentation in L1-INFRA_Atoms_Index.yaml"""
from pathlib import Path

path = Path("atoms/L1-INFRA_Atoms_Index.yaml")
lines = path.read_text(encoding="utf-8").splitlines(keepends=True)

# Find the marker
marker = "new_major_atoms:"
start_idx = None
for i, line in enumerate(lines):
    if line.strip() == marker:
        start_idx = i
        break

if start_idx is None:
    print("marker not found")
    exit(1)

# Determine block end: next line that starts at column 0 and is not blank/comment
def is_top_level(line: str) -> bool:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return False
    return not line.startswith(" ") and not line.startswith("\t")

end_idx = start_idx + 1
while end_idx < len(lines) and not is_top_level(lines[end_idx]):
    end_idx += 1

# Rebuild the block with normalized indentation
new_block = [marker + "\n"]
for line in lines[start_idx + 1 : end_idx]:
    stripped = line.lstrip(" ")
    if stripped == "":
        new_block.append("\n")
        continue
    indent = len(line) - len(stripped)
    if stripped.startswith("- "):
        new_block.append("  " + stripped)
    else:
        # dedent to 4 (under list item)
        new_block.append("    " + stripped)

new_lines = lines[:start_idx] + new_block + lines[end_idx:]
path.write_text("".join(new_lines), encoding="utf-8")
print("fixed")
