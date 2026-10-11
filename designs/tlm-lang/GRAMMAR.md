# TLM-LANG — Topological Logic Model Language

**Version** : 1.0.0  
**Date** : 2026-07-28  
**IntentHash** : `0xTLM_LANG_GRAMMAR_20260728`  
**Status** : Spécification Beta  

---

## 📋 Overview

TLM-LANG (Topological Logic Model Language) is a domain-specific language for expressing topological structures, graphs with typed nodes and constrained edges, and state transitions between topological configurations.

### 🎯 Purpose

- Define topological graphs with ternary semantics (TRL/CTL)
- Express invariants and constraints on graph topology
- Describe state transitions and relaxation paths
- Enable validation through RLM-243 services

---

## 🔤 Syntax Overview

### File Extensions

| Extension | Purpose |
|-----------|---------|
| `.dag3` | Directed Acyclic Graph with ternary nodes |
| `.topo` | Topological configuration file |

### Basic Structure

```
# Commentaire de ligne unique

---
metadata:
  name: "TopologyName"
  version: "1.0.0"
  description: "Brief description"

---
nodes:
  NODE_ID: { field: value, ... }
  ANOTHER_NODE: { ... }

---
edges:
  NODE_ID -> TARGET_ID: { constraint: value, weight: 0.5 }

---
invariants:
  NAME: { type: ACYCLICITY, enforced: true }
```

---

## 🏗️ Node Definitions

### Node Syntax

```
NODE_ID: {
  type: NODE_TYPE,
  trits: [1, 1, 1, 1, 1],
  properties: { ... },
  constraints: { ... }
}
```

### Node Types

| Type | Description |
|------|-------------|
| `ORIGIN` | Root/origin node, topological anchor |
| `SENSOR` | Data input node |
| `AGGREGATOR` | Data aggregation/processing |
| `VALIDATOR` | Validation/constraint enforcement |
| `RUNNER` | Execution context |
| `ORCHESTRATOR` | Coordination node |
| `GATEWAY` | External interface |

### Node Properties

| Property | Type | Description |
|----------|------|-------------|
| `trits` | `[1, 0, -1]` | Ternary state vector |
| `phase` | `0-2π` | Topological phase angle |
| `capacity` | `int` | Processing capacity |
| `resonance` | `float` | Resonance factor |

---

## 🔗 Edge Definitions

### Edge Syntax

```
SOURCE -> TARGET: {
  weight: 0.5,
  constraint: CONSTRAINT_NAME,
  direction: FORWARD|BIDIRECTIONAL|REVERSE,
  type: DATA|CONTROL|FEEDBACK
}
```

### Edge Constraints

| Constraint | Description |
|------------|-------------|
| `VALIDATE` | Must pass validation |
| `MINIMIZE` | Minimize cost/latency |
| `BALANCE` | Load balancing constraint |
| `SEQUENCE` | Must follow sequence |
| `EXCLUSIVE` | Mutually exclusive with other edges |

---

## 📐 Invariant Definitions

### Invariant Syntax

```
INVARIANT_NAME: {
  type: INVARIANT_TYPE,
  threshold: value,
  enforced: true|false,
  scope: GLOBAL|LOCAL|RUNNER_ID
}
```

### Invariant Types

| Type | Description | Formula |
|------|-------------|---------|
| `ACYCLICITY` | No cycles allowed | ∀ paths: length(path) < ∞ |
| `HAMMING_DIST` | Hamming distance constraint | d_H(x,y) ≤ threshold |
| `QUORUM` | Minimum node agreement | ≥ n/2 nodes agree |
| `LOAD_BALANCE` | Distribution constraint | max(load) - min(load) ≤ threshold |
| `RESONANCE` | Phase alignment | |θ_i - θ_j| ≤ threshold |
| `TOPOLOGY` | Graph structure | connected, DAG, etc. |

---

## 🔄 Transition Definitions

### Transition Syntax

```
TRANSITION_NAME: {
  from: CURRENT_STATE,
  to: NEXT_STATE,
  trigger: EVENT_TYPE,
  conditions: [CONDITION_1, ...],
  actions: [ACTION_1, ...]
}
```

### Event Types

| Event | Description |
|-------|-------------|
| `HEALTH_CHECK_FAIL` | Service health check failed |
| `VOTE_APPROVED` | Vote passed with majority |
| `METRIC_THRESHOLD` | Metric crossed threshold |
| `MANUAL_TRIGGER` | Manual intervention |

---

## 📄 Complete Example

```plaintext
# topology.dag3
---
metadata:
  name: "KIX-Orchestrator-Topology"
  version: "1.0.0"
  description: "KIX orchestrator with RLM services integration"
  author: "gerivdb"
  created: "2026-07-28"

---
nodes:
  KIX: {
    type: ORCHESTRATOR,
    trits: [1, 1, 0, 0, 1],
    phase: 0.0,
    capacity: 100,
    properties: {
      port: 8800,
      jwt_enabled: true
    }
  }
  
  RLM_DEPLOY: {
    type: RUNNER,
    trits: [1, 0, -1, 0, 1],
    phase: 0.785,
    capacity: 10,
    properties: {
      port: 8795,
      service: "RLM-DEPLOY"
    }
  }
  
  RLM_SECURE: {
    type: RUNNER,
    trits: [1, 1, 0, 0, 1],
    phase: 1.57,
    capacity: 8,
    properties: {
      port: 8796,
      service: "RLM-SECURE"
    }
  }
  
  RLM_INCIDENT: {
    type: RUNNER,
    trits: [1, 0, 1, 0, 1],
    phase: 2.35,
    capacity: 12,
    properties: {
      port: 8798,
      service: "RLM-INCIDENT"
    }
  }
  
  RLM_RELEASE: {
    type: RUNNER,
    trits: [1, 1, -1, 0, 1],
    phase: 3.14,
    capacity: 5,
    properties: {
      port: 8799,
      service: "RLM-RELEASE"
    }
  }

---
edges:
  KIX -> RLM_DEPLOY: {
    weight: 0.9,
    constraint: VALIDATE,
    type: CONTROL
  }
  
  KIX -> RLM_SECURE: {
    weight: 0.85,
    constraint: MINIMIZE,
    type: DATA
  }
  
  RLM_SECURE -> RLM_INCIDENT: {
    weight: 0.7,
    constraint: SEQUENCE,
    type: FEEDBACK
  }
  
  KIX -> RLM_RELEASE: {
    weight: 0.6,
    constraint: BALANCE,
    type: CONTROL
  }

---
invariants:
  ACYCLICITY: {
    type: ACYCLICITY,
    enforced: true,
    scope: GLOBAL
  }
  
  HAMMING_DIST: {
    type: HAMMING_DIST,
    threshold: 2,
    enforced: true,
    scope: GLOBAL
  }
  
  LOAD_BALANCE: {
    type: LOAD_BALANCE,
    threshold: 0.3,
    enforced: true,
    scope: RUNNER
  }
  
  RESONANCE: {
    type: RESONANCE,
    threshold: 1.57,
    enforced: false,
    scope: GLOBAL
  }

---
transitions:
  SERVICE_START: {
    from: "STOPPED",
    to: "RUNNING",
    trigger: VOTE_APPROVED,
    conditions: [ACYCLICITY],
    actions: [START_SERVICE, UPDATE_METRICS]
  }
  
  SERVICE_STOP: {
    from: "RUNNING",
    to: "STOPPED",
    trigger: VOTE_APPROVED,
    conditions: [LOAD_BALANCE],
    actions: [STOP_SERVICE, CLEANUP]
  }
```

---

## 🧪 Validation Rules

### RLM-243 Validation Endpoint

```
POST /v3/validate/topology
Content-Type: application/json

{
  "topology": "<.dag3 content>",
  "strict": true
}
```

### Response Format

```json
{
  "valid": true,
  "errors": [],
  "warnings": [],
  "score": 0.95,
  "invariant_status": {
    "ACYCLICITY": "PASS",
    "HAMMING_DIST": "PASS",
    "LOAD_BALANCE": "WARN"
  }
}
```

---

## 📦 File Structure

```
TLM-LANG/
├── GRAMMAR.md           # This specification
├── parser/
│   ├── lexer.py         # Tokenizer
│   ├── parser.py        # AST parser
│   └── ast.py           # AST node definitions
├── runtime/
│   ├── executor.py      # TRIX integration
│   └── scorer.py        # UAE integration
├── samples/
│   └── kix-topology.dag3
└── README.md            # Usage guide
```

---

## 🔧 Integration Points

### TRIX Integration

The TLM-LANG parser produces an AST that can be:
- Executed as syscalls via TRIX runtime
- Validated against topological invariants
- Used for state transitions and orchestration

### UAE (Unified Architecture Engine) Integration

- Phase angles used for resonance scoring
- Trit states for ternary computation
- Topological relaxation paths

### RLM-243 Validation

- All topologies validated through RLM-243 services
- Vote ternaire for critical transitions
- WAL logging for topology changes

---

## 📌 Next Steps

1. Implement parser (lexer.py, parser.py)
2. Build AST node definitions
3. Integrate with TRIX executor
4. Implement UAE scorer
5. Create sample topologies

---

## References

- ADR-2026-07-27-001 : Triade LLM/RLM/TLM
- ADR-033 : RLM-243 Recursive Ternary Memory
- TRIX Documentation : `D:\DO\WEB\TOOLS\L4-TOOLS\TRIX`
- UAE Documentation : `D:\DO\WEB\TOOLS\L4-TOOLS\UAE`