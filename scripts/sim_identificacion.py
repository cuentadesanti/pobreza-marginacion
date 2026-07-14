#!/usr/bin/env python
"""
SIMULACION DE IDENTIFICACION — Bloque 1 / Nivel 2 de la revision del Paper 1.

Pregunta de ambos revisores: ¿la separacion factor / metodo / estado que reporta el GLLVM
marginalizado es RECUPERABLE cuando la verdad se conoce, o es artefacto de la parametrizacion
(direcciones fijas, anclas LogNormal, K)?

Generador sintetico calcado del modelo (gllvm_marginal.build):
    Y_i = W' a_i + gamma_{s(i)} + Lam z_i + lam_true * v_sae * m_i + eps_i
    z ~ N(0, I_K),  m ~ N(0,1),  eps ~ N(0, diag(sigma^2)),  a_i = [1, rural, x_1..x_7]
con verdades tomadas del posterior real (idata_marginal_rung3.nc):
    Lam_true  = ejes canonicos de E[LamLam'] rotados a forma echelon sobre las anclas
                (piso_tierra / rezago_educ / lp_ingreso) — misma LamLam' que el ajuste real
    sigma, W  = medias posteriores;  v_sae = (lp_ingreso + lp_ingreso_ext)/sqrt(2) (direccion fija)
    gamma_true[j,s] ~ N(0, sg) centrada por fila (S=32)

Escenarios (2 replicas c/u, semillas fijas, N=1000):
    a_lam{0,03,06}   bien especificado, lam_true en {0, .3, .6}, sg=.5
    a_lam03_sg0      bien especificado sin efecto estatal verdadero (sg=0)
    b_anclas         anclas verdaderas DEBILES: filas ancla de Lam_true x 0.15 (el modelo
                     asume anclas fuertes via LogNormal(log .5, .4))
    c_gen2_fit3      K_true=2, ajusta K=3 (¿el factor extra absorbe metodo?)
    c_gen3_fit2      K_true=3, ajusta K=2 (¿el factor omitido infla lam?)
    d_referee        SIN metodo (lam_true=0) pero lp_ingreso/lp_ingreso_ext casi colineales
                     (corr ~.98, como en los datos reales: comparten la variable de ingreso)
                     VIA FACTORES (filas identicas + uniqueness minima). Si el modelo fabrica
                     lam_hat grande aqui, la critica del referee es correcta y se reporta asi.

Cada escenario se ajusta en DOS variantes del modelo:
    anclada  = la parametrizacion con anclas LogNormal en diagonal (gllvm_marginal --default)
    libre    = Lam sin anclas, solo LamLam' identificado — la variante CANONICA del paper
               (asi se produjo idata_marginal_rung3.nc y la carga 0.574)

Metricas por ajuste: sesgo y cobertura HDI90 de lam (bloque lineas_sae), error Frobenius
relativo de E[LamLam'] vs verdad, correlacion de comunalidades, corr(gamma_hat, gamma_true),
R-hat maximo, divergencias.

Uso:
    python scripts/sim_identificacion.py                      # grid completo (~2-3 h)
    python scripts/sim_identificacion.py --smoke              # prueba rapida
    python scripts/sim_identificacion.py --scenarios d_referee --reps 2
    python scripts/sim_identificacion.py --plot-only          # solo la figura desde el CSV

Salidas: outputs/sim_identificacion.csv, figures/02_escalera_gllvm/fig_sim_identificacion.png
"""
import os, sys, argparse, time
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_SEED = 20260713
ANCHOR_ROWS = {"piso_tierra": None, "rezago_educ": None, "lp_ingreso": None}  # se llena con IDX
S_STATES = 32


# ----------------------------------------------------------------------------- verdades
def truths_from_posterior():
    """Extrae del posterior real (rung3 marginalizado): Lam echelon, sigma, W, nombres."""
    import arviz as az
    idata = az.from_netcdf(os.path.join(OUT, "idata_marginal_rung3.nc"))
    post = idata.posterior
    ind = list(pd.read_csv(os.path.join(OUT, "loadings_rung3_K3.csv"), index_col=0).index)
    M = post["LamLamT"].mean(("chain", "draw")).values                 # (J,J) invariante
    w, V = np.linalg.eigh(M)
    top = np.argsort(-w)[:3]
    Lam0 = V[:, top] * np.sqrt(np.maximum(w[top], 0))                  # ejes canonicos (J,3)
    # rotacion a forma echelon sobre las anclas del modelo: bloque ancla = triangular inferior
    IDX = {n: i for i, n in enumerate(ind)}
    ar = [IDX["piso_tierra"], IDX["rezago_educ"], IDX["lp_ingreso"]]
    A = Lam0[ar, :]                                                    # (3,3)
    Q, R = np.linalg.qr(A.T)                                           # A = R' Q'
    Lam = Lam0 @ Q                                                     # bloque ancla = R' (tri inf)
    for k in range(3):                                                 # diagonal positiva
        if Lam[ar[k], k] < 0:
            Lam[:, k] = -Lam[:, k]
    sigma = post["sigma"].mean(("chain", "draw")).values
    W = post["W"].mean(("chain", "draw")).values                       # (9, J)
    del idata
    return Lam, sigma, W, ind, ar


def v_sae(ind):
    v = np.zeros(len(ind))
    v[ind.index("lp_ingreso")] = 1.0
    v[ind.index("lp_ingreso_ext")] = 1.0
    return v / np.linalg.norm(v)


# ----------------------------------------------------------------------------- generador
def generate(rng, N, Lam_true, sigma_true, W_true, ind, lam_true, sg, collinear_pair=False):
    """Devuelve Y, rural, X, state, gamma_true, Lam_gen (la verdad efectiva del escenario)."""
    J = len(ind)
    K = Lam_true.shape[1]
    Lam_g = Lam_true.copy()
    sig_g = sigma_true.copy()
    if collinear_pair:
        # colinealidad VIA FACTORES (sin componente de metodo): filas identicas, uniqueness minima
        i15, i16 = ind.index("lp_ingreso"), ind.index("lp_ingreso_ext")
        row = np.zeros(K); row[:min(K, 3)] = [0.15, 0.15, 0.45][:min(K, 3)]
        Lam_g[i15] = row; Lam_g[i16] = row
        sig_g[i15] = 0.07; sig_g[i16] = 0.07
    rural = rng.standard_normal(N)
    X = rng.standard_normal((N, 7))
    A = np.column_stack([np.ones(N), rural, X])                        # (N, 9)
    state = rng.integers(0, S_STATES, size=N)
    gamma = rng.normal(0, sg, size=(J, S_STATES)) if sg > 0 else np.zeros((J, S_STATES))
    gamma -= gamma.mean(axis=1, keepdims=True)                         # suma-cero como ZeroSumNormal
    z = rng.standard_normal((N, K))
    m = rng.standard_normal(N)
    eps = rng.standard_normal((N, J)) * sig_g[None, :]
    Y = A @ W_true + gamma.T[state] + z @ Lam_g.T + lam_true * np.outer(m, v_sae(ind)) + eps
    return Y, rural, X, state, gamma, Lam_g, sig_g


# ----------------------------------------------------------------------------- ajuste
def fit_and_score(Y, ind, K_fit, rural, X, state, Lam_gen, gamma_true, lam_true,
                  draws, tune, chains, seed, free=False):
    """free=False: parametrizacion ANCLADA (LogNormal en diagonal, ceros echelon).
    free=True: Lam libre — la variante CANONICA del paper (idata_marginal_rung3.nc), donde
    lo identificado es LamLam' y los ejes se leen post-hoc por eigen-descomposicion.
    Nota honesta: la anclada exhibe multimodalidad residual cuando el ancla verdadera es
    debil (la carga echelon de lp_ingreso es 0.15, cola del prior LogNormal): una cadena
    puede caer en el modo de colapso del ancla (rhat_max ~1.8 lo delata). mload y las
    comunalidades son robustos al modo; se reporta tal cual."""
    import pymc as pm, arviz as az
    import gllvm_marginal as gm
    mod, _ = gm.build(Y, ind, K_fit, rural, X, state=state, free=free)
    t0 = time.time()
    with mod:
        idata = pm.sample(nuts_sampler="numpyro", draws=draws, tune=tune, chains=chains,
                          random_seed=seed, target_accept=0.9, progressbar=False)
    mins = (time.time() - t0) / 60
    post = idata.posterior
    ml = post["mload"].values.reshape(-1, 3)                           # bloque 1 = lineas_sae
    lam_hat = float(ml[:, 1].mean())
    # HDI 90% (no equi-cola): con lam_true=0 el posterior se apila en la frontera y el
    # intervalo correcto es [~0, x]; percentiles 5-95 nunca cubririan 0 por construccion
    q5, q95 = az.hdi(ml[:, 1], hdi_prob=0.90)
    otros = float(np.abs(ml[:, [0, 2]].mean(0)).max())
    M_hat = post["LamLamT"].mean(("chain", "draw")).values
    M_true = Lam_gen @ Lam_gen.T
    frob = float(np.linalg.norm(M_hat - M_true) / np.linalg.norm(M_true))
    cc = float(np.corrcoef(np.diag(M_hat), np.diag(M_true))[0, 1])
    g_hat = post["gamma"].mean(("chain", "draw")).values
    gt = gamma_true - gamma_true.mean(axis=1, keepdims=True)
    g_corr = float(np.corrcoef(g_hat.ravel(), gt.ravel())[0, 1]) if gt.std() > 0 else np.nan
    g_rmse = float(np.sqrt(np.mean((g_hat - gt) ** 2)))
    rh = az.rhat(idata)
    rhat_max = float(max(float(rh[v].max()) for v in
                         ["LamLamT", "mload", "sigma", "W", "gamma"] if v in rh))
    div = int(idata.sample_stats["diverging"].sum())
    del idata
    return dict(lambda_hat=round(lam_hat, 3), lambda_q5=round(float(q5), 3),
                lambda_q95=round(float(q95), 3),
                # cobertura solo definida para lam_true>0: con soporte positivo el HDI nunca
                # toca 0 exactamente; para lam_true=0 el veredicto es lambda_hat/q95 directos
                cubre_ic90=int(q5 <= lam_true <= q95) if lam_true > 0 else np.nan,
                lambda_otros_max=round(otros, 3),
                frobenius_rel=round(frob, 3), corr_comunalidades=round(cc, 3),
                gamma_corr=round(g_corr, 3) if np.isfinite(g_corr) else np.nan,
                gamma_rmse=round(g_rmse, 3),
                rhat_max=round(rhat_max, 3), divergencias=div, minutos=round(mins, 1))


# ----------------------------------------------------------------------------- escenarios
SCENARIOS = {
    #  nombre           K_true K_fit lam   sg   anclas_debiles colineal
    "a_lam0":        dict(kt=3, kf=3, lam=0.0, sg=0.5, weak=False, col=False),
    "a_lam03":       dict(kt=3, kf=3, lam=0.3, sg=0.5, weak=False, col=False),
    "a_lam06":       dict(kt=3, kf=3, lam=0.6, sg=0.5, weak=False, col=False),
    "a_lam03_sg0":   dict(kt=3, kf=3, lam=0.3, sg=0.0, weak=False, col=False),
    "b_anclas":      dict(kt=3, kf=3, lam=0.3, sg=0.5, weak=True,  col=False),
    "c_gen2_fit3":   dict(kt=2, kf=3, lam=0.3, sg=0.5, weak=False, col=False),
    "c_gen3_fit2":   dict(kt=3, kf=2, lam=0.3, sg=0.5, weak=False, col=False),
    "d_referee":     dict(kt=3, kf=3, lam=0.0, sg=0.5, weak=False, col=True),
}


def run(args):
    Lam3, sigma, W, ind, ar = truths_from_posterior()
    print("diag ancla (verdad echelon):", np.round(Lam3[ar, [0, 1, 2]], 3))
    csv_path = os.path.join(OUT, "sim_identificacion.csv")
    names = args.scenarios.split(",") if args.scenarios else list(SCENARIOS)
    variantes = ["anclada", "libre"] if args.variant == "both" else [args.variant]
    # preservar filas previas de otras celdas (variante, escenario, rep) ya corridas
    if os.path.exists(csv_path):
        old = pd.read_csv(csv_path)
        if "variante" not in old.columns:
            old.insert(0, "variante", "anclada")
        keep = ~(old["variante"].isin(variantes) & old["escenario"].isin(names)
                 & (old["rep"] < args.reps))
        rows = old[keep].to_dict("records")
    else:
        rows = []
    for variante in variantes:
        for name in names:
            sc = SCENARIOS[name]
            for rep in range(args.reps):
                Lam_t = Lam3[:, :sc["kt"]].copy()
                if sc["weak"]:
                    Lam_t[ar, :] *= 0.15                               # anclas del modelo, debiles
                seed = BASE_SEED + 1000 * list(SCENARIOS).index(name) + rep
                rng = np.random.default_rng(seed)
                Y, rural, X, state, g_true, Lam_g, sig_g = generate(
                    rng, args.n, Lam_t, sigma, W, ind, sc["lam"], sc["sg"],
                    collinear_pair=sc["col"])
                # corr realizada del par lp tras quitar la estructura de media verdadera
                A = np.column_stack([np.ones(args.n), rural, X])
                R = Y - A @ W - g_true.T[state]
                i15, i16 = ind.index("lp_ingreso"), ind.index("lp_ingreso_ext")
                corr_par = float(np.corrcoef(R[:, i15], R[:, i16])[0, 1])
                print(f"\n=== {variante} | {name} rep{rep} (seed {seed}) | "
                      f"lam_true={sc['lam']} sg={sc['sg']} K {sc['kt']}->{sc['kf']} | "
                      f"corr par lp={corr_par:.3f} ===", flush=True)
                res = fit_and_score(Y, ind, sc["kf"], rural, X, state, Lam_g, g_true,
                                    sc["lam"], args.draws, args.tune, args.chains, seed,
                                    free=(variante == "libre"))
                row = dict(variante=variante, escenario=name, rep=rep, seed=seed,
                           K_true=sc["kt"], K_fit=sc["kf"], lambda_true=sc["lam"],
                           sigma_gamma_true=sc["sg"], corr_par_lp=round(corr_par, 3), **res)
                rows.append(row)
                print(row, flush=True)
                pd.DataFrame(rows).to_csv(csv_path, index=False)       # checkpoint incremental
    print(f"\n{csv_path} listo ({len(rows)} filas)")
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- figura
def make_figure(df):
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    import plotstyle as ps
    ps.use()
    FIG = ps.figdir("02_escalera_gllvm")
    if "variante" not in df.columns:
        df = df.copy(); df.insert(0, "variante", "anclada")
    order = [s for s in SCENARIOS if s in set(df["escenario"])]
    lab = {"a_lam0": "bien esp.\nλ=0", "a_lam03": "bien esp.\nλ=0.3",
           "a_lam06": "bien esp.\nλ=0.6", "a_lam03_sg0": "sin γ real\nλ=0.3",
           "b_anclas": "anclas\ndébiles", "c_gen2_fit3": "K 2→3",
           "c_gen3_fit2": "K 3→2", "d_referee": "referee:\ncolineal, λ=0"}
    MK = {"anclada": "o", "libre": "D"}
    OFF = {"anclada": -1, "libre": +1}
    variantes = [v for v in ["anclada", "libre"] if v in set(df["variante"])]
    fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.5),
                             gridspec_kw=dict(width_ratios=[2.1, 1, 1], wspace=0.3))
    ax = axes[0]
    for i, s in enumerate(order):
        ax.hlines(df.loc[df["escenario"] == s, "lambda_true"].iloc[0],
                  i - 0.38, i + 0.38, color=ps.INK2, lw=1.4, zorder=3)
        for v in variantes:
            sub = df[(df["escenario"] == s) & (df["variante"] == v)]
            col = ps.RED if s == "d_referee" else ps.BLUE
            for k, (_, r) in enumerate(sub.iterrows()):
                x = i + OFF[v] * 0.13 + (k - (len(sub) - 1) / 2) * 0.09
                ax.errorbar(x, r["lambda_hat"],
                            yerr=[[max(r["lambda_hat"] - r["lambda_q5"], 0)],
                                  [max(r["lambda_q95"] - r["lambda_hat"], 0)]],
                            fmt=MK[v], ms=4 if v == "libre" else 4.5,
                            mfc=col if v == "anclada" else "none",
                            color=col, ecolor=col, elinewidth=1.1, capsize=2.2, zorder=4)
    ax.set_xticks(range(len(order)), [lab[s].replace("\n", " ") for s in order],
                  fontsize=7, rotation=25, ha="right")
    ax.set_ylabel("carga de método λ̂ (líneas SAE), HDI 90%")
    ax.set_title("a. Recuperación de la carga de método", loc="left", fontsize=9)
    ax.axhline(0, color=ps.GRID, lw=0.8, zorder=1)
    ax.grid(axis="y", alpha=0.6)
    ax.legend(handles=[
        Line2D([], [], marker="o", ls="", color=ps.BLUE, ms=4.5, label="anclada"),
        Line2D([], [], marker="D", ls="", color=ps.BLUE, mfc="none", ms=4, label="libre (ΛΛᵀ)"),
        Line2D([], [], color=ps.INK2, lw=1.4, label="verdad")],
        frameon=False, fontsize=7, loc="upper left")

    for ax, colname, tit, ylim in [
            (axes[1], "frobenius_rel", "b. Error rel. de ΛΛᵀ (Frobenius)", None),
            (axes[2], "corr_comunalidades", "c. Corr. de comunalidades", (0, 1.05))]:
        for i, s in enumerate(order):
            for v in variantes:
                sub = df[(df["escenario"] == s) & (df["variante"] == v)]
                col = ps.RED if s == "d_referee" else ps.BLUE
                ax.scatter([i + OFF[v] * 0.14] * len(sub), sub[colname], s=20,
                           marker=MK[v], facecolors=col if v == "anclada" else "none",
                           edgecolors=col, zorder=4)
        ax.set_xticks(range(len(order)), [lab[s].replace("\n", " ") for s in order],
                      fontsize=6, rotation=60, ha="right")
        ax.set_title(tit, loc="left", fontsize=9)
        ax.grid(axis="y", alpha=0.6)
        if ylim:
            ax.set_ylim(*ylim)
    fig.suptitle("Simulación de identificación: N=1,000, J=17, verdades del posterior real, "
                 "2 réplicas por escenario y variante", y=1.02, fontsize=9, color=ps.INK2)
    p = os.path.join(FIG, "fig_sim_identificacion.png")
    fig.savefig(p, bbox_inches="tight")
    print(p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--draws", type=int, default=500)
    ap.add_argument("--tune", type=int, default=500)
    ap.add_argument("--chains", type=int, default=2)
    ap.add_argument("--scenarios", default="", help="lista separada por comas; vacio = todos")
    ap.add_argument("--variant", default="both", choices=["anclada", "libre", "both"],
                    help="anclada = LogNormal en diagonal; libre = solo LamLam' (canonica)")
    ap.add_argument("--smoke", action="store_true", help="rapido: N=400, 150/150, 1 rep")
    ap.add_argument("--plot-only", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        args.n, args.draws, args.tune, args.reps = 400, 150, 150, 1
    if args.plot_only:
        df = pd.read_csv(os.path.join(OUT, "sim_identificacion.csv"))
    else:
        df = run(args)
    make_figure(df)


if __name__ == "__main__":
    main()
