# CORE-AERO-001 — Independent Reproduction Report

**This session independently reproduced the packet's claimed result. Full commands and raw output below — nothing summarized away.**

## Chain of custody
1. Repo `coresyn-core-aero-001-verifier` added to session, cloned (`git rev-parse HEAD` = `88d06e74bae6bbebacd63d1fcc75f90fc79457d2`).
2. `CORE-AERO-001_VERIFIER_PACKET.zip` copied to an isolated scratch directory. Original in the repo checkout untouched throughout.
3. `sha256sum` on the zip: `461b49901520d0c4faf06b1e1669408329e19436251d489a89c5cc401cb541d0`.
4. `unzip -l` and `unzip -t`: 28 files listed, integrity test clean, no errors.
5. Extracted to an isolated directory.

## Environment match
Packet's `ARCHITECTURE_PIN.json` requires CPython 3.11.x, pure-Python, no BLAS. This sandbox: `Python 3.11.15` — matches.

## Run 1 (first execution, unmodified)
```
$ bash verify.sh
== CORE-AERO-001 verifier ==
[1/4] checking input integrity against HASHES.txt
[2/4] running reproduce_naca0012.py
Cl_alpha_per_rad = 6.2831853072 | within_tolerance = True | result.json sha256 = 0da1be96b7f9d5ab9bdbf13a31c83d86d945930b9c4feab47fc6d1faaff35ef2
[3/4] comparing produced OUTPUTS to EXPECTED_OUTPUTS
  OK result.json  0da1be96b7f9d5ab9bdbf13a31c83d86d945930b9c4feab47fc6d1faaff35ef2
  OK naca0012_coordinates.csv  4ea55912266676b00e31373c8412070454c0735d06743e8995bcf2e8e03b78d3
[4/4] asserting within_tolerance == true
  Cl_alpha_per_rad = 6.2831853072 | abs_diff_vs_recorded = 1.6928e-06 | tolerance = 0.0001
VERIFY OK: independent clean-room reproduction matches EXPECTED_OUTPUTS and is within tolerance.
NOTE: this is SELF-DECLARED (A0). External authority pending. Not externally validated yet.
$ echo $?
0
```

## Run 2 (repeatability check, same extraction, no changes)
Identical output, identical `result.json` hash (`0da1be96...`), exit 0. **Deterministic across runs.**

## Integrity/quality checks run beyond what verify.sh does itself
- `grep -io "nan\|inf"` on both output files: one hit, in the word "prove**nan**ce" — confirmed false positive by inspecting the actual `result.json` content. No real NaN/Inf.
- `python3 -W error reproduce_naca0012.py`: same output, same exit code, no warnings promoted to errors.
- Read `reproduce_naca0012.py` directly to classify the model by code, not by name (see `CORE_AERO_001_CANONICAL_EVIDENCE_RECORD.json` for the classification and the reasoning).

## Result
`Cl_alpha_per_rad = 6.2831853072`, vs. the recorded reference `6.283187` (abs diff `1.69e-06`), within the declared tolerance (`1e-4`), vs. the mathematical `2π = 6.283185307179586`.

## What this reproduction does and does not establish
**Does establish:** the packet is real, runs cleanly, is deterministic, and its self-declared A0 status is honestly represented — I could not find any gap between what the packet claims about itself and what it actually does.

**Does not establish:** external validation (this is still one session, not an independent third party in the sense the packet's own `manifest.json` defines — see its `coordinate_target: A2` requirement), CFD-equivalence (confirmed not CFD), NASA validation (confirmed not claimed), or industrial readiness (confirmed not claimed).
