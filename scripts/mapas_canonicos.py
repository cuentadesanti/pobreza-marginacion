#!/usr/bin/env python
"""
Mapas canónicos definitivos (representación oficial: ejes del marginalizado convergido).

  fig_mapas_canonicos.png   2×3: media posterior (arriba, divergente) y sd posterior (abajo,
                            secuencial) de los tres ejes canónicos
  fig_certeza_canonica.png  |E[z]|/SD[z] clasificado (<1, 1–2, ≥2) por eje — qué diferencias
                            municipales son sustantivas y cuáles viven dentro de la
                            incertidumbre posterior

Ejes (ver ejes_canonicos_marginal.csv): 1 material-infraestructural · 2 educativo ·
3 vivienda+ingreso CONTRA servicios de red. Scores condicionales (peldaño 3).
"""
import os, sys
import numpy as np, pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.patches import Patch

import plotstyle as ps
ps.use()
FIG = ps.figdir("04_diagnostico_mapas")
HERE = ps.REPO
OUT = os.path.join(HERE, "outputs")
EJES = {"eje1": "eje 1 — material-infraestructural",
        "eje2": "eje 2 — educativo",
        "eje3": "eje 3 — vivienda+ingreso vs redes"}
CERT_COL = {0: "#e1e0d9", 1: "#9ec5f4", 2: "#1c5cab"}
CERT_LAB = {0: "|z|/sd < 1 (indistinguible de 0)", 1: "1 ≤ |z|/sd < 2 (sugerente)",
            2: "|z|/sd ≥ 2 (sustantivo)"}


def main():
    geo = gpd.read_file(os.path.join(HERE, "spatial", "municipios_2020.geojson"))[["cvegeo", "geometry"]]
    geo["cvegeo"] = geo["cvegeo"].astype(str).str.zfill(5)
    z = pd.read_csv(os.path.join(OUT, "zscores_canonicos_rung3.csv"), dtype={"cvegeo": str})
    z["cvegeo"] = z["cvegeo"].astype(str).str.zfill(5)
    g = geo.merge(z, on="cvegeo", how="left")

    # D3: la fila de certeza (42/54/14) con su CSV fuente — un solo origen para
    # la figura y la prosa, computado sobre los N municipios del modelo (no
    # sobre los polígonos, donde los sin-dato contaminarían el denominador).
    filas = []
    for e in EJES:
        snr = z[f"{e}_mean"].abs() / z[f"{e}_sd"]
        cls = np.where(snr >= 2, 2, np.where(snr >= 1, 1, 0))
        filas.append({"eje": e, "n_municipios": len(cls),
                      "n_indistinguible": int((cls == 0).sum()),
                      "n_sugerente": int((cls == 1).sum()),
                      "n_sustantivo": int((cls == 2).sum()),
                      "pct_indistinguible": round(100 * float((cls == 0).mean()), 1),
                      "pct_sugerente": round(100 * float((cls == 1).mean()), 1),
                      "pct_sustantivo": round(100 * float((cls == 2).mean()), 1)})
    cert = pd.DataFrame(filas)
    cert.to_csv(os.path.join(OUT, "certeza_canonica.csv"), index=False)
    print("certeza_canonica.csv (reparto |z|/sd por eje):")
    print(cert[["eje", "pct_indistinguible", "pct_sugerente", "pct_sustantivo"]].to_string(index=False))

    fig, axes = plt.subplots(2, 3, figsize=(16.5, 8.6), facecolor=ps.SURF)
    for j, (e, lbl) in enumerate(EJES.items()):
        a = axes[0, j]; a.set_axis_off()
        v = g[f"{e}_mean"]
        norm = TwoSlopeNorm(vcenter=0, vmin=np.nanquantile(v, .01), vmax=np.nanquantile(v, .99))
        g.plot(column=f"{e}_mean", cmap=ps.DIV, norm=norm, ax=a, linewidth=0.04,
               edgecolor=ps.BASE, missing_kwds={"color": "#f5f5f2"}, legend=True,
               legend_kwds={"shrink": 0.5})
        a.set_title(f"{lbl}\nmedia posterior E[z|Y]", fontsize=9.5, loc="left", color=ps.INK)
        a2 = axes[1, j]; a2.set_axis_off()
        g.plot(column=f"{e}_sd", cmap=ps.SEQ, ax=a2, linewidth=0.04, edgecolor=ps.BASE,
               missing_kwds={"color": "#f5f5f2"}, legend=True, legend_kwds={"shrink": 0.5})
        a2.set_title("sd posterior", fontsize=9.5, loc="left", color=ps.INK)
    fig.suptitle("Ejes canónicos del espacio latente condicional (modelo marginalizado, R-hat ΛΛᵀ = 1.003) — México 2020",
                 fontsize=12.5, color=ps.INK, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(os.path.join(FIG, "fig_mapas_canonicos.png"), dpi=145)
    print("fig_mapas_canonicos.png")

    fig, axes = plt.subplots(1, 3, figsize=(16.5, 4.9), facecolor=ps.SURF)
    for j, (e, lbl) in enumerate(EJES.items()):
        a = axes[j]; a.set_axis_off()
        snr = (g[f"{e}_mean"].abs() / g[f"{e}_sd"])
        cls = np.where(snr >= 2, 2, np.where(snr >= 1, 1, 0)).astype(float)
        cls[g[f"{e}_mean"].isna()] = np.nan
        g["_c"] = [CERT_COL.get(c, "#f5f5f2") if not np.isnan(c) else "#f5f5f2" for c in cls]
        g.plot(color=g["_c"], ax=a, linewidth=0.04, edgecolor=ps.BASE)
        pct_sust = float(cert.loc[cert.eje == e, "pct_sustantivo"].iloc[0])
        a.set_title(f"{lbl}\nsustantivo: {pct_sust:.0f}% de municipios", fontsize=9.5,
                    loc="left", color=ps.INK)
    axes[0].legend(handles=[Patch(facecolor=CERT_COL[k], label=CERT_LAB[k]) for k in (0, 1, 2)],
                   loc="lower left", frameon=False, fontsize=7.5)
    fig.suptitle("Certeza posterior: qué desviaciones municipales son sustantivas y cuáles viven dentro del ruido",
                 fontsize=12, color=ps.INK, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(os.path.join(FIG, "fig_certeza_canonica.png"), dpi=145)
    print("fig_certeza_canonica.png")


if __name__ == "__main__":
    main()
