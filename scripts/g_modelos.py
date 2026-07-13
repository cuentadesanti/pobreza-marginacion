#!/usr/bin/env python
"""
Vista G Fase 2 — análisis defendible (líneas G1, G2, G4 del steer).

G1: ejes canónicos residuales ~ P + C + WC + X, FE estado (WLS 1/sd², HC1)
    Hipótesis: |β_competencia| > |β_presencia| (sin pre-registrar signo por eje).
G2: brecha de apropiación ~ C_pre + WC_pre + X, FE estado.
G4: log tasa EB de homicidios 2019-21 ~ {P sola} vs {P + C}: ¿competencia > presencia?

Exposición: OCVED ventana pre-2020 (2015-2018); robustez con calderon_0611 y w2018.
X SIEMPRE incluye proxies de observabilidad (internet, log_pob, urbano, dist_capital).
Robustez: sin proxies (contraste), sin 5 metrópolis, N=1 vs N>=2 (steer 7.6).

Lenguaje: ASOCIACIÓN COMPATIBLE CON — nada causal.
Salidas: outputs/g_modelos_principales.csv, outputs/g_robustez.csv
"""
import os
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, OUT = os.path.join(HERE, "data", "processed"), os.path.join(HERE, "outputs")
XCOLS = ["loc_peq_pct", "log_pob", "dep_ratio", "pct_60mas", "pct_primario",
         "empleo_precario_pct", "remesas_pc_usd"]
OBS = ["internet_pct", "dist_capital_km", "acc_km", "log_ntl"]   # proxies de observabilidad


def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def wls_fe(y, X, ent, w=None, labels=None):
    """WLS con FE de estado y errores HC1; devuelve dict beta/se/t para labels."""
    E = pd.get_dummies(ent, drop_first=True).astype(float).values
    M = np.column_stack([np.ones(len(y)), X, E])
    sw = np.sqrt(w) if w is not None else np.ones(len(y))
    Mw, yw = M * sw[:, None], y * sw
    b, *_ = np.linalg.lstsq(Mw, yw, rcond=None)
    u = yw - Mw @ b
    XtXi = np.linalg.pinv(Mw.T @ Mw)
    V = XtXi @ (Mw.T * u**2) @ Mw @ XtXi * len(y) / (len(y) - M.shape[1])
    se = np.sqrt(np.diag(V))
    k = X.shape[1]
    return {labels[i]: (float(b[1 + i]), float(se[1 + i]), float(b[1 + i] / se[1 + i]))
            for i in range(k)}


def main():
    G = norm(pd.read_parquet(os.path.join(PROC, "vistaG_crimen_municipal.parquet")))
    cov = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))
    F = norm(pd.read_parquet(os.path.join(PROC, "vistaF_satelital.parquet"))).drop(columns=["pob_tot"])
    zc = norm(pd.read_csv(os.path.join(OUT, "zscores_canonicos_rung3.csv")))
    oof = norm(pd.read_parquet(os.path.join(OUT, "satelital_oof.parquet")))
    oof = oof.query("outcome=='rung1' and modelo=='M3_lentes' and factor=='material'")
    hom = norm(pd.read_parquet(os.path.join(PROC, "homicidios_mun_2019_2021.parquet")))
    d = (cov.drop(columns=["pob_tot"]).merge(G, on="cvegeo").merge(F, on="cvegeo")
            .merge(zc, on="cvegeo")
            .merge(oof.assign(brecha=oof.z_obs - oof.z_pred)[["cvegeo", "brecha"]], on="cvegeo")
            .merge(hom[["cvegeo", "hom_3a"]], on="cvegeo"))
    assert len(d) >= 2450, d.shape
    d["ent"] = d["cvegeo"].str[:2]
    rg = d.hom_3a.sum() / (d.pob_conapo.sum() * 3)
    d["log_hom_eb"] = np.log((d.hom_3a + rg * 20000) / (d.pob_conapo * 3 + 20000) * 1e5)
    d["remesas_pc_usd"] = np.log1p(d["remesas_pc_usd"])
    Xfull = d[XCOLS + OBS].copy()
    Xfull = ((Xfull - Xfull.mean()) / Xfull.std()).values

    W = "reciente_1518"
    exp_cols = [f"P_{W}", f"C_{W}", f"WC_{W}"]
    EXP = d[exp_cols].fillna(0).values.astype(float)
    rows = []
    # ---- G1: ejes canónicos ----
    for ej in ["eje1", "eje2", "eje3"]:
        y = d[f"{ej}_mean"].values
        w = 1 / np.maximum(d[f"{ej}_sd"].values, 1e-3) ** 2
        res = wls_fe(y, np.column_stack([EXP, Xfull]), d.ent, w,
                     labels=["P", "C", "WC"] + XCOLS + OBS)
        for k in ["P", "C", "WC"]:
            b, se, t = res[k]
            rows.append(dict(linea="G1", outcome=ej, ventana=W, var=k,
                             beta=round(b, 3), se=round(se, 3), t=round(t, 1)))
        print(f"G1 {ej}: P {res['P'][0]:+.3f} (t{res['P'][2]:+.1f}) | "
              f"C {res['C'][0]:+.3f} (t{res['C'][2]:+.1f}) | WC {res['WC'][0]:+.3f} (t{res['WC'][2]:+.1f})")
    # ---- G2: brecha de apropiación ----
    res = wls_fe(d.brecha.values, np.column_stack([EXP, Xfull]), d.ent,
                 labels=["P", "C", "WC"] + XCOLS + OBS)
    for k in ["P", "C", "WC"]:
        b, se, t = res[k]
        rows.append(dict(linea="G2", outcome="brecha_apropiacion", ventana=W, var=k,
                         beta=round(b, 3), se=round(se, 3), t=round(t, 1)))
    print(f"G2 brecha: P {res['P'][0]:+.3f} (t{res['P'][2]:+.1f}) | C {res['C'][0]:+.3f} "
          f"(t{res['C'][2]:+.1f}) | WC {res['WC'][0]:+.3f} (t{res['WC'][2]:+.1f})")
    # ---- G4: homicidios — presencia sola vs presencia+competencia ----
    r1 = wls_fe(d.log_hom_eb.values, np.column_stack([d[[f"P_{W}"]].values, Xfull]), d.ent,
                labels=["P"] + XCOLS + OBS)
    r2 = wls_fe(d.log_hom_eb.values, np.column_stack([EXP, Xfull]), d.ent,
                labels=["P", "C", "WC"] + XCOLS + OBS)
    rows.append(dict(linea="G4", outcome="log_hom_eb", ventana=W, var="P_solo",
                     beta=round(r1["P"][0], 3), se=round(r1["P"][1], 3), t=round(r1["P"][2], 1)))
    for k in ["P", "C", "WC"]:
        b, se, t = r2[k]
        rows.append(dict(linea="G4", outcome="log_hom_eb", ventana=W, var=k,
                         beta=round(b, 3), se=round(se, 3), t=round(t, 1)))
    print(f"G4 homicidio: P solo {r1['P'][0]:+.3f} (t{r1['P'][2]:+.1f}) || con C: "
          f"P {r2['P'][0]:+.3f} (t{r2['P'][2]:+.1f}), C {r2['C'][0]:+.3f} (t{r2['C'][2]:+.1f})")
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "g_modelos_principales.csv"), index=False)

    # ---- robustez ----
    rob = []
    metros = d.pob_conapo.rank(ascending=False) <= 5
    escenarios = {
        "ventana_calderon": dict(W="calderon_0611", mask=None, X=Xfull),
        "ventana_2018": dict(W="w2018", mask=None, X=Xfull),
        "sin_proxies_cobertura": dict(W=W, mask=None,
                                      X=((d[XCOLS] - d[XCOLS].mean()) / d[XCOLS].std()).values),
        "sin_5_metropolis": dict(W=W, mask=~metros.values, X=Xfull),
    }
    for esc, cfg in escenarios.items():
        Wv = cfg["W"]; Xv = cfg["X"]; mk = cfg["mask"]
        E2 = d[[f"P_{Wv}", f"C_{Wv}", f"WC_{Wv}"]].fillna(0).values.astype(float)
        for ej, yv, wv in [("eje1", d.eje1_mean.values, 1/np.maximum(d.eje1_sd.values, 1e-3)**2),
                           ("brecha", d.brecha.values, None),
                           ("log_hom_eb", d.log_hom_eb.values, None)]:
            if mk is not None:
                y2, X2, E3, ent2 = yv[mk], Xv[mk], E2[mk], d.ent[mk]
                w2 = wv[mk] if wv is not None else None
            else:
                y2, X2, E3, ent2, w2 = yv, Xv, E2, d.ent, wv
            r = wls_fe(y2, np.column_stack([E3, X2]), ent2, w2,
                       labels=["P", "C", "WC"] + ["x"] * (X2.shape[1]))
            rob.append(dict(escenario=esc, outcome=ej,
                            beta_P=round(r["P"][0], 3), t_P=round(r["P"][2], 1),
                            beta_C=round(r["C"][0], 3), t_C=round(r["C"][2], 1)))
    RB = pd.DataFrame(rob); RB.to_csv(os.path.join(OUT, "g_robustez.csv"), index=False)
    print("\nRobustez (β_C vs β_P):")
    print(RB.to_string(index=False))
    # N=1 vs N>=2 (steer 7.6) — persistido a CSV (F3 de la revisión del paper 2:
    # el número titular no puede vivir solo en stdout)
    mc = []
    for Wv in (W, "calderon_0611", "w2018"):
        n1 = (d[f"N_orgs_{Wv}"] == 1).astype(float)
        n2p = (d[f"N_orgs_{Wv}"] >= 2).astype(float)
        r = wls_fe(d.log_hom_eb.values, np.column_stack([n1.values, n2p.values, Xfull]),
                   d.ent, labels=["N1", "N2plus"] + XCOLS + OBS)
        for k, nom in [("N1", "monopolio_N1"), ("N2plus", "competencia_N2plus")]:
            b, se, t = r[k]
            mc.append(dict(ventana=Wv, var=nom, beta=round(b, 3), se=round(se, 3),
                           t=round(t, 1)))
    MC = pd.DataFrame(mc)
    MC.to_csv(os.path.join(OUT, "g_monopolio_competencia.csv"), index=False)
    p = MC[MC.ventana == W].set_index("var")
    print(f"\n7.6 homicidio: monopolio N=1 {p.loc['monopolio_N1', 'beta']:+.3f} "
          f"(t{p.loc['monopolio_N1', 't']:+.1f}) vs competencia N≥2 "
          f"{p.loc['competencia_N2plus', 'beta']:+.3f} (t{p.loc['competencia_N2plus', 't']:+.1f})"
          f" | g_monopolio_competencia.csv")


if __name__ == "__main__":
    main()
