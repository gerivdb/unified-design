# Unified Design (MDU)

> **Le Gentil** — L'atlas global des invariants architecturaux de l'écosystème gerivdb

## Vision

Le **Méta-Design (MDU)** est la **constitution architecturale** de l'écosystème gerivdb. Il définit les invariants topo-logiques qui gouvernent l'interaction entre les couches, les patterns, et les agents.

## Les Quatre Piliers

| Pilier | Abbr | Rôle | Couleur |
|--------|------|------|---------|
| Sonar-Driven Design | SDD | Observabilité | #4CAF50 |
| Triadic Compound Eye | TCE | Orchestration Agents | #2196F3 |
| MorphoHDL Anamorphic Growth | MAG | Optimisation Matérielle | #9C27B0 |
| Connard Design | CD | Contrôle Qualité | #F44336 |

## Structure

```
┌──────────────────────────────────────────────────────────────┐
│                    META-DESIGN ATLAS                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌────────────┐  │
│  │   SONAR-DRIVEN  │  │ TRIADIC COMPOUND│  │ MORPHOHDL  │  │
│  │      DESIGN     │  │       EYE       │  │   GROWTH   │  │
│  │  (Observabilité)│  │   (Orchestration│  │(Optimisation│  │
│  └─────────────────┘  │      Agents)    │  │   Matérielle)│  │
│                        └─────────────────┘  └────────────┘  │
│                                   │                          │
│                                   ▼                          │
│                    ┌─────────────────────────┐               │
│                    │      CONNARD DESIGN     │               │
│                    │     (Contrôle Qualité)  │               │
│                    └─────────────────────────┘               │
└──────────────────────────────────────────────────────────────┘
```

## Validation

```bash
gerivdb meta validate
gerivdb connard validate
```

## Fichiers

- `META-DESIGN.md` — Atlas des invariants architecturaux
- `meta-design.yaml` — Schéma de validation YAML
- `ADR-013.md` — Protocole de validation

## Références

- ADR-013 : Meta-Design Validation Protocol
- ADR-2026-06-28-001 : Logical Architecture N1-N4
- ADR-CONNARD-001 : Connard Design Protocol

## License

MIT