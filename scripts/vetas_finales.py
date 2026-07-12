#!/usr/bin/env python
"""
Vetas 2-4 antes de congelar el manuscrito.

V2 — La geografía de la ignorancia: ¿qué predice la INCERTIDUMBRE posterior municipal
     (sd de los ejes canónicos)? Correlatos: tamaño, ruralidad, discordancia, violencia,
     exposición criminal. ¿La violencia ensucia la medición?
V3 — Estructura de los efectos estatales: PCA de la matriz gamma (17x32). ¿Hay un factor
     común de 'capacidad estatal' o son idiosincráticos por indicador?
V4 — Los 48 triple-severos: caracterización con nombre (región, tamaño, LISA, crimen,
     remesas) del 2% que acumula severidad en los tres ejes residuales.

Salidas: outputs/veta_ignorancia.csv, outputs/veta_gamma_pca.csv, outputs/veta_48_triple.csv
"""
import os
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, OUT = os.path.join(HERE, "data", "processed"), os.path.join(HERE, "outputs")
EJES = ["eje1", "eje2", "eje3"]


def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def main():
    d = norm(pd.read_parquet(os.path.join(PROC, "diagnostico_municipal_v1.parquet")))
    G = norm(pd.read_parquet(os.path.join(PROC, "vistaG_crimen_municipal.parquet")))
    hom = norm(pd.read_parquet(os.path.join(PROC, "homicidios_mun_2019_2021.parquet")))
    d = d.merge(G[["cvegeo", "P_reciente_1518", "C_reciente_1518", "V_reciente_1518",
                   "tasa_eb_reciente_1518"]], on="cvegeo") \
         .merge(hom[["cvegeo", "tasa_100k"]], on="cvegeo")
    d["log_pob"] = np.log10(d["pob_conapo"])
    d["log_hom"] = np.log1p(d["tasa_100k"])

    # ---------- V2: geografía de la ignorancia ----------
    print("V2 — ¿qué correlaciona con la INCERTIDUMBRE municipal (sd posterior)?")
    correlatos = ["log_pob", "loc_peq_pct", "discordancia_obs", "log_hom",
                  "tasa_eb_reciente_1518", "remesas_pc_usd"]
    rows = []
    for e in EJES:
        r = {c: float(np.corrcoef(d[f"{e}_sd"], d[c])[0, 1]) for c in correlatos}
        r_abs = {f"abs_{c}": float(np.corrcoef(d[f"{e}_sd"], d[c].abs())[0, 1])
                 for c in ["discordancia_obs"]}
        rows.append(dict(eje=e, **{k: round(v, 3) for k, v in {**r, **r_abs}.items()}))
        print(f"  {e}_sd:", {k: round(v, 2) for k, v in r.items()})
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "veta_ignorancia.csv"), index=False)

    # ---------- V3: estructura de gamma ----------
    gam = pd.read_csv(os.path.join(OUT, "gamma_marginal_rung3.csv"), index_col=0)  # 17 x 32
    Gm = gam.values - gam.values.mean(axis=1, keepdims=True)
    U, S, Vt = np.linalg.svd(Gm, full_matrices=False)
    share = S**2 / (S**2).sum()
    print(f"\nV3 — PCA de gamma (17x32): shares de varianza {np.round(share[:4], 3)}")
    pc1_ind = pd.Series(U[:, 0], index=gam.index).sort_values()
    print("  PC1 por indicador (¿capacidad estatal común?):")
    print("   más negativo:", pc1_ind.head(3).round(2).to_dict(),
          "| más positivo:", pc1_ind.tail(3).round(2).to_dict())
    est = pd.read_csv(os.path.join(PROC, "estatales_2020.csv"), dtype={"cve_ent": str})
    pc1_est = pd.Series(Vt[0, :] * S[0], index=gam.columns)
    cov = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))
    ents = sorted(cov.cvegeo.str[:2].unique())
    pe = pd.DataFrame({"cve_ent": ents, "pc1_gamma": pc1_est.values})
    pe = pe.merge(est[["cve_ent", "pibe_pc_mxn", "gasto_pibe_pct"]], on="cve_ent")
    for c in ["pibe_pc_mxn", "gasto_pibe_pct"]:
        m = pe.dropna(subset=[c])
        print(f"  corr(PC1_estatal, {c}) = {np.corrcoef(m.pc1_gamma, np.log10(m[c]) if c=='pibe_pc_mxn' else m[c])[0,1]:+.3f}")
    pd.DataFrame({"indicador": gam.index, "pc1": U[:, 0], "pc2": U[:, 1]}).round(3).to_csv(
        os.path.join(OUT, "veta_gamma_pca.csv"), index=False)

    # ---------- V4: los 48 triple-severos ----------
    for e in EJES:
        d[f"sev_{e}"] = (d[f"{e}_mean"] > d[f"{e}_mean"].quantile(0.75)).astype(int)
    d["acum"] = d[[f"sev_{e}" for e in EJES]].sum(axis=1)
    t3 = d[d.acum == 3].copy()
    print(f"\nV4 — triple-severos: {len(t3)} municipios, {t3.pob_conapo.sum():,.0f} hab")
    print("  por estado:", t3.nom_ent.value_counts().head(6).to_dict())
    print(f"  mediana pob: {t3.pob_conapo.median():,.0f} (nacional {d.pob_conapo.median():,.0f})")
    print(f"  % rural (loc_peq>80): {100*(t3.loc_peq_pct>80).mean():.0f}% (nacional {100*(d.loc_peq_pct>80).mean():.0f}%)")
    print(f"  régimen LISA: {t3.lisa.fillna('ns').value_counts().to_dict()}")
    print(f"  presencia criminal 15-18: {100*t3.P_reciente_1518.mean():.0f}% (nacional {100*d.P_reciente_1518.mean():.0f}%)")
    print(f"  remesas pc mediana: {t3.remesas_pc_usd.median():.0f} (nacional {d.remesas_pc_usd.median():.0f})")
    t3[["cvegeo", "nom_ent", "nom_mun", "pob_conapo", "eje1_mean", "eje2_mean", "eje3_mean",
        "lisa", "loc_peq_pct", "remesas_pc_usd", "P_reciente_1518"]].round(2).to_csv(
        os.path.join(OUT, "veta_48_triple.csv"), index=False)
    print("  top-8 por población:")
    print(t3.nlargest(8, "pob_conapo")[["nom_mun", "nom_ent", "pob_conapo"]].to_string(index=False))


if __name__ == "__main__":
    main()
