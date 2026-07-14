#!/usr/bin/env python
"""
Bloque 2.2 de la revisión — sensibilidad de las cargas de método a las direcciones v_b.

La carga 0.58 de la familia lineas_sae es condicional a la dirección exacta {+1,+1} y a los
pesos fijos de educación {+.5,+.5,−1} y vivienda {+1/3×3,−.5×2}. Barrido de ±20% en los
pesos (una perturbación por corrida, el resto en su valor base): si mload es estable, la
conclusión no es artefacto de la parametrización; si baila, se declara.

Corridas reducidas (500/500, 2 cadenas, numpyro) del rung3 marginalizado. Cada una ~minutos.
Salida: outputs/sensibilidad_vb.csv + figures/02_escalera_gllvm/fig_sensibilidad_vb.png
Uso: .venv/bin/python scripts/sensibilidad_vb.py
"""
import os

import numpy as np
import pandas as pd
import pymc as pm
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import gllvm_ladder as gl
import gllvm_marginal as gm
import plotstyle as ps

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")

BASE = {0: {"analf": .5, "sin_basica": .5, "rezago_educ": -1.0},
        1: {"lp_ingreso": 1.0, "lp_ingreso_ext": 1.0},
        2: {"sin_drenaje": 1/3, "sin_electr": 1/3, "sin_agua": 1/3,
            "car_vivienda": -.5, "car_servbas": -.5}}

# un escenario = (nombre, bloque perturbado, dict de pesos que reemplaza al bloque)
ESCENARIOS = [
    ("educ −20% censal", 0, {"analf": .4, "sin_basica": .4, "rezago_educ": -1.0}),
    ("educ +20% censal", 0, {"analf": .6, "sin_basica": .6, "rezago_educ": -1.0}),
    ("líneas asimétrica 1:0.8", 1, {"lp_ingreso": 1.0, "lp_ingreso_ext": 0.8}),
    ("líneas asimétrica 0.8:1", 1, {"lp_ingreso": 0.8, "lp_ingreso_ext": 1.0}),
    ("vivienda −20% CONEVAL", 2, {"sin_drenaje": 1/3, "sin_electr": 1/3, "sin_agua": 1/3,
                                  "car_vivienda": -.4, "car_servbas": -.4}),
    ("vivienda +20% CONEVAL", 2, {"sin_drenaje": 1/3, "sin_electr": 1/3, "sin_agua": 1/3,
                                  "car_vivienda": -.6, "car_servbas": -.6}),
]
FAMILIAS = ["educación", "líneas (SAE)", "vivienda-servicios"]


def corrida(contrastes, tag):
    Y, ind, rural, X, state, _ = gl.load_data()
    mod, _ = gm.build(Y, ind, 3, rural, X, state, contrastes=contrastes)
    with mod:
        idata = pm.sample(nuts_sampler="numpyro", draws=500, tune=500, chains=2,
                          random_seed=11, target_accept=0.9, progressbar=False)
    post = idata.posterior["mload"]
    rows = []
    for b in range(3):
        v = post.isel(mload_dim_0=b).values.ravel()
        rows.append(dict(escenario=tag, bloque=FAMILIAS[b], mload_mean=v.mean(),
                         mload_lo=np.quantile(v, .05), mload_hi=np.quantile(v, .95)))
    return rows


def main():
    ps.use()
    rows = []
    # referencia: el posterior archivado del modelo base (1000 draws x 4 cadenas)
    import arviz as az
    base = az.from_netcdf(os.path.join(OUT, "idata_marginal_rung3.nc")).posterior["mload"]
    for b in range(3):
        v = base.isel(mload_dim_0=b).values.ravel()
        rows.append(dict(escenario="base {+pesos originales}", bloque=FAMILIAS[b],
                         mload_mean=v.mean(), mload_lo=np.quantile(v, .05),
                         mload_hi=np.quantile(v, .95)))
    for tag, blk, pesos in ESCENARIOS:
        c = {k: dict(v) for k, v in BASE.items()}
        c[blk] = pesos
        rows += corrida(c, tag)
        print(f"✓ {tag}")
    df = pd.DataFrame(rows).round(4)
    df.to_csv(os.path.join(OUT, "sensibilidad_vb.csv"), index=False)

    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    esc = ["base {+pesos originales}"] + [e[0] for e in ESCENARIOS]
    colores = {"educación": "#8d7bd4", "líneas (SAE)": "#e34948", "vivienda-servicios": "#2a78d6"}
    for bi, fam in enumerate(FAMILIAS):
        s = df[df["bloque"] == fam].set_index("escenario").loc[esc]
        xs = np.arange(len(esc)) + (bi - 1) * 0.22
        ax.errorbar(xs, s["mload_mean"], yerr=[s["mload_mean"] - s["mload_lo"],
                    s["mload_hi"] - s["mload_mean"]], fmt="o", ms=6, capsize=3,
                    color=colores[fam], label=fam, lw=1.4)
    ax.set_xticks(np.arange(len(esc)), [e.replace(" ", "\n", 1) for e in esc], fontsize=7.5)
    ax.set_ylabel("carga de método λ_b (posterior, banda 90%)")
    ax.axhline(0, color="#c3c2b7", lw=1)
    ax.legend(frameon=False, fontsize=8.5)
    ax.set_title("Sensibilidad de las cargas de método a los pesos de las direcciones v_b "
                 "(±20%)", loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(ps.figdir("02_escalera_gllvm"), "fig_sensibilidad_vb.png"),
                dpi=160)
    print("sensibilidad_vb.csv + fig_sensibilidad_vb.png listos")


if __name__ == "__main__":
    main()
