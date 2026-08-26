# Location-dependent one-bit precision sensitivity in an Xcompact3D Taylor–Green vortex workflow

**CoreSyn Model Assurance Lab — Technical manuscript v2**  
**Date:** 26 August 2026

## Abstract

Reduced-precision computing can improve throughput and energy efficiency, but numerical acceptability can depend not only on nominal bit width but also on where quantization enters an iterative solver. We report a controlled case study in the Xcompact3D Taylor–Green vortex (TGV) test using frozen upstream revision `abb010e615cff520f949a210278945346995966c` and an FP32 build. Xcompact3D writes five TGV observables in the exact order **time, spatially averaged kinetic energy, spatially averaged energy dissipation from first derivatives, spatially averaged energy dissipation from second derivatives, and spatially averaged enstrophy**. A deterministic quantizer clears low IEEE-754 binary32 fraction bits of the evolving `var1` state. A mantissa sweep identified an abrupt contrast between native q23 and q22: q23 remained within the reference regime whereas q22 preserved time but produced a selective collapse in all four physical observables. A location control then showed that quantizing only the recorded output remained within a 0.1% gate in all five fields, with maximum relative errors of approximately 0.0000155%, 0.0003927%, 0.0000997%, 0.0000997%, and 0.0001299%, respectively. In contrast, applying the same one-bit truncation at integrator entry or immediately after explicit `var1` updates reproduced the selective collapse, with approximately 100% maximum relative error in kinetic energy, both dissipation measures, and enstrophy while time remained preserved. Thus, for this frozen TGV workflow, the effect is location-dependent and cannot be explained by output rounding alone. The result is a numerical sensitivity observation, not evidence of a universal physical precision threshold. Independent-case replication remains required.

## 1. Introduction

Mixed- and reduced-precision strategies are increasingly attractive in computational fluid dynamics because memory bandwidth, accelerator throughput, and energy use can depend strongly on numerical representation. A central model-assurance question is therefore not merely how many bits a computation uses, but where reduced precision can be introduced without materially changing solver outputs.

This study tests that question in a deliberately narrow setting. Rather than claiming that a particular mantissa width is universally sufficient or insufficient for CFD, we perturb a frozen Xcompact3D TGV workflow and ask whether removing a single binary32 fraction bit has the same consequence when applied (i) only after the computation, (ii) to the state entering the time-integration routine, or (iii) after explicit state updates inside that routine.

The falsifiable hypothesis is that if the observed q23-to-q22 contrast is merely an output-representation artifact, output-only q22 truncation should reproduce it. Conversely, if feedback of the perturbation through the iterative dynamics is necessary, output-only truncation should remain close to baseline while in-solver truncation changes the measured physical observables.

## 2. Methods

### 2.1 Frozen solver and case

All reported TGV experiments use Xcompact3D upstream commit:

`abb010e615cff520f949a210278945346995966c`

The solver is configured as an FP32 build (`DOUBLE_PRECISION=OFF`). The upstream Taylor–Green vortex test executes Xcompact3D with `reference_input.i3d` and compares the generated `time_evol.dat` against the frozen `reference_time_evol.dat`.

### 2.2 Exact semantics of the TGV output

The frozen upstream `Case-TGV.f90` defines the statistics and writes `time_evol.dat` in this exact order:

1. **time**: `(itime-1)*dt`;
2. **kinetic energy**: `eek`, the spatial mean of `0.5*(u^2+v^2+w^2)`;
3. **energy dissipation (first-derivative form)**: `eps`, a spatially averaged viscous/LES dissipation measure constructed from velocity gradients;
4. **energy dissipation (second-derivative form)**: `eps2`, a spatial average of `-nu * u · Laplacian(u)` evaluated component-wise;
5. **enstrophy**: `enst`, the spatial mean of one half the squared vorticity magnitude.

Therefore the earlier shorthand “columns 1–5” maps to **time, kinetic energy, dissipation-1, dissipation-2, enstrophy**. This mapping is taken directly from the frozen upstream implementation rather than inferred from numerical values.

### 2.3 Deterministic mantissa intervention

The intervention operates on IEEE-754 binary32 values through Fortran `transfer` and `ibclr`. For q22, bit 0 of the 23-bit fraction field is cleared. Thus q23 denotes the unmodified/native fraction-bit condition and q22 denotes deterministic removal of the least-significant fraction bit. This intervention is a controlled software truncation and must not be described as FP16, BF16, stochastic rounding, or hardware low-precision arithmetic.

### 2.4 X7 frontier experiment

A q23/q22/q21/q20 sweep was executed with the quantization intervention applied to `var1` in the time-integrator workflow. The output time evolution was compared field-wise against the frozen reference using maximum relative error, RMS relative error, maximum absolute error, and fixed percentage gates. A Fortran-safe parser was used because sufficiently small values can be emitted in exponent notation without an explicit `E` character.

### 2.5 X8 location control

Four conditions were defined:

1. **native_q23:** no fraction-bit clearing;
2. **outputonly_q22:** execute without in-solver q22 intervention, then clear fraction bit 0 in the recorded output before comparison;
3. **entry_q22:** clear fraction bit 0 of `var1` at entry to the relevant integration routine;
4. **postupdate_q22:** clear fraction bit 0 immediately after matched explicit `var1` state-update statements.

The output-only condition is the negative control for a trivial representation explanation. Entry and post-update conditions test whether feeding the perturbation through solver evolution is associated with the observed collapse.

### 2.6 Error metric

For observable j and sample i, relative error is computed as

`|x_ij - r_ij| / max(|r_ij|, 1e-30)`,

where `x` is the measured output and `r` the frozen reference. Reported maximum relative percentages are 100 times the maximum of this quantity over samples.

## 3. Results

### 3.1 One-bit frontier

The refined sweep localized the observed contrast to q23 versus q22. q22, q21, and q20 exhibited the same qualitative selective-collapse pattern: the time coordinate remained preserved while **kinetic energy, both energy-dissipation measures, and enstrophy** approached effectively zero relative to their nonzero reference values and therefore reached approximately 100% maximum relative error. q23 served as the native fraction-bit control and remained in the safe/reference regime.

This result alone does not establish a physical or universal threshold because the intervention is embedded at a particular solver location.

### 3.2 Output-only negative control

Applying q22 truncation only to the final recorded output did **not** reproduce the collapse:

| TGV field | Max relative error |
|---|---:|
| Time | 0.0000155% |
| Spatially averaged kinetic energy | 0.0003927% |
| Energy dissipation — first-derivative form | 0.0000997% |
| Energy dissipation — second-derivative form | 0.0000997% |
| Spatially averaged enstrophy | 0.0001299% |

All five fields remained below the 0.1% gate in this control.

### 3.3 In-solver location controls

Both tested in-solver q22 placements reproduced the selective collapse. With q22 applied at integrator entry, kinetic energy, both dissipation measures, and enstrophy reached approximately 100% maximum relative error while the time coordinate remained preserved. With q22 applied immediately after explicit `var1` updates, the same qualitative pattern was observed.

The controlled contrast is therefore:

`native q23: SAFE`

`output-only q22: SAFE`

`entry q22: physical-observable collapse`

`post-update q22: physical-observable collapse`

The important observation is not simply that one bit was removed, but that feeding the same deterministic truncation through the evolving state was associated with a radically different result from applying it only to recorded outputs.

## 4. Discussion

### 4.1 What the experiment supports

The X8 negative control rejects a simple explanation in which the measured q22 collapse is caused solely by representing the final output with one fewer fraction bit. In this TGV workflow, output-only q22 perturbation is orders of magnitude smaller than the in-solver effect and remains inside the strictest reported 0.1% gate.

The agreement between entry-state and post-update interventions further suggests that the observed sensitivity is associated with repeated feedback of deterministic truncation through solver evolution rather than one uniquely chosen injection line. Crucially, the affected outputs are now identified from the frozen upstream implementation: spatially averaged kinetic energy, two independently formulated dissipation diagnostics, and spatially averaged enstrophy.

The solver call sequence places `int_time(...)` before pressure/velocity correction and subsequent case postprocessing, so the in-solver intervention occurs upstream of the TGV diagnostic calculation. The output-only control, by contrast, changes only the recorded values after solver evolution. This structural separation strengthens the location-dependent interpretation.

### 4.2 What the experiment does not support

The evidence does **not** establish that 22 fraction bits are generally insufficient for Navier–Stokes simulation, that a universal 23-to-22 physical threshold exists, or that hardware reduced-precision formats would behave identically. It also does not yet establish generalization beyond this frozen TGV configuration.

The result should therefore be stated as a controlled numerical-sensitivity observation affecting named TGV diagnostics under a deterministic software intervention, not as a universal property of CFD precision.

### 4.3 Mechanistic interpretation

A deterministic least-significant-bit truncation introduces a small, directionally structured perturbation. When applied only once after simulation, its effect is bounded by the representation change itself. When repeatedly applied to evolving state, however, the perturbation is fed back into subsequent updates. Nonlinear dynamics, cancellation, dissipative mechanisms, and accumulation can then amplify or reorganize the perturbation. The present experiment demonstrates the empirical location dependence but does not isolate which of those mechanisms dominates.

The simultaneous collapse of kinetic energy, both dissipation diagnostics, and enstrophy is consistent with a broad degradation of the evolved velocity field rather than a formatting artifact in one diagnostic. That interpretation remains mechanistic rather than universal and requires direct state-level diagnostics for confirmation.

## 5. Reproducibility and evidence controls

The experiment was designed around the following assurance controls:

- frozen Xcompact3D upstream commit;
- explicit FP32 build configuration;
- deterministic and inspectable bit-clearing intervention;
- exact upstream mapping of TGV output semantics;
- patch and intervention manifests;
- raw `time_evol` outputs;
- frozen reference output;
- machine-generated metrics;
- SHA-256 evidence manifests;
- GitHub Actions logs and uploaded artifacts;
- negative output-only control;
- two in-solver intervention locations.

The X8 workflow run completed all four branches successfully, including build, TGV execution, measurement, evidence freezing, and artifact upload.

## 6. Limitations and preregistered next test

The principal limitation is external replication. An X9 experiment has been specified using the independent Xcompact3D `Cylinder-wake` test with native q23, entry q22, and post-update q22 conditions. At manuscript v2 freeze, repository-level GitHub Actions activation prevented that new/modified M11 workflow from launching; therefore **no Cylinder-wake scientific result is claimed here**.

X9 is a falsification test. Replication of the location-dependent contrast would support generalization to a second flow configuration. Failure to replicate would delimit the observation to TGV or to a narrower numerical regime. Either outcome is scientifically informative and must be reported.

Additional work should repeat runs where nondeterminism is possible, inspect direct state norms before the diagnostics are calculated, test alternative rounding operators, and perform the independent-case replication.

## 7. Conclusion

A controlled Xcompact3D TGV experiment exhibits a sharp, location-dependent response to deterministic removal of the least-significant FP32 fraction bit. Removing that bit only from recorded output produces sub-0.001% maximum relative errors in all measured fields, whereas feeding the same q22 truncation through the time-evolving `var1` state produces a collapse in **spatially averaged kinetic energy, two energy-dissipation diagnostics, and spatially averaged enstrophy**, while the time coordinate remains preserved. The result survives two in-solver placement controls and therefore cannot be attributed to output rounding alone.

The defensible claim is narrow: **for this frozen Xcompact3D TGV workflow, repeated one-bit state truncation produces a qualitatively different evolution of named physical diagnostics from equivalent output-only truncation.** Independent-case replication is the next required step before broader CFD claims.

## Data and code availability

The experimental workflows, patches, manifests, logs, metrics, raw outputs, and evidence hashes are maintained in the `Kikefractalformulastokes/coresyn-atlas` repository and associated GitHub Actions artifacts. The exact frozen upstream revision and intervention definition are recorded above to support reproduction.

## Claim boundary

**Supported:** controlled TGV numerical sensitivity; q23/q22 frontier under the implemented intervention; output-only negative control; entry/post-update location dependence; exact identification of the five TGV fields from frozen upstream source.

**Not yet supported:** universal precision threshold; hardware-format equivalence; cross-flow generalization; Cylinder-wake replication; a unique amplification mechanism.
