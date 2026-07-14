#!/usr/bin/env python
"""
Bloque 1 de la revisión — el hecho mecánico detrás de la carga 0.58: las dos líneas de
pobreza por ingreso son dos umbrales sobre la misma variable de ingreso estimada (SAE),
y su correlación municipal es casi 1. Ese co-movimiento se espera aunque no hubiera
método compartido; el paper debe declararlo.

Salida: outputs/corr_lineas.csv (correlación cruda en % y en escala logit-z del modelo).
"""
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
OUT = os.path.join(HERE, "outputs")


def main():
    Y = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet"))
    r_logit = Y["lp_ingreso"].corr(Y["lp_ingreso_ext"])
    # también la correlación parcial dado el resto de indicadores CONEVAL de ingreso cercano
    resto = [c for c in Y.columns if c not in ("lp_ingreso", "lp_ingreso_ext")]
    X = np.column_stack([np.ones(len(Y)), Y[resto].values])
    r1 = Y["lp_ingreso"].values - X @ np.linalg.lstsq(X, Y["lp_ingreso"].values, rcond=None)[0]
    r2 = Y["lp_ingreso_ext"].values - X @ np.linalg.lstsq(X, Y["lp_ingreso_ext"].values,
                                                          rcond=None)[0]
    r_parcial = float(np.corrcoef(r1, r2)[0, 1])
    df = pd.DataFrame([
        dict(medida="corr_logitz_lineas", valor=round(float(r_logit), 3)),
        dict(medida="corr_parcial_dado_resto", valor=round(r_parcial, 3)),
    ])
    df.to_csv(os.path.join(OUT, "corr_lineas.csv"), index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
