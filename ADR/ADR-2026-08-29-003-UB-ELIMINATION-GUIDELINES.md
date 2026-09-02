---
type: ADR
status: proposed
date: "2026-08-29"
intent_hash: 0xADR_UB_ELIMINATION_GUIDELINES_20260829
---

# ADR-2026-08-29-003: Undefined Behavior Elimination Guidelines

## Status
Proposed

## Context
The LLUX silent fail was caused by Undefined Behavior in `matvec_simd`:
```zig
const w_vec = @Vector(4, f32){ w0, w1, w2, w3 };  // May be unaligned!
const prod = w_vec * x_vec;  // UB if unaligned on some targets
```

Without debug traces, the compiler optimized the UB into a silent hang. With traces, the side effects prevented the optimization.

## Decision
Adopt **UB Elimination Guidelines** as mandatory practice:

### 1. No Implicit Vectorization
- **Ban**: `@Vector(N, T)` on potentially unaligned pointers
- **Require**: Explicit element-wise loads or `_mm_loadu_ps` (unaligned load)
- **Rationale**: `@Vector` on unaligned data = UB → silent hang

### 2. Explicit Alignment Checks
```zig
const align_ok = (@intFromPtr(ptr) % 16 == 0);
if (!align_ok) return fallback_scalar(ptr);
```

### 3. Safe Fallback Pattern
```zig
fn matvec_simd(...) void {
    if (cols % 4 != 0) return matvec_scalar(...);  // Explicit fallback
    // ... vectorized loop with explicit scalar loads
    while (j < cols) : (j += 1) {  // Tail handling
        acc += W[i * cols + j] * x[j];
    }
}
```

### 4. Trace Gates
```zig
std.debug.print("[kernel] enter\n", .{});  // Prevents UB optimization
// ... kernel code ...
std.debug.print("[kernel] done\n", .{});   // Forces execution
```

### 5. Compiler Flags
- `-fno-strict-aliasing` (prevent UB from aliasing)
- `-fno-delete-null-pointer-checks` (preserve safety checks)

### 5. Mandatory Trace Gates
Every kernel entry/exit must have `std.debug.print`:
```zig
pub fn kernel_entry(...) !void {
    std.debug.print("[kernel] enter\n", .{});
    // ... implementation ...
    std.debug.print("[kernel] exit\n", .{});  // Forces execution
}
```

## Enforcement
- **Pre-commit**: `kg-l-type-guard` checks for `@Vector` without alignment guard
- **CI**: `zig_validator --strict` fails on UB patterns
- **Runtime**: `ctulu-zig-debug-adapter` can watch `@Vector` operations live

## Forbidden Patterns
| Pattern | Reason | Alternative |
|---------|--------|-------------|
| `@Vector(N, T)` on pointer | UB if unaligned | Explicit scalar loads + unroll |
| `@ptrCast` to vector | UB if unaligned | Element-wise loads |
| `@alignCast` (2-arg) | Zig 0.15 removed | Use `std.mem.alignForward` |
| `catch \|_| {}` | Zig 0.15 forbids discard | Use `catch {}` |

## Verification
- `zig_validator --strict` checks for forbidden patterns
- `ctulu-zig-debug-adapter` can watch `@Vector` operations live
- `kg-l-type-guard` ensures kernel domains match data

## References
- Zig 0.15 Release Notes: `@ptrCast`, `@alignCast`, `@Vector` changes
- LLUX Incident: `0xCAUSAL_RESOLUTION_LLUX_Q40_GEMV_20260829`

## IntentHash
**0xADR_UB_ELIMINATION_GUIDELINES_20260829**