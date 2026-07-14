#!/usr/bin/env python
"""
GLLVM MARGINALIZADO HETEROSCEDÁSTICO — Nivel 1 del Bloque 1 (revisión Paper 1).

COPIA MODIFICADA de scripts/gllvm_marginal.py (el original queda intacto; otras corridas
lo usan). Cambio único de especificación: para los 4 indicadores SAE de CONEVAL
(car_segsoc, car_alim, lp_ingreso, lp_ingreso_ext — los MODELADOS por áreas pequeñas
según dict/diccionario_indicadores.csv), la unicidad deja de ser homoscedástica:

    antes:   Sigma      = Lam Lam' + sum_b lm_b^2 v_b v_b' + diag(sigma_j^2)
    ahora:   Sigma_i    = Lam Lam' + sum_b lm_b^2 v_b v_b' + diag(sigma_j^2 + se_ji^2)

con se_ji^2 = varianza de error de medición CONOCIDA por municipio, derivada de las
bandas oficiales de precisión de CONEVAL (data/processed/sae_se_municipal.parquet,
construida por scripts/build_sae_se.py; se en la MISMA escala que gllvm_Y).

IMPLEMENTACIÓN POR BANDAS DE se (nota de ingeniería): la primera versión usó MvNormal con
covarianza batched (2,455 x 17 x 17) — 2,455 choleskys POR GRADIENTE; las cadenas quedaron
en 8-80 s/iteración (inviable). Se reemplaza por la agrupación que ya contemplaban las
instrucciones: k-means (seed fija) sobre el vector (se_segsoc, se_alim, se_lp, se_lp_ext)
-> G=64 bandas; los municipios de una banda comparten diag(se_g^2) y su verosimilitud es
una MvNormal ESTÁNDAR por banda (64 choleskys por gradiente, costo ~ baseline). El error
de cuantización se reporta al construir (mediana ~0.01 en unidades de Y, sd(Y)=1). Los
scores E[z|Y] usan el se2 EXACTO por municipio (la banda solo aproxima la verosimilitud
del muestreo). La log-verosimilitud puntual (LOO) se re-ensambla al orden original.

Las dos preguntas que responde la corrida (outputs/nivel1_hetero_resumen.csv):
  (a) ¿mload de la familia lineas_sae (0.574 en el rung3 canónico) sobrevive al
      reconocer el error de medición oficial?
  (b) ¿La "geografía de la incertidumbre" (sd posterior de los ejes canónicos:
      corr +0.322 con log_pob, -0.259 con loc_peq_pct) sobrevive, cae o se invierte?
      Nota previa: el se oficial es MAYOR en municipios chicos/rurales
      (corr(se, log_pob) entre -0.34 y -0.56), lo contrario del patrón que el modelo
      homoscedástico atribuía a la sustancia.

Uso (canónico = sin anclas, como la corrida publicada):
    python scripts/gllvm_marginal_hetero.py --rung 3 --free --draws 1000 --tune 1000 --chains 4
"""
import os, argparse
import numpy as np, pandas as pd
import pymc as pm, pytensor.tensor as pt, arviz as az
from scipy.linalg import orthogonal_procrustes
import gllvm_ladder as gl

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")
PROC = os.path.join(HERE, "data", "processed")

# los 4 indicadores SAE (MODELADA ENIGH+SAE / EBPH-SAE en dict/diccionario_indicadores.csv)
SAE = ["car_segsoc", "car_alim", "lp_ingreso", "lp_ingreso_ext"]

CONTRASTES = {
    0: {"analf": .5, "sin_basica": .5, "rezago_educ": -1.0},              # educación
    1: {"lp_ingreso": 1.0, "lp_ingreso_ext": 1.0},                        # SAE-EBPH
    2: {"sin_drenaje": 1/3, "sin_electr": 1/3, "sin_agua": 1/3,
        "car_vivienda": -.5, "car_servbas": -.5},                          # vivienda-servicios
}
FAMILIAS = ["educacion", "lineas_sae", "viv_servicios"]


def load_se2(ind, cvegeo):
    """Matriz (N, J) de varianzas de error de medición conocidas: se^2 en escala gllvm_Y
    para los indicadores SAE, 0 para el resto."""
    se = pd.read_parquet(os.path.join(PROC, "sae_se_municipal.parquet"))
    se["cvegeo"] = se["cvegeo"].astype(str).str.zfill(5)
    se = se.set_index("cvegeo").reindex(pd.Series(cvegeo).astype(str).str.zfill(5))
    se2 = np.zeros((len(se), len(ind)))
    for j, n in enumerate(ind):
        if n in SAE:
            col = se[f"se_{n}"].values.astype(float)
            assert not np.isnan(col).any(), f"se_{n} con NaN tras imputación"
            se2[:, j] = col ** 2
    return se2


def agrupar_se(se2, G=64, seed=11):
    """k-means sobre el vector municipal de se (escala Y) -> (se2 por banda (G,J),
    índice de banda (N,), error de cuantización)."""
    from sklearn.cluster import KMeans
    se = np.sqrt(se2)
    cols = np.where(se2.any(axis=0))[0]                 # solo los indicadores SAE
    km = KMeans(n_clusters=G, random_state=seed, n_init=4).fit(se[:, cols])
    gidx = km.labels_
    se_g = np.zeros((G, se2.shape[1]))
    se_g[:, cols] = km.cluster_centers_
    err = np.abs(se - se_g[gidx])[:, cols]
    print(f"bandas de se: G={G} | error de cuantización |se_banda - se_exacto|: "
          f"mediana={np.median(err):.4f} p95={np.quantile(err, .95):.4f} "
          f"max={err.max():.4f} (unidades de Y, sd=1)")
    return se_g ** 2, gidx


def build(Y, ind, K, rural, X, se2g, gidx, state=None, free=False):
    N, J = Y.shape
    IDX = {n: i for i, n in enumerate(ind)}
    facs = ["material", "educativo", "monetario"]
    anchor_rows = [IDX[gl.ANCHOR[f]] for f in facs][:K]
    mask = np.ones((J, K))
    for r, ar in enumerate(anchor_rows):
        for c in range(r + 1, K):
            mask[ar, c] = 0.0
    A_cols = [np.ones(N), rural] + [X[:, j] for j in range(X.shape[1])]
    A = np.column_stack(A_cols)                         # (N, 2+P) diseño de la media
    with pm.Model() as mod:
        if free:
            Lam = pm.Normal("Lam", 0, 1, shape=(J, K))
        else:
            Loff = pm.Normal("Loff", 0, 1, shape=(J, K))
            diag = pm.LogNormal("diag", np.log(0.5), 0.4, shape=len(anchor_rows))
            Lm = Loff * mask
            for k, ar in enumerate(anchor_rows):
                Lm = pt.set_subtensor(Lm[ar, k], diag[k])
            Lam = pm.Deterministic("Lam", Lm)
        W = pm.Normal("W", 0, 1.0, shape=(A.shape[1], J))          # alpha, beta_r, B
        mu = pt.dot(pt.as_tensor_variable(A), W)
        if state is not None:
            S = int(state.max()) + 1
            gam = pm.ZeroSumNormal("gamma", sigma=0.5, shape=(J, S))
            mu = mu + gam.T[pt.as_tensor_variable(state)]
        lms = pm.HalfNormal("mload", 0.5, shape=len(CONTRASTES))
        sigma = pm.HalfNormal("sigma", 1.0, shape=J)
        Cov = pt.dot(Lam, Lam.T) + pt.diag(sigma ** 2)
        for bi, cvec in CONTRASTES.items():
            v = np.zeros(J)
            for n, w in cvec.items():
                v[IDX[n]] = w
            v = v / np.linalg.norm(v)
            vv = pt.as_tensor_variable(v)
            Cov = Cov + (lms[bi] ** 2) * pt.outer(vv, vv)
        pm.Deterministic("LamLamT", pt.dot(Lam, Lam.T))
        # === MODIFICACIÓN NIVEL 1: error de medición conocido en la diagonal, POR BANDA ===
        # los municipios de la banda g comparten diag(se_g^2): una MvNormal estándar por
        # banda (G choleskys por gradiente, no 2,455)
        G = se2g.shape[0]
        for g in range(G):
            idxs = np.where(gidx == g)[0]
            if len(idxs) == 0:
                continue
            Cov_g = Cov + pt.diag(pt.as_tensor_variable(se2g[g]))
            pm.MvNormal(f"Y_{g}", mu=mu[idxs], cov=Cov_g, observed=Y[idxs])
    return mod, facs


def loglik_conjunta(idata, gidx):
    """Re-ensambla la log-verosimilitud puntual de las G bandas al orden municipal
    original -> az.loo comparable con el baseline (una fila por municipio)."""
    import xarray as xr
    ll = idata.log_likelihood
    N = len(gidx)
    ejemplo = ll[list(ll.data_vars)[0]]
    C, D = ejemplo.sizes["chain"], ejemplo.sizes["draw"]
    out = np.empty((C, D, N))
    for g in np.unique(gidx):
        v = f"Y_{g}"
        if v not in ll:
            continue
        out[:, :, np.where(gidx == g)[0]] = ll[v].values
    ds = xr.Dataset({"Y": (("chain", "draw", "Y_dim_0"), out)},
                    coords={"chain": ejemplo.chain, "draw": ejemplo.draw,
                            "Y_dim_0": np.arange(N)})
    return az.InferenceData(posterior=idata.posterior, log_likelihood=ds,
                            sample_stats=idata.sample_stats)


def _cov_por_municipio(Lam, sig, lms, se2, ind):
    """Cov (J,J) base del draw + diag(se2_i) -> (N, J, J)."""
    J = len(ind)
    Cov = Lam @ Lam.T + np.diag(sig ** 2)
    for bi, cvec in CONTRASTES.items():
        v = np.zeros(J)
        for n, w in cvec.items():
            v[ind.index(n)] = w
        v = v / np.linalg.norm(v)
        Cov += (lms[bi] ** 2) * np.outer(v, v)
    return Cov[None, :, :] + np.eye(J)[None, :, :] * se2[:, None, :]


def scores_canonicos(idata, Y, ind, rural, X, state, se2, thin=4):
    """E[z|Y] y sd posterior POR MUNICIPIO en los ejes canónicos (eigen de E[LamLamT],
    signo del elemento mayor positivo; los ejes de cada draw se alinean al canónico por
    Procrustes). Sigma por municipio (base + diag(se2_i)); con se2=0 replica el canónico
    homoscedástico publicado."""
    post = idata.posterior
    C, D = post.sizes["chain"], post.sizes["draw"]
    N, K = len(Y), post["Lam"].shape[-1]
    M = post["LamLamT"].mean(("chain", "draw")).values
    w, V = np.linalg.eigh(M)
    orden = np.argsort(-w)[:K]
    Acan = V[:, orden] * np.sqrt(np.maximum(w[orden], 0))
    for k in range(K):
        if Acan[np.abs(Acan[:, k]).argmax(), k] < 0:
            Acan[:, k] = -Acan[:, k]
    A = np.column_stack([np.ones(N), rural] + [X[:, j] for j in range(X.shape[1])])
    zs_m, zs_v = [], []
    for c in range(C):
        for d in range(0, D, thin):
            Lam = post["Lam"].values[c, d]
            sig = post["sigma"].values[c, d]
            lms = post["mload"].values[c, d]
            mu = A @ post["W"].values[c, d]
            if "gamma" in post:
                mu = mu + post["gamma"].values[c, d].T[state]
            Covn = _cov_por_municipio(Lam, sig, lms, se2, ind)   # (N, J, J)
            Si = np.linalg.inv(Covn)
            R, _ = orthogonal_procrustes(Lam, Acan)             # Lam R ~ Acan
            resid = Y - mu
            # z_i = R' Lam' Si_i r_i ; Var_i = R' (I - Lam' Si_i Lam) R
            LtSi = np.einsum("jk,njl->nkl", Lam, Si)            # (N, K, J)
            z = np.einsum("nkj,nj->nk", LtSi, resid) @ R        # (N, K) canónico
            Vc = np.eye(K)[None] - np.einsum("nkj,jl->nkl", LtSi, Lam)   # (N, K, K)
            zs_m.append(z)
            zs_v.append(np.einsum("nkk->nk", np.einsum("ka,nkl,lb->nab", R, Vc, R)))
    zm = np.mean(zs_m, axis=0)
    zv = np.var(zs_m, axis=0) + np.clip(np.mean(zs_v, axis=0), 0, None)
    return zm, np.sqrt(zv), Acan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rung", type=int, default=3, choices=[2, 3])
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--draws", type=int, default=1000)
    ap.add_argument("--tune", type=int, default=1000)
    ap.add_argument("--chains", type=int, default=4)
    ap.add_argument("--free", action="store_true", help="Lam sin anclas (corrida canónica)")
    ap.add_argument("--scores-only", action="store_true",
                    help="no muestrea; recalcula scores/resumen desde el .nc archivado")
    ap.add_argument("--bandas", type=int, default=64, help="G bandas de se (k-means)")
    a = ap.parse_args()
    Y, ind, rural, X, state, cvegeo = gl.load_data()
    se2 = load_se2(ind, cvegeo)
    print("se cargado (media por indicador SAE, escala Y):",
          {n: round(float(np.sqrt(se2[:, ind.index(n)]).mean()), 3) for n in SAE})
    se2g, gidx = agrupar_se(se2, G=a.bandas)

    nc = os.path.join(OUT, f"idata_marginal_rung{a.rung}_hetero.nc")
    if a.scores_only:
        idata = az.from_netcdf(nc)
    else:
        mod, facs = build(Y, ind, a.k, rural, X, se2g, gidx,
                          state if a.rung == 3 else None, free=a.free)
        with mod:
            idata = pm.sample(nuts_sampler="numpyro", draws=a.draws, tune=a.tune,
                              chains=a.chains, random_seed=11, target_accept=0.9,
                              idata_kwargs={"log_likelihood": True})
        idata.to_netcdf(nc)

    rh = az.rhat(idata)
    print("\n=== CONVERGENCIA (hetero, rung", a.rung, "| free =", a.free, ") ===")
    monitored = (["sigma", "W", "mload"] if a.free else ["Lam", "sigma", "W", "mload"]) \
        + (["gamma"] if a.rung == 3 else [])
    for v in monitored:
        print(f"R-hat max {v}: {float(rh[v].max()):.3f}")
    rhat_max = max(float(rh[v].max()) for v in monitored + ["LamLamT"])
    print(f"R-hat max LamLamT: {float(rh['LamLamT'].max()):.3f}")
    div = int(idata.sample_stats["diverging"].sum())
    print(f"divergencias: {div} | BFMI min: {float(np.min(az.bfmi(idata))):.2f}")
    try:
        elpd_het = float(az.loo(loglik_conjunta(idata, gidx)).elpd_loo)
    except Exception as e:
        print("LOO hetero falló:", e); elpd_het = float("nan")
    print(f"ELPD-LOO hetero: {elpd_het:.1f}")

    mload_het = idata.posterior["mload"].mean(("chain", "draw")).values
    mload_het_sd = idata.posterior["mload"].std(("chain", "draw")).values
    print("mload hetero:", dict(zip(FAMILIAS, np.round(mload_het, 3))))

    # scores canónicos hetero
    zm, zs, Acan = scores_canonicos(idata, Y, ind, rural, X, state, se2)
    K = zm.shape[1]
    zc = pd.DataFrame(np.hstack([zm, zs]),
                      columns=[f"eje{k+1}_mean" for k in range(K)] +
                              [f"eje{k+1}_sd" for k in range(K)])
    zc.insert(0, "cvegeo", pd.Series(cvegeo).astype(str).str.zfill(5))
    zc.to_csv(os.path.join(OUT, f"zscores_canonicos_rung{a.rung}_hetero.csv"), index=False)
    pd.DataFrame(Acan, index=ind, columns=[f"eje{k+1}" for k in range(K)]).round(3) \
        .to_csv(os.path.join(OUT, "ejes_canonicos_marginal_hetero.csv"))

    # baseline homoscedástico: mismos scores desde el idata canónico archivado (se2 = 0)
    base_nc = os.path.join(OUT, f"idata_marginal_rung{a.rung}.nc")
    idata0 = az.from_netcdf(base_nc)
    zm0, zs0, _ = scores_canonicos(idata0, Y, ind, rural, X, state, np.zeros_like(se2))
    mload_base = idata0.posterior["mload"].mean(("chain", "draw")).values
    mload_base_sd = idata0.posterior["mload"].std(("chain", "draw")).values
    try:
        elpd_base = float(az.loo(idata0).elpd_loo)
    except Exception:
        elpd_base = float("nan")

    # geografía de la incertidumbre: corr(sd, log_pob) y corr(sd, loc_peq_pct)
    cov = pd.read_parquet(os.path.join(PROC, "gllvm_covars.parquet"))
    lpob = np.log10(cov["pob_conapo"].values) if "pob_conapo" in cov \
        else cov["log_pob"].values
    lpp = cov["loc_peq_pct"].values
    rows = []
    for k in range(K):
        rows.append(dict(
            eje=f"eje{k+1}",
            corr_sd_logpob_homo=round(float(np.corrcoef(zs0[:, k], lpob)[0, 1]), 3),
            corr_sd_logpob_hetero=round(float(np.corrcoef(zs[:, k], lpob)[0, 1]), 3),
            corr_sd_locpeq_homo=round(float(np.corrcoef(zs0[:, k], lpp)[0, 1]), 3),
            corr_sd_locpeq_hetero=round(float(np.corrcoef(zs[:, k], lpp)[0, 1]), 3),
            sd_media_homo=round(float(zs0[:, k].mean()), 3),
            sd_media_hetero=round(float(zs[:, k].mean()), 3)))
    geo = pd.DataFrame(rows)
    print("\nGeografía de la incertidumbre (antes -> después):")
    print(geo.to_string(index=False))

    res = []
    for i, f in enumerate(FAMILIAS):
        res.append(dict(métrica=f"mload_{f}", homo=round(float(mload_base[i]), 3),
                        hetero=round(float(mload_het[i]), 3),
                        sd_homo=round(float(mload_base_sd[i]), 3),
                        sd_hetero=round(float(mload_het_sd[i]), 3)))
    for _, r in geo.iterrows():
        res.append(dict(métrica=f"corr_sd_logpob_{r.eje}", homo=r.corr_sd_logpob_homo,
                        hetero=r.corr_sd_logpob_hetero))
        res.append(dict(métrica=f"corr_sd_locpeq_{r.eje}", homo=r.corr_sd_locpeq_homo,
                        hetero=r.corr_sd_locpeq_hetero))
        res.append(dict(métrica=f"sd_media_{r.eje}", homo=r.sd_media_homo,
                        hetero=r.sd_media_hetero))
    res.append(dict(métrica="elpd_loo", homo=round(elpd_base, 1), hetero=round(elpd_het, 1)))
    res.append(dict(métrica="rhat_max_monitoreado", homo=np.nan, hetero=round(rhat_max, 3)))
    res.append(dict(métrica="divergencias", homo=np.nan, hetero=div))
    pd.DataFrame(res).to_csv(os.path.join(OUT, "nivel1_hetero_resumen.csv"), index=False)
    print("\noutputs/nivel1_hetero_resumen.csv listo")

    # validación de la réplica del baseline contra lo publicado
    pub = pd.read_csv(os.path.join(OUT, "zscores_canonicos_rung3.csv"),
                      dtype={"cvegeo": str})
    r_sd = np.corrcoef(pub["eje1_sd"].values, zs0[:, 0])[0, 1]
    print(f"validación réplica baseline: corr(eje1_sd publicado, recalculado) = {r_sd:.3f}")


if __name__ == "__main__":
    main()
