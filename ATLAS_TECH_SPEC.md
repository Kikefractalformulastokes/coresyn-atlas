# CoreSyn Atlas — Ficha técnica real y plan de migración
**Respuesta técnica a Brandon / HAI-0000001 · 2026-07-24 · sin humo**

Voy punto por punto con lo que **realmente** existe. No voy a inventar URL, repo, hosting ni backups que no hay: eso sería justo lo contrario de la disciplina del proyecto. El Atlas es real, pero es un **artefacto HTML autocontenido**, no un servicio web desplegado.

## 1. URL real del Atlas en funcionamiento
**No existe una URL pública.** El Atlas se ejecuta como *Cowork artifact* (id `coresyn-atlas-research-universe`) que se renderiza dentro de la app de escritorio de Claude de Enrique. No hay `https://…` direccionable desde fuera. Cualquiera que te dé una URL "en producción" del Atlas estaría inventando.

## 2. Repositorio / workspace donde vive
**No hay repositorio git.** Vive en dos sitios: (a) el almacén de *artifacts* de la app de escritorio de Claude (con historial de versiones del propio artifact), y (b) las copias `index.html` entregadas en el chat de esta sesión. No hay GitHub/GitLab todavía.

## 3. Hosting actual
El "hosting" es el **almacén de artifacts de Claude Desktop** (infra de Anthropic para renderizar artifacts en la barra lateral). No es hosting web tradicional ni es públicamente accesible. No hay servidor, ni contenedor, ni función serverless.

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
**No hay sistema formal de backups.** Redundancia existente: copias `index.html` en el chat + versiones del artifact en la app + los JSON exportables. (El plan de migración de abajo resuelve esto de verdad.)

## 11. Plan de migración SIN pérdida (preservar el que existe, NO reconstruir)
Objetivo: convertir el Atlas actual en referencia canónica versionada, **conservando byte a byte** el estado de hoy.
1. **Congelar** el `index.html` actual como `v1` (hash SHA-256 para sellarlo).
2. **Repo git** (GitHub) `coresyn-atlas`: subir el `index.html` tal cual + `atlas-state.json` + `evidence-registry.json`. Primer commit = estado 2026-07-24.
3. **Hosting estático**: GitHub Pages / Vercel / Netlify apuntando al repo → así aparece la **URL real** que hoy no existe. (5 min con tu cuenta.)
4. **Dominio** (opcional): CNAME a `atlas.coresyn.io`.
5. **Versionado del estado**: cada cambio de nodo/evidencia = commit; el `atlas-state.json` es el diff legible. Opcional: separar los arrays a `data/atlas-state.json` y que el HTML los cargue, para versionar datos y lógica por separado — **sin cambiar nada del comportamiento actual**.
6. **Backups**: el propio git (historial completo) + release por hito.
Regla de la migración: no se reconstruye el Atlas; se toma el archivo existente y se le pone control de versiones + hosting encima. El estado actual es la fuente.

---
**Resumen para Brandon:** el Atlas es real y te entrego su código completo y su estado exportado. Lo que NO es, es un servicio desplegado con URL/repo/dominio/backup — eso está por montar, y el plan del punto 11 lo monta preservando exactamente lo que hay. Si alguien te presenta una URL/repo "ya en producción", trátalo como `CLAIM_SIN_EVIDENCIA` hasta ver el commit.
