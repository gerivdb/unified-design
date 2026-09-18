---
name: deterministic-execution-log-clipping
description: "Mécanisme de vérification anti-hallucination par capture déterministe des logs d'exécution. Inspiré de DeepMind Co-Scientist : réduction des résultats fabriqués de 90% à 4%, élimination de la fabrication complète (0.0%)."
version: "1.0.0"
status: active
layer: L1
intent_hash: 0xATOM_DETERMINISTIC_EXECUTION_LOG_CLIPPING_20260918
inherits:
  - agent-observability-architecture
  - independent-sources-rule
depends_on:
  - agent-observability-architecture
  - independent-sources-rule
capabilities:
  - name: assertion-verification-pipeline
    description: "Vérification d'affirmations : comparer l'affirmation de l'agent contre les logs d'exécution bruts et la télémétrie enregistrée dans la trace"
    parameters:
      source: execution_log_dag
      action_on_mismatch: [reject, rewrite]
  - name: deterministic-span-sensor
    description: "Capteur de trace déterministe : interroger le DAG pour un span execute_tool:<tool>"
    parameters:
      example: pytest_span
      false_positive_risk: zero
  - name: cross-family-evaluator
    description: "Évaluateur de familles croisées : éviter les biais de préférence en utilisant des évaluateurs de familles différentes"
    parameters:
      pattern: claude-verifies-gemini
      deterministic_sensor: required
  - name: anomaly-circuit-breaker
    description: "Coupe-circuit automatique : MAD du nombre d'étapes > 3.5 ou variance entropie tokens < 0.02 sur 4 spans consécutifs"
    parameters:
      mad_threshold: 3.5
      entropy_variance_threshold: 0.02
      consecutive_spans: 4
principles:
  - P0_DETERMINISTIC_VERIFICATION: la trace elle-même sert de capteur de vérification actif
  - P0_NO_LLM_JUDGE_ALONE: un juge LLM seul est vulnérable au piratage de récompense ; toujours coupler à un capteur déterministe
  - P0_EXECUTION_LOG_CLIPPING: toute affirmation non ancrée dans un span d'exécution concret est rejetée ou réécrite
  - P0_FABRICATION_RATE_ZERO: la fabrication complète de données doit être éliminée (0.0%)
