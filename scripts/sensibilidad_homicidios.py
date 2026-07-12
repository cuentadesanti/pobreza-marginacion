#!/usr/bin/env python
"""
Sensibilidad de la validación con homicidios (frente 4 del cierre):
  (a) municipio de RESIDENCIA vs ocurrencia (2019-2021)
  (b) ventana 2018-2022 (ocurrencia)
  (c) tasa suavizada empírica-Bayes para municipios chicos: (hom + r*m)/(exp + m), m=20k hab-año

Para cada variante, re-corre la comparación de conjuntos predictores (ridge, 5-fold CV):
17 indicadores / z bruto / Vista D / z condicional + discordancia / todo.
Queda cerrado si el orden "17 ≥ VistaD > z1 >> residual" se sostiene en todas.

Salida: outputs/sensibilidad_homicidios.csv
"""
import os, sys
import numpy as np, pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import KFold, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, OUT = os.path.join(HERE, "data", "processed"), os.path.join(HERE, "outputs")
SCRATCH = sys.argv[1] if len(sys.argv) > 1 else "."
DCOLS = ["dep_ratio", "pct_60mas", "pct_primario", "pct_secundario",
         "empleo_precario_pct", "remesas_pc_usd", "loc_peq_pct", "log_pob"]


def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def icd_homicidio(c):
    c = str(c).upper()
    return (c[:1] == "X" and c[1:3].isdigit() and 85 <= int(c[1:3]) <= 99) or \
           (c[:1] == "Y" and c[1:3].isdigit() and 0 <= int(c[1:3]) <= 9)


def conteo(anio, base="OCURR"):
    # CAUSA_DEF (ICD X85-Y09) es uniforme entre esquemas; PRESUNTO desaparece en 2022
    df = pd.read_csv(os.path.join(SCRATCH, f"defunciones_{anio}.csv"),
                     usecols=[f"ENT_{base}", f"MUN_{base}", "CAUSA_DEF", "ANIO_OCUR"],
                     dtype=str, low_memory=False)
    df = df[(df["ANIO_OCUR"].astype(int) == anio) & df["CAUSA_DEF"].map(icd_homicidio)]
    df = df[df[f"MUN_{base}"].astype(int) < 900]
    cv = df[f"ENT_{base}"].str.zfill(2) + df[f"MUN_{base}"].str.zfill(3)
    return cv.value_counts()


def tasa(anios, base="OCURR", suavizada=False, m=20000.0):
    pob = norm(pd.read_parquet(os.path.join(PROC, "municipal_components_2020.parquet"),
                               columns=["cvegeo", "pob_conapo"])).set_index("cvegeo")["pob_conapo"]
    from functools import reduce
    h = reduce(lambda a, b: a.add(b, fill_value=0),
               (conteo(a, base) for a in anios)).reindex(pob.index).fillna(0)
    exp = pob * len(anios)
    if suavizada:
        r_glob = h.sum() / exp.sum()
        return (h + r_glob * m) / (exp + m) * 1e5
    return h / exp * 1e5


def r2_sets(y, d, mask=None):
    cvk = KFold(5, shuffle=True, random_state=1)
    res, folds = {}, {}
    for name, X in d.items():
        Xu, yu = (X[mask], y[mask]) if mask is not None else (X, y)
        pipe = make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-2, 3, 20)))
        sc = cross_val_score(pipe, Xu, yu, cv=cvk, scoring="r2")
        res[name] = float(np.mean(sc)); folds[name] = sc
    # estabilidad de la diferencia clave por fold (criterio pre-registrado)
    dif = folds["17_indicadores"] - folds["z_resid_r3+disc"]
    res["_dif17_resid"] = float(np.mean(dif))
    res["_dif_signo_estable"] = bool(np.all(dif > 0))
    return res


def main():
    cov = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))
    Y17 = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet")); Y17.index = cov["cvegeo"].values
    z1 = norm(pd.read_csv(os.path.join(OUT, "zscores_rung1_K3.csv")))
    diag = norm(pd.read_parquet(os.path.join(PROC, "diagnostico_municipal_v1.parquet")))
    base = cov.merge(z1, on="cvegeo", suffixes=("", "_r1")).merge(
        diag[["cvegeo", "material_mean", "educativo_mean", "monetario_mean", "discordancia_obs"]],
        on="cvegeo", suffixes=("_r1", "_r3"))
    sets = {
        "17_indicadores": Y17.loc[base.cvegeo].values,
        "z_bruto_r1": base[["material_mean_r1", "educativo_mean_r1", "monetario_mean_r1"]].values,
        "vistaD": base[DCOLS].values,
        "z_resid_r3+disc": base[["material_mean_r3", "educativo_mean_r3", "monetario_mean_r3",
                                 "discordancia_obs"]].values,
        "vistaD+z3+disc": np.hstack([base[DCOLS].values,
                                     base[["material_mean_r3", "educativo_mean_r3",
                                           "monetario_mean_r3", "discordancia_obs"]].values]),
    }
    variantes = {
        "ocurr_2019_21 (original)": tasa([2019, 2020, 2021], "OCURR"),
        "resid_2019_21": tasa([2019, 2020, 2021], "RESID"),
        "ocurr_2018_22": tasa([2018, 2019, 2020, 2021, 2022], "OCURR"),
        "ocurr_suavizada_m10k": tasa([2019, 2020, 2021], "OCURR", suavizada=True, m=10000),
        "ocurr_suavizada_m20k": tasa([2019, 2020, 2021], "OCURR", suavizada=True, m=20000),
        "ocurr_suavizada_m50k": tasa([2019, 2020, 2021], "OCURR", suavizada=True, m=50000),
    }
    pob = base.merge(norm(pd.read_parquet(os.path.join(PROC, "municipal_components_2020.parquet"),
                                          columns=["cvegeo", "pob_conapo"])), on="cvegeo")["pob_conapo"]
    sin_metro = (pob.rank(ascending=False) > 5).values   # excluye las 5 mayores
    rows = []
    for vn, t in variantes.items():
        y = np.log1p(t.reindex(base.cvegeo).values)
        res = r2_sets(y, sets)
        rows.append(dict(variante=vn, **{k: (round(v, 3) if not isinstance(v, bool) else v)
                                         for k, v in res.items()}))
        print(vn, {k: (round(v, 3) if not isinstance(v, bool) else v) for k, v in res.items()})
    res = r2_sets(np.log1p(variantes["ocurr_2019_21 (original)"].reindex(base.cvegeo).values),
                  sets, mask=sin_metro)
    rows.append(dict(variante="ocurr_2019_21_sin_5_metros",
                     **{k: (round(v, 3) if not isinstance(v, bool) else v) for k, v in res.items()}))
    print("ocurr_2019_21_sin_5_metros", {k: (round(v, 3) if not isinstance(v, bool) else v)
                                         for k, v in res.items()})
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "sensibilidad_homicidios.csv"), index=False)


if __name__ == "__main__":
    main()
