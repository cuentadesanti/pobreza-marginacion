#!/usr/bin/env python
"""
Bloque 2.1 de la revisión — Moran's I residual de los modelos MARGINALIZADOS (M−γ, M+γ).

La Tabla 1 del paper deja "—" en el Moran residual de los peldaños marginalizados porque
la escalera lo calculaba sobre eta_mean = E[Y] de la predictiva posterior (que incluye
zΛ'), y en el marginalizado z está integrada. El análogo exacto es el residuo condicional:

    E[Y_i | Y_i, θ] = mu_i + C Σ⁻¹ (Y_i − mu_i),   C = ΛΛᵀ + Σ_b λ_b²(v_b v_bᵀ)
    r_i = Y_i − E[Y_i | Y_i]  = diag(σ²) Σ⁻¹ (Y_i − mu_i)

promediado sobre draws (thin=4, como scores_marginales). Moran's I por indicador con el
grafo Queen de spatial/icar_edges.npz (mismo estadístico que gllvm_ladder.residual_moran).

Salida: outputs/moran_marginal.csv (media 17 indicadores + detalle por indicador).
Uso: .venv/bin/python scripts/moran_marginal.py
"""
import os

import numpy as np
import pandas as pd
import arviz as az

import gllvm_ladder as gl

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")

CONTR = {0: {"analf": .5, "sin_basica": .5, "rezago_educ": -1.0},
         1: {"lp_ingreso": 1.0, "lp_ingreso_ext": 1.0},
         2: {"sin_drenaje": 1/3, "sin_electr": 1/3, "sin_agua": 1/3,
             "car_vivienda": -.5, "car_servbas": -.5}}


def eta_condicional(idata, Y, ind, rural, X, state, thin=4):
    post = idata.posterior
    C, D = post.sizes["chain"], post.sizes["draw"]
    A = np.column_stack([np.ones(len(Y)), rural] + [X[:, j] for j in range(X.shape[1])])
    etas = []
    for c in range(C):
        for d in range(0, D, thin):
            Lam = post["Lam"].values[c, d]
            sig = post["sigma"].values[c, d]
            lms = post["mload"].values[c, d]
            W = post["W"].values[c, d]
            mu = A @ W
            if "gamma" in post:
                mu = mu + post["gamma"].values[c, d].T[state]
            Com = Lam @ Lam.T
            for bi, cv in CONTR.items():
                v = np.zeros(len(ind))
                for n, w in cv.items():
                    v[ind.index(n)] = w
                v = v / np.linalg.norm(v)
                Com += (lms[bi] ** 2) * np.outer(v, v)
            Si = np.linalg.inv(Com + np.diag(sig ** 2))
            etas.append(mu + (Y - mu) @ (Si @ Com))   # (N,J); Com, Si simétricas
    return np.mean(etas, axis=0)


def main():
    Y, ind, rural, X, state, cvegeo = gl.load_data()
    edges, *_ = gl.load_spatial()
    rows = []
    for rung in (2, 3):
        idata = az.from_netcdf(os.path.join(OUT, f"idata_marginal_rung{rung}.nc"))
        eta = eta_condicional(idata, Y, ind, rural, X, state)  # γ entra solo si está en post
        mI, Is = gl.residual_moran(Y, eta, edges)
        rows.append(dict(modelo=f"marginal_rung{rung}", moran_I_mean=round(mI, 4),
                         **{f"I_{n}": round(v, 4) for n, v in zip(ind, Is)}))
        print(f"M{'+' if rung == 3 else '−'}γ (rung{rung}): Moran I residual medio = {mI:.4f}")
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "moran_marginal.csv"), index=False)
    print("outputs/moran_marginal.csv listo")


if __name__ == "__main__":
    main()
