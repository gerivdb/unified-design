---
type: ADR
version: "1.0.0"
status: proposed
date: "2026-08-16"
intent_hash: 0xADR_040_MOC3_DIP_PORTS_ADAPTERS_20260816
---

# ADR-040 - MOC-3 DIP / Ports & Adapters Inter-Strates

## Problem Statement

Le MDU v2.1.0 viole le principe Dependency Inversion (DIP) : les strates supérieures (L1-L4) dépendent d'implémentations concrètes définies dans `meta-design.yaml` et `META-DESIGN.md` au lieu de dépendre d'abstractions.

Constat dans `meta-design.yaml` :
- `capabilities` référence des implémentations concrètes : `protocol: "MCP"`, `storage_backend: "sqlite+wal"`, `validator_model: "openai-codex"`.
- `agents_par_pilier` liste des noms de repos concrets sans contrat abstrait.
- `design_rules` contient des checks couplés à des protocoles spécifiques (ex: `mcp_symbol_access_required`).

Conséquence : impossible de remplacer un composant (ex: passer de `sqlite+wal` à `postgres`) sans toucher au MDU canonique. Toute substitution d'implémentation casse la compatibilité des strates supérieures.

## Decision

### Adopter le pattern Ports & Adapters pour les capacités inter-strates

**Principe :** Les strates supérieures (L1-L4) ne dépendent que d'abstractions (ports) définies dans L0-CANON. Les implémentations concrètes (adapters) sont décrites par strate, pas dans le MDU canonique.

### Structure cible

```
L0-CANON/
  ports/
    registry.yaml              # Registre des ports
    symbol-retrieval/
      port.yaml                # Contrat abstrait
      input_schema.json        # Schéma d'entrée
      output_schema.json       # Schéma de sortie
    beads-sql-memory/
      port.yaml
      input_schema.json
      output_schema.json
    ...
```

### Règles

| Règle | Description |
|-------|-------------|
| **R-DIP-001** | Toute capacité du MDU doit référencer un `port_id` existant dans `ports/registry.yaml`. |
| **R-DIP-002** | Un `port_id` possède obligatoirement un contrat formel : `input_schema` + `output_schema` (JSON Schema). |
| **R-DIP-003** | Les implémentations concrètes (ex: `MCP`, `sqlite+wal`) sont décrites dans `adapters/*.yaml` par strate, pas dans `meta-design.yaml`. |
| **R-DIP-004** | `design_rules` référence des `port_id`, jamais des noms d'implémentation. |
| **R-DIP-005** | L'ajout d'une nouvelle implémentation pour un port existant ne modifie pas `meta-design.yaml` ni `META-DESIGN.md`. |

### Mapping de migration

| Capacité actuelle (concrète) | Port abstrait | Adapter existant |
|------------------------------|---------------|------------------|
| `symbol-retrieval` (MCP) | `symbol-retrieval` | `adapters/L1/symbol-retrieval-mcp.yaml` |
| `beads-sql-memory` (sqlite+wal) | `beads-sql-memory` | `adapters/L1/beads-sql-memory-sqlite.yaml` |
| `worktree-isolation` | `worktree-isolation` | `adapters/L2/worktree-isolation-git.yaml` |
| `exit-interceptor` | `exit-interceptor` | `adapters/L5/exit-interceptor-hook.yaml` |
| `tdd-airain-law` | `tdd-airain-law` | `adapters/L4/tdd-airain-law-test.yaml` |
| `trace-replay-proof` | `trace-replay-proof` | `adapters/L6/trace-replay-proof-sqlite.yaml` |

### Impact sur `meta-design.yaml`

Avant :
```yaml
capabilities:
  - name: symbol-retrieval
    description: "..."
    parameters:
      protocol: "MCP"
      transport: "stdio"
```

Après :
```yaml
capabilities:
  - port_id: symbol-retrieval
    description: "..."
    parameters:
      max_symbols_per_call: 50
      context_savings_tokens: 16000
```

## Alternatives Considered

1. Garder les implémentations concrètes dans `capabilities` (choix actuel) -- rejeté : couplage fort, violation DIP.
2. Dupliquer les capabilities par strate -- rejeté : duplication, drift.
3. Supprimer les capabilities du MDU -- rejeté : perte de traçabilité des invariants.
4. Ports & Adapters avec contrats formels (choisi) -- conforme DIP, substitution d'implémentation sans modification du MDU.

## Consequences

- **Positif** : Substitution d'implémentation possible sans toucher au MDU canonique.
- **Positif** : `meta-design.yaml` ne contient plus que des abstractions stables.
- **Positif** : Tests de conformité DIP possibles par vérification de `design_rules` contre `ports/registry.yaml`.
- **Négatif** : Coût initial de migration de 6 capabilities existantes.
- **Négatif** : Courbe d'apprentissage pour les contributeurs (concept Port/Adapter).

## Validation

- **Preuve** : Analyse statique de `meta-design.yaml` v2.1.0 -- 6 implémentations concrètes identifiées.
- **Conformité** : Respecte ADR-2026-06-28-001 (architecture logique N+1/N+2/N+3/N+4).
- **RSS-v2.3** : Conforme.

## Reference ADR

- **ADR** : ADR-040-moc3-dip-ports-adapters
- **IntentHash** : 0xADR_040_MOC3_DIP_PORTS_ADAPTERS_20260816
- **Dépôt** : gerivdb/unified-design
- **Statut ADR** : proposed
- **Màj requise si** : statut ADR passe à deprecated ou superseded


