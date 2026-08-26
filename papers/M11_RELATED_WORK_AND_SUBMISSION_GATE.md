# M11 — Related work and submission gate

Date: 26 August 2026

## Positioning

The manuscript should be positioned as a **controlled model-assurance study of location-dependent deterministic precision truncation in an iterative CFD workflow**, not as a claim that FP32 universally has a 23→22-bit physical threshold.

The closest literature establishes three important contexts:

1. Xcompact3D is an established open-source high-order finite-difference framework for turbulent-flow simulation and HPC (Bartholomew et al., SoftwareX 2020, DOI 10.1016/j.softx.2020.100550).
2. Taylor–Green vortex is an established CFD verification/validation benchmark, including high-fidelity comparisons and public datasets.
3. Reduced/mixed precision in fluid and atmospheric simulation is known to depend on algorithmic placement and accumulated roundoff, motivating component- or state-aware precision strategies rather than indiscriminate global reduction.

A particularly relevant contemporaneous preprint is Chen, Münsch & Iakymchuk (2026), *Mixed-Precision SEM-Based CFD Simulations on GPUs: A Taylor-Green Vortex case* (arXiv:2608.24348). It independently argues that mixed precision in a TGV CFD pipeline should be treated as a simulation-level control problem and reports sensitivity of gradient-based quantities such as enstrophy to targeted low-precision overrides. Because it appeared during preparation of M11, it must be cited as contemporaneous related work, not represented as prior motivation for experiments that were already executed.

## Core references to incorporate

- Bartholomew, P. et al. (2020). Xcompact3D: An open-source framework for solving turbulence problems on a Cartesian mesh. SoftwareX 12, 100550. DOI: 10.1016/j.softx.2020.100550.
- Brachet, M. E. et al. (1991). Direct simulation of three-dimensional turbulence in the Taylor–Green vortex. Fluid Dynamics Research 8, 1–8. DOI: 10.1016/0169-5983(91)90026-F.
- The Taylor–Green vortex as a benchmark for high-fidelity combustion simulations using low-Mach solvers. Computers & Fluids (2021), 104935. DOI: 10.1016/j.compfluid.2021.104935.
- On floating point precision in computational fluid dynamics using OpenFOAM (2023/2024 publication record; verify final bibliographic metadata before submission).
- Maynard, C. M. & Walters, D. N. Precision of the ENDGame: Mixed-precision arithmetic in the iterative solver of the Unified Model. arXiv:1811.03852 (verify final publication record before submission).
- Fluid Simulations Accelerated With 16 Bits: Approaching 4x Speedup on A64FX by Squeezing ShallowWaters.jl Into Float16 (2022 publication record; verify full metadata before submission).
- Chen, Y., Münsch, M. & Iakymchuk, R. (2026). Mixed-Precision SEM-Based CFD Simulations on GPUs: A Taylor-Green Vortex case. arXiv:2608.24348. CONTEMPORANEOUS WORK.

## Novelty boundary

M11 does **not** claim novelty for reduced precision in CFD, TGV as a benchmark, or the general fact that rounding errors can accumulate.

The candidate contribution is narrower:

> Within one frozen Xcompact3D TGV workflow, deterministic clearing of the least-significant FP32 fraction bit is benign when applied only to recorded outputs but is associated with collapse of kinetic-energy, dissipation, and enstrophy diagnostics when repeatedly fed through the evolving state; the contrast survives two in-solver placement controls.

Novelty must remain conditional until a systematic literature search confirms that this exact one-bit/location-control experiment has not already been reported.

## Submission gate

### Already satisfied

- [x] Frozen upstream revision.
- [x] Explicit FP32 configuration.
- [x] Deterministic intervention definition.
- [x] q23/q22 frontier experiment.
- [x] Output-only negative control.
- [x] Two in-solver placement controls.
- [x] Raw output/evidence artifacts and hashes from X8.
- [x] Exact mapping of `time_evol.dat` to time, kinetic energy, dissipation-1, dissipation-2, enstrophy.
- [x] Claim boundary explicitly excludes universal threshold and hardware-format equivalence.
- [x] Manuscript V2.

### Required before journal submission

- [ ] Produce publication figures directly from frozen X7/X8 artifacts, not hand-entered values.
- [ ] Verify complete bibliographic metadata and DOIs for every reference.
- [ ] Perform systematic novelty search using terms around bit truncation, mantissa reduction, precision placement, TGV, Xcompact3D, iterative feedback, enstrophy and dissipation.
- [ ] Add exact hardware/compiler/OS/MPI versions from workflow evidence.
- [ ] Add exact TGV input parameters and numerical scheme configuration from the frozen test input.
- [ ] Confirm repeatability/determinism with replicate executions or state clearly why the run is deterministic.
- [ ] Audit the phrase “collapse”: define it numerically and show raw/reference trajectories in figures.
- [ ] Resolve or execute X9 independent-flow falsification if infrastructure permits. X9 is highly desirable for stronger generalization but must not be fabricated or silently omitted.
- [ ] Independent internal review of methods, metrics, code patch and claim language.

## Recommended manuscript status

**CURRENT: STRONG TECHNICAL MANUSCRIPT / NOT YET JOURNAL-SUBMISSION-READY.**

The strongest defensible paper today is a narrow TGV numerical-sensitivity case study. X9 would materially strengthen the paper, but the current X7+X8 evidence can still support a carefully bounded technical manuscript if all remaining reproducibility and presentation gates are closed.
