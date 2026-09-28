#!/usr/bin/env python3
"""
Pre-commit hook — ADR-Design-Integration Traceability.

Bloque le commit si la traçabilité ADR → Design → Consumer → Integration est cassée.
"""

import re
import sys
from pathlib import Path

UNIFIED_DESIGN_ROOT = Path("D:/DO/WEB/TOOLS/L0-CANON/unified-design")
CONSUMER_MAP = {
    "KIVA-CLI": Path("D:/DO/WEB/TOOLS/L1-INFRA/KIVA-CLI"),
    "ECOS-CLI": Path("D:/DO/WEB/TOOLS/L1-INFRA/ECOS-CLI"),
    "ARGUS": Path("D:/DO/WEB/TOOLS/L1-INFRA/ARGUS"),
    "CTULU": Path("D:/DO/WEB/TOOLS/L4-TOOLS/CTULU"),
    "KG-CAUSAL": Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-CAUSAL"),
    "KG-L": Path("D:/DO/WEB/TOOLS/L4-TOOLS/KG-L"),
    "KIX": Path("D:/DO/WEB/TOOLS/L2-PLATFORM/KIX"),
    "LOOPX": Path("D:/DO/WEB/TOOLS/L3-CITIZENS/LOOPX"),
    "NEXUS": Path("D:/DO/WEB/TOOLS/L1-INFRA/NEXUS"),
    "TALEX": Path("D:/DO/WEB/TOOLS/L4-TOOLS/TALEX"),
    "TRIX": Path("D:/DO/WEB/TOOLS/L4-TOOLS/TRIX"),
    "VERSES": Path("D:/DO/WEB/TOOLS/L4-TOOLS/VERSES"),
    "VOLTX": Path("D:/DO/WEB/TOOLS/L0-CANON/VOLTX"),
    "WAZAA": Path("D:/DO/WEB/TOOLS/L4-TOOLS/WAZAA"),
}


def check_traceability():
    """Check traceability for all consumer/design pairs."""
    violations = []
    
    # Check ADR status
    adr_dir = UNIFIED_DESIGN_ROOT / "ADR"
    for adr_file in adr_dir.glob("ADR-*.md"):
        content = adr_file.read_text(encoding="utf-8")
        if re.search(r'^status:\s*proposed', content, re.MULTILINE):
            # Check if design is integrated
            design_name = adr_file.stem.replace("ADR-", "").lower()
            has_integration = False
            for consumer_path in CONSUMER_MAP.values():
                for pkg_dir in [None, "kiva_cli", "ecos_cli", "kix", "kg_l", "verses", "wazaa", "src"]:
                    if pkg_dir:
                        impl = consumer_path / pkg_dir / "*_integration.py"
                    else:
                        impl = consumer_path / "integrations" / "*_integration.py"
                    if list(consumer_path.rglob("*_integration.py")):
                        has_integration = True
                        break
                if has_integration:
                    break
            
            if has_integration:
                violations.append(f"ADR {adr_file.name} is proposed but design is integrated")
    
    return violations


def main():
    violations = check_traceability()
    
    if violations:
        print("TRACEABILITY VIOLATIONS:")
        for v in violations:
            print(f"  - {v}")
        print("\nFix these violations or use --no-verify to skip.")
        sys.exit(1)
    
    print("Traceability check passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
