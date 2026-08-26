# M11 Q22 binary audit protocol

Date: 2026-08-26

## Purpose

Before interpreting X7/X8 as solver sensitivity, independently validate the exact semantics of the q22 operator used in the experiment.

## Frozen checks

The standalone `audit/m11_q22_binary_semantics.f90` uses explicit `real32` and `int32` and applies the same operation as X8:

1. `raw = transfer(v, raw)`
2. `raw = ibclr(raw, 0)`
3. `y = transfer(raw, y)`

For each test value it records original and q22 decimal values, original and q22 hexadecimal words, XOR mask, absolute error, and relative error.

The executable MUST fail unless:

- the XOR mask contains no changed bit except bit 0;
- bit 0 is cleared in the result;
- relative perturbation is <= `2*epsilon(real32)` for every nonzero test value.

Test values include positive/negative normals, pi-like value, small magnitudes, a large finite value, and `tiny(real32)`.

## Interpretation gate

PASS means the standalone operator itself has the intended IEEE-754 binary32 semantics. It does not by itself prove that X8 state arrays were single precision at runtime or explain the collapse.

After PASS, instrument the solver around the first q22 application and record at minimum:

- `storage_size(var1)` and `kind(var1)`;
- min/max and L2-like norm immediately before q22;
- min/max and norm immediately after q22;
- maximum absolute and relative elementwise perturbation;
- first timestep/substep where physical-state magnitude departs materially from native q23.

If standalone binary semantics FAIL, X7/X8 physical interpretation is suspended and the manuscript must be corrected before submission.

If standalone semantics PASS but the first in-solver q22 call causes an O(1) state change, investigate runtime type/kind, transfer semantics, array assignment, compiler optimization, and instrumentation before making a physical-sensitivity claim.
