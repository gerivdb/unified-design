import glob
import sys

base = r"D:\DO\WEB\TOOLS\L0-CANON\unified-design"
replacements = {
    "\u2014": "-",
    "\u2013": "-",
    "\u2192": "->",
    "\u2190": "<-",
    "\u2194": "<->",
    "\u2264": "<=",
    "\u2260": "!=",
    "\u2248": "~=",
    "\u00e9": "e",
    "\u00e8": "e",
    "\u00e0": "a",
    "\u00f9": "u",
    "\u00ea": "e",
    "\u00e2": "a",
    "\u00f4": "o",
    "\u00fb": "u",
    "\u00ee": "i",
    "\u00ef": "i",
    "\u00e7": "c",
    "\u00ab": "<<",
    "\u00bb": ">>",
    "\u2019": "'",
    "\u2018": "'",
    "\u2713": "[OK]",
    "\u2714": "[OK]",
    "\u03B2": "beta",
    "\u2080": "0",
    "\u2081": "1",
}
count = 0
for path in glob.glob(base + "/**/*.yaml", recursive=True):
    try:
        c = open(path, encoding="utf-8").read()
        original = c
        for old, new in replacements.items():
            c = c.replace(old, new)
        if c != original:
            open(path, "w", encoding="utf-8").write(c)
            count += 1
    except Exception as e:
        pass
print(f"Cleaned {count} YAML files")
