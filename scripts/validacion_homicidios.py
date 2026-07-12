#!/usr/bin/env python
"""
Validación externa del espacio latente contra un outcome NO usado en su construcción:
tasa municipal de homicidios 2019–2021 (INEGI defunciones registradas, espejo datos.gob.mx).

Pregunta: ¿el espacio latente (3 factores) retiene el poder predictivo de los 17 indicadores
oficiales sobre la violencia, y la discordancia marginación-pobreza agrega señal propia?

Diseño: ridge con 5-fold CV (R² fuera de muestra), y = log1p(tasa por 100k, promedio 3 años,
municipio de OCURRENCIA). Homicidio = PRESUNTO == 2; sensibilidad con CAUSA_DEF X85–Y09.

Conjuntos comparados:
  17_indicadores   los 17 logit-z (toda la información elemental oficial)
  z_rung1 (K=3)    3 factores no condicionales — ¿cuánto se pierde al comprimir 17->3?
  vistaD           solo composición observable (cofactores + ruralidad)
  z_rung3+disc     3 factores condicionales + discordancia observable CONAPO-CONEVAL
  vistaD+z3+disc   el modelo completo del repo

Salidas: outputs/validacion_homicidios.csv, figures/06_validacion_homicidios/fig_validacion_homicidios.png,
         data/processed/homicidios_mun_2019_2021.parquet
"""
import os, sys
import numpy as np, pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, OUT, FIG = (os.path.join(HERE, d) for d in (os.path.join("data", "processed"), "outputs", "figures"))
SCRATCH = sys.argv[1] if len(sys.argv) > 1 else "."
YEARS = [2019, 2020, 2021]

C = ["#2a78d6", "#1baf7a", "#eda100", "#008300", "#4a3aa7", "#e34948"]
SURF, INK, MUT, GRID = "#fcfcfb", "#0b0b0b", "#898781", "#e1e0d9"


# estilo homogéneo del repo + figuras por capítulo (ver scripts/plotstyle.py)
import plotstyle as ps
ps.use()
FIG = ps.figdir("06_validacion_homicidios")

def icd_homicidio(c):
    c = str(c).upper()
    return (c[:1] == "X" and c[1:3].isdigit() and 85 <= int(c[1:3]) <= 99) or \
           (c[:1] == "Y" and c[1:3].isdigit() and 0 <= int(c[1:3]) <= 9)


def build_rates():
    rows = []
    for y in YEARS:
        df = pd.read_csv(os.path.join(SCRATCH, f"defunciones_{y}.csv"),
                         usecols=["ENT_OCURR", "MUN_OCURR", "CAUSA_DEF", "PRESUNTO", "ANIO_OCUR"],
                         dtype=str, low_memory=False)
        df = df[df["ANIO_OCUR"].astype(int) == y]                 # ocurridas en el año
        df = df[(df["MUN_OCURR"].astype(int) < 900)]              # excluye no especificado
        df["cvegeo"] = df["ENT_OCURR"].str.zfill(2) + df["MUN_OCURR"].str.zfill(3)
        h = df[df["PRESUNTO"] == "2"].groupby("cvegeo").size().rename(f"hom_{y}")
        hicd = df[df["CAUSA_DEF"].map(icd_homicidio)].groupby("cvegeo").size().rename(f"hom_icd_{y}")
        rows.append(pd.concat([h, hicd], axis=1))
        print(f"{y}: PRESUNTO=2 -> {int(h.sum()):,} | ICD X85-Y09 -> {int(hicd.sum()):,}")
    agg = pd.concat(rows, axis=1).fillna(0)
    pob = pd.read_parquet(os.path.join(PROC, "municipal_components_2020.parquet"),
                          columns=["cvegeo", "pob_conapo"]).set_index("cvegeo")
    agg = agg.join(pob, how="right").fillna(0)
    agg["hom_3a"] = agg[[f"hom_{y}" for y in YEARS]].sum(axis=1)
    agg["tasa_100k"] = agg["hom_3a"] / (3 * agg["pob_conapo"]) * 1e5
    agg["hom_icd_3a"] = agg[[f"hom_icd_{y}" for y in YEARS]].sum(axis=1)
    agg.index.name = "cvegeo"
    agg.reset_index().to_parquet(os.path.join(PROC, "homicidios_mun_2019_2021.parquet"), index=False)
    return agg


def main():
    agg = build_rates()
    Y17 = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet"))
    cov = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))
    diag = pd.read_parquet(os.path.join(PROC, "diagnostico_municipal_v1.parquet"))
    z1 = pd.read_csv(os.path.join(OUT, "zscores_rung1_K3.csv"), dtype={"cvegeo": str})

    d = diag.merge(agg[["tasa_100k"]], left_on="cvegeo", right_index=True)
    d = d.merge(z1, on="cvegeo", suffixes=("", "_r1"))
    y = np.log1p(d["tasa_100k"].values)
    cov = cov.set_index("cvegeo").loc[d["cvegeo"]]
    X17 = Y17.set_index(cov.index).loc[d["cvegeo"]].values if len(Y17) == len(cov) else None
    # gllvm_Y no trae cvegeo: alinear por orden con covars (misma construcción)
    Y17.index = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))["cvegeo"].values
    X17 = Y17.loc[d["cvegeo"]].values

    DCOLS = ["dep_ratio", "pct_60mas", "pct_primario", "pct_secundario",
             "empleo_precario_pct", "remesas_pc_usd", "loc_peq_pct", "log_pob"]
    XD = cov.loc[d["cvegeo"], DCOLS].values
    Z3 = d[["material_mean", "educativo_mean", "monetario_mean"]].values
    Z1 = d[["material_mean_r1", "educativo_mean_r1", "monetario_mean_r1"]].values
    DISC = d[["discordancia_obs"]].values

    sets = {
        "17 indicadores": X17,
        "z peldaño 1 (3 factores)": Z1,
        "Vista D (composición)": XD,
        "z peldaño 3 + discordancia": np.hstack([Z3, DISC]),
        "Vista D + z3 + discordancia": np.hstack([XD, Z3, DISC]),
    }
    cvk = KFold(5, shuffle=True, random_state=1)
    res = {}
    for name, X in sets.items():
        pipe = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-2, 3, 20)))
        res[name] = cross_val_score(pipe, X, y, cv=cvk, scoring="r2")
    tab = pd.DataFrame({k: [v.mean(), v.std()] for k, v in res.items()},
                       index=["r2_cv_media", "r2_cv_sd"]).T.round(3)
    tab.index.name = "conjunto"
    tab.to_csv(os.path.join(OUT, "validacion_homicidios.csv"))
    print("\n", tab.to_string())

    fig, ax = plt.subplots(figsize=(7.5, 3.8), facecolor=SURF)
    ax.set_facecolor(SURF)
    names = list(res)
    yy = np.arange(len(names))[::-1]
    for i, n in enumerate(names):
        ax.barh(yy[i], res[n].mean(), xerr=res[n].std(), height=0.6, color=C[i],
                error_kw=dict(ecolor=MUT, lw=1.2))
        ax.text(res[n].mean() + res[n].std() + 0.008, yy[i], f"{res[n].mean():.2f}",
                va="center", fontsize=8.5, color=INK)
    ax.set_yticks(yy); ax.set_yticklabels(names, fontsize=8.5)
    ax.grid(axis="x", color=GRID, lw=0.6); ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlabel("R² (5-fold CV) — log tasa de homicidios 2019–2021", fontsize=9)
    ax.set_title("Validación externa: ¿qué versión de la privación predice la violencia?",
                 fontsize=10.5, color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_validacion_homicidios.png"), dpi=160)
    print("figura lista")


if __name__ == "__main__":
    main()
