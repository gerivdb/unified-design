---
type: ADR
status: proposed
date: "2026-07-31"
intent_hash: 0xADR_033_SYMBOL_RETRIEVAL_MCP_20260731
---

# ADR-033: Symbol Retrieval via MCP (Serena Pattern)

## Context

Claude Code consomme environ 16 000 tokens de fenêtre de contexte avant la première saisie utilisateur, à cause de descriptions d'outils intégrées invisibles et non éditables (source: "Graph of Loops" L3 - Serena).

## Decision

Remplacer les lectures de fichiers complètes (Read/Edit bruts) par une récupération au niveau du symbole via Model Context Protocol (MCP) avec le serveur Serena.

- L'agent n'extrait que la fonction/classe spécifique et ses références
- Au lieu de lire un fichier de 2 000 lignes, on récupère seulement le symbole ciblé
- Économie estimée: ~16 000 tokens par session

## Implementation

Nouvel atom: `ATOM-049-symbol-retrieval-mcp`
- Capability: `symbol-retrieval` (protocol: MCP, transport: stdio)
- Hérite de: `sonar-driven-design`, `attention-mechanism`
- Nouvelles design_rules: `symbol-retrieval-mandatory` (check: mcp_symbol_access_required)

## Consequences

### Positive
- Récupération massive de mémoire de travail (~16k tokens)
- Précision accrue: l'agent voit exactement ce dont il a besoin
- Compatible avec l'architecture MDU existante

### Negative
- Dépendance au serveur MCP Serena (disponibilité, versioning)
- Latence ajoutée pour l'appel MCP (mitigé: max_latency_ms: 10)

## References

- Graph of Loops, Section 1: "La récupération du contexte (Le coût caché des 16 000 tokens)"
- ATOM-049-symbol-retrieval-mcp.yaml
- meta-design.yaml v2.1.0 (capabilities + design_rules extended)
- loop_engine/mcp_symbol_retriever.py