# coresyn-atlas

**CoreSyn Atlas — Research Universe.** Mapa científico vivo de CoreSyn: un árbol tecnológico de dominios (nodos) conectados por dependencias (aristas), coloreados por madurez de evidencia (🟢 Validated · 🟡 Active · 🟠 Recovery · 🔵 Future).

## Qué es (y qué no es)
- **Es**: un artefacto HTML autocontenido (HTML+CSS+JS vanilla, Canvas 2D, sin build, sin backend). `index.html` contiene la lógica y el estado renderizado.
- **No es (todavía)**: un servicio con backend ni una base de datos. Los exports legibles están versionados en la raíz del repositorio.

## Estado congelado (v1 · 2026-07-24)
- 26 nodos · 28 aristas · 🟢 2 · 🟡 10 incluyendo el nodo raíz CoreSyn (9 fronteras Active excluyendo la raíz) · 🟠 1 · 🔵 13.
- Observatory: Experimental 2 · Benchmarks 2 · White Papers 1 · Technical Reports 4 · Pilots 0 · Library 9.
- `index.html` SHA-256 declarado en el freeze v1: `817a8d1719dc28d59ac9476d5863270c20b649678b4f1bcd87118f7af81830c2`.

## Estructura
- `index.html` — interfaz autocontenida y estado renderizado del Atlas.
- `atlas-state.json` — export de 26 nodos y 28 aristas.
- `evidence-registry.json` — registro de 9 ítems de evidencia y contadores.
- `ATLAS_TECH_SPEC.md` — ficha técnica y plan de migración.
- `LIVING_UNIVERSE.md` — definición institucional y reglas de honestidad.
- `PROTOCOL.md` — protocolo de estados, evidencia, revisión y aceptación.

## Correr en local
```bash
python3 -m http.server 8000
# abrir http://localhost:8000
```

## Desplegar (GitHub Pages)
Ver `DEPLOY.md`. Resumen: push a `main` → Settings → Pages → Source: `main` / root.

## Regla de oro
Ningún dominio pasa a 🟢 por narrativa, dogfooding o revisión del propio ejecutor. Cambios de estado deben ser trazables a commits y evidencia inspeccionable. El diff de `atlas-state.json` es el historial legible del grafo.
