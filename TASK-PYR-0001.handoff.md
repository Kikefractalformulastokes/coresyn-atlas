# HANDOFF — TASK-PYR-0001 — 2026-07-27
**Autor:** Vera Verita / Claude (Cowork) · **Para revisión de:** HumanizAI / ChatGPT (assurance) · **Rama:** `cmos-v0.1`

## Alcance cubierto
CMOS v0.1 (protocolo file-based) + modelo de datos (JSON Schemas) + M0 (fuentes) + M1 (dataset geométrico) + M2 (baselines B1/B2 + benchmark reproducible) + programa CEOS PYR-LAB-001 + subgrafo Pyramid del Atlas (separado de v1). Deploy NO incluido (BLOCKED por DECISION-0001).

## Archivos creados
PROTOCOL.md · schemas/{source,measurement,hypothesis,experiment}.schema.json + examples/ + validate.py + test_schemas.py · pyramid-lab/sources/sources.json · pyramid-lab/data/geometry.dataset.v1.json · pyramid-lab/baselines/{b1_reconstruction,b2_montecarlo,test_baselines}.py · pyramid-lab/benchmarks/run_benchmark.py + results/ · pyramid-lab/atlas-subgraph/pyramid-subgraph.json · projects/PYR-LAB-001.json · decisions/DECISION-0001-deploy-target.md · tasks/TASK-PYR-0001.md

## Comandos ejecutados (reproducibles)
```
python3 schemas/validate.py
python3 -m pytest schemas/test_schemas.py -q
python3 -m pytest pyramid-lab/baselines/test_baselines.py -q
python3 pyramid-lab/benchmarks/run_benchmark.py
```

## Resultados (números)
- Validación de esquemas: **22 registros, 0 inválidos**.
- Tests: **10/10 verdes** (5 schema + 5 baselines).
- B1 (determinista, dataset v1): mean_side = 230.364 m · rmse_vs_nominal = 0.0728 m · max_residual = 0.11075 m · **closure_error = 0.20386 m** · hard-constraint violations = 0.
- B2 (Monte Carlo, seed 42, n=10000): closure_error mean = 0.21662 m, stddev = 0.06878, p05/p50/p95 = 0.10477 / 0.21594 / 0.3317 · mean_side = 230.36368 ± 0.02501 m.
- Reproducibilidad: re-ejecutar el benchmark produce **hashes de salida idénticos**.

## Hashes / manifiesto
- geometry.dataset.v1.json → `45c250820591f0839c7ff44f0c1e3a8f602b18e87d76eb2dccb12d7287f661de`
- b1_result.json → `329fec25a36e420ab077d6d4b274cd077fa5a383395a475b44bebd7bff18f2bf`
- b2_result.json → `6b51bf161de5d036fc30c3aa9ea5ae02d15ba000f9713c040c64b712ce7470cb`
- Atlas v1 index.html (intacto) → `817a8d1719dc28d59ac9476d5863270c20b649678b4f1bcd87118f7af81830c2`

## Bloqueos
- M8 (public launch) BLOCKED: sin acceso al repo/Cloudflare Pages de coresyn.io (DECISION-0001(a)).
- Figuras Cole 1925 por-lado: PENDING_VERIFICATION (transcritas de secundaria; confirmar contra primaria).

## Estado propuesto: REVIEW
## Siguiente acción
Que ChatGPT revise este handoff (arquitectura + reproducibilidad), Enrique apruebe, y merge a `cmos-v0.1`. Después: verificar cifras Cole (sube M1), B3 rule-based sequencing, y render del subgrafo en rama.

## Firma assurance (5 reglas)
- [x] Nada VALIDATED sin artefacto+hash — cumplido (solo REVIEW; nada marcado validado).
- [x] Sin evidencia → HYPOTHESIS — todas las hipótesis en HYPOTHESIS.
- [x] Reproducibilidad != validación — declarado en benchmark y milestones.
- [x] Atlas v1 inmutable — no tocado; hash confirmado.
- [x] No inventar infra/resultados — deploy marcado BLOCKED, cifras dudosas marcadas PENDING_VERIFICATION.
