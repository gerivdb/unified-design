---
name: contract-traceability
description: Toute correction de reference de contrat est un acte de gouvernance trace. Ferme la classe "correction silencieuse" du pattern F1-F9.
version: 1.0.0
intent_hash: 0xDESIGN_CONTRACT_TRACEABILITY_20260823
type: design
layer: L0
repo: gerivdb/unified-design
---

# DESIGN -- CONTRACT TRACEABILITY

## Principe

Tout contrat (ADR, INTENT, PRD, RULES) declare une **source** (ou il est ecrit)
et une **cible** (ce qu'il designe). La correction d'une reference fantome n'est
pas un acte technique : c'est un **acte de gouvernance** qui doit etre trace.

Sans ce design, corriger 14 fantomes reproduit le pattern F1-F9 : la correction
elle-meme devient un changement sans adossement tracable.

## Les deux preuves obligatoires

| Preuve | Support | Role |
|--------|---------|------|
| **Commit git** | message + diff | Preuve humaine : le quoi et le pourquoi |
| **Journal machine** | `GOVERNANCE-HUB/RUNTIME/corrections_journal.jsonl` | Trace exploitable : le lien ref -> commit |

Le journal ne remplace pas le commit, il y pointe. Un row sans `commit_sha`
verifiable est invalide.

## Format du journal (compact, une ligne par correction)

```json
{"ts":"2026-08-23T05:40:00+02:00","repo":"unified-design","ref":"ADR-049-RPKix-PDD-mismatch","action":"corrected_typo","target":"ADR-049-RSPix-PDD-mismatch.md:45","hotl_level":"A2","commit_sha":"abc1234"}
```

Actions valides :

| Action | Signification |
|--------|---------------|
| `corrected_typo` | Coquille dans la reference (le contrat existe) |
| `retarget_alias` | Reference reecrite vers l'artefact reel sous son nom canonique |
| `retired_reference` | Reference supprimee avec note dans la source |
| `created_stub` | Contrat cree retroactivement pour adosser la reference |
| `scanner_whitelist` | Fausse positive ou exemple documentaire -> exclusion RIG justifiee |

Autorise : plusieurs rows par commit (batch). Interdit : un row sans commit_sha,
un fix sans row.

## Regles

1. Le RIG ne corrige jamais silencieusement. Il detecte ; l'humain-l'agent
   corrige en committant ; le row de journal accompagne le commit.
2. La suite de regression peut exiger, pour un fantome resolu, la presence
   de son row dans le journal.
3. Le journal est append-only. Une correction erronee se corrige par un
   nouveau row, pas par une suppression.
4. Le niveau HOTL au moment de la correction est enregistre (auditabilite).

## Relations

- Consomme par : RIG (`check-ref-integrity.ps1`), regression F1-F9
- Complete : PRD-MOC-GEN-009 (P1/P3), friction F7
- Etat runtime : `GOVERNANCE-HUB/RUNTIME/corrections_journal.jsonl`

## Voir aussi

- `designs/autonomy-integrity-matrix/AUTONOMY_INTEGRITY_MATRIX.md`
- `GOVERNANCE-HUB/scripts/check-ref-integrity.ps1`
