#!/usr/bin/env python
"""
Tarea B (test) — ¿la brecha AA/BB del FISM vive en el piso 2013 o en el incremento?

La fórmula FAIS vigente (art. 34 LCF, reforma dic-2013):
    F_i,2020 = F_i,2013 (piso, perfil IGP≈marginación) + ΔF·(0.8 z + 0.2 e) (incremento,
    pobreza extrema CONEVAL). Si la brecha del perfil "más marginado que pobre" es legado
    del instrumento de medición, debe concentrarse en el piso y desvanecerse en el
    incremento.

Insumos: outputs/fism_2013_municipal.parquet, outputs/fism_fortamun_2020_municipal.parquet
         (constructor: scripts/build_b_fism_piso.py), diagnostico_municipal_v1.parquet,
         gllvm_Y.parquet.

Salidas:
  - outputs/b_fism_cobertura.csv          (paso gate: sesgo de la intersección)
  - outputs/b_fism_descomposicion.csv     (regresiones + resúmenes)
  - figures/05_dag/fig_b_cobertura_sesgo.png
  - figures/05_dag/fig_b_piso_incremento.png
"""
import os

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import plotstyle as ps

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
OUT = os.path.join(HERE, "outputs")

# INPC promedio anual, base 2a q. julio 2018 = 100 (serie histórica DOF/INEGI):
# 2013 = 82.036, 2020 = 107.430
DEFLACTOR_INPC = 107.430 / 82.036
RNG = np.random.default_rng(2013)
N_BOOT = 2000

SURF, INK, INK2, MUT, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
RED, BLUE, GRAY = "#e34948", "#2a78d6", "#d5d4cd"


def cargar():
    d = pd.read_parquet(os.path.join(PROC, "diagnostico_municipal_v1.parquet"))
    Y = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet"))
    Y.index = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))["cvegeo"].values
    d["nivel"] = Y.loc[d["cvegeo"]].mean(axis=1).values
    d["reg"] = d["lisa"].where(d["lisa"].isin(["AA", "BB"]), "ns")
    d["ent"] = d["cvegeo"].str[:2]

    f13 = pd.read_parquet(os.path.join(OUT, "fism_2013_municipal.parquet"))
    f13 = f13[~f13["cobertura_estatal"]]
    f20 = pd.read_parquet(os.path.join(OUT, "fism_fortamun_2020_municipal.parquet"))
    fin = pd.read_parquet(os.path.join(PROC, "finanzas_mun_2020.parquet"))[
        ["cvegeo", "aportaciones_pc"]]
    d = (d.merge(f13, on="cvegeo", how="left")
          .merge(f20, on="cvegeo", how="left")
          .merge(fin, on="cvegeo", how="left"))

    d["en_muestra"] = ((d["monto_2013"] > 0) & (d["fais_2020"] > 0)
                       & ~d["flag_captura"].fillna(False).astype(bool)
                       & (d["pob_conapo"] > 0))
    m = d[d["en_muestra"]].copy()
    m["piso_pc"] = m["monto_2013"] * DEFLACTOR_INPC / m["pob_conapo"]
    m["total_pc"] = m["fais_2020"] / m["pob_conapo"]
    m["inc_pc"] = m["total_pc"] - m["piso_pc"]
    m["fortamun_pc"] = m["fortamun_2020"] / m["pob_conapo"]
    return d, m


def gate_cobertura(d, filas):
    """Paso 4: la intersección vs. los excluidos del modelo — ¿quién entra al test?"""
    dentro, fuera = d[d["en_muestra"]], d[~d["en_muestra"]]
    vars_ = [("log_pob", "log población"), ("loc_peq_pct", "% en localidades <2,500 hab"),
             ("nivel", "privación total (logit-z)"), ("eje1_mean", "eje material"),
             ("eje2_mean", "eje educativo"), ("eje3_mean", "eje monetario")]
    rows = []
    for v, lab in vars_:
        a, b = dentro[v].dropna(), fuera[v].dropna()
        sd = np.sqrt((a.var() + b.var()) / 2)
        rows.append({"variable": v, "media_interseccion": a.mean(), "media_excluidos": b.mean(),
                     "smd": (a.mean() - b.mean()) / sd,
                     "ks_p": stats.ks_2samp(a, b).pvalue})
    for r in ("AA", "BB"):
        rows.append({"variable": f"share_{r}", "media_interseccion": (dentro["reg"] == r).mean(),
                     "media_excluidos": (fuera["reg"] == r).mean(),
                     "smd": np.nan, "ks_p": np.nan})
    cob = pd.DataFrame(rows)
    filas.append(("n_interseccion", len(dentro)))
    filas.append(("n_AA_interseccion", int((dentro["reg"] == "AA").sum())))
    filas.append(("n_BB_interseccion", int((dentro["reg"] == "BB").sum())))
    filas.append(("cobertura_modelo_pct", 100 * len(dentro) / len(d)))
    cob.round(4).to_csv(os.path.join(OUT, "b_fism_cobertura.csv"), index=False)

    fig, axes = plt.subplots(2, 4, figsize=(13.5, 6.2))
    paneles = [axes[0, 0], axes[0, 1], axes[0, 2], axes[1, 0], axes[1, 1], axes[1, 2]]
    for ax, (v, lab) in zip(paneles, vars_):
        for s, c, l in [(fuera, GRAY, "excluidos"), (dentro, RED, "intersección")]:
            x = s[v].dropna()
            ax.hist(x, bins=30, density=True, histtype="stepfilled",
                    alpha=0.45 if c == GRAY else 0.55, color=c, label=l, linewidth=0)
        smd = cob.loc[cob["variable"] == v, "smd"].iloc[0]
        ax.set_title(f"{lab}\nSMD = {smd:+.2f}", fontsize=8.5, loc="left", color=INK)
        ax.set_yticks([])
    paneles[0].legend(frameon=False, fontsize=8)
    # composición por estado (top 12 en la intersección) — columna derecha completa
    axes[0, 3].axis("off")
    axes[1, 3].axis("off")
    ax = plt.subplot2grid((2, 4), (0, 3), rowspan=2, fig=fig)
    tab = (pd.crosstab(d["nom_ent"], d["en_muestra"], normalize="columns") * 100)
    top = tab[True].sort_values(ascending=False).head(12).index[::-1]
    ypos = np.arange(len(top))
    ax.barh(ypos + 0.2, tab.loc[top, True], height=0.38, color=RED, label="intersección")
    ax.barh(ypos - 0.2, tab.loc[top, False], height=0.38, color=GRAY, label="excluidos")
    ax.set_yticks(ypos, top, fontsize=7.5)
    ax.set_xlabel("% de los municipios del grupo", fontsize=8)
    ax.set_title("composición por estado", fontsize=8.5, loc="left", color=INK)
    ax.legend(frameon=False, fontsize=7.5)
    fig.suptitle("¿Quién entra al test piso/incremento? Municipios con FISM reportado en "
                 "2013 Y 2020 (SRFT) vs. el resto del modelo",
                 fontsize=11, color=INK, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(os.path.join(ps.figdir("05_dag"), "fig_b_cobertura_sesgo.png"), dpi=160)
    plt.close(fig)
    return cob


def ols(y, X, labels):
    mod = sm.OLS(y, X).fit(cov_type="HC1")
    return pd.DataFrame({"term": labels, "coef": mod.params, "se": mod.bse,
                         "t": mod.tvalues, "n": int(mod.nobs)})


def diseno(m, tratamiento="dummies", extendido=True):
    cols = [np.ones(len(m)), m["nivel"], m["nivel"] ** 2, m["log_pob"]]
    labels = ["const", "nivel", "nivel2", "log_pob"]
    if extendido:
        cols += [m["loc_peq_pct"], np.log(m["fortamun_pc"])]
        labels += ["loc_peq_pct", "log_fortamun_pc"]
    if tratamiento == "dummies":
        cols += [(m["reg"] == "AA").astype(float), (m["reg"] == "BB").astype(float)]
        labels += ["AA", "BB"]
    else:
        cols += [m["discordancia_obs"]]
        labels += ["discordancia"]
    return np.column_stack(cols), labels


def bootstrap_estado(m, fn, n_boot=N_BOOT):
    """fn(df) -> vector de estadísticos; remuestreo por conglomerado estatal."""
    ents = m["ent"].unique()
    out = []
    for _ in range(n_boot):
        pick = RNG.choice(ents, size=len(ents), replace=True)
        bs = pd.concat([m[m["ent"] == e] for e in pick], ignore_index=True)
        try:
            out.append(fn(bs))
        except Exception:
            continue
    return np.array(out)


def main():
    d, m = cargar()
    filas = []
    gate_cobertura(d, filas)

    # peso del piso (la "acción imprescindible" del dictamen §2)
    share = m["piso_pc"] / m["total_pc"]
    # a nivel de fondo, con totales oficiales (no depende de la cobertura muestral):
    # FISM 2013 = $46,655 M (PEF) deflactado / FISMDF 2020 = $75,447 M
    filas += [("share_piso_fondo_oficial_pct", 100 * 46_655 * DEFLACTOR_INPC / 75_447),
              ("share_piso_mediana_pct", 100 * share.median()),
              ("share_piso_agregado_pct", 100 * m["piso_pc"].mul(m["pob_conapo"]).sum()
                / m["total_pc"].mul(m["pob_conapo"]).sum()),
              ("pct_incremento_negativo", 100 * (m["inc_pc"] < 0).mean()),
              ("deflactor_inpc_2013_2020", DEFLACTOR_INPC)]

    me = m.dropna(subset=["loc_peq_pct", "fortamun_pc", "discordancia_obs"])
    me = me[me["fortamun_pc"] > 0]
    filas.append(("n_spec_extendida", len(me)))

    regs = []

    # (0) replica de la spec del paper (log aportaciones EFIPEM) en la submuestra:
    #     ¿la selección SRFT preserva la brecha conocida?
    r = m.dropna(subset=["aportaciones_pc"]).query("aportaciones_pc>0")
    X, lab = diseno(r, extendido=False)
    t = ols(np.log(r["aportaciones_pc"]), X, lab); t["spec"] = "log_aportaciones_efipem_submuestra"
    regs.append(t)

    # (0b) muestra completa EFIPEM: IC de la DIFERENCIA AA-BB del +15.8%/-3.0% del paper
    #      (dictamen §5: "reporten el IC de la diferencia, no sólo los dos coeficientes")
    full = d.dropna(subset=["aportaciones_pc", "discordancia_obs"]).query(
        "aportaciones_pc>0").copy()
    def dif_full(bs):
        X, lab = diseno(bs, extendido=False)
        p = sm.OLS(np.log(bs["aportaciones_pc"]), X).fit().params
        return np.array([p[lab.index("AA")] - p[lab.index("BB")]])
    btf = bootstrap_estado(full, dif_full)
    lo, hi = np.percentile(btf[:, 0], [2.5, 97.5])
    filas += [("brecha_AABB_efipem_full_pct", 100 * (np.exp(np.median(btf[:, 0])) - 1)),
              ("brecha_AABB_efipem_full_pct_ci_lo", 100 * (np.exp(lo) - 1)),
              ("brecha_AABB_efipem_full_pct_ci_hi", 100 * (np.exp(hi) - 1)),
              ("n_efipem_full", len(full))]

    # (a,b) elasticidades comparables con el +15.8% del paper
    for dep, nombre in [("total_pc", "log_fais2020"), ("piso_pc", "log_piso2013")]:
        X, lab = diseno(me)
        t = ols(np.log(me[dep]), X, lab); t["spec"] = nombre
        regs.append(t)

    # (a,b,c) descomposición aditiva en niveles: beta_total = beta_piso + beta_incremento
    for dep in ["total_pc", "piso_pc", "inc_pc"]:
        X, lab = diseno(me)
        t = ols(me[dep], X, lab); t["spec"] = f"niveles_{dep}"
        regs.append(t)

    # tratamiento continuo (discordancia observada) — potencia con 249 munis
    for dep in ["total_pc", "piso_pc", "inc_pc"]:
        X, lab = diseno(me, tratamiento="continuo")
        t = ols(me[dep], X, lab); t["spec"] = f"niveles_{dep}_discordancia"
        regs.append(t)

    # robustez: EFE (efectos fijos estatales) sobre log total
    efe = pd.get_dummies(me["ent"], prefix="e", drop_first=True).astype(float)
    X, lab = diseno(me)
    Xf = np.column_stack([X, efe.values])
    t = ols(np.log(me["total_pc"]), Xf, lab + list(efe.columns))
    t = t[~t["term"].str.startswith("e_")]; t["spec"] = "log_fais2020_EFE"
    regs.append(t)

    # contrastes puntuales (OLS) — los IC vienen del bootstrap de abajo
    R0 = pd.concat(regs, ignore_index=True)

    def cf(spec, term):
        return R0[(R0["spec"] == spec) & (R0["term"] == term)]["coef"].iloc[0]

    filas += [
        ("ols_brecha_AABB_piso", cf("niveles_piso_pc", "AA") - cf("niveles_piso_pc", "BB")),
        ("ols_brecha_AABB_inc", cf("niveles_inc_pc", "AA") - cf("niveles_inc_pc", "BB")),
        ("ols_brecha_AABB_total", cf("niveles_total_pc", "AA") - cf("niveles_total_pc", "BB")),
        ("ols_dif_brecha_piso_menos_inc",
         (cf("niveles_piso_pc", "AA") - cf("niveles_piso_pc", "BB"))
         - (cf("niveles_inc_pc", "AA") - cf("niveles_inc_pc", "BB"))),
        ("ols_piso_BB_pct", 100 * (np.exp(cf("log_piso2013", "BB")) - 1)),
        ("ols_inc_BB_pc", cf("niveles_inc_pc", "BB")),
        ("ols_efipem_submuestra_AA_pct",
         100 * (np.exp(cf("log_aportaciones_efipem_submuestra", "AA")) - 1)),
    ]

    # bootstrap por estado: IC de las DIFERENCIAS (no de los coeficientes por separado)
    def contrastes(bs):
        X, lab = diseno(bs)
        iAA, iBB = lab.index("AA"), lab.index("BB")
        bT = sm.OLS(bs["total_pc"], X).fit().params
        bP = sm.OLS(bs["piso_pc"], X).fit().params
        bI = sm.OLS(bs["inc_pc"], X).fit().params
        gapP, gapI = bP[iAA] - bP[iBB], bI[iAA] - bI[iBB]
        Xc, labc = diseno(bs, tratamiento="continuo")
        iD = labc.index("discordancia")
        cP = sm.OLS(bs["piso_pc"], Xc).fit().params[iD]
        cI = sm.OLS(bs["inc_pc"], Xc).fit().params[iD]
        lP = sm.OLS(np.log(bs["piso_pc"]), X).fit().params
        return np.array([
            gapP - gapI,                 # ★ la brecha AA-BB, piso menos incremento
            gapP, gapI,                  # brecha AA-BB en cada componente
            bT[iAA] - bT[iBB],           # brecha AA-BB en el total
            bP[iAA] - bI[iAA],           # brazo AA: piso menos incremento
            bP[iBB] - bI[iBB],           # brazo BB: piso menos incremento
            lP[iBB],                     # elasticidad piso BB (log)
            cP - cI])                    # discordancia continua: piso menos incremento
    bt = bootstrap_estado(me, contrastes)
    nombres_bt = ["dif_brecha_piso_menos_inc", "brecha_AABB_piso", "brecha_AABB_inc",
                  "brecha_AABB_total", "dif_AA_piso_menos_inc", "dif_BB_piso_menos_inc",
                  "log_piso_BB", "dif_discordancia_piso_menos_inc"]
    for k, nombre in enumerate(nombres_bt):
        lo, hi = np.percentile(bt[:, k], [2.5, 97.5])
        filas += [(f"{nombre}_ci_lo", lo), (f"{nombre}_ci_hi", hi),
                  (f"{nombre}_punto", np.median(bt[:, k]))]

    R = R0[["spec", "term", "coef", "se", "t", "n"]]
    S = pd.DataFrame(filas, columns=["term", "coef"]).assign(spec="resumen", se=np.nan,
                                                             t=np.nan, n=len(me))
    pd.concat([R, S[R.columns]], ignore_index=True).round(6).to_csv(
        os.path.join(OUT, "b_fism_descomposicion.csv"), index=False)

    # ---- figura principal: la brecha descompuesta, ambos brazos ----
    X, lab = diseno(me)
    iAA, iBB = lab.index("AA"), lab.index("BB")
    puntos = {dep: sm.OLS(me[dep], X).fit(cov_type="HC1") for dep in
              ["total_pc", "piso_pc", "inc_pc"]}

    def boot_coefs(bs):
        X, lab = diseno(bs)
        i, j = lab.index("AA"), lab.index("BB")
        out = []
        for dep in ["total_pc", "piso_pc", "inc_pc"]:
            p = sm.OLS(bs[dep], X).fit().params
            out += [p[i], p[j]]
        return np.array(out)
    bcoef = bootstrap_estado(me, boot_coefs, n_boot=N_BOOT)

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8),
                                  gridspec_kw={"width_ratios": [1.15, 1]})
    nombres = ["transferencia\ntotal 2020", "piso 2013\n(fórmula IGP)",
               "incremento\n(fórmula pobreza)"]
    for k, dep in enumerate(["total_pc", "piso_pc", "inc_pc"]):
        for off, idx, col, colb in [(-0.12, iAA, 2 * k, RED), (0.12, iBB, 2 * k + 1, BLUE)]:
            b = puntos[dep].params[idx]
            lo, hi = np.percentile(bcoef[:, col], [2.5, 97.5])
            ax.errorbar(k + off, b, yerr=[[b - lo], [hi - b]], fmt="o", color=colb,
                        ms=8, capsize=4, lw=1.6)
    ax.axhline(0, color="#c3c2b7", lw=1)
    ax.set_xticks(np.arange(3), nombres, fontsize=9)
    ax.set_ylabel("pesos por habitante respecto del perfil concordante\n"
                  "(mismos controles en las tres regresiones)", fontsize=9)
    ax.scatter([], [], color=RED, label="AA: más marginado que pobre")
    ax.scatter([], [], color=BLUE, label="BB: más pobre que marginado")
    ax.legend(frameon=False, fontsize=8, loc="upper right")
    get = lambda n: [v for k_, v in filas if k_ == n][0]
    ax.set_title("(a) Brecha por perfil de medición en cada componente\n"
                 f"brecha AA−BB: piso {get('ols_brecha_AABB_piso'):+,.0f} vs. incremento "
                 f"{get('ols_brecha_AABB_inc'):+,.0f} pc; dif. IC 95% "
                 f"[{get('dif_brecha_piso_menos_inc_ci_lo'):+,.0f}, "
                 f"{get('dif_brecha_piso_menos_inc_ci_hi'):+,.0f}]",
                 fontsize=9.5, loc="left", color=INK)

    # (b) dispersión piso vs incremento coloreada por régimen
    for reg, c, zo, al in [("ns", GRAY, 1, 0.35), ("BB", BLUE, 3, 0.8), ("AA", RED, 3, 0.8)]:
        s = me[me["reg"] == reg]
        ax2.scatter(s["piso_pc"], s["inc_pc"], s=13, color=c, alpha=al, zorder=zo, lw=0)
    ax2.axhline(0, color="#c3c2b7", lw=1)
    ax2.set_xscale("log")
    ax2.set_xlabel("piso 2013 por habitante (pesos de 2020, log)", fontsize=9)
    ax2.set_ylabel("incremento 2014-2020 por habitante", fontsize=9)
    ax2.set_title("(b) Piso heredado vs. incremento de la fórmula nueva",
                  fontsize=9.5, loc="left", color=INK)
    fig.suptitle("¿Dónde vive la brecha del perfil de medición? Descomposición de la "
                 "transferencia FISM 2020 en piso 2013 + incremento",
                 fontsize=11.5, color=INK, x=0.02, ha="left")
    fig.text(0.02, 0.005,
             f"n = {len(me)} municipios con FISM reportado en 2013 y 2020 (SRFT); piso "
             f"deflactado con INPC (x{DEFLACTOR_INPC:.3f}).\nControles: privación total y "
             "cuadrado, log población, ruralidad, FORTAMUN pc. IC 95% bootstrap por estado. "
             "Asociación, no causalidad.", fontsize=7.5, color=MUT)
    fig.tight_layout(rect=[0, 0.06, 1, 0.90])
    fig.savefig(os.path.join(ps.figdir("05_dag"), "fig_b_piso_incremento.png"), dpi=160)

    print(pd.concat([R, S[R.columns]]).to_string(index=False))


if __name__ == "__main__":
    ps.use()
    main()
