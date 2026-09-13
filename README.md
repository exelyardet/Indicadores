# Indicadores

Monitor diario de indicadores económicos y financieros de Argentina y Estados Unidos: dólares, riesgo país, inflación, VIX, oro, petróleo (WTI/Brent), curva de rendimientos, indicadores del NBER y más — todo en una sola página, pensada para agregar a la pantalla de inicio del celular.

## Cómo publicarla (GitHub Pages, gratis)

Esta vez hay que subir **archivos y dos carpetas** (`scripts/` y `.github/`), manteniendo la estructura. La forma más simple:

1. Abrí la carpeta `app-para-subir` en tu compu. Adentro vas a ver: `index.html`, `manifest.json`, `icon-192.png`, `icon-512.png`, `README.md`, y las carpetas `scripts` y `.github`.
2. En GitHub, entrá a tu repo → **Add file → Upload files**.
3. Seleccioná **todo el contenido de adentro** de `app-para-subir` (los archivos sueltos + las 2 carpetas) y arrastralo — importante: arrastrá lo que está *adentro* de la carpeta, no la carpeta `app-para-subir` en sí (ese fue el error la vez pasada: quedó todo un nivel más adentro).
4. Hacé commit.
5. Andá a **Settings → Pages** → "Deploy from a branch" → rama **main**, carpeta **/(root)** → **Save** (si ya lo habías configurado, no hace falta repetirlo).
6. Andá a la pestaña **Actions** del repo y fijate que el workflow "Actualizar indicadores de EE.UU." haya corrido (se dispara solo al subir estos archivos). Si no corrió solo, entrá a ese workflow y tocá **Run workflow**.
7. Esperá 1-2 minutos y entrá a `https://exelyardet.github.io/Indicadores/`.
8. Desde el celular, abrí ese link y usá "Agregar a pantalla de inicio".

## Cómo actualizar

Es un sitio estático: no hay build ni instalación. Para cambiar algo, editá `index.html` directamente (texto, tarjetas, colores) y volvé a subirlo — GitHub Pages se actualiza solo en 1-2 minutos.

## Los números al lado del título (VIX, WTI, Brent, tasa a 10 años, inflación)

Estos 5 valores no se pueden traer de forma confiable desde el navegador (ni FRED ni TradingView lo permiten gratis para estos indicadores puntuales), así que se resuelven con un pequeño proceso automático:

- `.github/workflows/update-data.yml` es un "robot" de GitHub (gratis, ya incluido) que corre 3 veces por día.
- Ejecuta `scripts/fetch_us_indicators.py`, que consulta a FRED y guarda los últimos valores en `data/us-indicators.json`.
- La página lee ese archivo y muestra el número; si todavía no corrió ninguna vez, simplemente no aparece el número y queda el gráfico solo.

No hace falta que hagas nada para que esto funcione: una vez subido, corre solo. Podés ver su historial en la pestaña **Actions** del repo.

## Fuentes de datos

- **Dólares (Argentina):** [DolarAPI](https://dolarapi.com) — en vivo, sin necesidad de API key.
- **Riesgo país e inflación (Argentina):** [ArgentinaDatos](https://argentinadatos.com) — en vivo, sin necesidad de API key.
- **Reservas, tasas (BADLAR/TAMAR/política monetaria), EMAE/ISAC/IPI, REM:** por ahora son tarjetas de referencia con link directo a BCRA/INDEC, porque no tienen una API pública confiable para mostrar en vivo desde el navegador.
- **VIX, tasa a 10 años, CPI, WTI, Brent, curva de rendimientos e indicadores del NBER (EE.UU.):** gráficos de [FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org), más el valor numérico actualizado automáticamente (ver arriba).
- **Oro:** widget en vivo de [TradingView](https://www.tradingview.com) (es el único de estos que TradingView permite mostrar gratis embebido; VIX, WTI, Brent, tasas y datos macro los bloquea fuera de su propio sitio).

Los datos se muestran con fines informativos y no constituyen recomendación de inversión.
