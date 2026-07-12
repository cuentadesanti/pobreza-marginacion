#!/usr/bin/env python
"""
Producto municipal v1: diagnóstico de privación con incertidumbre.

Une, por CVEGEO (2,455 municipios del GLLVM):
  - scores latentes del peldaño 3 (media ± sd por factor; condicionales a composición+estado)
  - discordancia observable: media logit-z de indicadores CONAPO menos media CONEVAL
    (la materia prima de los regímenes LISA) y la clase LISA
  - Vista D (ruralidad, remesas pc) y Vista E (dependencia de transferencias)

Salida:
  data/processed/diagnostico_municipal_v1.parquet
  outputs/top_discordantes.csv  (los 25 municipios con mayor privación latente residual
                                 por factor, con su incertidumbre — "dónde las mediciones
                                 oficiales se quedan cortas y con cuánta certeza")
"""
import os
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
OUT = os.path.join(HERE, "outputs")

CONAPO = ["analf", "sin_basica", "sin_drenaje", "sin_electr", "sin_agua",
          "piso_tierra", "hacinam", "loc_peq", "ing_2sm"]
CONEVAL = ["rezago_educ", "car_salud", "car_segsoc", "car_vivienda", "car_servbas",
           "car_alim", "lp_ingreso", "lp_ingreso_ext"]


def main():
    z = pd.read_csv(os.path.join(OUT, "zscores_rung3_K3.csv"), dtype={"cvegeo": str})
    Y = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet"))
    comp = pd.read_parquet(os.path.join(PROC, "municipal_components_2020.parquet"),
                           columns=["cvegeo", "nom_ent", "nom_mun", "pob_conapo"])
    cov = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))[
        ["cvegeo", "loc_peq_pct", "remesas_pc_usd", "log_pob"]]
    lisa = pd.read_parquet(os.path.join(PROC, "lisa_classes.parquet"))
    fin = pd.read_parquet(os.path.join(PROC, "finanzas_mun_2020.parquet"))[
        ["cvegeo", "dep_transferencias_pct", "autonomia_fiscal_pct"]]

    d = z.merge(comp, on="cvegeo").merge(cov, on="cvegeo")
    # discordancia observable (misma dirección que los regímenes LISA: >0 = más marginado que pobre)
    d["discordancia_obs"] = Y[CONAPO].mean(axis=1).values - Y[CONEVAL].mean(axis=1).values
    d = d.merge(lisa[["cvegeo", "lisa"]], on="cvegeo", how="left").merge(fin, on="cvegeo", how="left")

    # señal/ruido por factor: |media|/sd — qué tan seguro es que el municipio se desvía
    for f in ["material", "educativo", "monetario"]:
        d[f"{f}_snr"] = d[f"{f}_mean"].abs() / d[f"{f}_sd"]
    d.to_parquet(os.path.join(PROC, "diagnostico_municipal_v1.parquet"), index=False)
    print("diagnostico_municipal_v1.parquet:", d.shape)

    # top discordantes CON certeza (snr>2) por factor
    rows = []
    for f in ["material", "educativo", "monetario"]:
        top = d[d[f"{f}_snr"] > 2].nlargest(25, f"{f}_mean")
        for _, r in top.iterrows():
            rows.append({"factor": f, "cvegeo": r["cvegeo"], "municipio": r["nom_mun"],
                         "estado": r["nom_ent"], "z": round(r[f"{f}_mean"], 2),
                         "sd": round(r[f"{f}_sd"], 2), "pob": int(r["pob_conapo"]),
                         "discordancia_obs": round(r["discordancia_obs"], 2),
                         "lisa": r["lisa"]})
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "top_discordantes.csv"), index=False)
    print("top_discordantes.csv:", len(rows), "filas")
    print("\nEjemplo — top 8 material:")
    print(pd.DataFrame(rows).query("factor=='material'").head(8).to_string(index=False))


if __name__ == "__main__":
    main()
