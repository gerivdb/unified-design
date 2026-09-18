---
name: agent-swarm-self-improving-loop
description: "ATOM pour l'architecture agentique auto-améliorante. Toute boucle agentique doit avoir une condition d'arrêt explicite. La mémoire est un graphe. Les corrections sont accumulées. Le prompt est séparé de SKILL.md."
version: "1.0.0"
status: active
layer: L1
intent_hash: 0xATOM_AGENT_SWARM_SELF_IMPROVING_LOOP_20260918
inherits:
  - consciousness
  - agent-observability-architecture
  - agent-swarm-self-improving-loop
depends_on:
  - consciousness
  - agent-observability-architecture
  - agent-swarm-self-improving-loop
  - meta-coherence
capabilities:
  - name: mandatory-stop-condition
    description: "Toute boucle agentique doit définir sa condition d'arrêt avant exécution (compteurs, seuils, hard caps)"
    parameters:
      required: true
      format: counters_not_adjectives
      hard_caps_required: true
  - name: graph-memory-requirement
    description: "La mémoire des agents doit être structurée en graphe, pas en liste plate"
    parameters:
      structure: graph
      node_verification: independent_sources
      correction_edges: required
  - name: no-repeat-errors
    description: "Une erreur corrigée ne doit pas être répétée ; correction accumulée obligatoire"
    parameters:
      correction_persistence: true
      graph_weight_update: required
  - name: skill-md-contract
    description: "SKILL.md est le contrat versionné ; le prompt est un échantillon d'intention"
    parameters:
      skill_md_role: versioned_contract
      prompt_role: sample
      layers: [L0, L1, L2, L3]
principles:
  - P0_ATOMIC_LOOP_CONTRACT: une boucle sans condition d'arrêt explicite est interdite
  - P0_GRAPH_MEMORY_NON_NEGOTIABLE: la mémoire plate est interdite pour les agents swarm
  - P0_CORRECTION_IS_LEARNING: toute correction enrichit le graphe de mémoire
  - P0_SKILL_MD_OVERRIDES_PROMPT: en cas de conflit, SKILL.md prime sur le prompt
