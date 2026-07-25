---
type: GUI
version: 1.0.0
status: active
intent_hash: 0xATOM_029_TRIX_ARCHITECTURE
---

# ATOM-029 : Architecture Ternaire TRIX

## Contexte matériel (ENV2)

- **CPU** : Xeon E5620 (Westmere, 4C/8T @ 2.4 GHz)
- **Contrainte** : pas de FP16 natif, RAM limitée à 24 Go DDR3
- **Solution** : logique ternaire b1.58 (poids ∈ {-1, 0, 1})

## Spécification

### Backend
- `ggml-trix` (C/Zig)
- Opérations : additions d'entiers uniquement (pas de multiplications flottantes)
- Cible : modèles 13B dans 2-3 Go de RAM

### Code source
- `src/simd/simd.zig` (déjà initié, à compléter)
- `src/trix/trix_inference.c` (backend principal)

### Opérations ternaires

```c
// Opération ternaire b1.58
int32_t ternary_add(int8_t a, int8_t b) {
    int16_t result = (int16_t)a + (int16_t)b;
    if (result > 1) return 1;
    if (result < -1) return -1;
    return (int8_t)result;
}
```

## Optimisations SSE4.2

Le Xeon E5620 supporte SSE4.2. Utiliser :
- `_mm_add_epi8` pour additions vectorielles
- `_mm_cmpgt_epi8` pour comparaisons
- `_mm_shuffle_epi8` pour permutations

## Benchmarks attendus

| Modèle | RAM requise | tok/s (CPU) |
|--------|-------------|-------------|
| 3B | ~1.5 Go | 15-20 |
| 7B | ~3 Go | 8-12 |
| 13B | ~5-6 Go | 3-5 |

## Références

- `docs/TRIX_BENCHMARK_REPORT.md` (dans ONTOLOGY)
- `atoms/trix-debug.zig` (débogage dispatch table)