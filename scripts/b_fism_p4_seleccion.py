#!/usr/bin/env python
"""
P4 del feedback humano — ¿el sesgo de submuestra del test piso/incremento es footnote?

El titular del §7.3 (+15.8% AA) se estima sobre la muestra completa EFIPEM (n≈2,241). El test
de descomposición vive en la submuestra con FISM rastreable en 2013 y 2020 (10.1% del modelo).
La pregunta del lector: ¿el efecto AA difiere entre esa submuestra y el resto? Si no, el sesgo
de cobertura no distorsiona el resultado y se degrada a nota al pie.

Test correcto (muestras anidadas, no dos regresiones separadas): sobre la muestra completa,
interactuar el régimen con un indicador de pertenencia a la submuestra FISM. Si AA×enFISM es
no significativo, el efecto AA es el mismo dentro y fuera → sin sesgo de selección.

Salida: outputs/b_fism_p4_seleccion.csv
"""
import os

import numpy as np
import pandas as pd
import statsmodels.api as sm

import b_fism_descomposicion as b

OUT = b.OUT


def main():
    d, _ = b.cargar()
    # muestra completa EFIPEM, misma spec del titular (gap_aportaciones_regimen)
    full = d.dropna(subset=["aportaciones_pc"]).query("aportaciones_pc>0").copy()
    full["enFISM"] = full["en_muestra"].astype(float)
    full["AA"] = (full["reg"] == "AA").astype(float)
    full["BB"] = (full["reg"] == "BB").astype(float)
    full["log_apo"] = np.log(full["aportaciones_pc"])

    X = pd.DataFrame({
        "const": 1.0, "nivel": full["nivel"], "nivel2": full["nivel"] ** 2,
        "log_pob": full["log_pob"], "AA": full["AA"], "BB": full["BB"],
        "enFISM": full["enFISM"],
        "AA_x_enFISM": full["AA"] * full["enFISM"],
        "BB_x_enFISM": full["BB"] * full["enFISM"],
    })
    mod = sm.OLS(full["log_apo"], X).fit(cov_type="HC1")

    rows = []
    for term in ["AA", "BB", "AA_x_enFISM", "BB_x_enFISM", "enFISM"]:
        c = mod.params[term]
        rows.append(dict(term=term, coef=round(c, 4),
                         pct=round(100 * (np.exp(c) - 1), 2),
                         se=round(mod.bse[term], 4), t=round(mod.tvalues[term], 2),
                         ci_lo_pct=round(100 * (np.exp(mod.conf_int().loc[term, 0]) - 1), 2),
                         ci_hi_pct=round(100 * (np.exp(mod.conf_int().loc[term, 1]) - 1), 2)))
    res = pd.DataFrame(rows)
    res["n_full"] = int(mod.nobs)
    res["n_enFISM"] = int(full["enFISM"].sum())
    res.to_csv(os.path.join(OUT, "b_fism_p4_seleccion.csv"), index=False)
    print(res.to_string(index=False))
    print(f"\nInterpretación: AA×enFISM t={mod.tvalues['AA_x_enFISM']:.2f} "
          f"(IC del efecto extra en % [{res[res.term=='AA_x_enFISM'].ci_lo_pct.iloc[0]}, "
          f"{res[res.term=='AA_x_enFISM'].ci_hi_pct.iloc[0]}]). "
          f"{'INDISTINGUIBLE → sesgo footnote' if abs(mod.tvalues['AA_x_enFISM'])<1.96 else 'DIFIERE → mantener sesgo declarado'}")


if __name__ == "__main__":
    main()
