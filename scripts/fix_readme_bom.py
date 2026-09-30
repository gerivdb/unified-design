#!/usr/bin/env python3
"""Fix UTF-8 BOM in README.md"""

from pathlib import Path

readme_path = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design/README.md")
content = readme_path.read_bytes()

# Remove BOM if present
if content.startswith(b'\xef\xbb\xbf'):
    content = content[3:]
    readme_path.write_bytes(content)
    print("README.md: BOM removed")
else:
    print("README.md: no BOM found")

# Ensure UTF-8 encoding
readme_path.write_text(readme_path.read_text(encoding='utf-8'), encoding='utf-8')
print("README.md: UTF-8 encoding verified")
