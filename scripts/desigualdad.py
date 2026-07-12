#!/usr/bin/env python
"""
El giro a DESIGUALDAD (5 capas; aquí las 3 prioritarias + capa 3 exprés).

A. Descomposición entre/dentro de estados, ponderada por población:
   - Theil T para los 17 indicadores en su escala natural (%, no negativa)
   - varianza ponderada para los 3 ejes canónicos (z real-valuado: Theil no aplica)
   - p90/p10 por indicador
B. Brecha de apropiación territorial: B_i = z_obs − ẑ_lentes (material bruto, M3 oof).
   B>0 = el territorio está más privado de lo que su actividad visible sugiere (actividad
   sin apropiación local). Regresión sobre remesas/sectores/aislamiento + FE estado.
C. Acumulación multidimensional: A_i = #{k: z_ik > q75_k} sobre los 3 ejes canónicos
   condicionales -> mapa 0/1/2/3 dimensiones severas.
Capa 3 exprés: R²cv(circunstancias estructurales -> z bruto) por eje (asociación, no causal).

Salidas: outputs/desigualdad_theil.csv, desigualdad_brecha_apropiacion.csv,
         desigualdad_acumulacion.csv, figures/04_diagnostico_mapas/fig_acumulacion.png
"""
import os
import numpy as np, pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold
from sklearn.metrics import r2_score

import plotstyle as ps
ps.use()
FIG = ps.figdir("04_diagnostico_mapas")
HERE = ps.REPO
PROC, OUT = os.path.join(HERE, "data", "processed"), os.path.join(HERE, "outputs")
EJES = ["eje1", "eje2", "eje3"]
ACUM_COL = {0: "#f0efec", 1: "#f4b8b8", 2: "#e34948", 3: "#8f1f1f"}


def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def theil_decomp(x, w, g):
    """Theil T ponderado (x>=0) y partición entre/dentro de grupos g."""
    x = np.maximum(x, 1e-9); w = w / w.sum()
    mu = np.sum(w * x)
    T = float(np.sum(w * (x / mu) * np.log(x / mu)))
    tb = 0.0
    for gr in np.unique(g):
        k = g == gr
        Wg, mug = w[k].sum(), np.sum(w[k] * x[k]) / w[k].sum()
        tb += Wg * (mug / mu) * np.log(mug / mu)
    return T, float(tb), T - float(tb)


def var_decomp(z, w, g):
    w = w / w.sum(); mu = np.sum(w * z)
    vt = np.sum(w * (z - mu) ** 2)
    vb = 0.0
    for gr in np.unique(g):
        k = g == gr
        Wg, mug = w[k].sum(), np.sum(w[k] * z[k]) / w[k].sum()
        vb += Wg * (mug - mu) ** 2
    return float(vt), float(vb), float(vt - vb)


def main():
    comp = norm(pd.read_parquet(os.path.join(PROC, "municipal_components_2020.parquet")))
    zc = norm(pd.read_csv(os.path.join(OUT, "zscores_canonicos_rung3.csv")))
    z1 = norm(pd.read_csv(os.path.join(OUT, "zscores_rung1_K3.csv")))
    cov = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))
    F = norm(pd.read_parquet(os.path.join(PROC, "vistaF_satelital.parquet"))).drop(columns=["pob_tot"])
    d = comp.merge(zc, on="cvegeo").merge(cov.drop(columns=["pob_tot"]), on="cvegeo",
                                          suffixes=("", "_cov")).merge(F, on="cvegeo") \
            .merge(z1[["cvegeo", "material_mean"]].rename(columns={"material_mean": "z1_material"}),
                   on="cvegeo")
    assert len(d) >= 2450
    d["ent"] = d["cvegeo"].str[:2]
    w = d["pob_conapo"].values.astype(float)
    g = d["ent"].values

    # ---------- A. Theil por indicador + varianza por eje ----------
    rows = []
    for c in [x for x in comp.columns if x.endswith("_pct")]:
        x = d[c].values.astype(float)
        T, tb, tw = theil_decomp(x, w, g)
        rows.append(dict(medida=c, tipo="theil_indicador", total=round(T, 4),
                         entre_estados=round(tb, 4), dentro_estados=round(tw, 4),
                         pct_entre=round(100 * tb / max(T, 1e-9), 1),
                         p90_p10=round(np.percentile(x, 90) / max(np.percentile(x, 10), 1e-9), 1)))
    for e in EJES:
        vt, vb, vw = var_decomp(d[f"{e}_mean"].values, w, g)
        rows.append(dict(medida=e, tipo="var_eje_canonico", total=round(vt, 4),
                         entre_estados=round(vb, 4), dentro_estados=round(vw, 4),
                         pct_entre=round(100 * vb / max(vt, 1e-9), 1), p90_p10=np.nan))
    vt, vb, vw = var_decomp(d["z1_material"].values, w, g)
    rows.append(dict(medida="z_material_bruto", tipo="var_eje", total=round(vt, 4),
                     entre_estados=round(vb, 4), dentro_estados=round(vw, 4),
                     pct_entre=round(100 * vb / max(vt, 1e-9), 1), p90_p10=np.nan))
    A = pd.DataFrame(rows)
    A.to_csv(os.path.join(OUT, "desigualdad_theil.csv"), index=False)
    print("A. % de la desigualdad ENTRE estados (resto = dentro):")
    print(A.sort_values("pct_entre", ascending=False)[["medida", "tipo", "pct_entre"]]
          .head(8).to_string(index=False))
    print("   ejes canónicos:",
          {e: float(A[A.medida == e].pct_entre.iloc[0]) for e in EJES},
          "| z bruto material:", float(A[A.medida == 'z_material_bruto'].pct_entre.iloc[0]))

    # ---------- B. brecha de apropiación ----------
    oof = norm(pd.read_parquet(os.path.join(OUT, "satelital_oof.parquet")))
    oof = oof.query("outcome=='rung1' and modelo=='M3_lentes' and factor=='material'")
    d = d.merge(oof[["cvegeo", "z_obs", "z_pred"]], on="cvegeo")
    d["brecha_apropiacion"] = d["z_obs"] - d["z_pred"]
    expl = ["remesas_pc_usd", "pct_primario", "pct_secundario", "pct_terciario",
            "empleo_precario_pct", "loc_peq_pct", "log_pob", "acc_km", "tri_mean"]
    X = d[expl].copy()
    X["remesas_pc_usd"] = np.log1p(X["remesas_pc_usd"])
    Xs = (X - X.mean()) / X.std()
    E = pd.get_dummies(d["ent"], drop_first=True).astype(float)
    M = np.column_stack([np.ones(len(d)), Xs.values, E.values])
    b, *_ = np.linalg.lstsq(M, d["brecha_apropiacion"].values, rcond=None)
    u = d["brecha_apropiacion"].values - M @ b
    XtXi = np.linalg.pinv(M.T @ M)
    se = np.sqrt(np.diag(XtXi @ (M.T * u**2) @ M @ XtXi * len(d) / (len(d) - M.shape[1])))
    B = pd.DataFrame({"explicador": ["const"] + expl,
                      "beta_std": np.round(b[:len(expl) + 1], 3),
                      "t_HC1": np.round(b[:len(expl) + 1] / se[:len(expl) + 1], 1)})
    B.to_csv(os.path.join(OUT, "desigualdad_brecha_apropiacion.csv"), index=False)
    print("\nB. Brecha de apropiación (B>0 = actividad sin apropiación local), FE estado:")
    print(B.iloc[1:].sort_values("beta_std", key=abs, ascending=False).to_string(index=False))

    # ---------- C. acumulación multidimensional ----------
    for e in EJES:
        d[f"sev_{e}"] = (d[f"{e}_mean"] > d[f"{e}_mean"].quantile(0.75)).astype(int)
    d["acumulacion"] = d[[f"sev_{e}" for e in EJES]].sum(axis=1)
    dist = d.groupby("acumulacion")["pob_conapo"].agg(["size", "sum"])
    dist["pct_munis"] = (100 * dist["size"] / len(d)).round(1)
    dist["pct_pob"] = (100 * dist["sum"] / d.pob_conapo.sum()).round(1)
    print("\nC. Acumulación (dimensiones severas simultáneas, ejes canónicos condicionales):")
    print(dist[["size", "pct_munis", "pct_pob"]].to_string())
    d[["cvegeo", "nom_ent", "nom_mun", "acumulacion"] + [f"sev_{e}" for e in EJES]].to_csv(
        os.path.join(OUT, "desigualdad_acumulacion.csv"), index=False)
    geo = gpd.read_file(os.path.join(HERE, "spatial", "municipios_2020.geojson"))[["cvegeo", "geometry"]]
    geo["cvegeo"] = geo["cvegeo"].astype(str).str.zfill(5)
    gmap = geo.merge(d[["cvegeo", "acumulacion"]], on="cvegeo", how="left")
    fig, ax = plt.subplots(figsize=(11.5, 7.4), facecolor=ps.SURF)
    ax.set_axis_off()
    gmap["_c"] = gmap["acumulacion"].map(ACUM_COL).fillna("#f5f5f2")
    gmap.plot(color=gmap["_c"], ax=ax, linewidth=0.05, edgecolor=ps.BASE)
    ax.legend(handles=[Patch(facecolor=ACUM_COL[k],
                             label=f"{k} dimensiones severas "
                                   f"({dist.loc[k, 'pct_munis'] if k in dist.index else 0}% munis)")
                       for k in (0, 1, 2, 3)], loc="lower left", frameon=False, fontsize=8.5)
    ax.set_title("Acumulación multidimensional de privación residual (ejes canónicos condicionales)\n"
                 "¿la desigualdad se concentra en los mismos municipios o cada dimensión tiene su geografía?",
                 fontsize=11, loc="left", color=ps.INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_acumulacion.png"), dpi=150)
    print("fig_acumulacion.png")

    # ---------- capa 3 exprés: circunstancias -> z bruto ----------
    circ = ["tri_mean", "acc_km", "loc_peq_pct", "pct_60mas", "dep_ratio", "elev_mean"]
    gkf = GroupKFold(5)
    y = d["z1_material"].values
    Xc = d[circ].values
    r2s = []
    for tr, te in gkf.split(Xc, y, groups=d["ent"]):
        m = HistGradientBoostingRegressor(max_depth=4, max_iter=300, random_state=1).fit(Xc[tr], y[tr])
        r2s.append(r2_score(y[te], m.predict(Xc[te])))
    print(f"\nCapa 3 exprés: R²cv(circunstancias estructurales → z material bruto) = "
          f"{np.mean(r2s):.3f} (asociación, no causal; falta composición indígena — pendiente)")


if __name__ == "__main__":
    main()
