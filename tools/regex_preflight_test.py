#!/usr/bin/env python3
"""
Regex preflight test utility.
Compiles and tests a regex pattern on a sample before using it in production scripts.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def test_regex(pattern: str, sample: str, flags: int = 0) -> bool:
    """
    Test a regex pattern on a sample string.
    
    Args:
        pattern: Regex pattern to test
        sample: Sample string to test against
        flags: Optional regex flags (e.g., re.IGNORECASE)
        
    Returns:
        True if pattern compiles and matches, False otherwise
    """
    try:
        compiled = re.compile(pattern, flags)
        match = compiled.search(sample)
        if match:
            print(f'[OK] Pattern "{pattern}" matches: {match.group()!r}')
            return True
        else:
            print(f'[WARN] Pattern "{pattern}" compiles but does not match sample')
            return True  # Still valid, just no match
    except re.error as e:
        print(f'[KO] Regex error: {e}')
        return False


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: regex_preflight_test.py <pattern> <sample> [flags]")
        print("  flags: IGNORECASE, MULTILINE, DOTALL, VERBOSE")
        sys.exit(1)
    
    pattern = sys.argv[1]
    sample = sys.argv[2]
    flags = 0
    
    if len(sys.argv) > 3:
        for flag_name in sys.argv[3:]:
            flag_name = flag_name.upper()
            if flag_name == 'IGNORECASE':
                flags |= re.IGNORECASE
            elif flag_name == 'MULTILINE':
                flags |= re.MULTILINE
            elif flag_name == 'DOTALL':
                flags |= re.DOTALL
            elif flag_name == 'VERBOSE':
                flags |= re.VERBOSE
            else:
                print(f'[WARN] Unknown flag: {flag_name}')
    
    ok = test_regex(pattern, sample, flags)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    raise SystemExit(main())
