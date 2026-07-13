#!/usr/bin/env python
"""
Discordancia bidireccional (§5): con M3 (solo lentes espaciales) sobre la privación BRUTA
(rung 1, donde las lentes tienen señal), residual por factor y las dos colas:

 (a) z_obs >> ẑ  -> "las luces dicen riqueza, lo social dice privación" (satélite SUBESTIMA)
 (b) z_obs << ẑ  -> "mejor de lo esperado por su geografía/luces" (hipótesis: remesas)

Salidas: outputs/satelital_discordancia.csv, figures/07_satelital/fig_satelital_discordancia.png
"""
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, OUT, FIG = (os.path.join(HERE, p) for p in (os.path.join("data", "processed"), "outputs", "figures"))
SURF, INK, INK2, MUT, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
RED, BLUE, GRAY = "#e34948", "#2a78d6", "#d5d4cd"
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


def main():
    oof = pd.read_parquet(os.path.join(OUT, "satelital_oof.parquet"))
    oof = norm(oof.query("outcome=='rung1' and modelo=='M3_lentes'"))
    comp = norm(pd.read_parquet(os.path.join(PROC, "municipal_components_2020.parquet"),
                                columns=["cvegeo", "nom_ent", "nom_mun", "pob_conapo"]))
    vd = norm(pd.read_parquet(os.path.join(PROC, "vistaD_v1.parquet"),
                              columns=["cvegeo", "remesas_pc_usd"]))
    lisa = norm(pd.read_parquet(os.path.join(PROC, "lisa_classes.parquet"))[["cvegeo", "lisa"]])
    d = oof.merge(comp, on="cvegeo").merge(vd, on="cvegeo").merge(lisa, on="cvegeo", how="left")
    d["residual"] = d["z_obs"] - d["z_pred"]

    rows = []
    for fac in ["material", "monetario"]:
        s = d[d.factor == fac].copy()
        for cola, sub in [("satelite_subestima", s.nlargest(20, "residual")),
                          ("mejor_de_lo_esperado", s.nsmallest(20, "residual"))]:
            for _, r in sub.iterrows():
                rows.append(dict(factor=fac, cola=cola, cvegeo=r.cvegeo, municipio=r.nom_mun,
                                 estado=r.nom_ent, z_obs=round(r.z_obs, 2),
                                 z_pred_lentes=round(r.z_pred, 2),
                                 residual=round(r.residual, 2), lisa=r.lisa,
                                 remesas_pc=round(r.remesas_pc_usd, 1),
                                 pob=int(r.pob_conapo)))
    D = pd.DataFrame(rows)
    D.to_csv(os.path.join(OUT, "satelital_discordancia.csv"), index=False)

    # test de la hipótesis remesas en la cola (b): ¿remesas pc más altas que el resto?
    print("Mediana remesas_pc por cola (material):")
    med_all = d.query("factor=='material'")["remesas_pc_usd"].median()
    for cola in ["satelite_subestima", "mejor_de_lo_esperado"]:
        med = D.query("factor=='material' and cola==@cola")["remesas_pc"].median()
        print(f"  {cola}: {med:.0f} USD pc (todos: {med_all:.0f})")

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.4))
    for ax, fac in zip(axes, ["material", "monetario"]):
        s = d[d.factor == fac]
        ax.scatter(s.z_pred, s.z_obs, s=8, color=GRAY, alpha=0.5, linewidths=0)
        top = s.nlargest(12, "residual"); bot = s.nsmallest(12, "residual")
        ax.scatter(top.z_pred, top.z_obs, s=22, color=RED, zorder=3)
        ax.scatter(bot.z_pred, bot.z_obs, s=22, color=BLUE, zorder=3)
        for _, r in pd.concat([top.nlargest(5, "pob_conapo"), bot.nlargest(5, "pob_conapo")]).iterrows():
            ax.annotate(r.nom_mun, (r.z_pred, r.z_obs), fontsize=6.5, color=INK2,
                        xytext=(4, 2), textcoords="offset points")
        lim = [min(s.z_pred.min(), s.z_obs.min()) - .2, max(s.z_pred.max(), s.z_obs.max()) + .2]
        ax.plot(lim, lim, color="#c3c2b7", lw=1)
        ax.set_xlabel(f"privación {fac} predicha por luces y geografía (fuera de muestra)")
        ax.set_ylabel(f"privación {fac} observada (estandarizada)")
        ax.set_title(f"({'ab'[fac=='monetario']}) {fac} — rojo: peor de lo que la actividad visible sugiere"
                     f"\nazul: mejor de lo esperado por sus luces/geografía", fontsize=9, loc="left")
    fig.suptitle("La actividad económica visible no siempre coincide con el bienestar local observado",
                 fontsize=12, color=INK, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(os.path.join(FIG, "fig_satelital_discordancia.png"), dpi=160)
    print("figura y csv listos")


if __name__ == "__main__":
    main()
