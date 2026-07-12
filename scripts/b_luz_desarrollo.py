#!/usr/bin/env python
"""
B — "El modelo simple que ¿daba para más?" (luz → desarrollo, corte transversal).

Semillas de INSTRUCCIONES_B_LUZ_DESARROLLO.md:
 1. Curva privación~log(NTL) con detección de quiebres (spline lineal, grid de nodos):
    piso rural / transición / saturación urbana; % de municipios por régimen.
 2. Escalera de complejidad OLS→spline→+covars→hgb con CV bloqueado por estado:
    ¿qué transformación rescata al modelo simple? ¿dónde se alcanza el 90% del hgb?
 3. Quiebre por macroregión (¿la log-lineal única es un promedio de curvas regionales?).
 4. Cruce de residuales de la curva simple con la discordancia satelital (remesas).
 5. Confusor población: ΔR² de la luz NETO de log_pob.

Salidas: outputs/b_luz_desarrollo_escalera.csv, outputs/b_breakpoints.csv,
         figures/07_satelital/fig_b_curva_quiebre.png, fig_b_escalera_complejidad.png
"""
import os
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score

import plotstyle as ps
ps.use()
FIG = ps.figdir("07_satelital")
HERE = ps.REPO
PROC, OUT = os.path.join(HERE, "data", "processed"), os.path.join(HERE, "outputs")
NORTE = {"02", "03", "05", "08", "10", "19", "25", "26", "28", "32"}
SUR = {"04", "07", "12", "20", "21", "23", "27", "30", "31"}
CONAPO9 = ["analf", "sin_basica", "sin_drenaje", "sin_electr", "sin_agua",
           "piso_tierra", "hacinam", "loc_peq", "ing_2sm"]


def norm(df):
    df = df.copy(); df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5); return df


def hinge(x, k):
    return np.maximum(x - k, 0.0)


def fit_knots(x, y, nk):
    """spline lineal continuo con nk nodos por grid-search de SSE (descriptivo, in-sample)."""
    qs = np.quantile(x, np.linspace(0.03, 0.97, 35))
    best = (None, -np.inf)
    from itertools import combinations
    cands = combinations(qs, nk)
    for ks in cands:
        X = np.column_stack([x] + [hinge(x, k) for k in ks])
        r2 = LinearRegression().fit(X, y).score(X, y)
        if r2 > best[1]:
            best = (ks, r2)
    ks = best[0]
    X = np.column_stack([x] + [hinge(x, k) for k in ks])
    m = LinearRegression().fit(X, y)
    # pendientes por segmento (acumulando hinges)
    slopes = np.cumsum(np.r_[m.coef_[0], m.coef_[1:]])
    return ks, best[1], m, slopes


def cv_r2(X, y, groups, est="ols"):
    gkf = GroupKFold(5); r2s = []
    for tr, te in gkf.split(X, y, groups=groups):
        if est == "ols":
            m = LinearRegression().fit(X[tr], y[tr])
        else:
            m = HistGradientBoostingRegressor(max_depth=4, max_iter=300, random_state=1).fit(X[tr], y[tr])
        r2s.append(r2_score(y[te], m.predict(X[te])))
    return float(np.mean(r2s)), float(np.std(r2s))


def main():
    F = norm(pd.read_parquet(os.path.join(PROC, "vistaF_satelital.parquet")))
    z = norm(pd.read_csv(os.path.join(OUT, "zscores_rung1_K3.csv")))
    cov = norm(pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")))
    Y = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet"))
    Y.index = cov["cvegeo"].values
    d = cov[["cvegeo", "loc_peq_pct", "log_pob"]].merge(F.drop(columns=["pob_tot"]), on="cvegeo").merge(z, on="cvegeo")
    assert len(d) >= 2450, d.shape
    d["marg9"] = Y.loc[d["cvegeo"], CONAPO9].mean(axis=1).values   # proxy marginación (componentes)
    d["ent"] = d["cvegeo"].str[:2]
    d["region"] = d["ent"].map(lambda e: "norte" if e in NORTE else ("sur-sureste" if e in SUR else "centro"))
    # eje de la CURVA: log10(radiancia+0.01) despliega piso y transición (log1p los aplasta)
    x = np.log10(d["ntl_mean"].values + 0.01)
    print(f"n={len(d)} | corr(log10 ntl, z_material bruto) = "
          f"{np.corrcoef(x, d.material_mean)[0,1]:+.3f} (debe ser negativa)")

    # ---------- 1. quiebres globales (2 nodos) y por región (1 nodo), dos outcomes ----------
    bps = []
    for yname in ["material_mean", "marg9"]:
        y = d[yname].values
        ks, r2, m2, slopes = fit_knots(x, y, 2)
        seg = np.digitize(x, ks)
        for i, (klo, s) in enumerate(zip([x.min()] + list(ks), slopes)):
            bps.append(dict(outcome=yname, ambito="global", nodo=i,
                            knot_logntl=(None if i == 0 else round(ks[i-1], 3)),
                            knot_radiancia=(None if i == 0 else round(float(10**ks[i-1] - 0.01), 3)),
                            pendiente=round(float(s), 3),
                            pct_municipios=round(100 * float((seg == i).mean()), 1),
                            r2_insample=round(r2, 3)))
        for reg in ["norte", "centro", "sur-sureste"]:
            k = d.region == reg
            ks1, r21, _, sl1 = fit_knots(x[k.values], y[k.values], 1)
            bps.append(dict(outcome=yname, ambito=reg, nodo=1,
                            knot_logntl=round(ks1[0], 3),
                            knot_radiancia=round(float(10**ks1[0] - 0.01), 3),
                            pendiente=round(float(sl1[1]), 3),
                            pct_municipios=round(100 * float((x[k.values] > ks1[0]).mean()), 1),
                            r2_insample=round(r21, 3)))
    B = pd.DataFrame(bps); B.to_csv(os.path.join(OUT, "b_breakpoints.csv"), index=False)
    kg = [b["knot_logntl"] for b in bps if b["ambito"] == "global" and b["outcome"] == "material_mean" and b["nodo"] > 0]
    print("quiebres globales material (log10):", kg,
          "| radiancia nW:", [round(float(10**k - 0.01), 3) for k in kg])

    # ---------- 2. escalera de complejidad (outcome: z material bruto) ----------
    y = d["material_mean"].values; g = d["ent"]
    ks2 = [b for b in kg]
    SPL = np.column_stack([x] + [hinge(x, k) for k in ks2])
    escalera = [
        ("E0 OLS ntl_mean (lineal puro)", d[["ntl_mean"]].values, "ols"),
        ("E1 OLS log_ntl (canónico Jean)", d[["log_ntl"]].values, "ols"),
        ("E2 + ntl_pc", np.column_stack([x, d.ntl_pc]), "ols"),
        ("E3 OLS spline(log_ntl) [2 nodos]", SPL, "ols"),
        ("E4 spline + loc_peq + acc_km", np.column_stack([SPL, d.loc_peq_pct, d.acc_km]), "ols"),
        ("E5 hgb lentes completas (M3)", d[["log_ntl", "ntl_pc", "elev_mean", "tri_mean", "acc_km"]].values, "hgb"),
    ]
    rows = []
    for nombre, X, est in escalera:
        r2m, r2s = cv_r2(X, y, g, est)
        rows.append(dict(peldano=nombre, r2cv=round(r2m, 3), sd=round(r2s, 3), n_params=X.shape[1]))
        print(f"{nombre}: R²cv = {r2m:.3f}")
    E = pd.DataFrame(rows)
    ref = E.r2cv.iloc[-1]
    E["pct_del_sofisticado"] = (100 * E.r2cv / ref).round(0)
    # confusor población
    r2_pob, _ = cv_r2(d[["log_pob"]].values, y, g)
    r2_pob_ntl, _ = cv_r2(np.column_stack([d.log_pob, SPL]), y, g)
    E.loc[len(E)] = dict(peldano="(control) OLS log_pob solo", r2cv=round(r2_pob, 3), sd=np.nan,
                         n_params=1, pct_del_sofisticado=np.nan)
    E.loc[len(E)] = dict(peldano="(control) log_pob + spline(log_ntl)", r2cv=round(r2_pob_ntl, 3),
                         sd=np.nan, n_params=4, pct_del_sofisticado=np.nan)
    E.to_csv(os.path.join(OUT, "b_luz_desarrollo_escalera.csv"), index=False)
    print(f"población sola: {r2_pob:.3f} | +spline luz: {r2_pob_ntl:.3f} "
          f"(Δ luz neta de urbanización = {r2_pob_ntl - r2_pob:+.3f})")

    # ---------- 4. cruce con discordancia satelital ----------
    _, _, m2, _ = fit_knots(x, y, 2)
    resid_simple = y - m2.predict(np.column_stack([x] + [hinge(x, k) for k in ks2]))
    oof = norm(pd.read_parquet(os.path.join(OUT, "satelital_oof.parquet")))
    oof = oof.query("outcome=='rung1' and modelo=='M3_lentes' and factor=='material'")
    mm = d[["cvegeo"]].assign(res_simple=resid_simple).merge(
        oof.assign(res_m3=oof.z_obs - oof.z_pred)[["cvegeo", "res_m3"]], on="cvegeo")
    print(f"corr(residual curva simple, residual M3 lentes) = "
          f"{np.corrcoef(mm.res_simple, mm.res_m3)[0,1]:+.3f}")

    # ---------- figuras ----------
    # estrella: curva con quiebres y regímenes
    fig, (a, b) = plt.subplots(1, 2, figsize=(13, 5.6))
    a.scatter(x, y, s=7, color=ps.GRAY, alpha=0.45, linewidths=0)
    xs = np.linspace(x.min(), x.max(), 200)
    a.plot(xs, m2.predict(np.column_stack([xs] + [hinge(xs, k) for k in ks2])),
           color=ps.BLUE, lw=2.4, zorder=4)
    cols_reg = ["#fdeeee", "#f6f5f1", "#eef4fd"]
    lims = [x.min()] + list(ks2) + [x.max()]
    labs = ["PISO OSCURO\n(luz≈0; la privación\nvaría de −1 a +2.5)",
            "PENUMBRA RURAL\n(la luz informa débil)",
            "RANGO INFORMATIVO\n(la luz discrimina mejor;\nSIN saturación municipal)"]
    for i in range(3):
        a.axvspan(lims[i], lims[i + 1], color=cols_reg[i], zorder=0)
        pct = 100 * ((x >= lims[i]) & (x <= lims[i + 1])).mean()
        a.text((lims[i] + lims[i + 1]) / 2, 2.35, f"{labs[i]}\n{pct:.0f}% munis",
               ha="center", fontsize=7, color=ps.INK2)
    for k in ks2:
        a.axvline(k, color=ps.INK2, lw=1, ls="--")
        a.text(k, -3.3, f"{10**k - 0.01:.2f} nW", ha="center", fontsize=7.5, color=ps.INK)
    a.set_xlabel("log10(radiancia nocturna media + 0.01) — nW/cm²/sr")
    a.set_ylabel("privación material bruta (z, peldaño 1) — alto = más privado")
    a.set_title("(a) La curva luz→privación NO es log-lineal, y la sorpresa va al revés:\n"
                "no hay saturación urbana a escala municipal — el piso oscuro es el problema",
                fontsize=10, loc="left")
    # regional
    for reg, c in [("norte", ps.C[0]), ("centro", ps.C[2]), ("sur-sureste", ps.C[5])]:
        k = (d.region == reg).values
        ks1, _, m1, _ = fit_knots(x[k], y[k], 1)
        xs = np.linspace(x[k].min(), x[k].max(), 100)
        b.plot(xs, m1.predict(np.column_stack([xs, hinge(xs, ks1[0])])), color=c, lw=2.2,
               label=f"{reg}: quiebre en {10**ks1[0] - 0.01:.2f} nW")
        b.scatter(x[k], y[k], s=5, color=c, alpha=0.18, linewidths=0)
        b.axvline(ks1[0], color=c, lw=1, ls=":")
    b.legend(frameon=False, fontsize=8.5, loc="upper right")
    b.set_xlabel("log10(radiancia + 0.01)")
    b.set_title("(b) El quiebre es regional: la 'relación única' es un\npromedio de curvas distintas",
                fontsize=10, loc="left")
    fig.suptitle("Luz y desarrollo a escala municipal: la premisa log-lineal se resuelve en piso rural + saturación + región",
                 fontsize=12, color=ps.INK, x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(os.path.join(FIG, "fig_b_curva_quiebre.png"))
    print("fig_b_curva_quiebre.png")

    # escalera
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    Ee = E.iloc[:6]
    yy = np.arange(len(Ee))[::-1]
    ax.barh(yy, Ee.r2cv, height=0.62, color=[ps.MUT, ps.MUT, ps.MUT, ps.BLUE, ps.BLUE, ps.AQUA],
            edgecolor=ps.SURF, linewidth=1.2)
    for yi, (_, r) in zip(yy, Ee.iterrows()):
        ax.text(max(r.r2cv, 0) + 0.006, yi, f"{r.r2cv:.2f}", va="center", fontsize=8.5)
    ax.axvline(0.9 * ref, color=ps.RED, lw=1.3, ls="--")
    ax.text(0.9 * ref, len(Ee) - 0.4, " 90% del sofisticado", color=ps.RED, fontsize=8)
    ax.set_yticks(yy); ax.set_yticklabels(Ee.peldano, fontsize=8.5)
    ax.axvline(0, color=ps.BASE, lw=1)
    ax.set_xlabel("R² (5-fold CV bloqueado por estado) — z material bruto")
    ax.set_title("¿Qué rescata al modelo simple? La transformación, no las variables",
                 fontsize=10.5, loc="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_b_escalera_complejidad.png"))
    print("fig_b_escalera_complejidad.png")


if __name__ == "__main__":
    main()
