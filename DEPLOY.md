# Deploy — coresyn-atlas

## GitHub Pages (recomendado, gratis)
1. Crea el repo `coresyn-atlas` en GitHub (público o privado).
2. Sube todo el contenido de esta carpeta (o `git init && git add . && git commit -m "Atlas v1 2026-07-24 (estado congelado)" && git push`).
3. Settings → Pages → Build and deployment → Source: **Deploy from a branch** → Branch: `main` / `/root` → Save.
4. En ~1 min tendrás la URL pública `https://<usuario>.github.io/coresyn-atlas/`.
5. Dominio propio (opcional): Settings → Pages → Custom domain → `atlas.coresyn.io` + registro CNAME en tu DNS.

## Alternativa: Vercel / Netlify
Importa el repo → framework "Other/Static" → deploy. URL inmediata + previews por commit.

## Versionado del estado
Cada cambio de nodo/evidencia = commit. El diff de `data/atlas-state.json` es el historial legible. Backups = historial git + releases por hito.

## Regla de migración
No se reconstruye el Atlas: se toma `index.html` tal cual (SHA sellado en README) y se le pone control de versiones + hosting encima.
