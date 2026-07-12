#!/usr/bin/env python
"""
Comparación apples-to-apples de los peldaños 2 y 3 MARGINALIZADOS (misma verosimilitud MvN):
¿qué cambia al introducir gamma_estado manteniendo fija la representación marginal?

  - ELPD con DIFERENCIA e incertidumbre (az.compare), no valores puntuales
  - eigenvalores y ángulos principales entre subespacios E[LamLam']
  - varianzas específicas (sigma) y cargas de método (mload) por peldaño
  - proporción de varianza absorbida por gamma_estado
  - correlación de scores canónicos 2 vs 3

Salida: outputs/comparacion_marginal_2v3.csv + stdout
"""
import os
import numpy as np, pandas as pd
import arviz as az
from scipy.linalg import subspace_angles

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")


def eig3(idata):
    M = idata.posterior["LamLamT"].mean(("chain", "draw")).values
    w, V = np.linalg.eigh(M)
    o = np.argsort(-w)
    return w[o], V[:, o[:3]], M


def main():
    i2 = az.from_netcdf(os.path.join(OUT, "idata_marginal_rung2.nc"))
    i3 = az.from_netcdf(os.path.join(OUT, "idata_marginal_rung3.nc"))
    ind = list(pd.read_csv(os.path.join(OUT, "loadings_rung1_K3.csv"), index_col=0).index)

    cmp = az.compare({"p2_marginal": i2, "p3_marginal_estado": i3})
    print("=== ELPD (az.compare, misma verosimilitud) ===")
    print(cmp[["rank", "elpd_loo", "elpd_diff", "dse"]].round(1).to_string())

    w2, V2, M2 = eig3(i2); w3, V3, M3 = eig3(i3)
    print("\neigenvalores p2:", np.round(w2[:5], 3))
    print("eigenvalores p3:", np.round(w3[:5], 3))
    ang = np.degrees(subspace_angles(V2, V3))
    print("ángulos principales entre subespacios top-3 (grados):", np.round(ang, 1))

    s2 = i2.posterior["sigma"].mean(("chain", "draw")).values
    s3 = i3.posterior["sigma"].mean(("chain", "draw")).values
    m2 = i2.posterior["mload"].mean(("chain", "draw")).values
    m3 = i3.posterior["mload"].mean(("chain", "draw")).values
    print("\nmload p2:", np.round(m2, 3), "| p3:", np.round(m3, 3))
    gam = i3.posterior["gamma"].mean(("chain", "draw")).values
    share_g = gam.var(axis=1)
    T = pd.DataFrame({"indicador": ind, "sigma_p2": np.round(s2, 3),
                      "sigma_p3": np.round(s3, 3),
                      "delta_sigma2": np.round(s2**2 - s3**2, 3),
                      "share_gamma_p3": np.round(share_g, 3)})
    T["gamma_explica_delta"] = np.round(T.share_gamma_p3 / T.delta_sigma2.clip(1e-6), 2)
    T.to_csv(os.path.join(OUT, "comparacion_marginal_2v3.csv"), index=False)
    print("\nTop-6 indicadores donde el estado absorbe uniqueness (Δσ² p2→p3 vs share γ):")
    print(T.nlargest(6, "delta_sigma2").to_string(index=False))
    print(f"\nvarianza estatal media absorbida: {share_g.mean():.3f} "
          f"| reducción media de σ²: {(s2**2 - s3**2).mean():.3f}")


if __name__ == "__main__":
    main()
