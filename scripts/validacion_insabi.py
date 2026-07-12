#!/usr/bin/env python
"""
Validación externa corta: ¿el efecto estatal de car_salud es la transición Seguro Popular→INSABI?

Hipótesis: el γ_s específico de car_salud (modelo marginalizado convergido) debe asociarse con
la DEPENDENCIA estatal del sistema en transición — medida como % de población afiliada a
INSABI/Seguro Popular en el propio Censo 2020 (PDER_SEGP del ITER, dato local) — mucho más que
los γ_s de indicadores placebo que no responden a esa transición (vivienda, drenaje, educación).

Signo esperado: MÁS dependencia SP/INSABI => MENOS carencia de salud medida (la afiliación
INSABI cuenta como acceso) => γ_car_salud NEGATIVO. Placebos: sin asociación clara.

Salida: outputs/validacion_insabi.csv + stdout
"""
import os, sys, glob
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT, PROC = os.path.join(HERE, "outputs"), os.path.join(HERE, "data", "processed")
SCRATCH = sys.argv[1] if len(sys.argv) > 1 else "."
PLACEBOS = ["car_vivienda", "sin_drenaje", "rezago_educ", "sin_basica", "piso_tierra"]


def main():
    it = pd.read_csv(glob.glob(os.path.join(SCRATCH, "iter/conjunto_de_datos_iter_00*.csv"))[0],
                     usecols=["ENTIDAD", "MUN", "LOC", "POBTOT", "PDER_SEGP", "PDER_SS"],
                     dtype=str)
    est = it[(it["MUN"] == "000") & (it["LOC"] == "0000") & (it["ENTIDAD"] != "00")].copy()
    for c in ["POBTOT", "PDER_SEGP", "PDER_SS"]:
        est[c] = pd.to_numeric(est[c], errors="coerce")
    est["dep_segp"] = 100 * est["PDER_SEGP"] / est["POBTOT"]      # % pob afiliada a SP/INSABI
    est = est.rename(columns={"ENTIDAD": "cve_ent"})[["cve_ent", "dep_segp"]]
    print(f"dependencia SP/INSABI estatal: media {est.dep_segp.mean():.1f}%, "
          f"rango [{est.dep_segp.min():.1f}, {est.dep_segp.max():.1f}]")

    gpath = os.path.join(OUT, "gamma_marginal_rung3.csv")
    if not os.path.exists(gpath):
        sys.exit("falta gamma_marginal_rung3.csv (re-correr gllvm_marginal --rung 3 --free)")
    gdf = pd.read_csv(gpath, index_col=0)
    gam = gdf.values
    ind = list(gdf.index)
    cov = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))
    ents = sorted(cov["cvegeo"].astype(str).str.zfill(5).str[:2].unique())
    G = pd.DataFrame(gam.T, columns=ind)
    G["cve_ent"] = ents
    d = G.merge(est, on="cve_ent")
    rows = []
    for indi in ["car_salud"] + PLACEBOS:
        r = np.corrcoef(d[indi], d["dep_segp"])[0, 1]
        rows.append(dict(indicador=indi, corr_gamma_vs_dependencia_SEGP=round(r, 3),
                         tipo=("HIPÓTESIS" if indi == "car_salud" else "placebo")))
        print(f"corr(γ_{indi}, dependencia SP/INSABI): {r:+.3f}"
              f"{'   <- hipótesis' if indi == 'car_salud' else ''}")
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "validacion_insabi.csv"), index=False)


if __name__ == "__main__":
    main()
