#!/usr/bin/env python
"""
Vista G (Fase 1) — exposición criminal municipal desde OCVED 2.0 (fuente auditada core_municipal).

Taxonomía obligatoria del steer (por ventana temporal):
  P  presencia documentada (>=1 evento)          N  actores distintos (orgs y células)
  C  competencia (N_orgs >= 2)                    F  fragmentación 1-sum(s^2) por células
  V  eventos violentos documentados               WC exposición vecinal (media de C en vecinos)
  tasas por 100k y suavizado EB (m=20k hab-año)

Ventanas: hist_0018 (2000-2018), calderon_0611, reciente_1518, w2018 (pre-2020 más cercana).
⚠ OCVED termina 2018-12-31 (verificado); no hay S_i (intervención estatal) en el xlsx público.
⚠ Ausencia de registro ≠ ausencia real: SIEMPRE acompañar de proxies de observabilidad
  (internet, log_pob, urbano, acc_km, dist a capital estatal) -> mismas filas.

Salidas: data/processed/vistaG_crimen_municipal.parquet, outputs/g_descriptivos.csv,
         figures/08_crimen/fig_g_presencia_competencia.png
"""
import os, sys, glob
import numpy as np, pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import plotstyle as ps
ps.use()
FIG = ps.figdir("08_crimen")
HERE = ps.REPO
PROC, OUT, SPAT = os.path.join(HERE, "data", "processed"), os.path.join(HERE, "outputs"), os.path.join(HERE, "spatial")
SCRATCH = sys.argv[1] if len(sys.argv) > 1 else "."
VENTANAS = {"hist_0018": (2000, 2018), "calderon_0611": (2006, 2011),
            "reciente_1518": (2015, 2018), "w2018": (2018, 2018)}
CAPITALES = {"01001","02002","03003","04002","05030","06002","07101","08019","09015","10005",
             "11015","12029","13048","14039","15106","16053","17007","18017","19039","20067",
             "21114","22014","23004","24028","25006","26030","27004","28041","29033","30087",
             "31050","32056"}


def norm5(s):
    return s.astype(str).str.replace(".0", "", regex=False).str.zfill(5)


def main():
    ev = pd.read_excel(os.path.join(SCRATCH, "ocved2.xlsx"))
    ev["cvegeo"] = norm5(ev["mun"])
    ev["anio"] = ev["year"].astype(int)
    base = pd.read_parquet(os.path.join(PROC, "municipal_components_2020.parquet"),
                           columns=["cvegeo", "pob_conapo"])
    base["cvegeo"] = norm5(base["cvegeo"])
    match = ev["cvegeo"].isin(set(base["cvegeo"])).mean()
    print(f"OCVED: {len(ev):,} eventos | match cvegeo con base municipal: {100*match:.1f}%")
    assert match > 0.97, "revisar claves OCVED"

    G = base.copy()
    for w, (a, b) in VENTANAS.items():
        e = ev[(ev.anio >= a) & (ev.anio <= b)]
        agg = e.groupby("cvegeo").agg(
            V=("counter", "sum"),
            N_orgs=("actor_main", lambda s: s[s != "Other"].nunique()),
            N_celulas=("actor_sub", "nunique")).reset_index()
        # fragmentación por células (shares de eventos)
        fr = (e.groupby(["cvegeo", "actor_sub"])["counter"].sum()
                .groupby("cvegeo").apply(lambda s: 1 - ((s / s.sum()) ** 2).sum())
                .rename("F").reset_index())
        agg = agg.merge(fr, on="cvegeo", how="left")
        G = G.merge(agg.rename(columns={c: f"{c}_{w}" for c in ["V", "N_orgs", "N_celulas", "F"]}),
                    on="cvegeo", how="left")
        for c in [f"V_{w}", f"N_orgs_{w}", f"N_celulas_{w}"]:
            G[c] = G[c].fillna(0)
        G[f"F_{w}"] = G[f"F_{w}"].fillna(0)
        G[f"P_{w}"] = (G[f"V_{w}"] > 0).astype(int)
        G[f"C_{w}"] = (G[f"N_orgs_{w}"] >= 2).astype(int)
        anios = b - a + 1
        G[f"tasa100k_{w}"] = G[f"V_{w}"] / (G.pob_conapo * anios) * 1e5
        rg = G[f"V_{w}"].sum() / (G.pob_conapo.sum() * anios)
        G[f"tasa_eb_{w}"] = (G[f"V_{w}"] + rg * 20000) / (G.pob_conapo * anios + 20000) * 1e5

    # exposición vecinal (grafo ICAR sobre el subconjunto gllvm de 2455; NaN fuera)
    cov = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))
    cov["cvegeo"] = norm5(cov["cvegeo"])
    ez = np.load(os.path.join(SPAT, "icar_edges.npz")); n1, n2 = ez["node1"], ez["node2"]
    idx = {c: i for i, c in enumerate(cov.cvegeo)}
    for w in VENTANAS:
        cvals = G.set_index("cvegeo")[f"C_{w}"].reindex(cov.cvegeo).values.astype(float)
        s = np.zeros(len(cov)); k = np.zeros(len(cov))
        for a_, b_ in zip(n1, n2):
            s[a_] += cvals[b_]; s[b_] += cvals[a_]; k[a_] += 1; k[b_] += 1
        wc = pd.Series(np.where(k > 0, s / np.maximum(k, 1), np.nan), index=cov.cvegeo,
                       name=f"WC_{w}")
        G = G.merge(wc.reset_index(), on="cvegeo", how="left")

    # ---- proxies de observabilidad ----
    it = pd.read_csv(glob.glob(os.path.join(SCRATCH, "iter/conjunto_de_datos_iter_00*.csv"))[0],
                     usecols=["ENTIDAD", "MUN", "LOC", "VPH_INTER", "TVIVPARHAB"], dtype=str)
    mu = it[(it.LOC == "0000") & (it.MUN != "000")].copy()
    for c in ["VPH_INTER", "TVIVPARHAB"]:
        mu[c] = pd.to_numeric(mu[c], errors="coerce")
    mu["cvegeo"] = mu.ENTIDAD.str.zfill(2) + mu.MUN.str.zfill(3)
    mu["internet_pct"] = 100 * mu.VPH_INTER / mu.TVIVPARHAB
    G = G.merge(mu[["cvegeo", "internet_pct"]], on="cvegeo", how="left")
    geo = gpd.read_file(os.path.join(SPAT, "municipios_2020.geojson"))[["cvegeo", "geometry"]]
    geo["cvegeo"] = norm5(geo["cvegeo"])
    cent = geo.set_index("cvegeo").to_crs(6372).geometry.centroid
    caps = cent.loc[[c for c in CAPITALES if c in cent.index]]
    G["dist_capital_km"] = [
        float(np.sqrt((caps[caps.index.str[:2] == c[:2]].x - cent[c].x) ** 2 +
                      (caps[caps.index.str[:2] == c[:2]].y - cent[c].y) ** 2).min()) / 1000
        if c in cent.index and (caps.index.str[:2] == c[:2]).any() else np.nan
        for c in G.cvegeo]
    assert len(G) >= 2450, G.shape
    G.to_parquet(os.path.join(PROC, "vistaG_crimen_municipal.parquet"), index=False)
    print(f"vistaG_crimen_municipal.parquet: {G.shape}")

    desc = []
    for w in VENTANAS:
        desc.append(dict(ventana=w, pct_P=round(100 * G[f"P_{w}"].mean(), 1),
                         pct_C=round(100 * G[f"C_{w}"].mean(), 1),
                         eventos=int(G[f"V_{w}"].sum()),
                         mediana_N_celulas_si_P=float(G.loc[G[f"P_{w}"] == 1, f"N_celulas_{w}"].median())))
    D = pd.DataFrame(desc); D.to_csv(os.path.join(OUT, "g_descriptivos.csv"), index=False)
    print(D.to_string(index=False))

    # mapa presencia/competencia histórica
    g = geo.merge(G[["cvegeo", "P_hist_0018", "C_hist_0018", "P_reciente_1518", "C_reciente_1518"]],
                  on="cvegeo", how="left")
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.6), facecolor=ps.SURF)
    for ax, w, ttl in [(axes[0], "hist_0018", "(a) 2000–2018 acumulado"),
                       (axes[1], "reciente_1518", "(b) 2015–2018 (ventana pre-2020)")]:
        ax.set_axis_off()
        cls = np.where(g[f"C_{w}"] == 1, 2, np.where(g[f"P_{w}"] == 1, 1, 0)).astype(float)
        cls[g[f"P_{w}"].isna()] = np.nan
        col = {0: "#f0efec", 1: "#9ec5f4", 2: "#e34948"}
        g["_c"] = [col.get(c, "#f5f5f2") if not np.isnan(c) else "#f5f5f2" for c in cls]
        g.plot(color=g["_c"], ax=ax, linewidth=0.04, edgecolor=ps.BASE)
        ax.set_title(f"{ttl}\ncompetencia (≥2 orgs): {100*np.nanmean(cls==2):.0f}% · solo presencia: "
                     f"{100*np.nanmean(cls==1):.0f}% · sin registro: {100*np.nanmean(cls==0):.0f}%",
                     fontsize=9.5, loc="left", color=ps.INK)
    axes[0].legend(handles=[Patch(facecolor="#f0efec", label="sin registro (≠ ausencia real)"),
                            Patch(facecolor="#9ec5f4", label="presencia documentada (1 org)"),
                            Patch(facecolor="#e34948", label="competencia documentada (≥2 orgs)")],
                   loc="lower left", frameon=False, fontsize=8)
    fig.suptitle("Vista G — presencia y competencia criminal documentada (OCVED 2.0; eventos, no censo)",
                 fontsize=12, color=ps.INK, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(os.path.join(FIG, "fig_g_presencia_competencia.png"), dpi=150)
    print("fig_g_presencia_competencia.png")


if __name__ == "__main__":
    main()
