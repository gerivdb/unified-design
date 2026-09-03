import yaml

with open(r'D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms_registry.yaml', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

# Find insertion point (before methodology)
atoms = data['atoms']
insert_idx = None
for i, atom in enumerate(atoms):
    path = atom.get('path', '')
    if 'methodology' in path:
        insert_idx = i
        break

new_atom = {
    'path': 'atoms/hitl-session-protocol.yaml',
    'hash': '96aacc8fd1b1',
    'description': 'description: "Protocole normatif que tout agent HITL doit suivre avant toute action mutante"',
    'depends_on': ['ATOM-HITL-GATE', 'ATOM-KIVA-AUTO-PR-WORKFLOW', 'ADR-024', 'ADR-030']
}

if insert_idx is not None:
    atoms.insert(insert_idx, new_atom)
else:
    atoms.append(new_atom)

with open(r'D:\DO\WEB\TOOLS\L0-CANON\unified-design\atoms_registry.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

print('Added hitl-session-protocol atom at index', insert_idx)