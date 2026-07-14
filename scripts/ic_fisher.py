#!/usr/bin/env python
"""
Bloque 4.1 de la revisión — IC de Fisher para las correlaciones estatales (n=32).

Los tres puntos que el paper reporta sin intervalo (PC1~PIBE +0.42, PC1~gasto −0.48,
salud~dependencia SP +0.61) son distinguibles de cero pero anchos con n=32; presentarlos
como puntos sobrevende la precisión. IC 95% por transformación z de Fisher.

Salida: outputs/ic_fisher_estatales.csv
"""
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")
N = 32


def fisher_ci(r, n=N, alpha=0.05):
    z = np.arctanh(r)
    se = 1 / np.sqrt(n - 3)
    lo, hi = z - 1.959964 * se, z + 1.959964 * se
    return np.tanh(lo), np.tanh(hi)


def main():
    t3 = pd.read_csv(os.path.join(OUT, "tabla3_gamma.csv")).set_index("medida")
    ins = pd.read_csv(os.path.join(OUT, "validacion_insabi.csv"))
    r_pibe = float(t3.loc["corr_PC1_log_pibe_pc", "valor"])
    r_gasto = float(t3.loc["corr_PC1_gasto_pibe_pct", "valor"])
    # la correlación salud~dependencia SP es la fila de car_salud
    fila = ins[ins.apply(lambda r: r.astype(str).str.contains("car_salud").any(), axis=1)]
    col_r = [c for c in ins.columns if ins[c].dtype.kind == "f"][0]
    r_salud = float(fila[col_r].iloc[0])
    rows = []
    for nombre, r in [("PC1_log_pibe_pc", r_pibe), ("PC1_gasto_pibe", r_gasto),
                      ("salud_dependencia_sp", r_salud)]:
        lo, hi = fisher_ci(r)
        rows.append(dict(correlacion=nombre, r=round(r, 3),
                         ci_lo=round(lo, 2), ci_hi=round(hi, 2), n=N))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "ic_fisher_estatales.csv"), index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
