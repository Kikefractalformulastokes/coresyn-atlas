# CoreSyn Atlas — Ficha técnica real y plan de migración
**Respuesta técnica a Brandon / HAI-0000001 · creado 2026-07-24 · ACTUALIZADO 2026-07-27 · sin humo**

> **ACTUALIZACIÓN 2026-07-27 — YA DESPLEGADO.** Lo que el 24-jul decía "por montar" ya está montado y verificado en vivo. El Atlas tiene ahora **URL pública real, repositorio git público y hosting estático real**. Cambios respecto a la versión original marcados abajo en los puntos 1, 2, 3, 10 y 11. El resto (stack, fuente de datos, ausencia de dominio propio) sigue igual.
>
> - **URL EN VIVO:** https://kikefractalformulastokes.github.io/coresyn-atlas/ (verificada: renderiza el v1 congelado, 2 dominios validados, CCFA001 verde, 25 territorios, 0 errores JS).
> - **Repo:** https://github.com/Kikefractalformulastokes/coresyn-atlas (público).
> - **Hosting:** GitHub Pages · rama `main` / root.

Voy punto por punto con lo que **realmente** existe. No inventé nada: el 24-jul no había URL/repo/hosting, y lo dije así; el 27-jul ya los hay porque los desplegamos de verdad (commit visible), y lo actualizo aquí.

## 1. URL real del Atlas en funcionamiento
**~~No existe una URL pública.~~ [2026-07-27] SÍ existe:** https://kikefractalformulastokes.github.io/coresyn-atlas/ — sirve el `index.html` autocontenido tal cual (v1 congelado). Verificada abriéndola en navegador: universo renderiza, CCFA001 · Cosmology (2M++) en 🟢, KPIs 2 validados / 9 activos / 1 recovery / 13 futuros / 25 territorios. El *Cowork artifact* (id `coresyn-atlas-research-universe`) sigue existiendo dentro de la app de escritorio como la versión "editable"; la URL de arriba es la versión pública congelada.

## 2. Repositorio / workspace donde vive
**~~No hay repositorio git.~~ [2026-07-27] Repo git público:** https://github.com/Kikefractalformulastokes/coresyn-atlas — primer commit "Atlas v1 2026-07-24 — estado congelado (26 nodos / 28 aristas)", 7 archivos: `index.html`, `atlas-state.json`, `evidence-registry.json`, `ATLAS_TECH_SPEC.md`, `README.md`, `LIVING_UNIVERSE.md`, `DEPLOY.md`, más `.nojekyll`. El artifact de la app de escritorio sigue siendo la copia de trabajo con su propio historial de versiones.

## 3. Hosting actual
**~~almacén de artifacts de Claude Desktop~~ [2026-07-27] GitHub Pages** (rama `main` / root del repo de arriba). Hosting estático real, público, HTTPS, sin servidor/contenedor/función serverless — se sirve el HTML tal cual. El almacén de artifacts de Claude Desktop sigue existiendo en paralelo para la versión editable.

## 4. Fuente de datos de nodos y aristas
**Hardcoded dentro del propio HTML.** Dos arrays JavaScript:
- `NODES` (26 nodos): cada uno con `id, name, state, status, vision, goal, deps, apps, sectors, year`.
- `REGISTRY` (9 ítems de evidencia): `id, title, category, branch, date, status, summary, evidenceUrl, sourceType, limitations, visibility`.
Las **aristas (28)** son el campo `deps` de cada nodo (dependencias del árbol). No hay base de datos, ni API, ni feed externo. Los contadores del Observatory se **derivan** del `REGISTRY` en cliente (no se teclean).

## 5. ¿Conexiones manuales, automáticas o híbridas?
**Manuales.** Cada estado (🟢/🟡/🟠/🔵) y cada dependencia se editó a mano (por Claude, con confirmación de Enrique) en esta sesión. Lo único "automático" es cálculo en cliente: el layout radial, la lógica de "locked", y el derivar los contadores del registro. No hay ingestión automática de datos.

## 6. Historial de aparición de nodos y conexiones
**No hay control de versiones formal.** El historial real es: (a) la secuencia de ediciones de esta sesión (reconstruible como changelog a partir del chat), y (b) el historial de versiones del artifact en la app de escritorio. Hitos de hoy: se pasó de "casi todo Future" a 2 validados (CCFA001, p-Laplacian), se añadió el estado 🟠 Recovery, el Observatory registry-driven, y correcciones de honestidad (revisión externa QMUL/USAL sin dictamen; se retiró lo no respaldado).

## 7. Captura / exportación completa
**Sí, y es real: el archivo `index.html` completo (≈50,7 KB, autocontenido).** Ese archivo ES el Atlas entero — HTML+CSS+JS en un solo fichero, abrible en cualquier navegador sin dependencias. Además adjunto:
- `atlas-state.json` — export limpio de los 26 nodos + 28 aristas.
- `evidence-registry.json` — los 9 ítems de evidencia + contadores.
El propio Atlas tiene un "Evidence Editor" que exporta/importa el estado como JSON.

## 8. Stack técnico y comandos de despliegue
- **Stack:** HTML5 + CSS (vanilla) + JavaScript vanilla. Canvas 2D para el universo y las constelaciones. **Sin frameworks, sin backend, sin paso de build, sin dependencias externas.**
- **Comandos de despliegue actuales:** ninguno — no está desplegado. Al ser estático, desplegarlo es servir el HTML tal cual. Ejemplo local: `python3 -m http.server` en la carpeta del archivo.

## 9. Configuración de dominio
**Ninguna.** No hay dominio ni DNS asociados.

## 10. Sistema de backups
**~~No hay sistema formal de backups.~~ [2026-07-27] Sí lo hay:** el historial completo de git en GitHub (cada commit es un backup versionado e inmutable) + los JSON exportables + las copias del artifact en la app. Pendiente opcional: crear un *release* etiquetado (`v1`) por hito para sellar el estado congelado.

## 11. Plan de migración SIN pérdida (preservar el que existe, NO reconstruir) — **ESTADO DE EJECUCIÓN**
Objetivo: convertir el Atlas actual en referencia canónica versionada, **conservando byte a byte** el estado de hoy.
1. ✅ **[HECHO] Congelar** el `index.html` actual como `v1` (hash SHA-256 `817a8d1719dc28d59ac9476d5863270c20b649678b4f1bcd87118f7af81830c2`).
2. ✅ **[HECHO] Repo git** (GitHub) `coresyn-atlas`: `index.html` tal cual + `atlas-state.json` + `evidence-registry.json` + docs. Primer commit = estado 2026-07-24 → https://github.com/Kikefractalformulastokes/coresyn-atlas
3. ✅ **[HECHO] Hosting estático**: GitHub Pages apuntando al repo → **URL real verificada:** https://kikefractalformulastokes.github.io/coresyn-atlas/
4. ⏳ **[PENDIENTE OPCIONAL] Dominio**: CNAME a `atlas.coresyn.io` (requiere config DNS de Enrique).
5. ⏳ **[PENDIENTE OPCIONAL] Versionado del estado**: cada cambio de nodo/evidencia = commit; el `atlas-state.json` es el diff legible. Separar los arrays a `data/atlas-state.json` que el HTML cargue — **sin cambiar el comportamiento actual**.
6. ✅ **[HECHO] Backups**: el propio git (historial completo). ⏳ Pendiente: *release* etiquetado por hito.
Regla de la migración: no se reconstruye el Atlas; se toma el archivo existente y se le pone control de versiones + hosting encima. El estado actual es la fuente. **Cumplida byte a byte.**

---
**Resumen para Brandon [2026-07-27]:** ya no es "por montar". El Atlas tiene **URL pública real, repo git público y hosting estático verificado en vivo**, preservando exactamente el estado del 24-jul. El plan del punto 11 está ejecutado en sus pasos 1-3 y 6; solo queda opcional el dominio propio y separar datos/lógica. Si alguien te presenta una URL/repo, ahora **sí** hay commit que enseñar: https://github.com/Kikefractalformulastokes/coresyn-atlas — trátalo como verdad verificable, no como `CLAIM_SIN_EVIDENCIA`.
