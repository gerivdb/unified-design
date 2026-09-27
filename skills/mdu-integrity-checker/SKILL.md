# MDU Integrity Checker

Skill d'intégrité MDU (Meta-Design Universe) pour unified-design.
Vérifie la métacoherence des designs, détecte les gaps d'implémentation,
et enforce le contrat THINK/DO/CHECK.

## Outils

| Outil | Chemin | Usage |
|-------|--------|-------|
| `design_impl_verifier.py` | `scripts/design_impl_verifier.py` | Vérifie l'implémentation d'un design |
| `metacoherence_gate.py` | `scripts/metacoherence_gate.py` | Audit métacoherence THINK/DO/CHECK |
| `gap_combleur.py` | `scripts/gap_combleur.py` | Détecte et reporte les gaps |
| `pre-commit-design-verifier.py` | `.kilocode/hooks/pre-commit-design-verifier.py` | Hook pre-commit |

## Usage

### Vérifier un design individuel

```bash
python scripts/design_impl_verifier.py designs/TRIX/design.yaml
python scripts/design_impl_verifier.py --json designs/TRIX/design.yaml
```

### Audit métacoherence complet

```bash
# Vérifier tous les designs
python scripts/metacoherence_gate.py --check designs/

# Mode strict (échoue si violations)
python scripts/metacoherence_gate.py --check designs/ --strict

# Période d'audit personnalisée
python scripts/metacoherence_gate.py --check designs/ --audit-period 7d
```

### Détecter les gaps

```bash
# Dry-run
python scripts/gap_combleur.py --check designs/ --dry-run

# Générer rapport JSON
python scripts/gap_combleur.py --check designs/ --report gaps-report.json
```

### Hook pre-commit

```bash
# Vérifier avant commit
python .kilocode/hooks/pre-commit-design-verifier.py --threshold 80
```

## Critères d'acceptation

- [ ] `design_impl_verifier.py` passe sur tous les designs `active` avec contrat
- [ ] `metacoherence_gate.py` retourne 0 violations en mode strict
- [ ] `gap_combleur.py --dry-run` détecte tous les gaps manquants
- [ ] Hook pre-commit bloque les commits non conformes

## Références

- **PRD-MOC** : `MOC/PRD-MOC-UNIFIED-DESIGN-METACOHERENCE-AUTOMATION-20260927.md`
- **Design** : `designs/ecosystem-meta-coherence/design.yaml`
- **Gouvernance** : `DESIGNS_GOVERNANCE.md`
