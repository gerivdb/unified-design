---
name: deepmind-co-scientist-reliability
description: "ATOM pour le protocole de fiabilité DeepMind Co-Scientist. Toute affirmation d'agent doit être vérifiée par un capteur déterministe sur la trace d'exécution. Les évaluateurs LLM seuls sont interdits. Les résultats fabriqués sont ciblés à 4%, la fabrication complète à 0.0%."
version: "1.0.0"
status: active
layer: L1
intent_hash: 0xATOM_DEEPMIND_CO_SCIENTIST_RELIABILITY_20260918
inherits:
  - agent-observability-architecture
  - deterministic-execution-log-clipping
  - deepmind-co-scientist-reliability
depends_on:
  - agent-observability-architecture
  - deterministic-execution-log-clipping
  - deepmind-co-scientist-reliability
  - meta-coherence
capabilities:
  - name: assertion-anchoring
    description: "Toute affirmation d'agent doit être ancrée dans un span d'exécution concret du DAG de trace"
    parameters:
      allowed_sources: [execution_log_dag, telemetry_spans]
      reject_if_unanchored: true
      action: [reject, rewrite]
  - name: llm-judge-prohibition
    description: "Interdiction d'utiliser un évaluateur LLM seul pour valider une affirmation d'agent"
    parameters:
      exception: cross_family_evaluator_with_deterministic_sensor
      false_positive_risk: zero
  - name: fabrication-rate-enforcement
    description: "Respect des cibles de taux de fabrication : 4% pour les résultats fabriqués, 0.0% pour la fabrication complète"
    parameters:
      fabricated_target: 4%
      complete_fabrication_target: 0.0%
      measurement: double_blind_review
  - name: dangerous-direction-refusal
    description: "Refuser automatiquement les directions de recherche jugées dangereuses"
    parameters:
      refusal_rate_target: 98.7%
      criteria: safety_policy_violation
      human_override: required
principles:
  - P0_CO_SCIENTIST_VERIFICATION: l'affirmation de l'agent est vérifiée par capture déterministe des logs d'exécution, pas par évaluation textuelle
  - P0_ZERO_FABRICATION: la fabrication complète de données est interdite (0.0%), mesurée par double aveugle
  - P0_SAFETY_OVER_AUTONOMY: une direction dangereuse est refusée même si elle semble prometteuse ; l'override humain est requis
  - P0_EXECUTION_LOG_CLIPPING_ATOMIC: l'atom interdit le stockage ou l'acceptation d'une affirmation sans span d'exécution correspondant
