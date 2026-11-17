---
name: ragx-query-skill
description: >
  Skill de requête RAGX. Permet d'interroger le pont RAGX via
  POST /conversations/search (recherche sémantique ternaire) et POST /query
  (requête SQL read-only sur DuckDB). Retourne les Knowledge Items les plus
  pertinents pour une requête donnée.
version: "1.0.0"
status: active
layer: L0-CANON
intent_hash: 0xSKILL_RAGX_QUERY_20261117
triggers:
  - "rechercher KI dans RAGX"
  - "query sémantique ternaire RAGX"
  - "interroger base de connaissances RAGX"
inputs:
  - type: query
    description: "Texte de la requête de recherche"
  - type: top_k
    description: "Nombre de résultats retournés (défaut 5)"
outputs:
  - type: search_results
    description: "Liste des KI les plus pertinents avec score de similarité"
  - type: query_result
    description: "Résultat de requête SQL read-only"
tools:
  - http_client
artifacts:
  - path: reports/ragx-query-*.json
    format: json
governance:
  adr: ADR-2026-10-09-001-RAGX-CUBE-A-SEPARATION
  design: documentation-ragx-integration
  atom: atom-documentation-technique
  atom: atom-documentation-universitaire
---

# Skill : RAGX Query

## Description

Skill de requête RAGX. Permet d'interroger le pont RAGX via
POST /conversations/search (recherche sémantique ternaire) et POST /query
(requête SQL read-only sur DuckDB). Retourne les Knowledge Items les plus
pertinents pour une requête donnée.

## When to use

- Quand on cherche un Knowledge Item spécifique dans RAGX
- Pour valider qu'un KI a été correctement injecté et indexé
- Pour faire de la recherche sémantique sur les connaissances stockées

## Process

### ÉTAPE-1 — Formuler la requête
Définir le texte de recherche et le nombre de résultats souhaités (top_k).

### ÉTAPE-2 — Appeler RAGX
Appeler POST http://127.0.0.1:8853/conversations/search avec le payload JSON.

### ÉTAPE-3 — Vérifier les résultats
Vérifier que les KI retournés possèdent un IntentHash valide et une provenance claire.

## Anti-patterns

- Interroger RAGX sans token d'authentification (CONVERSATIONS_SEARCH_TOKEN requis)
- Utiliser des requêtes non-SQL sur l'endpoint /query

## References

- **Design** : `designs/documentation-ragx-integration/design.yaml`
- **Primitive** : `atoms/documentation-technique.atom.yaml`, `atoms/documentation-universitaire.atom.yaml`
- **Repo cible** : `gerivdb/RAGX` (L0-CANON)
