import sys
import yaml
import glob
import os
import re

def extract_frontmatter(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        # YAML pur ou commentaires initiales
        try:
            for doc in yaml.safe_load_all(content):
                if isinstance(doc, dict):
                    return doc
        except Exception:
            pass
        # Chercher premier document derri re un marker ---
        m = re.search(r'^---\s*\n(.*?)(?:\n---\s*\n|$)', content, re.DOTALL | re.MULTILINE)
        if m:
            try:
                return yaml.safe_load(m.group(1))
            except Exception:
                return None
        return None
    return yaml.safe_load(match.group(1))

def validate_file(path, asserts):
    try:
        data = extract_frontmatter(path)
        if data is None:
            print(f"[KO] {path}: missing YAML frontmatter")
            return False
        for key in asserts:
            if key not in data:
                print(f"[KO] {path}: missing key '{key}'")
                return False
        print(f"[OK] {path}")
        return True
    except Exception as e:
        print(f"[KO] {path}: {e}")
        return False

def main():
    args = sys.argv[1:]
    asserts = []
    files = []
    i = 0
    while i < len(args):
        if args[i] == '--assert':
            asserts.append(args[i+1])
            i += 2
        else:
            files.append(args[i])
            i += 1

    if not files:
        print("Usage: validate_yaml.py [--assert key] file1 [file2 ...]")
        sys.exit(1)

    all_ok = True
    for pattern in files:
        if '*' in pattern or '?' in pattern:
            matches = glob.glob(pattern, recursive=True)
        else:
            matches = [pattern]
        for path in matches:
            if os.path.isfile(path):
                if not validate_file(path, asserts):
                    all_ok = False

    sys.exit(0 if all_ok else 1)

if __name__ == '__main__':
    main()
