#!/usr/bin/env python
"""
Modelos satelitales (v2, tras revisión):

Outcomes:
  rung1 / rung3         factores latentes (bruto / condicional), ponderados 1/sd²
  indicadores           6 indicadores OBSERVADOS en logit-z (validación independiente del GLLVM)

Modelos: M0 Vista D sola | M1 NTL | M2 geografía | M3 NTL+geo | M4 Vista D + lentes
La fila decisiva es ΔR² = M4 − M0 (cuánto agregan las lentes SOBRE el contexto tabular).

Evaluación: GroupKFold bloqueado por estado; Moran residual; MAE por régimen LISA; R² regional.
Salidas: outputs/satelital_modelos.csv, satelital_delta.csv, satelital_importancias.csv,
         satelital_oof.parquet
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
NTL = ["log_ntl", "ntl_pc"]
GEO = ["elev_mean", "tri_mean", "acc_km"]
VD = ["dep_ratio", "pct_60mas", "pct_primario", "pct_secundario",
      "empleo_precario_pct", "remesas_pc_usd", "loc_peq_pct", "log_pob"]
MODELOS = {"M0_vistaD": VD, "M1_ntl": NTL, "M2_geografia": GEO,
           "M3_lentes": NTL + GEO, "M4_vistaD+lentes": VD + NTL + GEO}
IND_OBS = ["piso_tierra", "car_servbas", "car_vivienda", "lp_ingreso", "rezago_educ", "car_salud"]
NORTE = {"02", "03", "05", "08", "10", "19", "25", "26", "28", "32"}
SUR = {"04", "07", "12", "20", "21", "23", "27", "30", "31"}


def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def base():
    cov = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))
    F = norm(pd.read_parquet(os.path.join(PROC, "vistaF_satelital.parquet")))
    lisa = norm(pd.read_parquet(os.path.join(PROC, "lisa_classes.parquet"))[["cvegeo", "lisa"]])
    d = cov.merge(F, on="cvegeo", how="left").merge(lisa, on="cvegeo", how="left")
    assert len(d) >= 2450, d.shape
    d = d.reset_index(drop=True)
    d["ent"] = d["cvegeo"].str[:2]
    d["region"] = d["ent"].map(lambda e: "norte" if e in NORTE
                               else ("sur-sureste" if e in SUR else "centro"))
    d["lisa"] = d["lisa"].fillna("ns").where(d["lisa"].isin(["AA", "BB"]), "ns")
    for c in sorted(set(sum(MODELOS.values(), []))):
        if d[c].isna().any():
            d[c] = d[c].fillna(d[c].median())
    return d


def outcomes(d):
    """(tag, nombre, y, w) para cada outcome."""
    sets = []
    for rung in (1, 3):
        z = norm(pd.read_csv(os.path.join(OUT, f"zscores_rung{rung}_K3.csv")))
        z = d[["cvegeo"]].merge(z, on="cvegeo")
        assert len(z) == len(d)
        for fac in ["material", "educativo", "monetario"]:
            w = 1.0 / np.maximum(z[f"{fac}_sd"].values, 1e-3) ** 2
            sets.append((f"rung{rung}", fac, z[f"{fac}_mean"].values, w))
    Y = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet"))
    Y.index = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))["cvegeo"].values
    Y = Y.loc[d["cvegeo"]]
    for indi in IND_OBS:
        sets.append(("indicadores", indi, Y[indi].values, np.ones(len(d))))
    return sets


def moran_i(res, n1, n2):
    r = res - res.mean()
    return float(len(r) * (r[n1] * r[n2]).sum() * 2 / (2 * len(n1) * (r ** 2).sum()))


def main():
    d = base()
    ez = np.load(os.path.join(SPAT, "icar_edges.npz")); n1, n2 = ez["node1"], ez["node2"]
    gkf = GroupKFold(n_splits=5)
    rows, imps, oof_frames = [], [], []
    for tag, fac, y, w in outcomes(d):
        for mname, cols in MODELOS.items():
            X = d[cols].values
            for est in ["ridge", "hgb"]:
                oof = np.full(len(d), np.nan); r2s = []
                for tr, te in gkf.split(X, y, groups=d["ent"]):
                    if est == "ridge":
                        sc = StandardScaler().fit(X[tr])
                        m = Ridge(alpha=1.0).fit(sc.transform(X[tr]), y[tr], sample_weight=w[tr])
                        oof[te] = m.predict(sc.transform(X[te]))
                    else:
                        m = HistGradientBoostingRegressor(max_depth=4, max_iter=300, random_state=1)
                        m.fit(X[tr], y[tr], sample_weight=w[tr])
                        oof[te] = m.predict(X[te])
                    r2s.append(r2_score(y[te], oof[te]))
                res = y - oof
                row = dict(outcome=tag, factor=fac, modelo=mname, estimador=est,
                           r2cv_media=np.mean(r2s), r2cv_sd=np.std(r2s),
                           mae=mean_absolute_error(y, oof), moran_resid=moran_i(res, n1, n2))
                for reg in ["AA", "BB", "ns"]:
                    k = (d["lisa"] == reg).values
                    row[f"mae_{reg}"] = mean_absolute_error(y[k], oof[k]) if k.any() else np.nan
                for rg in ["norte", "centro", "sur-sureste"]:
                    k = (d["region"] == rg).values
                    row[f"r2_{rg}"] = r2_score(y[k], oof[k])
                rows.append(row)
                if est == "hgb" and mname in ("M3_lentes", "M0_vistaD"):
                    oof_frames.append(pd.DataFrame({"cvegeo": d["cvegeo"], "outcome": tag,
                                                    "factor": fac, "modelo": mname,
                                                    "z_obs": y, "z_pred": oof}))
                if est == "hgb" and tag == "rung3" and mname == "M4_vistaD+lentes":
                    mf = HistGradientBoostingRegressor(max_depth=4, max_iter=300,
                                                       random_state=1).fit(X, y, sample_weight=w)
                    pi = permutation_importance(mf, X, y, n_repeats=8, random_state=1)
                    for c, v in zip(cols, pi.importances_mean):
                        imps.append(dict(factor=fac, modelo=mname, feature=c, imp=v))
        print(f"{tag} {fac}: listo")
    R = pd.DataFrame(rows).round(4)
    R.to_csv(os.path.join(OUT, "satelital_modelos.csv"), index=False)
    pd.DataFrame(imps).round(4).to_csv(os.path.join(OUT, "satelital_importancias.csv"), index=False)
    pd.concat(oof_frames).to_parquet(os.path.join(OUT, "satelital_oof.parquet"), index=False)

    # ---- la fila decisiva: incremento de Vista F sobre Vista D ----
    piv = R[R.estimador == "hgb"].pivot_table(index=["outcome", "factor"],
                                              columns="modelo", values="r2cv_media")
    piv["delta_vistaF"] = piv["M4_vistaD+lentes"] - piv["M0_vistaD"]
    piv.round(3).to_csv(os.path.join(OUT, "satelital_delta.csv"))
    print("\nR² CV (hgb) y ΔR² de las lentes sobre Vista D:")
    print(piv.round(3).to_string())


if __name__ == "__main__":
    main()
