# Integration Framework — Documentation

## Objectif

Le `integration-framework` standardise l'application des designs `unified-design` dans les repos consumers. Il fournit :

- **DesignGate** : vérification pré-action des préconditions et invariants
- **DesignOpsLoop** : orchestration boucle THINK/DO/CHECK
- **DesignInjector** : injection de designs dans le codebase consumer
- **DesignTestHarness** : tests d'intégration standardisés
- **DesignBootSequence** : séquence BOOT/CLOSEOUT pour les consumers

## Architecture

```
unified-design/
├── tools/
│   └── integration_framework.py   # Module principal (Python)
├── templates/
│   └── integration-template.py    # Template pour générer les modules d'intégration
├── tests/
│   └── test_integration_framework.py  # Tests du framework
└── docs/
    └── integration-framework.md   # Cette documentation
```

## Usage

### 1. DesignGate

```python
from tools.integration_framework import DesignGate

gate = DesignGate("safe-action-pattern", strict_mode=True)
ok = gate.verify({
    "command": "run",
    "context": {"preconditions_checked": True}
})
if not ok:
    for v in gate.get_violations():
        print(v.code, v.message)
```

### 2. DesignOpsLoop

```python
from tools.integration_framework import DesignOpsLoop

loop = DesignOpsLoop("safe-action-pattern")
thought = loop.think({"command": "run", "context": {"preconditions_checked": True}})
result = loop.do(thought)
check = loop.check(result)
assert check.passed is True
```

### 3. DesignInjector

```python
from tools.integration_framework import DesignInjector

injector = DesignInjector("safe-action-pattern")
injector.inject(Path("/path/to/consumer"))
assert injector.verify_injection(Path("/path/to/consumer")) is True
```

### 4. DesignTestHarness

```python
from tools.integration_framework import DesignTestHarness

harness = DesignTestHarness("safe-action-pattern")
result = harness.test_design_enforcement()
assert result["passed"] is True
```

### 5. DesignBootSequence

```python
from tools.integration_framework import DesignBootSequence

boot = DesignBootSequence("kiva-cli")
result = boot.boot()
assert result.success is True
```

## Génération d'intégration

Pour générer un module d'intégration pour un consumer :

```python
from tools.integration_framework import DesignInjector

injector = DesignInjector("safe-action-pattern")
injector.inject(Path("/path/to/consumer/codebase"))
```

Ou utiliser le template manuellement :

```bash
# Copier le template
cp templates/integration-template.py consumer/integrations/safe_action_pattern_integration.py

# Remplacer les placeholders
# {{DESIGN_SLUG}} → safe_action_pattern
# {{CLASS_NAME}} → SafeActionPattern
# {{DESIGN_NAME}} → safe-action-pattern
# {{INSTANCE_METHOD}} → verify
# {{RESPONSE_FIELD}} → status
# {{ALLOW_VALUE}} → OK
# {{CONSUMER_NAME}} → kiva-cli
```

## Tests

```bash
# Lancer les tests du framework
python -m pytest tests/test_integration_framework.py -v

# Lancer les tests d'intégration d'un consumer
python -m pytest consumer/tests/test_*_integration.py -v
```

## Références

- **Design** : `designs/integration-framework/design.yaml`
- **Primitive** : `primitives/integration-framework-primitive.yaml`
- **PRD-MOC** : `PRD/PRD-MOC-INTEGRATION-FRAMEWORK-20260928.md`
- **ADR** : ADR-2026-09-19-SAFE-ACTION-PATTERN
