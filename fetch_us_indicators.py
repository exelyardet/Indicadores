#!/usr/bin/env python3
"""
Trae los últimos valores de un puñado de series de FRED (sin necesitar API key,
usando el mismo endpoint público que usa el botón "Download Data" de FRED) y
los guarda en data/us-indicators.json para que el sitio estático los muestre
como un número al lado del título de cada indicador.

Se ejecuta automáticamente vía GitHub Actions (ver .github/workflows/update-data.yml),
así que no hace falta correrlo a mano. Si igual querés probarlo localmente:
    python3 scripts/fetch_us_indicators.py
"""
import csv
import io
import json
import sys
import urllib.request
from datetime import datetime, timezone

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={id}"

# id de FRED -> (clave en el json de salida, cuántos meses/observaciones atrás
# comparar para calcular variación interanual; None = no calcular variación)
SERIES = {
    "VIXCLS": ("VIXCLS", None),
    "DCOILWTICO": ("DCOILWTICO", None),
    "DCOILBRENTEU": ("DCOILBRENTEU", None),
    "DGS10": ("DGS10", None),
    "CPIAUCSL": ("CPI_YOY", 12),  # mensual: 12 observaciones atrás = 12 meses
}


def fetch_series(series_id):
    url = FRED_CSV.format(id=series_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    rows = list(csv.reader(io.StringIO(raw)))
    if not rows or len(rows) < 2:
        raise ValueError(f"Respuesta vacía o inesperada para {series_id}")
    header = rows[0]
    data_rows = rows[1:]
    # columna 0 = DATE, columna 1 = valor de la serie
    clean = [(r[0], r[1]) for r in data_rows if len(r) >= 2 and r[1] not in ("", ".")]
    if not clean:
        raise ValueError(f"Sin observaciones válidas para {series_id}")
    return clean


def main():
    out = {"updated": datetime.now(timezone.utc).isoformat()}
    errors = []

    for series_id, (out_key, months_back) in SERIES.items():
        try:
            clean = fetch_series(series_id)
            latest_date, latest_val = clean[-1]
            latest_val = float(latest_val)

            if months_back is None:
                out[out_key] = {"value": round(latest_val, 2), "date": latest_date}
            else:
                if len(clean) > months_back:
                    prev_date, prev_val = clean[-1 - months_back]
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

    import os
    os.makedirs("data", exist_ok=True)
    with open("data/us-indicators.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
