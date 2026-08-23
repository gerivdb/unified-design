# unified-design — MetaCluster Design Unified (MDU)

**Repo** : `gerivdb/unified-design`  
**Strate** : L0-CANON  
**Rôle** : Design unifié de l'écosystème gerivdb (N+1 à N+4)  
**Version** : 1.0.0  
**Statut** : ACTIVE  

---

## Mission

unified-design est le **repo de référence** pour tous les designs
architecturaux de l'écosystème gerivdb. Il centralise :

- `META-DESIGN.md` : design global N+4
- `designs/` : designs locaux par strate
- `atoms/` : catalogue atoms universel
- `schemas/` : schémas design.yaml
- `validation/` : validateur `gerivdb design validate`

## Structure

```
unified-design/
├── META-DESIGN.md              # MDU complet (N+4)
├── designs/                    # Designs par strate
│   ├── L0-CANON/
│   ├── L1-INFRA/
│   ├── L2-PLATFORM/
│   ├── L3-CITIZENS/
│   └── L4-TOOLS/
│       └── DESIGN-FLEX-001.md  # FLEX Harmony Topology Engine
├── atoms/                      # Catalogue atoms universel
├── schemas/                    # Schémas design.yaml
├── validation/                 # Validateur designs
└── README.md
```

## Références

- `REPO-STANDARDS/META-DESIGN.md` : source initiale MDU
- `META-DESIGN.md` (racine et docs/) : décision architecturelle MDU
- `INTENT-016` : magistral MDU
- `PRD-MOC-FLEX-ENV2-TOPOLOGY-HARMONY.md` : DESIGN-FLEX-001
