#!/usr/bin/env python
"""
Modelos satelitales M1-M4 × 3 factores (§3-4 de INSTRUCCIONES_ANALISIS_SATELITAL.md).

M1: z_k ~ NTL | M2: z_k ~ geografía | M3: NTL+geografía | M4: M3 + Vista D
Estimadores: Ridge (referencia lineal) y HistGradientBoosting (no lineal).
Evaluación: GroupKFold espacialmente bloqueado por estado (cve_ent), ponderado por 1/sd²
del score posterior; Moran I residual (icar_edges); MAE por régimen LISA; R² por macro-región.

Salidas: outputs/satelital_modelos.csv, outputs/satelital_importancias.csv,
         outputs/satelital_oof.parquet (predicciones out-of-fold para la discordancia §5)
"""
import os
import numpy as np, pandas as pd
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.inspection import permutation_importance
from sklearn.metrics import r2_score, mean_absolute_error

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, OUT, SPAT = (os.path.join(HERE, p) for p in (os.path.join("data", "processed"),
                                                   "outputs", "spatial"))
FACTORES = ["material", "educativo", "monetario"]
NTL = ["log_ntl", "ntl_pc"]
GEO = ["elev_mean", "tri_mean", "acc_km"]
VD = ["dep_ratio", "pct_60mas", "pct_primario", "pct_secundario",
      "empleo_precario_pct", "remesas_pc_usd", "loc_peq_pct", "log_pob"]
MODELOS = {"M1_ntl": NTL, "M2_geografia": GEO, "M3_lentes": NTL + GEO, "M4_lentes+vistaD": NTL + GEO + VD}
NORTE = {"02", "03", "05", "08", "10", "19", "25", "26", "28", "32"}
SUR = {"04", "07", "12", "20", "21", "23", "27", "30", "31"}


def region(e):
    return "norte" if e in NORTE else ("sur-sureste" if e in SUR else "centro")


def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def load(rung=3):
    cov = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))
    z = norm(pd.read_csv(os.path.join(OUT, f"zscores_rung{rung}_K3.csv")))
    F = norm(pd.read_parquet(os.path.join(PROC, "vistaF_satelital.parquet")))
    lisa = norm(pd.read_parquet(os.path.join(PROC, "lisa_classes.parquet"))[["cvegeo", "lisa"]])
    d = cov.merge(z, on="cvegeo").merge(F, on="cvegeo", how="left").merge(lisa, on="cvegeo", how="left")
    assert len(d) >= 2450, d.shape
    d = d.reset_index(drop=True)          # orden = gllvm_covars = orden de icar_edges
    d["ent"] = d["cvegeo"].str[:2]
    d["region"] = d["ent"].map(region)
    d["lisa"] = d["lisa"].fillna("ns").where(d["lisa"].isin(["AA", "BB"]), "ns")
    # imputación mínima para features con NaN (raster sin cobertura): mediana + bandera
    feats = sorted(set(sum(MODELOS.values(), [])))
    for c in feats:
        if d[c].isna().any():
            print(f"  imputa mediana en {c}: {d[c].isna().sum()} NaN")
            d[c] = d[c].fillna(d[c].median())
    return d


def moran_i(res, n1, n2):
    r = res - res.mean()
    return float(len(r) * (r[n1] * r[n2]).sum() * 2 / (2 * len(n1) * (r ** 2).sum()))


def main():
    ez = np.load(os.path.join(SPAT, "icar_edges.npz"))
    n1, n2 = ez["node1"], ez["node2"]
    gkf = GroupKFold(n_splits=5)
    rows, imps, oof_frames = [], [], []
    for rung in (3, 1):
      d = load(rung)
      for fac in FACTORES:
        y = d[f"{fac}_mean"].values
        rungtag = f"rung{rung}"
        w = 1.0 / np.maximum(d[f"{fac}_sd"].values, 1e-3) ** 2
        for mname, cols in MODELOS.items():
            X = d[cols].values
            for est in ["ridge", "hgb"]:
                oof = np.full(len(d), np.nan)
                r2s = []
                for tr, te in gkf.split(X, y, groups=d["ent"]):
                    if est == "ridge":
                        sc = StandardScaler().fit(X[tr])
                        m = Ridge(alpha=1.0).fit(sc.transform(X[tr]), y[tr], sample_weight=w[tr])
                        oof[te] = m.predict(sc.transform(X[te]))
                    else:
                        m = HistGradientBoostingRegressor(max_depth=4, max_iter=300,
                                                          random_state=1)
                        m.fit(X[tr], y[tr], sample_weight=w[tr])
                        oof[te] = m.predict(X[te])
                    r2s.append(r2_score(y[te], oof[te]))
                res = y - oof
                row = dict(outcome=rungtag, factor=fac, modelo=mname, estimador=est,
                           r2cv_media=np.mean(r2s), r2cv_sd=np.std(r2s),
                           mae=mean_absolute_error(y, oof),
                           moran_resid=moran_i(res, n1, n2))
                for reg in ["AA", "BB", "ns"]:
                    k = d["lisa"] == reg
                    row[f"mae_{reg}"] = mean_absolute_error(y[k], oof[k]) if k.any() else np.nan
                for rg in ["norte", "centro", "sur-sureste"]:
                    k = (d["region"] == rg).values
                    row[f"r2_{rg}"] = r2_score(y[k], oof[k])
                rows.append(row)
                if est == "hgb":
                    oof_frames.append(pd.DataFrame({"cvegeo": d["cvegeo"], "outcome": rungtag,
                                                    "factor": fac, "modelo": mname,
                                                    "z_obs": y, "z_pred": oof}))
                # importancia por permutación (solo hgb, M3/M4, ajuste completo)
                if est == "hgb" and rung == 3 and mname in ("M3_lentes", "M4_lentes+vistaD"):
                    mfull = HistGradientBoostingRegressor(max_depth=4, max_iter=300,
                                                          random_state=1).fit(X, y, sample_weight=w)
                    pi = permutation_importance(mfull, X, y, n_repeats=8, random_state=1)
                    for c, v in zip(cols, pi.importances_mean):
                        imps.append(dict(factor=fac, modelo=mname, feature=c, imp=v))
        print(f"rung{rung} {fac}: listo")
    R = pd.DataFrame(rows).round(4)
    R.to_csv(os.path.join(OUT, "satelital_modelos.csv"), index=False)
    pd.DataFrame(imps).round(4).to_csv(os.path.join(OUT, "satelital_importancias.csv"), index=False)
    pd.concat(oof_frames).to_parquet(os.path.join(OUT, "satelital_oof.parquet"), index=False)
    print("\nR² CV (hgb):")
    print(R[R.estimador == "hgb"].pivot_table(index=["outcome", "modelo"], columns="factor",
                                              values="r2cv_media").round(3).to_string())


if __name__ == "__main__":
    main()
