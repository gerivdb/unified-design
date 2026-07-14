---
type: ADR
status: proposed
date: "2026-07-15"
intent_hash: 0xADR_013_META_DESIGN_VALIDATION_PROTOCOL
---

# ADR-013 — Meta-Design Validation Protocol

## Contexte

Le méta-design (MDU) de l'écosystème gerivdb était historiquement logé dans `REPO-STANDARDS/META-DESIGN.md`, ce qui créait une anomalie : ranger la constitution architecturale dans un repo de standards de formatage.

Cette localisation:
1. **Confusion thermodynamique** : REPO-STANDARDS mélange standards de formatage et méta-architecture
2. **Difficulté de découverte** : Les devs n'attendent pas le MDU dans un repo de "standards"
3. **Impact sur l'apprentissage** : Les agents comme loopany ont du mal à localiser le méta-modèle canonique

## Décision

Créer un repo dédié `gerivdb/unified-design` (L0-CANON) pour héberger le MDU, avec:
- `META-DESIGN.md` — L'atlas des invariants architecturaux
- `meta-design.yaml` — Schéma de validation YAML
- `ADR-013` — Protocole de validation

## Conséquences

### Positives
- **Adresse canonique** : `D:\DO\WEB\TOOLS\L0-CANON\unified-design`
- **Découverte facilitée** : Nom intuitif `unified-design`
- **Séparation cohérente** : MDU distinct des standards de formatage
- **API claire** : `gerivdb meta validate` pointe vers le nouveau repo

### Négatives
- **Migration requise** : Mise à jour des références dans GOVERNANCE-HUB et REPO-STANDARDS
- **Double maintien temporaire** : Références obsolètes à nettoyer

## Architecture

```
┌─────────────────────┐
│ unified-design (L0) │
│  ├── META-DESIGN.md │  ← MDU - Atlas des invariants
│  ├── meta-design.yaml│  ← Schéma de validation
│  └── ADR-013.md      │  ← Protocole de validation
└─────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│ REPO-STANDARDS                  │
│  ├── RSS, linters...            │
│  └── référence MDU → unified-design │
└─────────────────────────────────┘
```

## Validation

Le MDU est validé par:
1. **Schema** : `meta-design.yaml`
2. **ADR** : ADR-013
3. **CLI** : `gerivdb meta validate`

## Références

- ADR-2026-06-28-001-LOGICAL-ARCHITECTURE-N1-N4
- ADR-CONNARD-001-CONNARD-DESIGN-PROTOCOL
- SECONDARY_SOTS.md — Référence actuelle

## Changements

| Date | Action |
|------|--------|
| 2026-07-15 | Création du repo unified-design |
| 2026-07-15 | Migration du MDU vers L0-CANON |
| 2026-07-15 | Mise à jour des références GOVERNANCE-HUB |
| 2026-07-15 | Mise à jour SECONDARY_SOTS.md |