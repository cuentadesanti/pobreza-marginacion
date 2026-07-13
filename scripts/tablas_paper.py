#!/usr/bin/env python
"""
Capa C3 — CSVs fuente de las tablas centrales de los papers (ensamblaje, no cómputo nuevo).

Todo se RE-LEE de artefactos existentes:
  tabla1_escalera.csv     ladder_summary_K3.csv (escalera con z muestreada, no converge) +
                          diagnósticos recomputados de idata_marginal_rung{2,3}.nc
                          (az.rhat sobre LamLamT, az.loo) — nada copiado de memoria.
  desacuerdo_familias.csv mload posterior por familia (idata p2 y p3) + agregados municipales
                          de desacuerdo_agencias.csv (% sustantivo, medias por régimen LISA).
  tabla3_gamma.csv        SVD de gamma_marginal_rung3.csv (share PC1/PC2) + correlación del
                          score estatal PC1 con log PIBE pc (gamma_estados_decomposicion.csv).

Los papers citan estas tablas; scripts/check_captions.py verifica la sincronía.
"""
import os
import numpy as np, pandas as pd
import arviz as az

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")
FAMILIAS = ["educacion", "lineas_sae", "viv_servicios"]   # orden del dict CONTRASTES


def main():
    # ---------- tabla 1: escalera + secuencia marginal ----------
    lad = pd.read_csv(os.path.join(OUT, "ladder_summary_K3.csv"))
    rows = []
    for _, r in lad.iterrows():
        rows.append(dict(bloque="escalera_z_muestreada", modelo=f"peldaño {int(r.rung)}",
                         moran_resid=round(r.residual_moran_I, 3),
                         rhat=round(r.rhat_alpha_sigma, 2), elpd=round(r.elpd_loo, 1),
                         converge="no (multimodal)"))
    for rung, etiqueta in [(2, "marginalizado sin γ_s (p2)"), (3, "marginalizado con γ_s (p3, canónico)")]:
        idata = az.from_netcdf(os.path.join(OUT, f"idata_marginal_rung{rung}.nc"))
        rhat = float(np.nanmax(az.rhat(idata, var_names=["LamLamT"]).LamLamT.values))
        elpd = float(az.loo(idata).elpd_loo)
        rows.append(dict(bloque="marginalizado_MvN", modelo=etiqueta, moran_resid=np.nan,
                         rhat=round(rhat, 3), elpd=round(elpd, 1),
                         converge="sí" if rhat < 1.01 else "no (multimodal)"))
    t1 = pd.DataFrame(rows)
    t1.to_csv(os.path.join(OUT, "tabla1_escalera.csv"), index=False)
    print("tabla1_escalera.csv"); print(t1.to_string(index=False))

    # ---------- tabla 2: desacuerdo por familia ----------
    m2 = az.from_netcdf(os.path.join(OUT, "idata_marginal_rung2.nc")).posterior["mload"]
    m3 = az.from_netcdf(os.path.join(OUT, "idata_marginal_rung3.nc")).posterior["mload"]
    ml2 = m2.mean(("chain", "draw")).values
    ml3 = m3.mean(("chain", "draw")).values
    des = pd.read_csv(os.path.join(OUT, "desacuerdo_agencias.csv"), dtype={"cvegeo": str})
    rows = []
    for i, fam in enumerate(FAMILIAS):
        col = f"m_{fam}"
        sust = 100 * float((des[col].abs() / des[f"{col}_sd"] >= 2).mean())
        lisa_m = des.groupby(des.lisa.fillna("ns"))[col].mean()
        rows.append(dict(familia=fam, mload_p2=round(float(ml2[i]), 3),
                         mload_p3=round(float(ml3[i]), 3),
                         pct_sustantivo=round(sust, 1),
                         media_AA=round(float(lisa_m.get("AA", np.nan)), 3),
                         media_BB=round(float(lisa_m.get("BB", np.nan)), 3)))
    t2 = pd.DataFrame(rows)
    t2.to_csv(os.path.join(OUT, "desacuerdo_familias.csv"), index=False)
    print("\ndesacuerdo_familias.csv"); print(t2.to_string(index=False))

    # ---------- tabla 3: descomposición de gamma ----------
    gam = pd.read_csv(os.path.join(OUT, "gamma_marginal_rung3.csv"), index_col=0)   # 17 x 32
    Gm = gam.values - gam.values.mean(axis=1, keepdims=True)
    U, S, Vt = np.linalg.svd(Gm, full_matrices=False)
    share = S ** 2 / (S ** 2).sum()
    est = pd.read_csv(os.path.join(OUT, "gamma_estados_decomposicion.csv"),
                      dtype={"cve_ent": str})
    est["cve_ent"] = est.cve_ent.str.zfill(2)
    # las columnas de gamma son POSICIONALES ('0'..'31'): mapear al orden de estados del
    # modelo (claves ent ordenadas de gllvm_covars), como en vetas_finales.py — un zfill
    # directo desalinearía todo un estado
    cov = pd.read_parquet(os.path.join(HERE, "data", "processed", "gllvm_covars.parquet"))
    ents = sorted(cov.cvegeo.astype(str).str.zfill(5).str[:2].unique())
    assert len(ents) == gam.shape[1]
    pc1_est = pd.Series(Vt[0, :] * S[0], index=ents, name="pc1")
    m = est.merge(pc1_est.rename_axis("cve_ent").reset_index(), on="cve_ent").dropna(
        subset=["pibe_pc_mxn"])
    corr_pibe = float(np.corrcoef(m.pc1, np.log10(m.pibe_pc_mxn))[0, 1])
    corr_gasto = float(np.corrcoef(m.dropna(subset=["gasto_pibe_pct"]).pc1,
                                   m.dropna(subset=["gasto_pibe_pct"]).gasto_pibe_pct)[0, 1])
    pc1_ind = pd.read_csv(os.path.join(OUT, "veta_gamma_pca.csv"))
    t3 = pd.DataFrame([
        dict(medida="share_varianza_PC1_pct", valor=round(100 * float(share[0]), 1)),
        dict(medida="share_varianza_PC2_pct", valor=round(100 * float(share[1]), 1)),
        dict(medida="share_sectorial_pct", valor=round(100 * float(1 - share[0]), 1)),
        dict(medida="corr_PC1_log_pibe_pc", valor=round(corr_pibe, 2)),
        dict(medida="corr_PC1_gasto_pibe_pct", valor=round(corr_gasto, 2)),
    ])
    t3.to_csv(os.path.join(OUT, "tabla3_gamma.csv"), index=False)
    print("\ntabla3_gamma.csv"); print(t3.to_string(index=False))
    print("\nPC1 por indicador (extremos):",
          pc1_ind.nsmallest(3, "pc1")[["indicador", "pc1"]].values.tolist(),
          pc1_ind.nlargest(3, "pc1")[["indicador", "pc1"]].values.tolist())


if __name__ == "__main__":
    main()
