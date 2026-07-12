#!/usr/bin/env python
"""
Análisis de la escalera GLLVM (outputs/ -> figures/ + csv de apoyo).

Produce:
  figures/fig_escalera_cargas.png        cambio de cargas post-Procrustes entre peldaños
  figures/fig_escalera_vardecomp.png     varianza por bloque e indicador, por peldaño
  figures/fig_escalera_metricas.png      Moran residual, ELPD-LOO, sd latente, rho BYM2
  figures/fig_gamma_estados.png          efectos estatales del peldaño 3: test DAG
                                         (directo vs modelado) y descomposición fiscal
  outputs/dag_test_directo_vs_modelado.csv
  outputs/gamma_estados_decomposicion.csv
"""
import os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT, FIG, PROC = (os.path.join(HERE, d) for d in ("outputs", "figures", os.path.join("data", "processed")))

# paleta de referencia (modo claro) — slots categóricos en orden fijo
C = ["#2a78d6", "#1baf7a", "#eda100", "#008300", "#4a3aa7", "#e34948", "#e87ba4", "#eb6834"]
INK, INK2, MUT, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
SURF = "#fcfcfb"
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "font.family": "sans-serif",
    "axes.edgecolor": "#c3c2b7", "axes.labelcolor": INK2, "text.color": INK,
    "xtick.color": MUT, "ytick.color": MUT, "axes.grid": True, "grid.color": GRID,
    "grid.linewidth": 0.6, "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 9,
})

SAE = ["car_segsoc", "car_alim", "lp_ingreso", "lp_ingreso_ext"]  # modelados por CONEVAL
DIRECTOS = ["rezago_educ", "car_salud", "car_vivienda", "car_servbas"]
K = 3
RUNGS = [1, 2, 3, 4]
RLAB = {1: "1 base", 2: "2 +VistaD", 3: "3 +estado", 4: "4 +BYM2"}


def load_loadings():
    return {r: pd.read_csv(os.path.join(OUT, f"loadings_rung{r}_K{K}.csv"), index_col=0)
            for r in RUNGS if os.path.exists(os.path.join(OUT, f"loadings_rung{r}_K{K}.csv"))}


def fig_cargas(L):
    facs = list(next(iter(L.values())).columns)
    ind = list(next(iter(L.values())).index)
    fig, axes = plt.subplots(1, len(facs), figsize=(11, 5.6), sharey=True)
    y = np.arange(len(ind))[::-1]
    for a, f in zip(axes, facs):
        for j, r in enumerate(sorted(L)):
            a.scatter(L[r][f].values, y, s=26, color=C[j], label=RLAB[r], zorder=3,
                      edgecolors=SURF, linewidths=1.2)
        a.axvline(0, color="#c3c2b7", lw=1, zorder=1)
        a.set_title(f"factor {f}", fontsize=10, color=INK)
        a.set_yticks(y); a.set_yticklabels(ind, fontsize=8)
        a.grid(axis="x")
    axes[0].legend(frameon=False, fontsize=8, loc="lower right")
    fig.suptitle("Cargas por peldaño (alineadas por Procrustes al peldaño 1) — K=3",
                 fontsize=12, color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_escalera_cargas.png"), dpi=160)
    plt.close(fig)


def fig_vardecomp():
    order = ["factores", "ruralidad", "cofactores", "estado", "metodo", "uniqueness"]
    labels = {"factores": "factores z", "ruralidad": "ruralidad", "cofactores": "cofactores D",
              "estado": "estado", "metodo": "método", "uniqueness": "uniqueness"}
    cols = {b: C[i] for i, b in enumerate(order)}
    Vs = {r: pd.read_csv(os.path.join(OUT, f"vardecomp_rung{r}_K{K}.csv"), index_col=0)
          for r in RUNGS if os.path.exists(os.path.join(OUT, f"vardecomp_rung{r}_K{K}.csv"))}
    fig, axes = plt.subplots(1, len(Vs), figsize=(12.5, 5.6), sharey=True)
    for a, r in zip(np.atleast_1d(axes), sorted(Vs)):
        v = Vs[r]; y = np.arange(len(v))[::-1]; left = np.zeros(len(v))
        for b in order:
            if b in v.columns:
                a.barh(y, v[b].values, left=left, height=0.72, color=cols[b],
                       label=labels[b], edgecolor=SURF, linewidth=1.4)
                left += v[b].values
        a.set_title(RLAB[r], fontsize=10, color=INK)
        a.set_yticks(y); a.set_yticklabels(v.index, fontsize=8)
        a.set_xlim(0, 1); a.grid(False)
    # leyenda con TODOS los bloques (el último panel no tiene 'estado')
    from matplotlib.patches import Patch
    present = [b for b in order if any(b in Vs[r].columns for r in Vs)]
    np.atleast_1d(axes)[-1].legend(
        handles=[Patch(facecolor=cols[b], label=labels[b]) for b in present],
        frameon=False, fontsize=8, bbox_to_anchor=(1.02, 1), loc="upper left")
    fig.suptitle("Descomposición de varianza por indicador (fracción de var(η)+σ²) — K=3",
                 fontsize=12, color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_escalera_vardecomp.png"), dpi=160)
    plt.close(fig)


def fig_metricas():
    s3 = pd.read_csv(os.path.join(OUT, f"ladder_summary_K{K}.csv"))
    s2p = os.path.join(OUT, "ladder_summary_K2.csv")
    s2 = pd.read_csv(s2p) if os.path.exists(s2p) else None
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6))
    panels = [("residual_moran_I", "Moran I residual (media 17 indicadores)"),
              ("elpd_loo", "ELPD-LOO"), ("mean_latent_sd", "sd posterior media de z")]
    for a, (col, title) in zip(axes, panels):
        a.plot(s3["rung"], s3[col], "-o", color=C[0], lw=2, ms=7, label="K=3",
               markeredgecolor=SURF, markeredgewidth=1.2)
        if s2 is not None:
            a.plot(s2["rung"], s2[col], "-o", color=C[1], lw=2, ms=7, label="K=2",
                   markeredgecolor=SURF, markeredgewidth=1.2)
        a.set_title(title, fontsize=9.5, color=INK)
        a.set_xticks(RUNGS); a.set_xticklabels([RLAB[r] for r in RUNGS], fontsize=7.5)
        if col == "residual_moran_I":
            a.axhline(0, color="#c3c2b7", lw=1)
    axes[0].legend(frameon=False, fontsize=8)
    rho = s3.loc[s3["rung"] == 4, "rho_spatial"]
    sub = f"ρ espacial BYM2 (peldaño 4, K=3): {rho.iloc[0]}" if len(rho) and isinstance(rho.iloc[0], str) else ""
    fig.suptitle("Métricas de la escalera" + (f"   |   {sub}" if sub else ""), fontsize=11, color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_escalera_metricas.png"), dpi=160)
    plt.close(fig)


def gamma_analysis():
    """Efectos estatales del peldaño 3: test del DAG + descomposición fiscal."""
    import arviz as az
    p = os.path.join(OUT, f"idata_rung3_K{K}.nc")
    if not os.path.exists(p):
        print("(sin idata_rung3 — se omite el análisis de gamma)")
        return None, None
    idata = az.from_netcdf(p)
    gam = idata.posterior["gamma"].mean(("chain", "draw")).values      # (J, S)
    ind = list(pd.read_csv(os.path.join(OUT, f"loadings_rung1_K{K}.csv"), index_col=0).index)
    cov = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))
    ents = sorted(cov["cvegeo"].str[:2].unique())                      # orden de cat.codes

    # --- test DAG: |gamma| por indicador, SAE vs directos ---
    mag = pd.DataFrame({"indicador": ind, "gamma_abs_media": np.abs(gam).mean(axis=1)})
    mag["grupo"] = ["SAE" if i in SAE else ("directo CONEVAL" if i in DIRECTOS else "CONAPO censal")
                    for i in ind]
    mag.sort_values("gamma_abs_media", ascending=False).to_csv(
        os.path.join(OUT, "dag_test_directo_vs_modelado.csv"), index=False)

    # --- gamma promedio por estado vs covariables fiscales ---
    est = pd.read_csv(os.path.join(PROC, "estatales_2020.csv"), dtype={"cve_ent": str})
    gbar = pd.DataFrame({"cve_ent": ents, "gamma_media": gam.mean(axis=0),
                         "gamma_sae": gam[[ind.index(i) for i in SAE], :].mean(axis=0),
                         "gamma_censal": gam[[ind.index(i) for i in ind if i not in SAE], :].mean(axis=0)})
    gbar = gbar.merge(est, on="cve_ent")
    gbar["log_pibe_pc"] = np.log10(gbar["pibe_pc_mxn"])
    for xv in ["log_pibe_pc", "gasto_pibe_pct"]:
        m = gbar[["gamma_media", xv]].dropna()
        r = np.corrcoef(m["gamma_media"], m[xv])[0, 1]
        gbar.attrs[xv] = r
    gbar.round(4).to_csv(os.path.join(OUT, "gamma_estados_decomposicion.csv"), index=False)

    # --- figura ---
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.2))
    # (a) test DAG
    a = axes[0]
    grp = mag.groupby("grupo")["gamma_abs_media"].mean().reindex(
        ["SAE", "directo CONEVAL", "CONAPO censal"])
    a.bar(range(3), grp.values, color=[C[5], C[1], C[0]], width=0.62)
    for i, v in enumerate(grp.values):
        a.text(i, v, f" {v:.3f}", ha="center", va="bottom", fontsize=8.5, color=INK)
    a.set_xticks(range(3)); a.set_xticklabels(grp.index, fontsize=8)
    a.set_title("|γ_s| media: modelados (SAE) vs directos\n(predicción DAG: SAE > directos)",
                fontsize=9, color=INK)
    a.grid(axis="y")
    # (b,c) gamma vs fiscal
    for a, xv, xlab in [(axes[1], "log_pibe_pc", "log10 PIBE per cápita"),
                        (axes[2], "gasto_pibe_pct", "gasto estatal / PIBE (%)")]:
        m = gbar.dropna(subset=[xv])
        a.scatter(m[xv], m["gamma_media"], s=30, color=C[0], edgecolors=SURF, linewidths=1.1)
        for _, row in m.iterrows():
            a.annotate(row["cve_ent"], (row[xv], row["gamma_media"]), fontsize=6,
                       color=MUT, xytext=(3, 2), textcoords="offset points")
        b, a0 = np.polyfit(m[xv], m["gamma_media"], 1)
        xs = np.linspace(m[xv].min(), m[xv].max(), 10)
        a.plot(xs, a0 + b * xs, color=C[5], lw=1.6)
        a.axhline(0, color="#c3c2b7", lw=1)
        a.set_xlabel(xlab, fontsize=8.5)
        a.set_title(f"γ̄_s vs {xlab}\nr = {gbar.attrs[xv]:.2f}", fontsize=9, color=INK)
    axes[1].set_ylabel("efecto estatal medio γ̄_s (logit-z)", fontsize=8.5)
    fig.suptitle("Peldaño 3: qué son los efectos estatales — medición (SAE) y capacidad fiscal",
                 fontsize=11, color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_gamma_estados.png"), dpi=160)
    plt.close(fig)
    return mag, gbar


def recompute_from_idata():
    """Regenera vardecomp y zscores desde los .nc con la lógica corregida (invariante a
    rotación / alineada por cadena), por si la corrida usó la versión anterior del script."""
    import arviz as az
    from scipy.linalg import orthogonal_procrustes
    import importlib, gllvm_ladder as gl
    importlib.reload(gl)
    Y, ind, rural, X, state, cvegeo = gl.load_data()
    ref = pd.read_csv(os.path.join(OUT, f"loadings_rung1_K{K}.csv"), index_col=0)
    facs = list(ref.columns)
    for r in RUNGS:
        p = os.path.join(OUT, f"idata_rung{r}_K{K}.nc")
        if not os.path.exists(p):
            continue
        idata = az.from_netcdf(p)
        gl.variance_decomposition(idata, ind, rural, X, state).to_csv(
            os.path.join(OUT, f"vardecomp_rung{r}_K{K}.csv"))
        zch = idata.posterior["z"].values; Lch = idata.posterior["Lam"].values
        zrot = np.empty_like(zch)
        for c in range(zch.shape[0]):
            Rm, _ = orthogonal_procrustes(Lch[c].mean(0), ref.values)
            zrot[c] = zch[c] @ Rm
        zc = pd.DataFrame(np.hstack([zrot.mean((0, 1)), zrot.std((0, 1))]),
                          columns=[f"{f}_mean" for f in facs] + [f"{f}_sd" for f in facs])
        zc.insert(0, "cvegeo", cvegeo)
        zc.to_csv(os.path.join(OUT, f"zscores_rung{r}_K{K}.csv"), index=False)
        # diagnóstico de label switching entre cadenas: dispersión de las rotaciones
        disp = np.mean([np.abs(orthogonal_procrustes(Lch[c].mean(0), ref.values)[0]
                               - np.eye(len(facs))).max() for c in range(zch.shape[0])])
        print(f"rung {r}: max|R−I| medio entre cadenas = {disp:.3f} "
              f"({'OK, mismas rotaciones' if disp < 0.15 else 'ROTACIONES DISTINTAS entre cadenas'})")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    recompute_from_idata()
    L = load_loadings()
    fig_cargas(L)
    fig_vardecomp()
    fig_metricas()
    mag, gbar = gamma_analysis()
    print("Figuras y csv listos.")
    if mag is not None:
        print("\nTest DAG (|γ| medio por grupo):")
        print(mag.groupby("grupo")["gamma_abs_media"].describe().round(3))
        print("\nCorrelaciones γ̄_s: log_pibe_pc r=%.2f, gasto_pibe_pct r=%.2f"
              % (gbar.attrs["log_pibe_pc"], gbar.attrs["gasto_pibe_pct"]))
    # cambio máximo de carga entre peldaños (post-Procrustes)
    if 1 in L and 2 in L:
        for r in [2, 3, 4]:
            if r in L:
                d = (L[r] - L[1]).abs()
                print(f"\nΔcarga máx |peldaño {r} − 1|: {d.max().max():.3f} "
                      f"({d.stack().idxmax()})")
