#!/usr/bin/env python
"""
Robustez del giro a desigualdad (revisión):
  A. Sensibilidad de la partición entre/dentro a la ponderación: población vs municipio
     equiponderado vs excluyendo municipios <1,000 hab.
  C. Acumulación: razón observado/esperado con bootstrap, tabla completa de intersecciones,
     Jaccard entre conjuntos de alta privación, umbrales 70/75/80/90.
  Capa 3: R² INCREMENTAL de circunstancias (geografía -> +demografía -> +estructura
     económica -> +estado) — 'estado' separado porque no es circunstancia elemental.

Salidas: outputs/desigualdad_robustez.csv (+ stdout con las piezas)
"""
import os
import numpy as np, pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GroupKFold, KFold
from sklearn.metrics import r2_score

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC, OUT = os.path.join(HERE, "data", "processed"), os.path.join(HERE, "outputs")
EJES = ["eje1", "eje2", "eje3"]


def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def var_decomp(z, w, g):
    w = w / w.sum(); mu = np.sum(w * z)
    vt = np.sum(w * (z - mu) ** 2); vb = 0.0
    for gr in np.unique(g):
        k = g == gr
        vb += w[k].sum() * (np.sum(w[k] * z[k]) / w[k].sum() - mu) ** 2
    return 100 * vb / max(vt, 1e-12)


def theil_pct_entre(x, w, g):
    x = np.maximum(x, 1e-9); w = w / w.sum(); mu = np.sum(w * x)
    T = np.sum(w * (x / mu) * np.log(x / mu)); tb = 0.0
    for gr in np.unique(g):
        k = g == gr
        Wg, mug = w[k].sum(), np.sum(w[k] * x[k]) / w[k].sum()
        tb += Wg * (mug / mu) * np.log(mug / mu)
    return 100 * tb / max(T, 1e-12)


def main():
    comp = norm(pd.read_parquet(os.path.join(PROC, "municipal_components_2020.parquet")))
    zc = norm(pd.read_csv(os.path.join(OUT, "zscores_canonicos_rung3.csv")))
    z1 = norm(pd.read_csv(os.path.join(OUT, "zscores_rung1_K3.csv")))
    cov = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))
    F = norm(pd.read_parquet(os.path.join(PROC, "vistaF_satelital.parquet"))).drop(columns=["pob_tot"])
    d = comp.merge(zc, on="cvegeo").merge(cov.drop(columns=["pob_tot"]), on="cvegeo",
                                          suffixes=("", "_c")).merge(F, on="cvegeo") \
            .merge(z1[["cvegeo", "material_mean"]].rename(columns={"material_mean": "z1_material"}),
                   on="cvegeo") \
            .merge(norm(pd.read_parquet(os.path.join(PROC, "vistaD_indigena.parquet"))),
                   on="cvegeo")
    assert len(d) >= 2450, f"merge perdió municipios: {len(d)}"
    d["ent"] = d["cvegeo"].str[:2]
    g = d["ent"].values
    rows = []

    # ---------- A. sensibilidad de ponderación ----------
    esquemas = {"pob": d.pob_conapo.values.astype(float),
                "municipio_equiponderado": np.ones(len(d)),
                "pob_sin_menores_1000": np.where(d.pob_conapo >= 1000, d.pob_conapo, 0.0)}
    print("A. % entre estados según esquema de ponderación:")
    for nombre, w in esquemas.items():
        vals = {"z1_material": var_decomp(d.z1_material.values, w, g),
                "eje1": var_decomp(d.eje1_mean.values, w, g),
                "lp_ingreso_pct": theil_pct_entre(d.lp_ingreso_pct.values, w, g),
                "sin_agua_pct": theil_pct_entre(d.sin_agua_pct.values, w, g)}
        print(f"  {nombre}: " + " | ".join(f"{k} {v:.1f}%" for k, v in vals.items()))
        for k, v in vals.items():
            rows.append(dict(bloque="A_ponderacion", esquema=nombre, medida=k, valor=round(v, 1)))

    # ---------- C. acumulación: razón, bootstrap, intersecciones, Jaccard, umbrales ----------
    print("\nC. Acumulación por umbral (razón observado/esperado de 3 severas):")
    rng = np.random.default_rng(1)
    for q in (0.70, 0.75, 0.80, 0.90):
        S = np.column_stack([(d[f"{e}_mean"] > d[f"{e}_mean"].quantile(q)).values for e in EJES])
        p = 1 - q
        obs3 = S.all(axis=1).mean(); esp3 = p ** 3
        boots = []
        for _ in range(1000):
            i = rng.integers(0, len(d), len(d))
            boots.append(S[i].all(axis=1).mean() / esp3)
        lo, hi = np.percentile(boots, [2.5, 97.5])
        jac = {}
        for a in range(3):
            for b in range(a + 1, 3):
                inter = (S[:, a] & S[:, b]).sum(); uni = (S[:, a] | S[:, b]).sum()
                jac[f"J({EJES[a]},{EJES[b]})"] = round(inter / max(uni, 1), 2)
        print(f"  q{int(q*100)}: obs/esp = {obs3/esp3:.2f} IC95 [{lo:.2f}, {hi:.2f}] | {jac}")
        rows.append(dict(bloque="C_acumulacion", esquema=f"q{int(q*100)}",
                         medida="razon_obs_esp_3sev", valor=round(obs3 / esp3, 2),
                         ic_lo=round(lo, 2), ic_hi=round(hi, 2), **jac))
    S = np.column_stack([(d[f"{e}_mean"] > d[f"{e}_mean"].quantile(0.75)).values for e in EJES])
    tab = pd.Series([tuple(r) for r in S.astype(int)]).value_counts().sort_index()
    print("  intersecciones completas (eje1,eje2,eje3) q75:")
    print("  " + " | ".join(f"{k}:{v}" for k, v in tab.items()))

    # ---------- capa 3: R² incremental ----------
    y = d.z1_material.values
    bloques = [("geografía heredada", ["tri_mean", "elev_mean", "acc_km", "loc_peq_pct"]),
               ("+ demografía", ["pct_60mas", "dep_ratio"]),
               ("+ estructura económica", ["pct_primario", "pct_secundario", "empleo_precario_pct"]),
               # D5: composición indígena (ITER, P3YM_HLI/P3HLINHE verificadas en el
               # diccionario oficial) — al final para no alterar la secuencia ya citada
               ("+ composición indígena", ["pct_hli", "pct_hli_nhe"])]
    cols, r2prev = [], None
    print("\nCapa 3: R² incremental (CV bloqueado por estado; 'estado' aparte al final):")
    gkf = GroupKFold(5)
    for nombre, nuevos in bloques:
        cols += nuevos
        X = d[cols].values
        r2s = [r2_score(y[te], HistGradientBoostingRegressor(max_depth=4, max_iter=300,
                        random_state=1).fit(X[tr], y[tr]).predict(X[te]))
               for tr, te in gkf.split(X, y, groups=d.ent)]
        r2 = float(np.mean(r2s))
        print(f"  {nombre}: R² {r2:.3f} (Δ {r2 - (r2prev or 0):+.3f})")
        rows.append(dict(bloque="capa3_incremental", esquema=nombre, medida="r2cv",
                         valor=round(r2, 3)))
        r2prev = r2
    # estado al final: con FE de estado ya no se puede bloquear por estado -> KFold simple, anotado
    X = pd.concat([d[cols], pd.get_dummies(d.ent, drop_first=True).astype(float)], axis=1).values
    r2s = [r2_score(y[te], HistGradientBoostingRegressor(max_depth=4, max_iter=300,
                    random_state=1).fit(X[tr], y[tr]).predict(X[te]))
           for tr, te in KFold(5, shuffle=True, random_state=1).split(X)]
    print(f"  + estado (KFold simple, NO bloqueado — no comparable estrictamente): "
          f"R² {np.mean(r2s):.3f}")
    rows.append(dict(bloque="capa3_incremental", esquema="+ estado (KFold simple)",
                     medida="r2cv", valor=round(float(np.mean(r2s)), 3)))
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "desigualdad_robustez.csv"), index=False)


if __name__ == "__main__":
    main()
