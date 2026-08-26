# DAG-3 Graph Engineering Design Specification

> **Metacohérence KG-L (2026-08-26)** : ce document décrit le design
> **Graph Engineering** (agents isolés, barrier nodes, modèles Opus/Haiku/Sonnet).
> Il ne décrit **pas** l'implémentation triadique du repo `gerivdb/DAG-3`
> (parser ASCII, opérateurs ternaires 243 états, involution Janus).
> 
> **Politique retenue : séparation des concepts.**
> - `DAG-3` = moteur de graphe triadique (strate L2_PLATFORM).
> - Graph Engineering = concept d'architecture séparé, non implémenté dans DAG-3.
> 
> Si une implémentation Graph Engineering est nécessaire, elle doit être
> documentée dans un design dédié, pas dans ce document.

**Document ID:** GERIVDB-GE-DESIGN-2026-07-29  
**Version:** 1.0  
**Status:** Proposed  
**Engineer:** Bellard Protocol  

**Related Documents:** 
- Source: `drafts/archi Graph Engineering DAG-3 Archit.md`
- Master Intent: `CTULU-L4-Master-Intent.md`

---



## 1. Executive Summary

This document specifies the design for the Graph Engineering DAG-3 architecture, which transforms the legacy sequential loop execution model into a parallel graph-based execution framework. The design introduces isolated agent nodes, explicit data flow edges, barrier synchronization, and specialized roles for judgment and correction to achieve significant performance improvements while maintaining correctness.

**Key Improvements:**
- 65% reduction in wall-clock time through parallelization
- 89% first-pass success rate via Opus-powered judgment nodes
- Clear separation of concerns between detection and correction agents
- Optimized resource utilization on Z600 Xeon E5620 hardware

---



## 2. Goals and Non-Goals

### Goals
1. Replace sequential task execution with parallel graph execution
2. Isolate agent contexts to prevent cognitive overload and bias
3. Implement unbiased judgment via independent session mechanisms (`-p` flag)
4. Optimize visual verification using headless browser technology
5. Separate detection (review) and correction (fixing) responsibilities
6. Enable dynamic graph configuration and orchestration
7. Provide knowledge persistence through procedural (`claw.md`) and visual (`design.md`) anchors
8. Support thermonuclear review for pre-release validation

### Non-Goals
1. Eliminate all token consumption (parallelism inherently increases token usage)
2. Remove the need for human oversight in all cases
3. Replace existing agent models (Haiku, Sonnet, Opus) with new models
4. Eliminate the barrier node synchronization requirement
5. Support arbitrary graph topologies without validation

---



## 3. Architecture Overview

### 3.1 Core Components

#### 3.1.1 Nodes (Agents)
- **Isolated Execution Context**: Each node operates in its own context window with dedicated memory
- **Model Assignment**: Nodes are assigned models based on task type:
  - Code Generation: Haiku (8k context, Low priority)
  - Test Writing: Sonnet (16k context, Medium priority)
  - Code Review: Opus (32k context, High priority)
  - **Judgment**: Opus (64k context, **Critical priority**) - *Mandatory*
  - Security Audit: Opus (32k context, Critical priority)
- **Node Types**:
  - Root Node: Task splitting and distribution
  - Worker Nodes (A, B, C...): Specialized task execution (Haiku/Sonnet/Opus)
  - Barrier Node: Synchronization point requiring all worker reports
  - Fixing Agent: Applies corrections based on unified reports
  - Orchestrator Node: Coordinates specialist agents (Security, Design, Simplify)

#### 3.1.2 Edges (Data Flow)
- **Directed Connections**: Unidirectional data flow between nodes
- **Flow Controllers**: Manage data transformation and routing
- **Fan-out/Fan-in Patterns**: 
  - Diamond pattern for parallel processing (root -> workers -> barrier)
  - Barrier enforcement for collective synchronization

#### 3.1.3 Special Mechanisms
- **Second Opinion (`-p`)**: Independent session with zero context inheritance for unbiased judgment
- **Headless Shell Integration**: Optimized Chrome for visual verification
- **Knowledge Anchors**: 
  - `claw.md`: Procedural memory for commands and workflows
  - `design.md`: Visual authority for UI/compliance verification
- **Skill Chains**: Configurable verification pipelines (triple/quad chains)

---


## 4. Detailed Design

### 4.1 Topology Transformation

#### 4.1.1 Legacy Loop Engineering (To be Deprecated)

```
+-------------+     +-------------+     +-------------+
|   WORK      |---->>|  VERIFY     |---->>|   NEXT      |
|  (Agent)    |     |  (Blocking) |     |  (Step)     |
+-------------+     +-------------+     +-------------+
                                              |
      +----------------------------------------+
```
*Characteristics: Linear progression, single agent bottleneck*


#### 4.1.2 Graph Engineering (Current Implementation)
```
                     +-----------------+
                     |   ROOT NODE     |
                     |  (Task Splitting)|
                     +----------------+
                              |
               +----------------------------+
               |              |              |
                                           
     +-----------------+ +-----------------+ +-----------------+
     |   NODE A        | |   NODE B        | |   NODE C        |
     |  (Context ISO)  | |  (Context ISO)  | |  (Context ISO)  |
     |  Haiku          | |  Sonnet         | |  Haiku          |
     +----------------+ +----------------+ +----------------+
              |                   |                   |
              +--------------------------------------+
                                  |
                     +------------------------+
                     |   BARRIER NODE          |
                     |  (Opus -- Judgment)      |
                     +------------------------+
                                  |
                     +------------------------+
                     |   FIXING AGENT          |
                     |  (Correction Phase)     |
                     +-------------------------+

```
*Key Components:*
- **Nodes**: Isolated agents with dedicated context windows
- **Edges**: Data flow controllers between nodes
- **Shapes**: 
  - Diamond: Fan-out -> parallel processing -> fan-in reduction
  - Barrier: Fan-in requiring all agents to report before progression

### 4.2 The Judgment Paradox Resolution

#### 4.2.1 Problem Statement
Cheap models (Haiku) generate excessive false positives (87%), leading to higher net cost due to rework.

#### 4.2.2 Experimental Evidence
| Metric | Haiku (Cheap) | Opus (Premium) |
|--------|---------------|----------------|
| Report Length | 47 "errors" | 6 "errors" |
| False Positives | 41 (87%) | 0 (0%) |
| Human Review Required | Yes | No |
| Net Cost | Higher (review + rework) | Lower (first-pass success) |

#### 4.2.3 Root Cause Analysis
```
+-------------------------------------------------------------+
|  THE JUDGMENT PARADOX                                       |
|                                                             |
|  "The node that performs judgment is the ONLY place        |
|   where saving tokens costs you EVERYTHING"               |
|                                                             |
|  [Context Blindness]   ->   [False Positives]              |
|                                                          |
|  [Re-review Required]   ->   [Net Cost > Opus]             |


+-------------------------------------------------------------+
```

#### 4.2.4 Operational Rule
```plaintext
IF (Node.Type == JUDGMENT) THEN
    Model = OPUS
ELSE
    Model = Optimize per task complexity
END IF
```

### 4.3 Isolation: The `-p` Flag Mechanism

#### 4.3.1 Context Inheritance Problem
```
+-------------------------------------------------------------+
|  BIAS OF THE CREATOR                                       |
|                                                             |
|  Builder Agent Context:                                    |
|  [History] -> [Decisions] -> [Assumptions] -> [Biased View]  |
|                                                             |
|  Advisor reads SAME context -> Inherits SAME bias          |
|  -> Cannot detect builder's blind spots                    |


+-------------------------------------------------------------+
```

#### 4.3.2 Solution: Independent Session Launch
```bash
# Launch independent session
claude -p "Review this code with zero context" --model opus

# Session Characteristics:
# - Separate process (background)
# - Zero history inheritance
# - Fresh context window
# - No knowledge of design decisions
# - Unbiased judgment
```


#### 4.3.3 Architectural Impact
```
+-------------------------------------------------------------+
|  GRAPH NODE EXECUTION WITH -p FLOW                         |
|                                                             |
|  [Worker Node] --output-->> [Second Opinion Check]          |
|                               |                             |
|                                                            |
|                     [Independent Session]                   |
|                     Model: Opus                             |
|                     Context: Fresh                         |
|                               |                             |
|                                                            |
|                     [Pass/Fail Decision]                    |
|                               |                             |
|                    +--------------------+                  |
|                                                           |
|               [Proceed]           [Rework Required]         |
+-------------------------------------------------------------+
```
*Constraints: +200-500ms latency, double token consumption (Opus-only recommendation)*

### 4.4 Performance Optimization: Chrome Headless Shell

#### 4.4.1 Legacy Browser Bottleneck
```
+-------------------------------------------------------------+
|  FULL CHROME INSTANCE                                      |
|                                                             |
|  Memory Footprint: ~800MB                                  |
|  Launch Time: ~3.2s                                        |
|  Per Screenshot: ~1.8s                                     |
|                                                             |
|  PROBLEM: 10 iterations = 18s + memory saturation         |
+-------------------------------------------------------------+
```

#### 4.4.2 Headless Shell Optimization
```bash
# Headless Chrome Shell launch
google-chrome --headless --disable-gpu --screenshot=output.png

# Characteristics:
# - No UI rendering engine
# - Stripped dependencies
# - Minimal memory footprint
```

#### 4.4.3 Performance Comparison (Z600 Xeon E5620)
| Metric | Full Chrome | Headless Shell |  |
|--------|-------------|----------------|---|
| Memory | 800 MB | 120 MB | -85% |
| Launch | 3.2 s | 0.8 s | -75% |
| Screenshot | 1.8 s | 0.4 s | -78% |
| Concurrent (4) | Swap thrashing | Stable |  |

#### 4.4.4 Integration into Graph
```
+-------------------------------------------------------------+
|  EMBEDDED SKILL PIPELINE                                   |
|                                                             |
|  [Code Node] -->> [Build] -->> [Headless Shell]             |
|                                    |                       |
|                                                           |
|                              [Screenshot Capture]          |
|                                    |                       |
|                                                           |
|                         [design.md Verification]           |
|                                    |                       |
|                                                           |
|                              [Pass/Fail]                   |
+-------------------------------------------------------------+
```

### 4.5 Knowledge Persistence: `.md` File Anchors

#### 4.5.1 `claw.md` -- Procedural Memory
```
+-------------------------------------------------------------+
|  ~/project/claw.md                                         |
|                                                             |
|  ## BUILD COMMANDS                                         |
|  make -j4 SSE42=1                                          |
|  ./tests/run --q243 --benchmark                           |
|                                                             |
|  ## TEST COMMANDS                                          |
|  pytest -v -m "not slow"                                   |
|  ./verify --headless                                      |
|                                                             |
|  ## DEPLOYMENT                                             |
|  ./deploy --environment=staging --version=3.2.1           |
+-------------------------------------------------------------+
```
*Rationale: Prevents command rediscovery, reduces token waste, stabilizes execution, eliminates hallucinated parameters*

#### 4.5.2 `design.md` -- Visual Authority
```
+-------------------------------------------------------------+
|  ~/project/design.md                                       |
|                                                             |
|  ## COLOR PALETTE                                          |
|  Primary: #0A1628                                          |
|  Accent: #00D4FF                                           |
|                                                             |
|  ## LAYOUT CONSTRAINTS                                     |
|  - Max width: 1280px                                      |
|  - Grid: 12 columns                                       |
|  - Spacing: 24px                                          |
|                                                             |
|  ## TYPOGRAPHY                                             |
|  - Headings: Inter 600                                    |
|  - Body: Inter 400 (16px/1.5)                             |
+-------------------------------------------------------------+
```
*Integration: [Output] -> [Headless Shell Capture] -> [Compare with design.md] -> [Compliance Score: 97%] -> [Pass if Score  95%]*

### 4.6 Orchestrator Skill: Meta-Node Architecture

#### 4.6.1 Single Agent Overload Problem
```
+-------------------------------------------------------------+
|  ONE AGENT: 5 DIRECTIVES                                   |
|                                                             |
|  Check: [Security] + [Design] + [Simplify] + [Verify] +   |
|         [Performance]                                      |
|                                                             |
|  Problem: 95% accuracy on 1 directive -> 77% on 5          |
|           (0.95^5 = 0.773)                                 |
+-------------------------------------------------------------+
```

#### 4.6.2 Orchestrator Pattern
```
                     +-----------------------------------------+
                     |      ORCHESTRATOR NODE                  |
                     |    (Skill: review-orchestrator)        |
                     +----------------------------------------+
                                     |
               +------------------------------------------+
               |                     |                     |
                                                         
+---------------------+ +---------------------+ +---------------------+
|  Security Agent     | |  Design Agent       | |  Simplify Agent     |
|  Context: ISO       | |  Context: ISO       | |  Context: ISO       |
|  "Find CVEs"        | |  "Check design.md"  | |  "Reduce complexity"|
+--------------------+ +--------------------+ +--------------------+
            |                       |                       |
            +----------------------------------------------+
                                    |
                     +----------------------------+
                     |     ORCHESTRATOR            |
                     |  Compile Findings           |
                     |  -> Unified Report           |
                     +----------------------------+
                                    |
                     +----------------------------+
                     |     FIXING AGENT            |
                     |  Apply Corrections          |
                     +-----------------------------+
```

#### 4.6.3 Skill Chain Configuration
```
+-------------------------------------------------------------+
|  TRIPLE CHAIN (Standard Review)                           |
|                                                             |
|  1. simplify   ->  Reduce code complexity                  |
|  2. verify     ->  Confirm behavior correctness            |
|  3. code-review ->  Style & standards check                |
|                                                             |
|  QUAD CHAIN (Enhanced)                                    |
|                                                             |
|  1. simplify                                               |
|  2. verify                                                 |
|  3. code-review                                            |
|  4. design-skill  ->  Visual compliance vs design.md       |
+-------------------------------------------------------------+
```

### 4.7 Thermonuclear Code Review: Pre-Release Gauntlet

#### 4.7.1 Architecture
```
                     +-----------------------------------------+
                     |  TRIGGER: "thermonuclear-review"      |
                     |  Phase: Pre-release/Tag               |
                     +----------------------------------------+
                                     |
               +------------------------------------------+
               |                     |                     |
                                                         
+---------------------+ +---------------------+ +---------------------+
|  SQL Injection      | |  Access Control     | |  Memory Safety      |
|  Specialist         | |  Specialist         | |  Specialist         |
|  (Isolated)         | |  (Isolated)         | |  (Isolated)         |
+--------------------+ +--------------------+ +--------------------+
            |                       |                       |
            +----------------------------------------------+
                                    |
                     +----------------------------+
                     |  CORRELATION ENGINE         |
                     |  -> Find cross-cutting CVEs  |
                     |  -> Prioritize by severity   |
                     +----------------------------+
                                    |
                     +----------------------------+
                     |  FIXING FLEET               |
                     |  -> Apply all corrections    |
                     |  -> Verify fixes             |
                     +-----------------------------+
```

#### 4.7.2 Execution Timing
```
+-------------------------------------------------------------+
|  WHEN TO RUN                                               |
|                                                             |
|  Embedded Skills:  On every commit (fast, cheap)          |
|  Thermonuclear:    Pre-release only (thorough, expensive)  |
|                                                             |
|  Cost Analysis:                                            |
|  +----------------------------------------------------+    |
|  | Run on every commit  ->  $1000/day (unsustainable) |    |
|  | Run on release only  ->  $100/release (optimal)    |    |
|  +----------------------------------------------------+    |
+-------------------------------------------------------------+
```

### 4.8 Skill Creator Plugin: Tooling for Verification

#### 4.8.1 Installation Scope Options
```bash
# User Scope (global -- recommended for base skills)
claude plugin install skill-creator --scope user

# Project Scope (local -- project-specific validation)
claude plugin install skill-creator --scope project
```

#### 4.8.2 Generated Skill Structure
```
+-------------------------------------------------------------+
|  generated-skill/                                          |
|  -- SKILL.md          # Skill definition & usage         |
|  -- references/       # Reference materials              |
|  |   +-- patterns.md   # Known failure modes              |
|  +-- scripts/          # Verification scripts              |
|      -- verify.sh     # Automated validation              |
|      +-- examples/     # Test cases                       |
+-------------------------------------------------------------+
```

#### 4.8.3 Skill Creation Prompt Template
```plaintext
Create a skill for [DESCRIPTION]
- Must be comprehensive
- Include verification scripts
- Add reference materials
- Test with example cases
- Should be [Standalone | Embedded]
```

### 4.9 Fixing Agents: Separation of Concerns

#### 4.9.1 Role Specialization
```
+-------------------------------------------------------------+
|  DETECTION AGENTS (Reviewers)                              |
|  +----------------------------------------------------+    |
|  | - Find problems                                    |    |
|  | - Generate reports                                |    |
|  | - DO NOT modify code                              |    |
|  +----------------------------------------------------+    |
|                                                             |
|  +--------------------------------------------------------+ |
|  |  FIXING AGENTS (Correctors)                           | |
|  |  +------------------------------------------------+   | |
|  |  | - Read unified report                         |   | |
|  |  | - Apply fixes systematically                  |   | |
|  |  | - DO NOT introduce new logic                  |   | |
|  |  +------------------------------------------------+  | |
|  +--------------------------------------------------------+ |
+-------------------------------------------------------------+
```

#### 4.9.2 Why Separation Matters
```
+-------------------------------------------------------------+
|  SINGLE AGENT PROBLEM                                      |
|  [Agent finds bug] -> [Agent fixes bug] -> [Introduces new bug] |
|                                                             |
|  SEPARATED ROLES                                           |
|  [Reviewer finds bug] -> [Corrector fixes] -> [No new bugs]  |
|                                                             |
|  Rationale: Corrector works from structured report, not   |
|             from context-biased memory                    |
+-------------------------------------------------------------+
```

### 4.10 Verdict: Graph Engineering Implementation

#### 4.10.1 Performance Summary
| Metric | Loop Engineering | Graph Engineering |  |
|--------|------------------|-------------------|---|
| Wall-clock time | 100% | 35% | -65% |
| Token consumption | 1 | 4 | +300% |
| First-pass success | 62% | 89% | +27% |
| Debuggability | High | Low (parallel complexity) |  |
| Resource utilization | Single core | Parallel |  |

#### 4.10.2 Critical Success Factors
```
+-------------------------------------------------------------+
|  CRITICAL: JUDGMENT NODE MUST BE OPUS                      |
|                                                             |
|  +----------------------------------------------------+    |
|  |  "The node that performs judgment is the ONLY      |    |
|  |   place where saving tokens costs you EVERYTHING"  |    |
|  +----------------------------------------------------+    |
|                                                             |
|  CRITICAL: CHROME HEADLESS FOR PERFORMANCE                 |
|                                                             |
|  +----------------------------------------------------+    |
|  |  Replace full Chrome -> Headless Shell              |    |
|  |  Memory: -85%  |  Speed: +75%                    |    |
|  +----------------------------------------------------+    |
|                                                             |
|  CRITICAL: ORCHESTRATOR FOR COMPLEXITY                    |
|                                                             |
|  +----------------------------------------------------+    |
|  |  One orchestrator -> Many specialists               |    |
|  |  95% per specialist -> 98% combined                 |    |
|  +----------------------------------------------------+    |
+-------------------------------------------------------------+
```

#### 4.10.3 Maturity Level Assessment
```
+-------------------------------------------------------------+
|  GRAPH ENGINEERING MATURITY MAP                            |
|                                                             |
|  Level 1: Basic Loop Engineering                           |
|  Level 2: Static Graph (Fixed nodes)                       |
|  Level 3: Dynamic Graph (Self-configuring)                 |
|  Level 4: Adaptive Graph (Recursive refinement)            |
|  Level 5: Self-Healing Graph (Auto-correction)             |
|                                                             |
|  Current Status: Level 3 (Dynamic Graph)                   |
|  Target: Level 4 (Adaptive) -- Q4 2026                     |
+-------------------------------------------------------------+
```

### 4.11 Implementation Guidelines for GERIVDB

#### 4.11.1 Node Allocation Strategy
```
+-------------------------------------------------------------+
|  TASK -> MODEL MAPPING                                      |
|                                                             |
|  +----------------------------------------------------+    |
|  | Task Type      | Model   | Context Size | Priority |    |
|  ------------------------------------------------    |
|  | Code Generation | Haiku   | 8k           | Low     |    |
|  | Test Writing    | Sonnet  | 16k          | Medium  |    |
|  | Code Review     | Opus    | 32k          | High    |    |
|  | Judgment        | Opus    | 64k          | Critical|    |
|  | Security Audit  | Opus    | 32k          | Critical|    |
|  +----------------------------------------------------+    |
+-------------------------------------------------------------+
```

#### 4.11.2 Verification Chain Configuration
```yaml
# .graph-config.yaml
verification:
  chain:
    - name: simplify
      model: sonnet
      context: 16k
    - name: verify
      model: sonnet
      context: 16k
    - name: code-review
      model: opus
      context: 32k
    - name: design
      model: opus
      context: 32k
      requires: design.md
   
  headless:
    browser: chrome-headless-shell
    memory_limit: 256MB
    timeout: 5s
   
  second_opinion:
    enabled: true
    model: opus
    parallel: true
```

#### 4.11.3 Resource Budgeting (Z600 Xeon E5620)
```
+-------------------------------------------------------------+
|  RESOURCE ALLOCATION PER NODE                              |
|                                                             |
|  Memory:                                                   |
|  +----------------------------------------------------+    |
|  | Base: 512MB per node                              |    |
|  | Headless Chrome: +120MB per concurrent            |    |
|  | Total: 4512 + 4120 = 2.5GB (safe)              |    |
|  +----------------------------------------------------+    |
|                                                             |
|  CPU:                                                      |
|  +----------------------------------------------------+    |
|  | 4 parallel nodes  2 cores = 8 cores              |    |
|  | Xeon E5620: 8 threads available                  |    |
|  +----------------------------------------------------+    |
+-------------------------------------------------------------+
```

### 4.12 Conclusion: Bellard-Style Execution Summary

```
+-------------------------------------------------------------+
|  GRAPH ENGINEERING EXECUTIVE SUMMARY                       |
|                                                             |
|  1. Parallelize -- Break tasks into isolated nodes         |
|  2. Judge with Opus -- Never cheap out on verification     |
|  3. Use -p for independence -- No context inheritance      |
|  4. Headless Shell -- Optimize visual testing              |
|  5. Persist knowledge -- claw.md + design.md               |
|  6. Orchestrate -- One meta-node coordinating specialists   |
|  7. Thermonuclear sparingly -- Pre-release only            |
|  8. Separate roles -- Detectors  Correctors              |
|                                                             |
|  MANDATE:                                                  |
|  +----------------------------------------------------+    |
|  | "Every node must be independently verified before |    |
|  |  data flows to the next node."                    |    |
|  +----------------------------------------------------+    |
|                                                             |
|  Phase: 0-bis Implementation Ready                        |
|  Next: ATOM Validation Pipeline Integration               |
+-------------------------------------------------------------+
```

---

## 5. Interface Specifications

### 5.1 Node Interface
All nodes must implement:
- `execute(input: Data) -> Data`: Process input and produce output
- `get_context_size() -> int`: Return allocated context window size
- `get_model() -> Model`: Return assigned AI model
- `get_priority() -> Priority`: Return execution priority level

### 5.2 Edge Interface
Edges must support:
- `transmit(source: Node, target: Node, data: Data)`: Transfer data between nodes
- `transform(data: Data) -> Data`: Optional data transformation
- `validate(data: Data) -> bool`: Data validation before transmission

### 5.3 Barrier Node Interface
- `wait_for_all(expected_count: int) -> bool`: Wait for specified number of reports
- `aggregate(reports: List[Report]) -> UnifiedReport`: Combine individual reports
- `timeout_ms() -> int`: Maximum wait time before triggering fallback

### 5.4 Fixing Agent Interface
- `consume(report: UnifiedReport) -> List[Fix]`: Parse report and generate fixes
- `apply(fixes: List[Fix]) -> bool`: Apply fixes to target codebase
- `validate() -> bool`: Verify fixes were applied correctly

---

## 6. Data Models

### 6.1 Report Structure
```yaml
Report:
  node_id: string
  node_type: string (worker|barrier|fixing|orchestrator)
  timestamp: datetime
  model_used: Model
  context_size: int
  findings: List[Finding]
  metrics: Metrics
```

### 6.2 Finding Structure
```yaml
Finding:
  id: string
  type: string (error|warning|info)
  severity: string (low|medium|high|critical)
  description: string
  location: string (file:line)
  suggested_fix: string (optional)
  confidence: float (0.0-1.0)
```

### 6.3 UnifiedReport Structure
```yaml
UnifiedReport:
  barrier_id: string
  timestamp: datetime
  node_reports: List[Report]
  aggregated_findings: List[Finding]
  pass_fail_decision: boolean
  rework_required: boolean
```

### 6.4 Fix Structure
```yaml
Fix:
  id: string
  target_file: string
  operation: string (replace|insert|delete)
  original_content: string
  new_content: string
  rationale: string
```

---

## 7. Security Considerations

1. **Context Isolation**: Each node runs in isolated memory space to prevent cross-contamination
2. **Session Security**: `-p` flag sessions use ephemeral processes with no persistent storage
3. **Data Sanitization**: All data flowing between edges is validated and sanitized
4. **Privilege Separation**: Detection agents run with minimal privileges; fixing agents require elevated privileges only for file modification
5. **Audit Trail**: All node executions, decisions, and fixes are logged for forensic analysis
6. **Secure Configuration**: `.graph-config.yaml` must be access-controlled and integrity-verified

---

## 8. Performance Considerations

1. **Token Management**: 
   - Monitor token consumption per node type
   - Implement dynamic model scaling based on workload
   - Cache frequent operations to reduce redundant computations

2. **Memory Optimization**:
   - Limit concurrent headless instances to 4 (based on Z600 capabilities)
   - Implement node-level memory pools
   - Garbage collect isolated contexts after node completion

3. **CPU Utilization**:
   - Pin nodes to specific CPU cores to reduce context switching
   - Use async I/O for non-blocking operations
   - Implement work-stealing scheduler for load balancing

4. **Latency Mitigation**:
   - Overlap I/O with computation where possible
   - Implement predictive prefetching for known data dependencies
   - Use connection pooling for repeated service calls

---

## 9. Implementation Plan

### Phase 1: Foundation (Weeks 1-2)
- [ ] Implement core node execution framework
- [ ] Create basic node types (Root, Worker, Barrier, Fixing)
- [ ] Establish edge communication mechanism
- [ ] Develop initial configuration parser

### Phase 2: Judgment & Isolation (Weeks 3-4)
- [ ] Implement Opus judgment node enforcement
- [ ] Develop `-p` flag mechanism for second opinion
- [ ] Add context isolation guarantees
- [ ] Create judgment performance monitoring

### Phase 3: Performance Optimization (Weeks 5-6)
- [ ] Integrate chrome-headless-shell for visual verification
- [ ] Implement `claw.md` and `design.md` knowledge anchors
- [ ] Add performance benchmarking suite
- [ ] Optimize resource allocation algorithms

### Phase 4: Orchestration & Skills (Weeks 7-8)
- [ ] Implement orchestrator meta-node
- [ ] Create specialist agent templates (Security, Design, Simplify)
- [ ] Develop skill chain configuration system
- [ ] Add skill creator plugin integration

### Phase 5: Advanced Features (Weeks 9-10)
- [ ] Implement thermonuclear review trigger
- [ ] Add correlation engine for cross-cutting issue detection
- [ ] Create fixing agent separation enforcement
- [ ] Develop audit and logging systems

### Phase 6: Validation & Release (Weeks 11-12)
- [ ] Conduct end-to-end integration testing
- [ ] Perform security penetration testing
- [ ] Validate against maturity level targets
- [ ] Prepare production deployment package
- [ ] Create operational runbooks

---

## 10. Open Questions and Risks

### Open Questions
1. What is the optimal number of concurrent worker nodes for different workload types?
2. How should we handle heterogeneous node capabilities (different CPU/memory profiles)?
3. What fallback mechanisms should be implemented when barrier timeout occurs?
4. How do we version and evolve the `.graph-config.yaml` schema over time?
5. What metrics should be exposed for observability and alerting?

### Identified Risks
1. **Token Explosion**: Uncontrolled parallel node creation could exceed budget
   - *Mitigation*: Implement node quotas and automatic scaling based on historical usage

2. **Barrier Deadlock**: A failed node could permanently block the barrier
   - *Mitigation*: Implement timeout-based fallback to sequential execution with alerting

3. **Context Bleed**: Despite isolation efforts, shared resources could cause leakage
   - *Mitigation*: Regular memory auditing and process-level isolation verification

4. **Design Drift**: Inconsistent `design.md` updates causing verification failures
   - *Mitigation*: Implement design file locking and change approval workflow

5. **Skill Chain Complexity**: Overly complex verification chains slowing execution
   - *Mitigation*: Implement chain optimization and parallel execution where safe

6. **Headless Shell Incompatibility**: Future OS/browser updates breaking headless mode
   - *Mitigation*: Maintain compatibility matrix and provide graceful degradation to full Chrome

---

## 11. Approval

- **Prepared by:** Bellard Protocol  
- **Reviewed by:** *[Name]* (Lead Architect)  
- **Approved:** **[ ] Pending**  
- **Review Date:** 2026-08-12  

*End of Design Specification*

