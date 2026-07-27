# coresyn-atlas

**CoreSyn Atlas — Research Universe.** Mapa científico vivo de CoreSyn: un árbol tecnológico de dominios (nodos) conectados por dependencias (aristas), coloreados por madurez de evidencia (🟢 Validated · 🟡 Active · 🟠 Recovery · 🔵 Future).

## Qué es (y qué no es)
- **Es**: un artefacto HTML autocontenido (HTML+CSS+JS vanilla, Canvas 2D, sin build, sin backend). `index.html` es el Atlas entero.
- **No es (todavía)**: un servicio con backend, ni datos en base de datos. Los datos viven en `index.html` (arrays `NODES` y `REGISTRY`) y se exportan en `data/`.

## Estado congelado (v1 · 2026-07-24)
- 26 nodos · 28 aristas · 🟢 2 (CCFA001·Cosmology 2M++, p-Laplacian SGS CFD) · 🟡 10 · 🟠 1 · 🔵 13.
- Observatory verificado: Experimental 2 · Benchmarks 2 · White Papers 1 · Technical Reports 4 · Pilots 0 · Library 9.
- `index.html` SHA-256: `817a8d1719dc28d59ac9476d5863270c20b649678b4f1bcd87118f7af81830c2`

## Estructura
- `index.html` — el Atlas (fuente única de la lógica y, hoy, de los datos).
- `data/atlas-state.json` — export legible de nodos + aristas (para versionar el estado y para consumo externo / Atlas OS).
- `data/evidence-registry.json` — registro de evidencia (los contadores del Observatory se derivan de aquí).
- `ATLAS_TECH_SPEC.md` — ficha técnica real + plan de migración.
- `LIVING_UNIVERSE.md` — definición institucional del CoreSyn Living Universe y sus reglas de honestidad.

## Correr en local
```bash
python3 -m http.server 8000
# abrir http://localhost:8000
```

## Desplegar (GitHub Pages)
Ver `DEPLOY.md`. Resumen: push a `main` → Settings → Pages → Source: `main` / root → URL pública.

## Regla de oro
Ningún dominio pasa a 🟢 sin artefacto reproducible verificado. Cambios de estado = commits (el diff de `data/atlas-state.json` es el historial legible).
