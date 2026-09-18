---
name: reasoningbank-persistent-strategy
description: "ATOM pour la Banque de Raisonnement (ReasoningBank). Toute trace d'exécution d'agent doit être distillée en stratégies réutilisables avant archivage. Les échecs produisent des garde-fous négatifs. Les stratégies sont réinjectées dans les prompts futurs."
version: "1.0.0"
status: active
layer: L1
intent_hash: 0xATOM_REASONINGBANK_PERSISTENT_STRATEGY_20260918
inherits:
  - agent-observability-architecture
  - reasoningbank-persistent-strategy
depends_on:
  - agent-observability-architecture
  - reasoningbank-persistent-strategy
  - meta-coherence
capabilities:
  - name: mandatory-distillation
    description: "Toute trace brute doit passer par le pipeline de distillation avant d'être stockée dans le ReasoningBank"
    parameters:
      forbid_raw_storage: true
      stages: [ast_stdout_elision, semantic_deduplication, causal_graph_pruning]
  - name: failure-to-guardrail
    description: "Un échec d'agent doit produire au moins un garde-fou négatif stocké dans le ReasoningBank"
    parameters:
      minimum_output: 1
      format: negative_guardrail
  - name: success-to-heuristic
    description: "Un succès d'agent doit produire au moins une heuristique généralisable stockée dans le ReasoningBank"
    parameters:
      minimum_output: 1
      generalizability_check: required
  - name: prompt-reinjection
    description: "Les stratégies du ReasoningBank sont réinjectées dans les prompts agents lors de l initialisation de session"
    parameters:
      injection_point: session_bootstrap
      freshness_check: 24h
principles:
  - P0_REASONINGBANK_ATOMICITY: chaque expérience agent = une entrée ReasoningBank distillée, pas de trace brute stockée
  - P0_FAILURE_FIRST: les échecs sont la source prioritaire de garde-fous ; les succès produisent des heuristiques
  - P0_REINJECT_NOT_ONLY_READ: le ReasoningBank n'est pas une archive consultable, c'est une mémoire active injectée dans les prompts
  - P0_COMPRESSION_GUARANTEE: toute entrée ReasoningBank respecte les ratios de compression du pipeline avant stockage
