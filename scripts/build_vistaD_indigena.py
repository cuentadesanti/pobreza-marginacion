#!/usr/bin/env python
"""
Composición indígena municipal desde el ITER 2020 (tarea D5 del handoff).

Columnas VERIFICADAS en el diccionario oficial del ITER
(diccionario_datos_iter_00CSV20.csv, dentro de data/raw/iter_2020.zip):
  P3YM_HLI  — población de 3 años y más que habla alguna lengua indígena
  P3HLINHE  — ídem y además NO habla español (monolingüe)
  P_3YMAS   — denominador (población de 3 años y más)

Unidad: filas agregadas municipales del ITER (LOC == 0000). Valores enmascarados
('*', 'N/D') → NaN. Salida: data/processed/vistaD_indigena.parquet con
  pct_hli      = 100 · P3YM_HLI / P_3YMAS
  pct_hli_nhe  = 100 · P3HLINHE / P_3YMAS
"""
import os
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, PROC = os.path.join(HERE, "data", "raw"), os.path.join(HERE, "data", "processed")
CSV_IN_ZIP = "iter_00_cpv2020/conjunto_de_datos/conjunto_de_datos_iter_00CSV20.csv"
COLS = ["ENTIDAD", "MUN", "LOC", "P_3YMAS", "P3YM_HLI", "P3HLINHE"]


def main():
    with zipfile.ZipFile(os.path.join(RAW, "iter_2020.zip")) as z, z.open(CSV_IN_ZIP) as f:
        df = pd.read_csv(f, usecols=COLS, dtype=str)
    df = df[(df.LOC.astype(int) == 0) & (df.MUN.astype(int) != 0)].copy()
    df["cvegeo"] = df.ENTIDAD.str.zfill(2) + df.MUN.str.zfill(3)
    for c in ["P_3YMAS", "P3YM_HLI", "P3HLINHE"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["pct_hli"] = 100 * df.P3YM_HLI / df.P_3YMAS
    df["pct_hli_nhe"] = 100 * df.P3HLINHE / df.P_3YMAS
    out = df[["cvegeo", "pct_hli", "pct_hli_nhe"]].reset_index(drop=True)
    assert len(out) >= 2450, f"solo {len(out)} municipios (¿se perdieron claves?)"
    assert out.cvegeo.str.len().eq(5).all()
    n_na = int(out[["pct_hli", "pct_hli_nhe"]].isna().any(axis=1).sum())
    out.to_parquet(os.path.join(PROC, "vistaD_indigena.parquet"), index=False)
    print(f"vistaD_indigena.parquet: {len(out)} municipios | NaN (enmascarados): {n_na}")
    print(out[["pct_hli", "pct_hli_nhe"]].describe().round(2).to_string())


if __name__ == "__main__":
    main()
