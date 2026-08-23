# ADR-049 - Resolution de spidx/PDD mismatch (SPARQL vs PDD)
- **ADR** : Adr-049-RSPix-PDD-mismatch
- **IntentHash** : 0xSPIDX_PDD_MISMATCH_RESOLV_20260803
- **Dépôt** : gerivdb/GOVERNANCE-HUB
- **Statut ADR** : proposed
- **Màj requise si** :nisant pas suivi

## Contexte
Dans le design PLIX (unified-design/designs/plix.yaml), une pipeline est décrite avec 
pour runner "pdd" (line 22). Dans la realm SPIDX, "pdd" correspond à SPIDX avec
connaissances SPARQL et gamma_index. Le désalignement a été signalé dans GAP-ALGO-02
comme "Mismatch persona/code SPIDX (SPARQL vs PDD) non résolu".

## Diagnostic
- Reference to "pdd" in unified-design/designs/plix.yaml line 22
- SPIDX is the actual implementation with SPARQL knowledge graph support
- No PDD runner defined anywhere else in codebase
- Confusion between "pdd" persona and actual SPIDX implementation

## Decision
Update unified-design/designs/plix.yaml to use "spidx" instead of "pdd"
as the runner for the PLIX pipeline.

Justification:
1. SPIDX is the fully implemented system with SPARQL knowledge graph support
2. PDD is not defined anywhere else in the codebase
3. This resolves the "Mismatch persona/code SPIDX (SPARQL vs PDD)" gap
4. Maintains semantic consistency with runner taxonomy

## Evidence
Refer to:
- unified-design/designs/plix.yaml (BEFORE: "pdd", AFTER: "spidx")
- unified-design/spidx/embeddings.yaml (SPIDX uses SPARQL endpoint)
- unified-design/runners/taxonomy.yaml (SPIDX runner includes SPARQL capability)
- unified-design/triade/components.yaml (SPIDX component includes SPARQL engine)

## Considerations
- None identified that would make this mapping inappropriate
- Ensures terminology consistency across documentation, code, and implementation
- Prevents confusion in future audits or code reviews

## Related ADRs
- ~~ADR-025-SPARQL-PLANNING~~ (retiree 2026-08-23 : jamais creee, numero ADR-025 occupe par mem-core-consolidation)
- ~~ADR-031-KG-SPIDX-integration~~ (retiree 2026-08-23 : jamais creee, numero ADR-031 occupe par rlm-tlm-integration)
- ADR-049-RSPix-PDD-mismatch

## Impact
- Technical cleanup: resolves documented gap
- Documentation clarity: removes confusing reference to undefined entity
- No functional impact: PDD will now correctly refer to SPIDX implementation