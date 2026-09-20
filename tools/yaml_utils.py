#!/usr/bin/env python3
"""
YAML utilities for unified-design.
Provides safe_load_first_doc() for files that mix YAML frontmatter and Markdown body.
"""
from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print('[ERR] PyYAML is required. Install with: pip install pyyaml')
    raise


def safe_load_first_doc(content: str) -> dict | None:
    """
    Extract and parse only the first YAML document from a string.
    Handles YAML frontmatter + Markdown body (separated by ---).
    
    Args:
        content: File content as string
        
    Returns:
        Parsed YAML dict, or None if no valid YAML found
    """
    # Try YAML frontmatter pattern: ---\nYAML\n---
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except Exception:
            return None
    
    # Try first YAML document only (for multi-doc YAML)
    try:
        for doc in yaml.safe_load_all(content):
            if isinstance(doc, dict):
                return doc
    except Exception:
        pass
    
    # Fallback: search for first --- block
    m = re.search(r'^---\s*\n(.*?)(?:\n---\s*\n|$)', content, re.DOTALL | re.MULTILINE)
    if m:
        try:
            return yaml.safe_load(m.group(1))
        except Exception:
            return None
    
    return None


def safe_load_first_doc_file(path: Path) -> dict | None:
    """
    Read a file and extract the first YAML document.
    
    Args:
        path: Path to the file
        
    Returns:
        Parsed YAML dict, or None if no valid YAML found
    """
    try:
        content = path.read_text(encoding='utf-8')
        return safe_load_first_doc(content)
    except Exception as e:
        print(f'[ERR] Cannot read {path}: {e}')
        return None
