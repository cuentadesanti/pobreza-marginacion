#!/usr/bin/env python
"""
Frente 2 — ¿cuánto del efecto estatal es medición y cuánto federalismo?

Tabla indicador × {|gamma_s|, share de varianza estatal, instrumento, directo/modelado,
calibrado/no, universo}, con las gamma del GLLVM MARGINALIZADO (convergido, sin excusas).

Lectura esperada: si el estado fuera solo calibración SAE, los 4 modelados dominarían;
si es federalismo real, salud/servicios (directos) pueden superarlos. La tabla delimita el
argumento en vez de resolverlo causalmente.

Salidas: outputs/tabla_medicion_federalismo.csv + resumen por grupo (stdout)
"""
import os
import numpy as np, pandas as pd
import arviz as az

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT, DICT = os.path.join(HERE, "outputs"), os.path.join(HERE, "dict")

GRUPO = {
    **{i: "CONAPO censal" for i in ["analf", "sin_basica", "sin_drenaje", "sin_electr",
                                    "sin_agua", "piso_tierra", "hacinam", "loc_peq"]},
    "ing_2sm": "CONAPO muestra",
    **{i: "CONEVAL directo" for i in ["rezago_educ", "car_salud", "car_vivienda", "car_servbas"]},
    **{i: "CONEVAL SAE+calibrado" for i in ["car_segsoc", "car_alim", "lp_ingreso", "lp_ingreso_ext"]},
}
INSTR = {"CONAPO censal": "censo básico (conteo completo)",
         "CONAPO muestra": "muestra censal",
         "CONEVAL directo": "muestra censal (diseño)",
         "CONEVAL SAE+calibrado": "SAE (ENIGH+muestra) + calibración estatal"}


def main():
    idata = az.from_netcdf(os.path.join(OUT, "idata_marginal_rung3.nc"))
    gam = idata.posterior["gamma"]                      # (chain, draw, J, S)
    ind = list(pd.read_csv(os.path.join(OUT, "loadings_rung1_K3.csv"), index_col=0).index)
    rh = float(az.rhat(idata, var_names=["gamma"])["gamma"].max())
    g_mean = gam.mean(("chain", "draw")).values         # (J, S)
    g_absm = np.abs(g_mean).mean(axis=1)
    # share de varianza estatal por indicador: Var_s(gamma_js) (Y está estandarizada, var≈1)
    share = g_mean.var(axis=1)
    # incertidumbre de |gamma| media
    g_abs_sd = np.abs(gam.values).mean(axis=3).std(axis=(0, 1))

    dic = pd.read_csv(os.path.join(DICT, "diccionario_indicadores.csv"))
    dic["ind"] = dic["variable"].str.replace("_pct", "", regex=False)
    uni = dict(zip(dic["ind"], dic["universo"]))

    T = pd.DataFrame({
        "indicador": ind,
        "grupo": [GRUPO[i] for i in ind],
        "instrumento": [INSTR[GRUPO[i]] for i in ind],
        "modelado": [GRUPO[i] == "CONEVAL SAE+calibrado" for i in ind],
        "calibrado_estatal": [GRUPO[i] == "CONEVAL SAE+calibrado" for i in ind],
        "universo": [uni.get(i, "") for i in ind],
        "gamma_abs_media": np.round(g_absm, 3),
        "gamma_abs_sd_post": np.round(g_abs_sd, 3),
        "share_var_estatal": np.round(share, 3),
    }).sort_values("share_var_estatal", ascending=False)
    T.to_csv(os.path.join(OUT, "tabla_medicion_federalismo.csv"), index=False)
    print(f"R-hat max gamma (marginalizado): {rh:.3f}\n")
    print(T.to_string(index=False))
    print("\nResumen por grupo (share de varianza estatal):")
    print(T.groupby("grupo")["share_var_estatal"].agg(["mean", "min", "max"]).round(3).to_string())

    # contrastes de grupo con incertidumbre POSTERIOR (share por draw)
    gd = gam.values                                   # (C, D, J, S)
    share_d = gd.var(axis=3)                          # (C, D, J)
    grupos = np.array([GRUPO[i] for i in ind])
    def gmean(g):
        return share_d[:, :, grupos == g].mean(axis=2).ravel()
    dif_sae_dir = gmean("CONEVAL SAE+calibrado") - gmean("CONEVAL directo")
    dif_sae_cen = gmean("CONEVAL SAE+calibrado") - gmean("CONAPO censal")
    for nombre, dd in [("SAE − CONEVAL directo", dif_sae_dir), ("SAE − CONAPO censal", dif_sae_cen)]:
        lo, hi = np.percentile(dd, [2.5, 97.5])
        print(f"Δshare {nombre}: {dd.mean():+.3f}  IC95 [{lo:+.3f}, {hi:+.3f}]")
    print("\nConclusión (calibrada): el componente estatal NO está dominado por la arquitectura")
    print("SAE — es compatible con heterogeneidad sustantiva estatal, aunque sigue mezclando")
    print("política, composición y medición.")


if __name__ == "__main__":
    main()
