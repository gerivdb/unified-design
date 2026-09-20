#!/usr/bin/env python3
"""Check UTF-8 BOM in staged YAML files."""
import sys
from pathlib import Path

BOM = b'\xef\xbb\xbf'

def main() -> int:
    failed = False
    for path in sys.argv[1:]:
        p = Path(path)
        if p.suffix.lower() not in {'.yaml', '.yml', '.md'}:
            continue
        data = p.read_bytes()
        if data.startswith(BOM):
            print(f'BOM detected: {path}')
            failed = True
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())
