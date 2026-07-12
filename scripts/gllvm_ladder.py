#!/usr/bin/env python
"""
GLLVM espacial bayesiano — escalera de 4 peldaños.
Marginación (CONAPO) vs. pobreza multidimensional (CONEVAL), municipios México 2020.

Modelo (verosimilitud GAUSSIANA en escala logit para los 17 indicadores; los SAE de CONEVAL
son estimaciones modeladas, NO conteos -> tratarlos como binomiales daría precisión falsa):

    eta_ij = alpha_j + lambda_j' z_i + beta_r,j * ruralidad_i + beta_D,j' x_i + m_ij
    Y_ij  ~ Normal(eta_ij, sigma_j)        # sigma_j = uniqueness específica por indicador

    z_i : factores latentes. K=2 = (material, monetario); K=3 = (material, educativo, monetario)
          Peldaño 4: z recibe estructura BYM2 (mezcla iid + ICAR) POR factor.
    ruralidad_i = loc_peq_pct estandarizado (ÚNICO eje urbano-rural; urbano ≡ 100 - loc_peq)
    x_i : cofactores Vista D (remesas log pc, empleo precario, demografía, mezcla sectorial, log pob)
    m_ij: bloques de método (educación / líneas de ingreso / vivienda-servicios)

Escalera (cada peldaño responde una pregunta distinta):
    rung1 base        -> ¿qué miden los factores solos?
    rung2 +VistaD     -> ¿cuánto de eso era composición observable?   (ruralidad + cofactores)
    rung3 +estado     -> ¿cuánto era geografía discreta?              (rung2 + efectos fijos estatales)
    rung4 +BYM2 en z  -> ¿queda estructura espacial suave?            (rung2 + BYM2, SIN estado)
    * rung3 y rung4 son DOS geografías alternativas sobre rung2, NO se apilan (compiten por varianza).

Comparabilidad: mismas anclas en los 4 peldaños; las cargas de cada peldaño se alinean por
Procrustes contra el PELDAÑO 1 como referencia común -> "cuánto cambia cada carga" mide cambio
real (marginal->condicional), no rotación.

Uso:
    python scripts/gllvm_ladder.py --K 3 --rung all --sampler numpyro
    python scripts/gllvm_ladder.py --K 2 --rung 4 --draws 1500 --tune 1500

Salidas en outputs/:
    idata_rungN_K{K}.nc, loadings_rungN_K{K}.csv (alineadas a rung1),
    zscores_rungN_K{K}.csv (media + sd por municipio), vardecomp_rungN_K{K}.csv,
    ladder_summary_K{K}.csv
"""
import os, argparse, json
# --- setup pytensor tolerante al sandbox (inofensivo en una máquina normal) ---
def _safe_pytensor_env():
    home = os.environ.get("HOME", "")
    ok = False
    if home:
        try:
            os.makedirs(os.path.join(home, ".pytensor"), exist_ok=True); ok = True
        except Exception:
            ok = False
    if not ok:
        wd = os.getcwd(); cdir = os.path.join(wd, ".pytensor"); os.makedirs(cdir, exist_ok=True)
        os.environ.setdefault("PYTENSOR_FLAGS", f"base_compiledir={cdir}")
        os.environ.setdefault("HOME", wd)
_safe_pytensor_env()

import numpy as np, pandas as pd, pymc as pm, pytensor.tensor as pt, arviz as az
from scipy.linalg import orthogonal_procrustes
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
SPAT = os.path.join(HERE, "spatial")
OUT  = os.path.join(HERE, "outputs"); os.makedirs(OUT, exist_ok=True)

ANCHOR = {"material": "sin_agua", "educativo": "rezago_educ", "monetario": "lp_ingreso"}
METHOD_BLOCKS = [
    ["analf", "sin_basica", "rezago_educ"],                                   # educación
    ["lp_ingreso", "lp_ingreso_ext"],                                         # líneas de ingreso
    ["sin_drenaje", "sin_electr", "sin_agua", "car_vivienda", "car_servbas"], # vivienda-servicios
]
COFACTORS = ["remesas_log", "empleo_precario_pct", "dep_ratio", "pct_60mas",
             "pct_primario", "pct_secundario", "log_pob"]


def load_data():
    Y = pd.read_parquet(os.path.join(PROC, "gllvm_Y.parquet"))       # 2455 x 17, logit-z
    cov = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet")).copy()
    assert len(Y) == len(cov), f"{len(Y)} vs {len(cov)}"
    ind = list(Y.columns)
    rural = ((cov["loc_peq_pct"] - cov["loc_peq_pct"].mean()) / cov["loc_peq_pct"].std()).values
    cov["remesas_log"] = np.log1p(cov["remesas_pc_usd"])
    X = cov[COFACTORS].copy(); X = ((X - X.mean()) / X.std()).values
    state = cov["cvegeo"].str[:2].astype("category").cat.codes.values
    return Y.values.astype(float), ind, rural, X, state, cov["cvegeo"].values


def load_spatial():
    z = np.load(os.path.join(SPAT, "icar_edges.npz"))
    n1, n2, N = z["node1"], z["node2"], int(z["n"])
    A = csr_matrix((np.ones(len(n1) * 2), (np.r_[n1, n2], np.r_[n2, n1])), shape=(N, N))
    ncomp, labels = connected_components(A, directed=False)
    scale = bym2_scale(n1, n2, N, labels)   # factor de escala ICAR (Riebler et al. 2016)
    return (n1, n2), labels, ncomp, scale


def bym2_scale(n1, n2, N, labels):
    """Escala del ICAR para varianza marginal ~1 (media geométrica de la diag de la pseudo-inversa
    del Laplaciano), calculada por componente conexo. Solo se corre una vez."""
    A = np.zeros((N, N))
    A[n1, n2] = 1; A[n2, n1] = 1
    D = np.diag(A.sum(1))
    Q = D - A
    diag_inv = np.zeros(N)
    for c in np.unique(labels):
        idx = np.where(labels == c)[0]
        if len(idx) < 2:
            diag_inv[idx] = 1.0; continue
        Qc = Q[np.ix_(idx, idx)]
        inv = np.linalg.pinv(Qc)               # pinv (SVD) descarta el modo nulo automáticamente
        diag_inv[idx] = np.diag(inv)
    return float(np.exp(np.mean(np.log(diag_inv[diag_inv > 0]))))


def build_gllvm(Y, ind, K, rural=None, X=None, state=None,
                edges=None, comp_labels=None, sp_scale=1.0):
    N, J = Y.shape
    IDX = {n: i for i, n in enumerate(ind)}
    facs = ["material", "monetario"] if K == 2 else ["material", "educativo", "monetario"]
    anchor_rows = [IDX[ANCHOR[f]] for f in facs]
    mask = np.ones((J, K))
    for r, ar in enumerate(anchor_rows):
        for c in range(r + 1, K):
            mask[ar, c] = 0.0
    with pm.Model() as mod:
        Loff = pm.Normal("Loff", 0, 1, shape=(J, K))
        diag = pm.HalfNormal("diag", 1.0, shape=K)          # diagonal positiva -> fija signo/etiqueta
        Lm = Loff * mask
        for k, ar in enumerate(anchor_rows):
            Lm = pt.set_subtensor(Lm[ar, k], diag[k])
        Lam = pm.Deterministic("Lam", Lm)

        # --- factores latentes z (BYM2 por factor en el peldaño espacial, iid en el resto) ---
        if edges is not None:
            n1, n2 = edges
            rho = pm.Beta("rho_sp", 2, 2, shape=K)          # mezcla: proporción espacial POR factor = métrica 4
            theta = pm.Normal("theta", 0, 1, shape=(N, K))  # componente no estructurado
            phi = pm.Normal("phi", 0, 1, shape=(N, K))      # componente estructurado (ICAR)
            for k in range(K):
                pm.Potential(f"icar_{k}", -0.5 * pt.sum(pt.sqr(phi[n1, k] - phi[n2, k])))
            for c in np.unique(comp_labels):                # suma-cero suave por componente conexo
                idx = np.where(comp_labels == c)[0]
                pm.Potential(f"sz_{c}", -0.5 * pt.sqr(pt.sum(phi[idx, :], axis=0)).sum() * 0.001)
            # BYM2: z = sqrt(1-rho)*theta + sqrt(rho/scale)*phi  -> varianza marginal ~1 (identificación)
            z = pm.Deterministic(
                "z", pt.sqrt(1 - rho)[None, :] * theta
                      + pt.sqrt(rho / sp_scale)[None, :] * phi)
        else:
            z = pm.Normal("z", 0, 1, shape=(N, K))

        alpha = pm.Normal("alpha", 0, 2, shape=J)
        eta = alpha + pm.math.dot(z, Lam.T)
        if rural is not None:
            br = pm.Normal("beta_rural", 0, 0.5, shape=J)
            eta = eta + pt.as_tensor_variable(rural)[:, None] * br[None, :]
        if X is not None:
            bD = pm.Normal("betaD", 0, 0.5, shape=(X.shape[1], J))
            eta = eta + pt.dot(pt.as_tensor_variable(X), bD)
        if state is not None:
            S = int(state.max()) + 1
            gam = pm.ZeroSumNormal("gamma", sigma=0.5, shape=(J, S))
            eta = eta + gam.T[pt.as_tensor_variable(state)]
        for bi, blk in enumerate(METHOD_BLOCKS):
            mf = pm.Normal(f"mfac{bi}", 0, 1, shape=N)
            lm = pm.HalfNormal(f"mload{bi}", 0.5)
            idxs = [IDX[n] for n in blk]
            eta = pt.set_subtensor(eta[:, idxs], eta[:, idxs] + (lm * mf)[:, None])
        sigma = pm.HalfNormal("sigma", 1.0, shape=J)
        pm.Normal("Y", eta, sigma, observed=Y)
    return mod, facs


def procrustes_to_ref(idata, ref):
    """Alinea las cargas de un posterior contra una matriz de referencia (peldaño 1) por draw."""
    L = idata.posterior["Lam"].values  # (chain, draw, J, K)
    C, D, J, K = L.shape
    draws = np.empty((C * D, J, K)); i = 0
    for c in range(C):
        for d in range(D):
            R, _ = orthogonal_procrustes(L[c, d], ref); draws[i] = L[c, d] @ R; i += 1
    return draws.mean(0), draws.std(0)


def residual_moran(Y, eta_mean, edges):
    n1, n2 = edges; N = Y.shape[0]; W = 2 * len(n1); Is = []
    for j in range(Y.shape[1]):
        r = Y[:, j] - eta_mean[:, j]; r = r - r.mean()
        Is.append((N / W) * (np.sum(r[n1] * r[n2]) * 2) / np.sum(r ** 2))
    return float(np.mean(Is)), Is


def variance_decomposition(idata, ind, rural, X, state):
    """Descompone la varianza de eta_ij (por indicador) en las contribuciones aditivas del modelo,
    usando las medias posteriores de cada término. Devuelve un DataFrame indicador x bloque con la
    fracción de varianza atribuible a: factores latentes, ruralidad, cofactores, estado, método,
    espacial, y uniqueness (sigma_j^2). Las fracciones suman ~1 por indicador."""
    post = idata.posterior
    N, J = len(rural), len(ind)
    m = lambda v: post[v].mean(("chain", "draw")).values

    # E[z Lam'] draw a draw (invariante a rotación/reflexión de los factores; promediar
    # z y Lam por separado entre cadenas se cancela si hay label switching)
    zL = np.zeros((N, J)); ndraw = 0
    zday = post["z"].values; Lday = post["Lam"].values  # (C,D,N,K), (C,D,J,K)
    for c in range(zday.shape[0]):
        for d in range(zday.shape[1]):
            zL += zday[c, d] @ Lday[c, d].T; ndraw += 1
    contrib = {"factores": zL / ndraw}                  # (N,J)
    if "beta_rural" in post:
        contrib["ruralidad"] = rural[:, None] * m("beta_rural")[None, :]
    if "betaD" in post:
        contrib["cofactores"] = X @ m("betaD")
    if "gamma" in post:                                 # gamma: (J,S) -> por municipio via state
        gam = m("gamma"); contrib["estado"] = gam.T[state]
    # bloques de método
    meth = np.zeros((N, J)); IDX = {n: i for i, n in enumerate(ind)}
    bi = 0
    while f"mfac{bi}" in post:
        mf = m(f"mfac{bi}"); lm = float(m(f"mload{bi}"))
        for name in METHOD_BLOCKS[bi]:
            meth[:, IDX[name]] += lm * mf
        bi += 1
    if meth.any():
        contrib["metodo"] = meth
    # espacial: si z ya incluye BYM2, su varianza estructurada está dentro de "factores";
    # reportamos aparte la fracción espacial de z via rho para trazabilidad
    var_by_block = {b: np.var(c, axis=0) for b, c in contrib.items()}   # (J,) por bloque
    uniqueness = m("sigma") ** 2                                         # (J,)
    var_by_block["uniqueness"] = uniqueness
    total = np.sum(list(var_by_block.values()), axis=0)
    frac = {b: v / total for b, v in var_by_block.items()}
    df = pd.DataFrame(frac, index=ind)
    df.index.name = "indicador"
    return df


def run_rung(rung, K, data, spatial, sampler, draws, tune, chains, seed, ref_loadings):
    Y, ind, rural, X, state, cvegeo = data
    edges, comp_labels, _, sp_scale = spatial
    kw = dict(rural=None, X=None, state=None, edges=None, comp_labels=None, sp_scale=sp_scale)
    # rung2,3,4 TODOS incluyen Vista D; rung3=+estado; rung4=+BYM2 (SIN estado, no se apilan)
    if rung >= 2: kw.update(rural=rural, X=X)
    if rung == 3: kw.update(state=state)
    if rung == 4: kw.update(edges=edges, comp_labels=comp_labels)
    mod, facs = build_gllvm(Y, ind, K, **kw)
    sk = dict(draws=draws, tune=tune, chains=chains, random_seed=seed,
              target_accept=0.9, progressbar=True)
    with mod:
        if sampler in ("numpyro", "nutpie", "blackjax"):
            idata = pm.sample(nuts_sampler=sampler, **sk)
        else:
            idata = pm.sample(cores=chains, init="jitter+adapt_diag", **sk)
        idata.extend(pm.sample_posterior_predictive(idata, progressbar=False))
        # log-verosimilitud pointwise para ELPD-LOO (PyMC no la guarda por defecto -> az.loo daría NaN)
        pm.compute_log_likelihood(idata, progressbar=False)

    ref = ref_loadings if ref_loadings is not None else idata.posterior["Lam"].values[0].mean(0)
    Lam_mean, Lam_sd = procrustes_to_ref(idata, ref)
    pd.DataFrame(Lam_mean, index=ind, columns=facs).to_csv(
        os.path.join(OUT, f"loadings_rung{rung}_K{K}.csv"))
    # z por municipio (media + sd): alineado POR CADENA contra ref (las anclas fijan el modo,
    # pero si una cadena cae en otra rotación, el promedio ingenuo entre cadenas se cancela)
    zch = idata.posterior["z"].values          # (C, D, N, K)
    Lch = idata.posterior["Lam"].values
    zrot = np.empty_like(zch)
    for c in range(zch.shape[0]):
        R, _ = orthogonal_procrustes(Lch[c].mean(0), ref)
        zrot[c] = zch[c] @ R
    zmean = zrot.mean((0, 1)); zsd = zrot.std((0, 1))
    zc = pd.DataFrame(np.hstack([zmean, zsd]),
                      columns=[f"{f}_mean" for f in facs] + [f"{f}_sd" for f in facs])
    zc.insert(0, "cvegeo", cvegeo)
    zc.to_csv(os.path.join(OUT, f"zscores_rung{rung}_K{K}.csv"), index=False)

    # descomposición de varianza por bloque (indicador x bloque, fracciones que suman ~1)
    vardec = variance_decomposition(idata, ind, rural, X, state)
    vardec.to_csv(os.path.join(OUT, f"vardecomp_rung{rung}_K{K}.csv"))

    eta_mean = idata.posterior_predictive["Y"].mean(("chain", "draw")).values
    mI, _ = residual_moran(Y, eta_mean, edges)
    rh = az.rhat(idata)
    rhat_stable = float(max(float(rh[v].max()) for v in ["alpha", "sigma"] if v in rh))
    try: elpd = float(az.loo(idata).elpd_loo)
    except Exception: elpd = float("nan")
    # no persistir la log-verosimilitud (4 cadenas x draws x 2455 x 17 ~ GBs en el .nc)
    if hasattr(idata, "log_likelihood"):
        del idata.log_likelihood
    rho_str = ""
    if "rho_sp" in idata.posterior:
        rho = idata.posterior["rho_sp"].mean(("chain", "draw")).values
        rho_str = "|".join(f"{f}:{r:.2f}" for f, r in zip(facs, rho))
    idata.to_netcdf(os.path.join(OUT, f"idata_rung{rung}_K{K}.nc"))
    return dict(rung=rung, K=K, facs="|".join(facs), residual_moran_I=round(mI, 4),
                rhat_alpha_sigma=round(rhat_stable, 3), elpd_loo=round(elpd, 1),
                mean_latent_sd=round(float(zsd.mean()), 3), rho_spatial=rho_str), Lam_mean


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--K", type=int, default=3, choices=[2, 3])
    ap.add_argument("--rung", default="all", help="1|2|3|4|all")
    ap.add_argument("--sampler", default="numpyro", help="numpyro|nutpie|pymc")
    ap.add_argument("--draws", type=int, default=1000)
    ap.add_argument("--tune", type=int, default=1000)
    ap.add_argument("--chains", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    data = load_data(); spatial = load_spatial()
    print(f"N={len(data[0])} municipios, J={data[0].shape[1]} indicadores, "
          f"componentes espaciales={spatial[2]}, escala BYM2={spatial[3]:.3f}")
    rungs = [1, 2, 3, 4] if a.rung == "all" else [int(a.rung)]
    rows, ref = [], None
    for r in rungs:
        print(f"\n=== Rung {r} (K={a.K}) ===")
        row, Lam = run_rung(r, a.K, data, spatial, a.sampler, a.draws, a.tune,
                            a.chains, a.seed, ref)
        if r == 1 or ref is None:
            ref = Lam  # el peldaño 1 fija la referencia común de rotación
        rows.append(row)
        pd.DataFrame(rows).to_csv(os.path.join(OUT, f"ladder_summary_K{a.K}.csv"), index=False)
        print(row)
    print("\nResumen escalera:\n", pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
