#!/usr/bin/env python
"""
Mapas del diagnóstico municipal (figura insignia).

Descarga (con caché) las geometrías municipales del Marco Geoestadístico via gaia/wscatgeo
(sin token) usando el cliente local ~/code/inegi-client, y pinta 4 paneles desde
diagnostico_municipal_v1.parquet:

  (a) discordancia observable CONAPO−CONEVAL (divergente: rojo = más marginado que pobre)
  (b) z material residual del peldaño 3 (divergente)
  (c) sd posterior de z material (secuencial: dónde estamos menos seguros)
  (d) régimen LISA (categórico: AA / BB / ns)

Salida: figures/fig_mapa_diagnostico.png; caché geo en <scratch>/geo_municipal.geojson
"""
import os, sys, json
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, FIG = os.path.join(HERE, "data", "processed"), os.path.join(HERE, "figures")
SCRATCH = sys.argv[1] if len(sys.argv) > 1 else "."
CACHE = os.path.join(SCRATCH, "geo_municipal.geojson")

SURF, INK, MUT = "#fcfcfb", "#0b0b0b", "#898781"
# paleta de referencia: divergente azul-rojo con gris neutro; secuencial azul
DIV = LinearSegmentedColormap.from_list("div", ["#104281", "#3987e5", "#f0efec", "#e34948", "#8f1f1f"])
SEQ = LinearSegmentedColormap.from_list("seq", ["#cde2fb", "#3987e5", "#0d366b"])
LISA_COL = {"AA": "#e34948", "BB": "#2a78d6", "ns": "#e1e0d9"}


def get_geo():
    import geopandas as gpd
    if os.path.exists(CACHE):
        return gpd.read_file(CACHE)
    sys.path.insert(0, os.path.expanduser("~/code/inegi-client"))
    from inegi import INEGIClient
    c = INEGIClient()
    feats = []
    for e in range(1, 33):
        g = c.municipios_geojson(f"{e:02d}")
        feats.extend(g["features"])
        print(f"{e:02d}: {len(g['features'])} municipios")
    fc = {"type": "FeatureCollection", "features": feats}
    with open(CACHE, "w") as f:
        json.dump(fc, f)
    return gpd.read_file(CACHE)


def main():
    geo = get_geo()[["cvegeo", "geometry"]]
    d = pd.read_parquet(os.path.join(PROC, "diagnostico_municipal_v1.parquet"))
    g = geo.merge(d, on="cvegeo", how="left")
    print(f"geometrías: {len(geo)} | con diagnóstico: {g['material_mean'].notna().sum()}")

    fig, axes = plt.subplots(2, 2, figsize=(13, 10), facecolor=SURF)
    panels = [
        ("discordancia_obs", "(a) Discordancia observable (CONAPO − CONEVAL, logit-z)\nrojo = más marginado que pobre", DIV, True),
        ("material_mean", "(b) z material residual, peldaño 3\n(privación no explicada por composición ni estado)", DIV, True),
        ("material_sd", "(c) Incertidumbre del z material (sd posterior)\ndónde el dato municipal es menos concluyente", SEQ, False),
        ("lisa", "(d) Régimen LISA de discordancia", None, False),
    ]
    for ax, (col, title, cmap, diverging) in zip(axes.flat, panels):
        ax.set_facecolor(SURF); ax.set_axis_off()
        ax.set_title(title, fontsize=9.5, color=INK, loc="left")
        if col == "lisa":
            g["_c"] = g["lisa"].map(LISA_COL).fillna("#f5f5f2")
            g.plot(color=g["_c"], ax=ax, linewidth=0.05, edgecolor="#c3c2b7")
            from matplotlib.patches import Patch
            ax.legend(handles=[Patch(facecolor=LISA_COL[k],
                                     label={"AA": "AA: más marginado que pobre",
                                            "BB": "BB: más pobre que marginado",
                                            "ns": "no significativo"}[k]) for k in ("AA", "BB", "ns")],
                      loc="lower left", frameon=False, fontsize=8)
        else:
            v = g[col]
            norm = TwoSlopeNorm(vcenter=0, vmin=np.nanquantile(v, 0.01),
                                vmax=np.nanquantile(v, 0.99)) if diverging else None
            g.plot(column=col, cmap=cmap, norm=norm, ax=ax, linewidth=0.05,
                   edgecolor="#c3c2b7", missing_kwds={"color": "#f5f5f2"},
                   legend=True, legend_kwds={"shrink": 0.55})
    fig.suptitle("Diagnóstico municipal del espacio latente marginación-pobreza — México 2020",
                 fontsize=13, color=INK, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(os.path.join(FIG, "fig_mapa_diagnostico.png"), dpi=150)
    print("figures/fig_mapa_diagnostico.png lista")


if __name__ == "__main__":
    main()
