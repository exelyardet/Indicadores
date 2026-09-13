#!/usr/bin/env python3
"""
Trae los últimos valores de un puñado de series de FRED usando la API oficial
(https://fred.stlouisfed.org/docs/api/fred/) y los guarda en
data/us-indicators.json para que el sitio estático los muestre como un número
al lado del título de cada indicador.

Necesita una API key gratuita de FRED en la variable de entorno FRED_API_KEY
(se pide una vez en https://fred.stlouisfed.org/docs/api/api_key.html y se
carga como secreto del repositorio: Settings → Secrets and variables →
Actions → New repository secret, con el nombre FRED_API_KEY).

Se ejecuta automáticamente vía GitHub Actions (ver .github/workflows/update-data.yml).
Para probarlo a mano:
    FRED_API_KEY=tu_key python3 scripts/fetch_us_indicators.py
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API_KEY = os.environ.get("FRED_API_KEY", "").strip()
FRED_API = "https://api.stlouisfed.org/fred/series/observations"

# id de FRED -> (clave en el json de salida, cuántas observaciones atrás
# comparar para calcular variación interanual; None = no calcular variación)
SERIES = {
    "VIXCLS": ("VIXCLS", None),
    "DCOILWTICO": ("DCOILWTICO", None),
    "DCOILBRENTEU": ("DCOILBRENTEU", None),
    "DGS10": ("DGS10", None),
    "CPIAUCSL": ("CPI_YOY", 12),  # mensual: 12 observaciones atrás = 12 meses
}


def fetch_observations(series_id, limit=15):
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": limit,
    }
    url = FRED_API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "indicadores-app/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    obs = payload.get("observations", [])
    # la API devuelve más nuevo primero (sort_order=desc); nos quedamos con
    # las que tengan valor real (FRED usa "." para datos faltantes)
    clean = [(o["date"], o["value"]) for o in obs if o.get("value") not in (None, ".", "")]
    if not clean:
        raise ValueError(f"Sin observaciones válidas para {series_id}")
    return clean  # clean[0] = la más reciente


def main():
    out = {"updated": datetime.now(timezone.utc).isoformat()}
    errors = []

    if not API_KEY:
        errors.append("Falta la variable de entorno FRED_API_KEY (secreto del repo).")
        print(errors[0], file=sys.stderr)

    for series_id, (out_key, obs_back) in SERIES.items():
        if not API_KEY:
            out[out_key] = {"value": None, "date": None}
            continue
        try:
            clean = fetch_observations(series_id, limit=(obs_back or 0) + 3)
            latest_date, latest_val = clean[0]
            latest_val = float(latest_val)

            if obs_back is None:
                out[out_key] = {"value": round(latest_val, 2), "date": latest_date}
            else:
                if len(clean) > obs_back:
                    prev_date, prev_val = clean[obs_back]
                    prev_val = float(prev_val)
                    yoy = (latest_val / prev_val - 1) * 100 if prev_val else None
                    out[out_key] = {
                        "value": round(yoy, 1) if yoy is not None else None,
                        "date": latest_date,
                        "index_value": round(latest_val, 2),
                    }
                else:
                    out[out_key] = {"value": None, "date": latest_date}
        except Exception as e:  # noqa: BLE001
            errors.append(f"{series_id}: {e}")
            out[out_key] = {"value": None, "date": None}

    if errors:
        out["errors"] = errors
        print("Errores al traer algunas series:", errors, file=sys.stderr)

    os.makedirs("data", exist_ok=True)
    with open("data/us-indicators.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
