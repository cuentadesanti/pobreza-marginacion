#!/usr/bin/env python
"""
Vista G Fase 3 — línea G5: coerción política como ruta específica (criterio 5 del steer).

Fuente: Trejo & Ley, "High-Profile Criminal Violence" (Dataverse doi:10.7910/DVN/VIXNNE,
codebook verificado). Panel municipio-año 2007-2012, 2,018 municipios. CAPAM: ataques del
crimen organizado (asesinatos, intentos, secuestros, amenazas públicas) contra autoridades,
candidatos y activistas. Es EXPOSICIÓN HISTÓRICA: entra rezagada (2007-12 → outcomes 2020),
nunca contemporánea.

Modelos (FE estado, HC1, proxies de observabilidad SIEMPRE; WLS 1/sd² donde hay sd):
  G5a  ejes canónicos residuales 2020 ~ coerción 2007-12 + X          (¿ruta a privación?)
  G5b  log tasa EB homicidio 2019-21  ~ coerción 2007-12 + X          (persistencia)
  G5c  coerción 2007-12 ~ competencia OCVED Calderón × fragmentación  (¿dónde ocurre?)
       (misma era: C_calderon_0611 y juxtaposition 2007-12 son contemporáneos entre sí)
  G5d  descriptivo estatal: tasa de coerción vs PC1 de γ (32 obs, correlación)

O = R × D: CAPAM se construye de prensa — la detección viaja con visibilidad mediática;
los proxies de observabilidad van en TODAS las especificaciones y la robustez los quita
para dimensionar el sesgo. Lenguaje: asociación compatible con; nada causal.

Salidas: outputs/g5_coercion.csv (+ stdout)
"""
import os
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW, PROC, OUT = (os.path.join(HERE, "data", "raw"), os.path.join(HERE, "data", "processed"),
                  os.path.join(HERE, "outputs"))
XCOLS = ["loc_peq_pct", "log_pob", "dep_ratio", "pct_60mas", "pct_primario",
         "empleo_precario_pct", "remesas_pc_usd"]
OBS = ["internet_pct", "dist_capital_km", "acc_km", "log_ntl"]


def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def wls_fe(y, X, ent, w=None, labels=None):
    E = pd.get_dummies(ent, drop_first=True).astype(float).values
    M = np.column_stack([np.ones(len(y)), X, E])
    sw = np.sqrt(w) if w is not None else np.ones(len(y))
    Mw, yw = M * sw[:, None], y * sw
    b, *_ = np.linalg.lstsq(Mw, yw, rcond=None)
    u = yw - Mw @ b
    XtXi = np.linalg.pinv(Mw.T @ Mw)
    V = XtXi @ (Mw.T * u**2) @ Mw @ XtXi * len(y) / (len(y) - M.shape[1])
    se = np.sqrt(np.diag(V))
    return {labels[i]: (float(b[1 + i]), float(se[1 + i]), float(b[1 + i] / se[1 + i]))
            for i in range(X.shape[1])}


def main():
    tl = pd.read_stata(os.path.join(RAW, "trejo_ley", "Dataset_HighProfileCriminalViolence.dta"))
    tl["cvegeo"] = tl.cve_inegi.astype(int).astype(str).str.zfill(5)   # bug de ceros: zfill SIEMPRE
    agg = tl.groupby("cvegeo").agg(coercion_sum=("aggr_sum", "sum"),
                                   coercion_any=("aggr_dummy", "max"),
                                   juxt_mean=("juxtaposition", "mean"),
                                   cvmr_mean=("cvmr1000", "mean")).reset_index()
    print(f"Trejo-Ley colapsado: {len(agg)} municipios | ataques totales {int(agg.coercion_sum.sum())} "
          f"| munis con >=1: {int((agg.coercion_sum > 0).sum())}")

    cov = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))
    F = norm(pd.read_parquet(os.path.join(PROC, "vistaF_satelital.parquet"))).drop(columns=["pob_tot"])
    zc = norm(pd.read_csv(os.path.join(OUT, "zscores_canonicos_rung3.csv")))
    G = norm(pd.read_parquet(os.path.join(PROC, "vistaG_crimen_municipal.parquet")))
    hom = norm(pd.read_parquet(os.path.join(PROC, "homicidios_mun_2019_2021.parquet")))
    d = (cov.merge(F, on="cvegeo").merge(zc, on="cvegeo")
            .merge(G[["cvegeo", "pob_conapo", "internet_pct", "dist_capital_km",
                      "P_calderon_0611", "C_calderon_0611", "WC_calderon_0611"]], on="cvegeo")
            .merge(hom[["cvegeo", "hom_3a"]], on="cvegeo")
            .merge(agg, on="cvegeo", how="inner"))   # muestra = panel Trejo-Ley
    print(f"cruce con espacio latente 2020: {len(d)} municipios (cobertura del panel, no universo)")
    d["ent"] = d["cvegeo"].str[:2]
    rg = d.hom_3a.sum() / (d.pob_conapo.sum() * 3)
    d["log_hom_eb"] = np.log((d.hom_3a + rg * 20000) / (d.pob_conapo * 3 + 20000) * 1e5)
    d["remesas_pc_usd"] = np.log1p(d["remesas_pc_usd"])
    d["coercion_r100k"] = 1e5 * d.coercion_sum / d.pob_conapo      # 6 años acumulados
    d["juxt_mean"] = d.juxt_mean.fillna(d.juxt_mean.mean())
    Xfull = d[XCOLS + OBS].copy()
    Xfull = ((Xfull - Xfull.mean()) / Xfull.std()).values

    rows = []
    EXP = np.column_stack([d.coercion_any.values.astype(float),
                           np.log1p(d.coercion_r100k.values)])
    lab = ["coercion_any", "log_coercion_r100k"]

    # ---- G5a: ¿la coerción histórica predice privación residual 2020? ----
    for ej in ["eje1", "eje2", "eje3"]:
        y = d[f"{ej}_mean"].values
        w = 1 / np.maximum(d[f"{ej}_sd"].values, 1e-3) ** 2
        r = wls_fe(y, np.column_stack([EXP, Xfull]), d.ent, w, labels=lab + XCOLS + OBS)
        for k in lab:
            rows.append(dict(linea="G5a", outcome=ej, var=k, beta=round(r[k][0], 3),
                             se=round(r[k][1], 3), t=round(r[k][2], 1)))
        print(f"G5a {ej}: any {r[lab[0]][0]:+.3f} (t{r[lab[0]][2]:+.1f}) | "
              f"tasa {r[lab[1]][0]:+.3f} (t{r[lab[1]][2]:+.1f})")

    # ---- G5b: persistencia — coerción 2007-12 → homicidio 2019-21 ----
    r = wls_fe(d.log_hom_eb.values, np.column_stack([EXP, Xfull]), d.ent, labels=lab + XCOLS + OBS)
    for k in lab:
        rows.append(dict(linea="G5b", outcome="log_hom_eb", var=k, beta=round(r[k][0], 3),
                         se=round(r[k][1], 3), t=round(r[k][2], 1)))
    print(f"G5b homicidio 2019-21: any {r[lab[0]][0]:+.3f} (t{r[lab[0]][2]:+.1f}) | "
          f"tasa {r[lab[1]][0]:+.3f} (t{r[lab[1]][2]:+.1f})")
    # condicionando en competencia OCVED de la misma era (¿canal propio o el mismo?)
    C = d.C_calderon_0611.fillna(0).values.astype(float)
    r2 = wls_fe(d.log_hom_eb.values, np.column_stack([EXP, C[:, None], Xfull]), d.ent,
                labels=lab + ["C_calderon"] + XCOLS + OBS)
    rows.append(dict(linea="G5b", outcome="log_hom_eb", var="coercion_any|C",
                     beta=round(r2[lab[0]][0], 3), se=round(r2[lab[0]][1], 3), t=round(r2[lab[0]][2], 1)))
    rows.append(dict(linea="G5b", outcome="log_hom_eb", var="C_calderon",
                     beta=round(r2["C_calderon"][0], 3), se=round(r2["C_calderon"][1], 3),
                     t=round(r2["C_calderon"][2], 1)))
    print(f"     condicionando C_calderon: any {r2[lab[0]][0]:+.3f} (t{r2[lab[0]][2]:+.1f}), "
          f"C {r2['C_calderon'][0]:+.3f} (t{r2['C_calderon'][2]:+.1f})")

    # ---- G5c: ¿dónde ocurre la coerción? competencia × fragmentación (misma era) ----
    jx = (d.juxt_mean - d.juxt_mean.mean()) / d.juxt_mean.std()
    inter = C * jx.values
    r = wls_fe(d.coercion_any.values.astype(float),
               np.column_stack([C[:, None], jx.values[:, None], inter[:, None], Xfull]), d.ent,
               labels=["C_calderon", "juxt", "CxJuxt"] + XCOLS + OBS)
    for k in ["C_calderon", "juxt", "CxJuxt"]:
        rows.append(dict(linea="G5c", outcome="coercion_any", var=k, beta=round(r[k][0], 3),
                         se=round(r[k][1], 3), t=round(r[k][2], 1)))
    print(f"G5c coercion ~ C {r['C_calderon'][0]:+.3f} (t{r['C_calderon'][2]:+.1f}) + "
          f"juxt {r['juxt'][0]:+.3f} (t{r['juxt'][2]:+.1f}) + CxJ {r['CxJuxt'][0]:+.3f} "
          f"(t{r['CxJuxt'][2]:+.1f})   [LPM]")

    # ---- G5d: descriptivo estatal vs PC1 de gamma ----
    gpca = pd.read_csv(os.path.join(OUT, "veta_gamma_pca.csv"))
    est = d.groupby("ent").apply(
        lambda x: 1e5 * x.coercion_sum.sum() / x.pob_conapo.sum(), include_groups=False)
    gam = pd.read_csv(os.path.join(OUT, "gamma_marginal_rung3.csv"), index_col=0)
    Gm = gam.values - gam.values.mean(axis=1, keepdims=True)
    U, S, Vt = np.linalg.svd(Gm, full_matrices=False)
    pc1_est = pd.Series(Vt[0, :] * S[0], index=[c.zfill(2) for c in gam.columns])
    m = pd.concat([est.rename("coercion_r100k"), pc1_est.rename("pc1_gamma")], axis=1).dropna()
    print(f"G5d estatal (n={len(m)}): corr(tasa coerción, PC1_gamma) = "
          f"{np.corrcoef(m.coercion_r100k, m.pc1_gamma)[0, 1]:+.3f} (descriptivo)")
    rows.append(dict(linea="G5d", outcome="pc1_gamma_estatal", var="corr_coercion",
                     beta=round(float(np.corrcoef(m.coercion_r100k, m.pc1_gamma)[0, 1]), 3),
                     se=np.nan, t=np.nan))

    # ---- robustez: sin proxies, sin metrópolis ----
    Xsin = ((d[XCOLS] - d[XCOLS].mean()) / d[XCOLS].std()).values
    metros = d.pob_conapo.rank(ascending=False) <= 5
    for esc, (Xv, mk) in {"sin_proxies_cobertura": (Xsin, None),
                          "sin_5_metropolis": (Xfull, ~metros.values)}.items():
        for out_, yv, wv in [("eje1", d.eje1_mean.values,
                              1 / np.maximum(d.eje1_sd.values, 1e-3) ** 2),
                             ("log_hom_eb", d.log_hom_eb.values, None)]:
            if mk is not None:
                y2, X2, E2, ent2 = yv[mk], Xv[mk], EXP[mk], d.ent[mk]
                w2 = wv[mk] if wv is not None else None
            else:
                y2, X2, E2, ent2, w2 = yv, Xv, EXP, d.ent, wv
            r = wls_fe(y2, np.column_stack([E2, X2]), ent2, w2,
                       labels=lab + ["x"] * X2.shape[1])
            rows.append(dict(linea="G5_rob", outcome=out_, var=f"{esc}:coercion_any",
                             beta=round(r[lab[0]][0], 3), se=round(r[lab[0]][1], 3),
                             t=round(r[lab[0]][2], 1)))
            print(f"rob {esc} {out_}: any {r[lab[0]][0]:+.3f} (t{r[lab[0]][2]:+.1f})")

    pd.DataFrame(rows).to_csv(os.path.join(OUT, "g5_coercion.csv"), index=False)
    print("outputs/g5_coercion.csv")


if __name__ == "__main__":
    main()
