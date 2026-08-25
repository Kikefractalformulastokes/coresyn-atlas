# M11 External Replication Protocol — Information–Physics Frontier

Status: FROZEN / pre-result protocol
Date: 2026-08-25

## Purpose
Test whether the previously observed separation between integral/global CFD fidelity and structural/constraint fidelity survives execution in genuine third-party solvers.

This protocol is frozen before external results are inspected. Criteria must not be relaxed after observing outcomes.

## Current evidence boundary
- Internal pseudo-spectral 3D Navier–Stokes experiment: observation present.
- Independent internal central-4 + SSP-RK3 compressible/isothermal TGV implementation: observation replicated across a second discretization.
- These are cross-discretization observations, NOT external OpenSBLI or Xcompact3D reproductions.

## External solver A — Xcompact3D
Use the official Taylor–Green vortex benchmark configuration as the external incompressible/high-order reference. Preserve the upstream benchmark input except changes strictly necessary for execution resources/decomposition. Record every deviation.

Primary role: test whether structural degradation can separate from integral metrics in a solver whose incompressibility treatment strongly constrains divergence.

## External solver B — OpenSBLI
Use the official TGsym Taylor–Green configuration from the OpenSBLI repository as the external compressible reference. Preserve upstream equations, numerical family and diagnostics wherever possible. Record every deviation.

Primary role: test the effect in a third-party compressible code-generation/OPS workflow.

## Frozen observables
For each solver/configuration and precision perturbation, collect where available:
1. kinetic energy E(t)
2. enstrophy Omega(t)
3. relative state/velocity L2 error versus reference
4. energy spectrum E(k,t)
5. vorticity/coherent-structure similarity or correlation
6. RMS divergence ||div u|| where meaningful
7. solver-native residual/stability diagnostics

## Frozen tolerances
PASS bands are evaluated at 1%, 2%, and 5% relative error for applicable observables.

## Registered prediction
The registered qualitative prediction is:

    integral/global observables survive representational reduction
    before fine-scale field/spectral structure.

No requirement is imposed that the critical bit/precision threshold be identical across solvers.

## Primary falsification test
The strong cross-solver claim FAILS if external solvers show that global and structural diagnostics lose fidelity together, with no reproducible separation under the frozen perturbation protocol.

The claim is DEGRADED if separation occurs only in one numerical family or only after solver-specific tuning.

The claim is SUPPORTED if the absolute threshold changes by solver but the ordering global-before-structural persists without post-hoc threshold changes.

## Constraint-specific test
Xcompact3D is used to test whether preserving the incompressibility constraint is sufficient to preserve structural fidelity.

If divergence remains near its solver reference while field/spectral diagnostics degrade earlier than integral metrics, this supports:

    constraint preservation != structural fidelity.

## Precision perturbation rule
The reference run uses the solver's normal high-precision configuration. Reduced/mixed/quantized variants must be defined before inspecting their final physics metrics. All implementation differences must be logged. A failed or unstable reduced-precision run is retained as a result, not silently replaced.

## No-go rules
- Do not describe an independently written look-alike solver as an OpenSBLI/Xcompact3D reproduction.
- Do not tune thresholds after seeing results.
- Do not remove failed precision policies from the evidence ledger.
- Do not claim NS-MDS causality from these tests alone.
- Do not claim universal bit thresholds.

## Manuscript decision gate
External PASS -> integrate cross-solver matrix into manuscript v1.0 and proceed to reproducibility release/submission preparation.
External mixed result -> narrow claim and publish solver dependence explicitly.
External FAIL -> report falsification/limitation; do not retain the strong cross-solver claim.

## Target manuscript object
Information–Physics Frontier:

    B_min = f(O, C, k, t, epsilon, S)

where O is the protected observable, C a physical/numerical constraint, k scale, t time, epsilon tolerance, and S solver/discretization.

CoreSyn — Proof before trust.
