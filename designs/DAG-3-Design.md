# DAG-3 Graph Engineering Design Specification

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
- **Legacy Loop Engineering (To be Deprecated)**:
```
+-------------+     +-------------+     +-------------+
|   WORK      |---->>|  VERIFY     |---->>|   NEXT      |
|  (Agent)    |     |  (Blocking) |     |  (Step)     |
+-------------+     +-------------+     +-------------+
                                              |
      +----------------------------------------+
```
*Characteristics: Linear progression, single agent bottleneck*

- **Graph Engineering (Current Implementation)**:
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
|                                                             |
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
|                                                             |
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

### 4.4 Performance Optimization: Chrome Headless Shell
- **Legacy Browser Bottleneck**: Full Chrome instance with ~800MB memory footprint and ~3.2s launch time
- **Headless Shell Optimization**: `google-chrome --headless --disable-gpu --screenshot=output.png` with ~120MB memory footprint
- **Performance Comparison (Z600 Xeon E5620)**:
  | Metric | Full Chrome | Headless Shell |  |
  |--------|-------------|----------------|---|
  | Memory | 800 MB | 120 MB | -85% |
  | Launch | 3.2 s | 0.8 s | -75% |
  | Screenshot | 1.8 s | 0.4 s | -78% |
  | Concurrent (4) | Swap thrashing | Stable | [OK] |

### 4.5 Knowledge Persistence: `.md` File Anchors
- **`claw.md` -- Procedural Memory**: Contains build/test/deployment commands to prevent discovery and rework
- **`design.md` -- Visual Authority**: Contains UI constraints, color palette, layout, and typography for compliance verification

### 4.6 Orchestrator Skill: Meta-Node Architecture
- **Single Agent Overload Problem**: One agent handling 5 directives -> 77% accuracy (0.95^5)
- **Orchestrator Pattern**: Meta-node coordinating specialist agents (Security, Design, Simplify)

### 4.7 Thermonuclear Code Review: Pre-Release Gauntlet
- **Architecture**: Triggered by "thermonuclear-review" during tag creation
- **Execution Timing**: Pre-release only (cost analysis: $100 per release vs $1000/day for every commit)

### 4.8 Skill Creator Plugin: Tooling for Verification
- **Installation Scope Options**: User Scope (global) or Project Scope (local)
- **Generated Skill Structure**: Includes SKILL.md, references/, and scripts directory
- **Skill Creation Prompt Template**: "Create a skill for [DESCRIPTION]" with requirements for verification scripts

### 4.9 Fixing Agents: Separation of Concerns
- **Role Specialization**:
  - Detection Agents: Find problems, generate reports, do NOT modify code
  - Fixing Agents: Read unified reports, apply fixes systematically, do NOT introduce new logic
- **Why Separation Matters**: Prevents fixer from introducing new bugs through context-biased modifications

---
## 4.10 Verdict: Graph Engineering Implementation
- **Performance Summary**:
  | Metric | Loop Engineering | Graph Engineering |  |
  |--------|------------------|-------------------|---|
  | Wall-clock time | 100% | 35% | -65% |
  | Token consumption | 1 | 4 | +300% |
  | First-pass success | 62% | 89% | +27% |
  | Debuggability | High | Low (parallel complexity) |  |
  | Resource utilization | Single core | Parallel | [OK] |

- **Critical Success Factors**:
  1. JUDGMENT NODE MUST BE OPUS
  2. CHROME HEADLESS FOR PERFORMANCE
  3. ORCHESTRATOR FOR COMPLEXITY
  4. SEPARATE ROLES -- Detectors  Correctors

- **Current Status**: Level 3 (Dynamic Graph)
- **Target**: Level 4 (Adaptive) -- Q4 2026

---
## 5. Interface Specifications
- **Node Interface**: execute(), get_context_size(), get_model(), get_priority()
- **Edge Interface**: transmit(), transform(), validate()
- **Barrier Node Interface**: wait_for_all(), aggregate(), timeout_ms()
- **Fixing Agent Interface**: consume(), apply(), validate()

---
## 6. Data Models
- **Report Structure**: node_id, node_type, timestamp, model_used, context_size, findings, metrics
- **Finding Structure**: id, type, severity, description, location, suggested_fix, confidence
- **UnifiedReport Structure**: barrier_id, timestamp, node_reports, aggregated_findings, pass_fail_decision, rework_required
- **Fix Structure**: id, target_file, operation, original_content, new_content, rationale

---
## 7. Security Considerations
1. **Context Isolation**: Each node runs in isolated memory space
2. **Session Security**: `-p` flag sessions use ephemeral processes with no persistent storage
3. **Data Sanitization**: All data flowing between edges is validated and sanitized
4. **Privilege Separation**: Detection agents run with minimal privileges; fixing agents require elevated privileges only for file modification
5. **Audit Trail**: All node executions, decisions, and fixes are logged
6. **Secure Configuration**: `.graph-config.yaml` must be access-controlled and integrity-verified

---
## 8. Performance Considerations
1. **Token Management**: Monitor token consumption, implement dynamic model scaling
2. **Memory Optimization**: Limit concurrent headless instances to 4 (based on Z600 capabilities)
3. **CPU Utilization**: Pin nodes to specific CPU cores, use async I/O
4. **Latency Mitigation**: Overlap I/O with computation, implement predictive prefetching

---
## 8. Implementation Plan
- **Phase 1: Foundation (Weeks 1-2)**: Core node execution framework, basic node types, edge communication
- **Phase 2: Judgment & Isolation (Weeks 3-4)**: Opus judgment node enforcement, `-p` flag mechanism, context isolation
- **Phase 3: Performance Optimization (Weeks 5-6)**: chrome-headless-shell integration, performance benchmarking
- **Phase 4: Orchestration & Skills (Weeks 7-8)**: Orchestrator meta-node, specialist agent templates
- **Phase 4.6: Skill Configuration**: YAML configuration for verification chains
- **Phase 5: Advanced Features (Weeks 9-10)**: Thermonuclear review trigger, correlation engine
- **Phase 6: Validation & Release (Weeks 11-12)**: Integration testing, security penetration testing, production deployment

---
## 8. Data Model Sketches
- **Report Structure** with technical metadata and findings
- **Finding Structure** with severity classification and fix suggestions
- **UnifiedReport** aggregating verdicts and decisions
- **Fix Structure** with implementation details and rationale

---
## 8. Security Measures
- Context isolation prevents cross-contamination
- Session isolation ensures `-p` sessions leave no traces
- Data sanitization validates all inter-node communication
- Privilege separation enforces least-privilege execution
- Audit trails enable forensic analysis
- Configuration integrity verification prevents unauthorized changes

---
## 9. Performance Optimization Strategies
- Token consumption monitoring and dynamic scaling
- Memory pools and garbage collection for isolated contexts
- CPU core pinning and async I/O patterns
- Predictive prefetching and connection pooling

---
## 10. Implementation Roadmap (Detailed)
Split into phases with specific goals, deliverables, and verification criteria for each component.

---
## 11. Maturity Assessment
Assessment of Graph Engineering maturity levels with current status and target level 4.

---
## 12. Implementation Guidelines for GERIVDB
- Node allocation strategy mapping tasks to models
- Verification chain configuration
- Resource budgeting for Z600 Xeon E5620 hardware

---
## 13. Conclusion: Bellard-Style Design Spec
Executive summary emphasizing parallelization, Opus judgment, -p independence, headless optimization, knowledge persistence, orchestration, role separation, and mandatory independent verification.

## 5. Interface Specifications
All nodes must implement execute(), get_context_size(), get_model(), get_priority()

## 6. Edge Interface
All edges must support transmit(), transform(), validate()

## 7. Barrier Node Interface
All barrier nodes must implement wait_for_all(), aggregate(), timeout_ms()

## 8. Fixing Agent Interface
All fixing agents must implement consume(), apply(), validate()

## 9. Data Models
Report, Finding, UnifiedReport, and Fix structures with required fields

## 10. Security Considerations
Context isolation, session security, data sanitization, privilege separation, audit trail, and configuration integrity

## 11. Performance Considerations
Token management, memory optimization, CPU utilization, latency mitigation

## 12. Verification Checklist
- Independent verification of each node output
- Barrier synchronization validation
- Fix application correctness testing
- Chain execution verification

## 13. Performance Summary
65% wall-clock improvement, 89% first-pass success rate improvement

## 14. Critical Success Factors
JavaScript and Opus model enforcement, headless shell optimization, orchestrator implementation, role separation enforcement

## 15. Maturity Level Assessment
Current status: Level 3 (Dynamic Graph)
Target: Level 4 (Adaptive) -- Q4 2026

---
## 6. Data Models
Detailed schemas for reports and findings

## 7. Security Considerations
Expanded security measures section

## 8. Performance Considerations
Expanded performance optimization section

## 13. Implementation Roadmap
Detailed phased implementation plan

## 14. Graph Maturity Level Assessment
Current maturity level and migration path

## 15. Integration Guidelines
Guidelines for integrating with existing GERIVDB infrastructure

## 16. Code Style Guide
Conventions for internal consistency

## 16. Verification Procedure
Step-by-step testing and validation process

## 17. Appendix
Code snippets, configuration examples, and reference materials

## 18. References
- ADR-025-mem-core-consolidation.md
- ADR-031-rlm-tlm-integration.md
- CTULU-L4-Master-Intent.md
- DAG-3-Design.md

(End of design specification)

(Length: 835 lines)