---
name: umodel-agent-ready-data
description: "ATOM pour le modèle de données unifié UModel d'Alibaba Cloud. Garantit que toute télémétrie, signal ou playbook intégré au MDU respecte les 4 piliers Agent-Ready : sémantiquement riche, contextualisé, actionnable, structuré/standardisé."
version: "1.0.0"
status: active
layer: L1
intent_hash: 0xATOM_UMODEL_AGENT_READY_DATA_20260918
inherits:
  - agent-observability-architecture
  - umodel-agent-ready-data
depends_on:
  - agent-observability-architecture
  - umodel-agent-ready-data
  - meta-coherence
capabilities:
  - name: semantic-metadata-check
    description: "Vérifier que toute donnée ingérée possède des métadonnées auto-descriptives (unité, type, requête)"
    parameters:
      required_fields: [unit, type, query_description]
      reject_if_missing: true
  - name: knowledge-graph-linkage
    description: "Tout nouvel événement doit être relié au graphe de connaissances existant (entité -> dépendances)"
    parameters:
      mandatory_link: true
      orphan_policy: reject
  - name: actionability-audit
    description: "Auditer que chaque signal/alerte dispose d'un levier d'action associé (playbook, script, runbook)"
    parameters:
      coverage_required: 100%
      exception_process: ADR
  - name: unified-schema-validation
    description: "Valider la conformité au schéma unifié avant ingestion dans le triple magasin"
    parameters:
      stores: [Prometheus, Elasticsearch, Jaeger]
      validation_point: ingestion
principles:
  - P0_UMODEL_PILLARS: aucune donnée Agent-Ready ne peut violer les 4 piliers UModel
  - P0_GRAPH_FIRST_INTEGRATION: l'intégration privilégie le graphe sémantique plutôt que les tables cloisonnées
  - P0_ACTIONABILITY_BY_DEFAULT: un signal sans action est une dette observabilité
  - P0_MCP_EXPOSURE: la topologie unifiée est exposée aux agents via MCP, pas via dashboards statiques
