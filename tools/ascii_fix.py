"""
ATOM-ASCII-AUTO-FIX
Correcteur automatique des caractères non-ASCII avant commit.
"""

import sys
import os
import re

def fix_ascii(content: str) -> str:
    """Remplace les caractères non-ASCII (ord > 127) par leur equivalent ASCII ou supprime."""
    replacements = {
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        '\u2013': '-', '\u2014': '--', '\u2026': '...',
        '\u00a0': ' ', '\u00e9': 'e', '\u00e8': 'e', '\u00ea': 'e',
        '\u00eb': 'e', '\u00e0': 'a', '\u00e2': 'a', '\u00e7': 'c',
        '\u00f6': 'o', '\u00fc': 'u', '\u00f1': 'n',
    }
    result = content
    for unicode_char, ascii_char in replacements.items():
        result = result.replace(unicode_char, ascii_char)
    # Remove remaining non-ASCII characters
    result = re.sub(r'[^\x00-\x7F]', '', result)
    return result

def fix_file(filepath: str) -> bool:
    """Fix non-ASCII characters in a file. Returns True if changes were made."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        fixed = fix_ascii(content)
        if content != fixed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed)
            return True
    except Exception as e:
        print(f"[ATOM-ASCII-AUTO-FIX] Error processing {filepath}: {e}")
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: ascii_fix.py <file_or_directory>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isfile(target):
        changed = fix_file(target)
        if changed:
            print(f"[ATOM-ASCII-AUTO-FIX] Fixed non-ASCII in {target}")
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for fname in files:
                fpath = os.path.join(root, fname)
                if fix_file(fpath):
                    print(f"[ATOM-ASCII-AUTO-FIX] Fixed non-ASCII in {fpath}")

if __name__ == "__main__":
    main()