# Compliance Scanner Design

> Scanner de conformite MDU/RSS/ARGUS — detection automatisee des manques de conformite.

## Vue d'ensemble

Le **Compliance Scanner** est un design MDU L0 qui implemente la detection automatisee des gaps de conformite dans tous les repos `gerivdb/*`. Il resout le probleme identifie dans `PRD-RADX-MDU-CONFORMITY-2026-08-28.md` : aucun agent n\'etait explicitement charge de verifier qu\'un repo a son design, son atom, son citizen, ses ADRs indexees et son checkpoint MDU.

## Capacites

### repo-audit
Scanner complet d\'un repo pour verifier sa conformite MDU/RSS/ARGUS.

**Checks implementes** :
- `design_registered` : Le repo a-t-il un design dans `unified-design/designs/<repo>/` ?
- `atom_registered` : Le repo a-t-il un atom dans `unified-design/atoms/<repo>.yaml` ?
- `citizen_registered` : Le repo est-il declare dans `unified-design/citizens.yaml` ?
- `adr_indexed` : Les ADRs du repo sont-elles referencées dans `catalog/adrs.index.yaml` ?
- `mdu_checkpoint` : Le repo a-t-il un checkpoint dans `.mdu/checkpoint.json` ?
- `rss_compliant` : Le repo respecte-t-il les normes RSS (REPO-STANDARDS L4) ?
- `argus_clean` : ARGUS ne detecte-t-il aucune pathologie (GAP/GHOST/DRIFT/...) sur ce repo ?

## Architecture

```
Compliance Scanner
    |
    +-- unified-design (source de verite MDU)
    |     |
    |     +-- designs/ (registre designs)
    |     +-- atoms/ (registre atoms)
    |     +-- citizens.yaml (registre citizens)
    |     +-- catalog/ (index designs, ADRs)
    |     +-- .mdu/checkpoint.json (checkpoints)
    |
    +-- argus (moteur detection pathologies)
    |     |
    |     +-- scanners/ (7 pathologies)
    |     +-- rules/ (CorrelationRules NEXUS)
    |
    +-- repo-standards (normes RSS L4)
          |
          +-- META-DESIGN.md
          +-- meta-design.yaml
          +-- atoms_registry.yaml
```

## Integration ARGUS

Le Compliance Scanner s\'integre a ARGUS comme un scanner specialise :
- Invoque via `argus scan --check compliance`
- Produit un rapport `COMPLIANCE_REPORT.json`
- Alimente le WAL ARGUS pour traçabilité
- Declenche corrections auto-applicables (patches) pour gaps simples

## Utilisation

```bash
# Scan complet conformite
python unified-design/scripts/compliance_scanner.py --all-repos --strict

# Scan un repo specifique
python unified-design/scripts/compliance_scanner.py --repo RADX --report-json report.json

# Integration ARGUS
argus scan --repo RADX --check compliance
```

## Livrables

| Fichier | Description |
|:---|:---|
| `designs/compliance-scanner/design.yaml` | Design MDU |
| `designs/compliance-scanner/compliance-scanner.md` | Ce document |
| `atoms/compliance-scanner.yaml` | Atom MDU |
| `scripts/compliance_scanner.py` | Implementation (a creer) |

## References

- PRD MOC : `PRD-RADX-MDU-CONFORMITY-2026-08-28.md` (Section 4.4)
- ARGUS : `L1-INFRA/ARGUS/README.md`
- MDU L0 : `unified-design/META-DESIGN.md`
- REPO-STANDARDS : `L4-TOOLS/REPO-STANDARDS/META-DESIGN.md'
