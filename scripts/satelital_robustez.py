#!/usr/bin/env python
"""
Robustez del capítulo satelital (revisión):

A. Sensibilidad al bloqueo espacial para el titular NTL->material bruto (y car_servbas):
   (i) estado (32 grupos), (ii) clusters espaciales KMeans-15 sobre centroides (sin outcomes),
   (iii) leave-one-macroregion-out (3 grupos).
B. Remesas y discordancia satelital, más allá de las colas:
   e_i = z_obs - ẑ_M3 (rung1);  e ~ log1p(remesas_pc) + loc_peq + log_pob + FE estado (OLS, HC1)
   + razón de medianas entre colas con bootstrap, umbrales 5/10/15%, filtro pob>=5k, log1p.

Salidas: outputs/satelital_robustez_bloqueo.csv, outputs/satelital_remesas_reg.csv (+ stdout)
"""
import os
import numpy as np, pandas as pd
import geopandas as gpd
from sklearn.model_selection import GroupKFold
from sklearn.cluster import KMeans
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, OUT, SPAT = (os.path.join(HERE, p) for p in (os.path.join("data", "processed"),
                                                   "outputs", "spatial"))
NORTE = {"02", "03", "05", "08", "10", "19", "25", "26", "28", "32"}
SUR = {"04", "07", "12", "20", "21", "23", "27", "30", "31"}


def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def main():
    F = norm(pd.read_parquet(os.path.join(PROC, "vistaF_satelital.parquet"))).drop(columns=["pob_tot"])
    cov = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))
    z1 = norm(pd.read_csv(os.path.join(OUT, "zscores_rung1_K3.csv")))
    Y = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet"))
    Y.index = cov["cvegeo"].values
    d = cov.merge(F, on="cvegeo").merge(z1, on="cvegeo")
    d["car_servbas_obs"] = Y.loc[d["cvegeo"], "car_servbas"].values
    d["ent"] = d["cvegeo"].str[:2]
    d["region"] = d["ent"].map(lambda e: "norte" if e in NORTE
                               else ("sur" if e in SUR else "centro"))
    geo = gpd.read_file(os.path.join(HERE, "spatial", "municipios_2020.geojson"))[["cvegeo", "geometry"]]
    geo["cvegeo"] = geo["cvegeo"].astype(str).str.zfill(5)
    cent = geo.set_index("cvegeo").to_crs(6372).geometry.centroid
    d["cx"] = cent.loc[d["cvegeo"]].x.values; d["cy"] = cent.loc[d["cvegeo"]].y.values
    d["km15"] = KMeans(15, n_init=10, random_state=1).fit_predict(d[["cx", "cy"]])

    # ---------- A. bloqueo ----------
    XNTL = d[["log_ntl", "ntl_pc"]].values
    rows = []
    for yname, y in [("z_material_rung1", d["material_mean"].values),
                     ("car_servbas_obs", d["car_servbas_obs"].values)]:
        for bloque, groups, ns in [("estado32", d["ent"], 5),
                                   ("kmeans15_espacial", d["km15"], 5),
                                   ("macroregion_LORO", d["region"], 3)]:
            gkf = GroupKFold(n_splits=ns)
            r2s = []
            for tr, te in gkf.split(XNTL, y, groups=groups):
                m = HistGradientBoostingRegressor(max_depth=4, max_iter=300, random_state=1)
                m.fit(XNTL[tr], y[tr])
                r2s.append(r2_score(y[te], m.predict(XNTL[te])))
            rows.append(dict(outcome=yname, bloqueo=bloque,
                             r2=np.mean(r2s), r2_min_fold=np.min(r2s)))
            print(f"A. {yname} | {bloque}: R²={np.mean(r2s):.3f} (peor fold {np.min(r2s):.3f})")
    pd.DataFrame(rows).round(3).to_csv(os.path.join(OUT, "satelital_robustez_bloqueo.csv"), index=False)

    # ---------- B. remesas ----------
    oof = norm(pd.read_parquet(os.path.join(OUT, "satelital_oof.parquet")))
    oof = oof.query("outcome=='rung1' and modelo=='M3_lentes'")
    res = []
    for fac in ["material", "monetario"]:
        s = oof[oof.factor == fac].merge(
            d[["cvegeo", "remesas_pc_usd", "loc_peq_pct", "log_pob", "ent", "pob_tot"]], on="cvegeo")
        s["e"] = s["z_obs"] - s["z_pred"]          # e<0 = mejor de lo esperado por las lentes
        s["lrem"] = np.log1p(s["remesas_pc_usd"])
        # OLS con FE de estado y HC1
        E = pd.get_dummies(s["ent"], drop_first=True).astype(float).values
        X = np.column_stack([np.ones(len(s)), s["lrem"], s["loc_peq_pct"], s["log_pob"], E])
        yv = s["e"].values
        b, *_ = np.linalg.lstsq(X, yv, rcond=None)
        u = yv - X @ b
        XtXi = np.linalg.pinv(X.T @ X)
        V = XtXi @ (X.T * (u ** 2)) @ X @ XtXi * len(s) / (len(s) - X.shape[1])
        se = np.sqrt(np.diag(V))
        res.append(dict(factor=fac, beta_lrem=b[1], se_HC1=se[1], t=b[1] / se[1], n=len(s)))
        print(f"B. {fac}: e ~ log1p(remesas): β={b[1]:+.4f} (HC1 se={se[1]:.4f}, t={b[1]/se[1]:+.1f})")
        # colas: umbrales y bootstrap de razón de medianas (solo material para el titular)
        if fac == "material":
            for q in (0.05, 0.10, 0.15):
                for filtro, sq in [("todos", s), ("pob>=5k", s[s.pob_tot >= 5000])]:
                    lo = sq.nsmallest(int(q * len(sq)), "e")["remesas_pc_usd"].median()
                    hi = sq.nlargest(int(q * len(sq)), "e")["remesas_pc_usd"].median()
                    print(f"   colas {int(q*100)}% ({filtro}): mejor-de-lo-esperado {lo:.0f} vs "
                          f"subestimadas {hi:.0f} USD pc (razón {lo/max(hi,0.1):.0f}x)")
            rng = np.random.default_rng(1)
            ratios = []
            for _ in range(2000):
                bs = s.sample(len(s), replace=True, random_state=None)
                lo = bs.nsmallest(int(0.1 * len(bs)), "e")["remesas_pc_usd"].median()
                hi = bs.nlargest(int(0.1 * len(bs)), "e")["remesas_pc_usd"].median()
                ratios.append(lo / max(hi, 0.1))
            print(f"   bootstrap razón de medianas (colas 10%): "
                  f"IC95 [{np.percentile(ratios,2.5):.0f}, {np.percentile(ratios,97.5):.0f}]x")
    pd.DataFrame(res).round(4).to_csv(os.path.join(OUT, "satelital_remesas_reg.csv"), index=False)


if __name__ == "__main__":
    main()
