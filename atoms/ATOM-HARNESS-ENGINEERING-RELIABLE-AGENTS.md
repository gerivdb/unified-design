---
name: harness-engineering-reliable-agents
description: "ATOM pour le Harness Engineering. Tout agent de production doit être encapsulé dans un harnais : Contract Validator, Context Compiler, Policy Engine, State Manager, Verification Engine, Trace Recorder. Le modèle probabiliste est transformé en exécutant déterministe."
version: "1.0.0"
status: active
layer: L1
intent_hash: 0xATOM_HARNESS_ENGINEERING_RELIABLE_AGENTS_20260918
inherits:
  - agent-observability-architecture
  - deterministic-execution-log-clipping
  - harness-engineering-reliable-agents
depends_on:
  - agent-observability-architecture
  - deterministic-execution-log-clipping
  - harness-engineering-reliable-agents
  - meta-coherence
capabilities:
  - name: mandatory-harness
    description: "Tout agent de production doit être encapsulé dans un harnais ; pas d'agent libre"
    parameters:
      enforce: true
      exception: none
  - name: contract-validation-gate
    description: "Le contrat de tâche est validé avant toute exécution ; rejet si invalide"
    parameters:
      validation_point: pre_execution
      reject_on_invalid: true
  - name: context-compilation
    description: "Le contexte est compilé (fenêtre glissante, fraîcheur, embedding drift), pas injecté brut"
    parameters:
      context_window: bounded
      freshness_check: required
      embedding_drift: monitored
  - name: policy-enforcement
    description: "Les politiques sont appliquées par le harnais, pas par l'agent ; override humain seulement"
    parameters:
      enforcement: mandatory
      override: human_only
  - name: durable-state
    description: "L'état est durable et rejouable ; WAL obligatoire"
    parameters:
      persistence: append_only_ledger
      replay: deterministic
      recovery: automatic
principles:
  - P0_HARNESS_MANDATORY: pas d'agent de production sans harnais
  - P0_CONTRACT_GATE: pas d'exécution sans contrat validé
  - P0_CONTEXT_COMPILED: pas de contexte brut injecté
  - P0_POLICY_NOT_AGENT: les politiques sont dans le harnais, pas dans l'agent
  - P0_STATE_REPLAYABLE: tout état doit être rejouable déterministement
