# Indicadores

Monitor diario de indicadores económicos y financieros de Argentina y Estados Unidos: dólares, riesgo país, inflación, VIX, oro, petróleo (WTI/Brent), curva de rendimientos, indicadores del NBER y más — todo en una sola página, pensada para agregar a la pantalla de inicio del celular.

## Cómo publicarla (GitHub Pages, gratis)

1. Subí estos archivos (`index.html`, `manifest.json`, `icon-192.png`, `icon-512.png`) a la raíz de este repositorio.
2. Andá a **Settings → Pages**.
3. En "Build and deployment" → "Source" elegí **Deploy from a branch**.
4. En "Branch" elegí **main** y la carpeta **/(root)**, guardá.
5. Esperá 1-2 minutos y la app va a quedar publicada en algo como `https://exelyardet.github.io/Indicadores/`.
6. Desde el celular, abrí ese link en Chrome o Safari y usá "Agregar a pantalla de inicio".

## Cómo actualizar

Es un sitio estático: no hay build ni instalación. Para cambiar algo, editá `index.html` directamente (texto, tarjetas, colores) y volvé a subir el archivo — GitHub Pages se actualiza solo en 1-2 minutos.

## Fuentes de datos

- **Dólares (Argentina):** [DolarAPI](https://dolarapi.com) — en vivo, sin necesidad de API key.
- **Riesgo país e inflación (Argentina):** [ArgentinaDatos](https://argentinadatos.com) — en vivo, sin necesidad de API key.
- **Reservas, tasas (BADLAR/TAMAR/política monetaria), EMAE/ISAC/IPI, REM:** por ahora son tarjetas de referencia con link directo a BCRA/INDEC, porque no tienen una API pública confiable para mostrar en vivo desde el navegador. Se pueden agregar más adelante con un pequeño proceso automático (GitHub Actions) que consulte al BCRA/INDEC y guarde los valores en un archivo del repositorio.
- **VIX, tasa a 10 años, CPI, WTI, Brent, curva de rendimientos e indicadores del NBER (EE.UU.):** gráficos embebidos de [FRED (Federal Reserve Economic Data)](https://fred.stlouisfed.org).
- **Oro:** widget embebido de [TradingView](https://www.tradingview.com).

Los datos se muestran con fines informativos y no constituyen recomendación de inversión.
