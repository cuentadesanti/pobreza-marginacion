#!/usr/bin/env python
"""
Veta 1 — El desacuerdo inter-agencia, mapeado (la pregunta fundacional con la maquinaria final).

El modelo canónico estima el método como CONTRASTE inter-agencia por familia:
  educación:          +(analf, sin_basica)/2  −(rezago_educ)         [CONAPO vs CONEVAL]
  vivienda-servicios: +(drenaje,electr,agua)/3 −(car_viv,car_serv)/2 [CONAPO vs CONEVAL]
  líneas de ingreso:  +(lp, lp_ext)  [intra-CONEVAL: método SAE compartido]

Score municipal de desacuerdo por familia: proyección GLS del residuo (y − μ) sobre la
dirección del contraste, escalada por su carga posterior — análogo a E[z|Y] pero para m.
Positivo = CONAPO reporta MÁS privación relativa que CONEVAL en esa familia.

HALLAZGO que reorienta la veta (mloads del p2 libre): educación ≈ 0.012 — las agencias
CASI NO desacuerdan en educación (el factor absorbe lo común); líneas SAE = 0.58 — el
componente de método dominante es la FIRMA EBPH (las dos líneas se mueven juntas más allá
del factor monetario); viv-servicios = 0.135 sin estado → 0.029 con estado — el desacuerdo
de vivienda es fenómeno ESTATAL (calibración; dependencia 3 del DAG, observada).

Salidas: outputs/desacuerdo_agencias.csv, figures/04_diagnostico_mapas/fig_desacuerdo_agencias.png
"""
import os
import numpy as np, pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

import plotstyle as ps
ps.use()
FIG = ps.figdir("04_diagnostico_mapas")
HERE = ps.REPO
PROC, OUT, SPAT = os.path.join(HERE, "data", "processed"), os.path.join(HERE, "outputs"), os.path.join(HERE, "spatial")
import sys
sys.path.insert(0, os.path.join(HERE, "scripts"))
import gllvm_ladder as gl
import arviz as az

CONTR = {"m_educacion": {"analf": .5, "sin_basica": .5, "rezago_educ": -1.0},
         "m_lineas_sae": {"lp_ingreso": 1.0, "lp_ingreso_ext": 1.0},
         "m_viv_servicios": {"sin_drenaje": 1/3, "sin_electr": 1/3, "sin_agua": 1/3,
                             "car_vivienda": -.5, "car_servbas": -.5}}


def main():
    Y, ind, rural, X, state, cvegeo = gl.load_data()
    idata = az.from_netcdf(os.path.join(OUT, "idata_marginal_rung2.nc"))  # p2: sin FE que absorban
    post = idata.posterior
    A = np.column_stack([np.ones(len(Y)), rural] + [X[:, j] for j in range(X.shape[1])])
    Vs = {k: np.zeros(len(ind)) for k in CONTR}
    for k, cv in CONTR.items():
        for n, w in cv.items():
            Vs[k][ind.index(n)] = w
        Vs[k] = Vs[k] / np.linalg.norm(Vs[k])
    names = list(CONTR)
    C, D = post.sizes["chain"], post.sizes["draw"]
    ms, mv = [], []
    for c in range(C):
        for d_ in range(0, D, 4):
            LLt = post["LamLamT"].values[c, d_]
            sig = post["sigma"].values[c, d_]
            lms = post["mload"].values[c, d_]
            mu = A @ post["W"].values[c, d_]
            Cov = LLt + np.diag(sig ** 2)
            for bi, k in enumerate(names):
                Cov += (lms[bi] ** 2) * np.outer(Vs[k], Vs[k])
            Si = np.linalg.inv(Cov)
            resid = Y - mu
            B = np.stack([lms[bi] ** 2 * (Vs[k] @ Si) for bi, k in enumerate(names)])  # (3, J)
            ms.append(resid @ B.T)                                                     # (N, 3)
            mv.append(np.array([lms[bi] ** 2 - B[bi] @ Vs[k] * lms[bi] ** 2
                                for bi, k in enumerate(names)]))
    M = np.mean(ms, axis=0)
    Msd = np.sqrt(np.var(ms, axis=0) + np.clip(np.mean(mv, axis=0), 0, None)[None, :])
    mload_mean = post["mload"].mean(("chain", "draw")).values
    print("cargas de método (sd del desacuerdo por familia):",
          dict(zip(names, np.round(mload_mean, 3))))

    df = pd.DataFrame(M, columns=names)
    for i, k in enumerate(names):
        df[f"{k}_sd"] = Msd[:, i]
    df.insert(0, "cvegeo", pd.Series(cvegeo).astype(str).str.zfill(5))
    # correlatos
    lisa = pd.read_parquet(os.path.join(PROC, "lisa_classes.parquet"))[["cvegeo", "lisa"]]
    lisa["cvegeo"] = lisa["cvegeo"].astype(str).str.zfill(5)
    cov = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))
    cov["cvegeo"] = cov["cvegeo"].astype(str).str.zfill(5)
    df = df.merge(lisa, on="cvegeo", how="left").merge(
        cov[["cvegeo", "loc_peq_pct", "pct_60mas", "log_pob"]], on="cvegeo")
    df.to_csv(os.path.join(OUT, "desacuerdo_agencias.csv"), index=False)
    for fam in names:
        print(f"\ncorrelatos de {fam}:")
        for c in ["loc_peq_pct", "pct_60mas", "log_pob"]:
            print(f"  corr({fam}, {c}) = {np.corrcoef(df[fam], df[c])[0,1]:+.3f}")
        print(f"  por LISA: " + df.groupby(df.lisa.fillna('ns'))[fam].mean().round(3).to_dict().__str__())
        print(f"  % sustantivo (|m|/sd>=2): "
              f"{100 * float((df[fam].abs() / df[f'{fam}_sd'] >= 2).mean()):.1f}")

    # mapa: desacuerdo educativo y de vivienda-servicios
    geo = gpd.read_file(os.path.join(SPAT, "municipios_2020.geojson"))[["cvegeo", "geometry"]]
    geo["cvegeo"] = geo["cvegeo"].astype(str).str.zfill(5)
    g = geo.merge(df, on="cvegeo", how="left")
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.8), facecolor=ps.SURF)
    for ax, col, ttl in [
        (axes[0], "m_lineas_sae",
         "(a) HUELLA DEL MODELO DE INGRESO en áreas pequeñas (carga 0.58 — el componente dominante)\nrojo: las dos líneas de ingreso se desvían JUNTAS hacia más pobreza\nde lo que el factor monetario explica"),
        (axes[1], "m_viv_servicios",
         "(b) Desacuerdo VIVIENDA-SERVICIOS CONAPO vs CONEVAL (carga 0.135 sin estado;\n0.029 con estado: es un fenómeno ESTATAL — huella de la calibración estatal)")]:
        ax.set_axis_off()
        v = g[col]
        norm = TwoSlopeNorm(vcenter=0, vmin=np.nanquantile(v, .01), vmax=np.nanquantile(v, .99))
        g.plot(column=col, cmap=ps.DIV, norm=norm, ax=ax, linewidth=0.04, edgecolor=ps.BASE,
               missing_kwds={"color": "#f5f5f2"}, legend=True, legend_kwds={"shrink": 0.55})
        ax.set_title(ttl, fontsize=9.5, loc="left", color=ps.INK)
    fig.suptitle("La anatomía del método: la huella del modelo de ingreso domina, el desacuerdo de vivienda es huella de calibración estatal, y en educación las agencias casi acuerdan",
                 fontsize=12, color=ps.INK, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(os.path.join(FIG, "fig_desacuerdo_agencias.png"), dpi=150)
    print("fig_desacuerdo_agencias.png")


if __name__ == "__main__":
    main()
