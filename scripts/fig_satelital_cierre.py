#!/usr/bin/env python
"""
Dos figuras de cierre del capítulo satelital:
  fig_satelital_delta.png  ΔR² de las lentes sobre Vista D (factores brutos + 6 indicadores
                           observados + residual) — la fila decisiva, visualizada
  fig_satelital_mapa.png   mapa de la discordancia satelital e = z_obs − ẑ_M3 (material bruto):
                           dónde el satélite subestima la privación (rojo) y dónde el municipio
                           está mejor de lo esperado (azul; hipótesis remesas confirmada)
"""
import os
import numpy as np, pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, OUT, FIG = (os.path.join(HERE, p) for p in (os.path.join("data", "processed"), "outputs", "figures"))
SURF, INK, INK2, MUT, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
DIV = LinearSegmentedColormap.from_list("div", ["#104281", "#3987e5", "#f0efec", "#e34948", "#8f1f1f"])
plt.rcParams.update({"figure.facecolor": SURF, "axes.facecolor": SURF, "font.size": 9,
                     "axes.edgecolor": "#c3c2b7", "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": MUT, "ytick.color": MUT,
                     "axes.spines.top": False, "axes.spines.right": False})


# estilo homogéneo del repo + figuras por capítulo (ver scripts/plotstyle.py)
import plotstyle as ps
ps.use()
FIG = ps.figdir("07_satelital")

def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def fig_delta():
    D = pd.read_csv(os.path.join(OUT, "satelital_delta.csv"))
    orden = [("rung1", "material"), ("rung1", "monetario"), ("rung1", "educativo"),
             ("indicadores", "car_servbas"), ("indicadores", "piso_tierra"),
             ("indicadores", "rezago_educ"), ("indicadores", "car_vivienda"),
             ("indicadores", "car_salud"), ("indicadores", "lp_ingreso"),
             ("rung3", "material"), ("rung3", "educativo"), ("rung3", "monetario")]
    lbl = {("rung1", f): f"z {f} bruto" for f in ["material", "monetario", "educativo"]}
    lbl.update({("indicadores", i): i for i in ["car_servbas", "piso_tierra", "rezago_educ",
                                                "car_vivienda", "car_salud", "lp_ingreso"]})
    lbl.update({("rung3", f): f"z {f} residual" for f in ["material", "educativo", "monetario"]})
    rows = [(lbl[k], float(D[(D.outcome == k[0]) & (D.factor == k[1])].delta_vistaF.iloc[0]),
             k[0]) for k in orden]
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    y = np.arange(len(rows))[::-1]
    col = {"rung1": "#2a78d6", "indicadores": "#1baf7a", "rung3": "#898781"}
    ax.barh(y, [r[1] for r in rows], color=[col[r[2]] for r in rows], height=0.66,
            edgecolor=SURF, linewidth=1.2)
    for yi, (_, v, _) in zip(y, rows):
        ax.text(v + (0.004 if v >= 0 else -0.004), yi, f"{v:+.2f}", va="center",
                ha="left" if v >= 0 else "right", fontsize=8, color=INK)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
    ax.axvline(0, color="#c3c2b7", lw=1)
    ax.set_xlabel("ΔR² = R²(Vista D + lentes) − R²(Vista D)   [CV bloqueado por estado, hgb]")
    ax.set_title("Cuánto agregan las lentes satelitales SOBRE el contexto tabular\n"
                 "azul: factores brutos · verde: indicadores observados (independiente del GLLVM) · gris: residual",
                 fontsize=10, loc="left", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_satelital_delta.png"), dpi=160)
    print("fig_satelital_delta.png")


def fig_mapa():
    oof = norm(pd.read_parquet(os.path.join(OUT, "satelital_oof.parquet")))
    s = oof.query("outcome=='rung1' and modelo=='M3_lentes' and factor=='material'").copy()
    s["e"] = s["z_obs"] - s["z_pred"]
    geo = gpd.read_file(os.path.join(HERE, "spatial", "municipios_2020.geojson"))[["cvegeo", "geometry"]]
    geo["cvegeo"] = geo["cvegeo"].astype(str).str.zfill(5)
    g = geo.merge(s[["cvegeo", "e"]], on="cvegeo", how="left")
    vd = norm(pd.read_parquet(os.path.join(PROC, "vistaD_v1.parquet"),
                              columns=["cvegeo", "remesas_pc_usd"]))
    g = g.merge(vd, on="cvegeo", how="left")

    fig, ax = plt.subplots(figsize=(11.5, 7.6), facecolor=SURF)
    ax.set_facecolor(SURF); ax.set_axis_off()
    norm_ = TwoSlopeNorm(vcenter=0, vmin=np.nanquantile(g.e, 0.02), vmax=np.nanquantile(g.e, 0.98))
    g.plot(column="e", cmap=DIV, norm=norm_, ax=ax, linewidth=0.05, edgecolor="#c3c2b7",
           missing_kwds={"color": "#f5f5f2"}, legend=True,
           legend_kwds={"shrink": 0.55, "label": "e = z material observado − predicho por lentes"})
    # contornos de las colas 10%
    q10, q90 = g.e.quantile(0.1), g.e.quantile(0.9)
    g[g.e <= q10].plot(ax=ax, facecolor="none", edgecolor="#104281", linewidth=0.5)
    g[g.e >= q90].plot(ax=ax, facecolor="none", edgecolor="#8f1f1f", linewidth=0.5)
    med_lo = g[g.e <= q10].remesas_pc_usd.median()
    med_hi = g[g.e >= q90].remesas_pc_usd.median()
    ax.set_title("Discordancia satelital (material bruto): rojo = el satélite subestima la privación · "
                 "azul = mejor de lo esperado por sus luces/geografía\n"
                 f"mediana de remesas pc: cola azul {med_lo:.0f} USD vs cola roja {med_hi:.0f} USD "
                 "(~20×, IC95 14–28×) — la economía de transferencias no emite luz",
                 fontsize=10, loc="left", color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_satelital_mapa.png"), dpi=150)
    print("fig_satelital_mapa.png")


if __name__ == "__main__":
    fig_delta()
    fig_mapa()
