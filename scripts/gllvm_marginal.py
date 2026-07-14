#!/usr/bin/env python
"""
GLLVM MARGINALIZADO — la salida al frente 1 (multimodalidad).

En vez de muestrear z_i (7,365 latentes que fabrican modos), se integra analíticamente:

    Y_i ~ MvNormal(mu_i, Sigma)
    mu_i  = alpha + beta_r*rural_i + B'x_i [+ gamma_{s(i)}]      (peldaño 2 [3])
    Sigma = Lam Lam' + sum_b lm_b^2 (M_b M_b') + diag(sigma^2)   (factores + bloques + uniqueness)

El muestreador ve ~600 parámetros estructurales (peldaño 3) en lugar de ~8,000.
Identificación: anclas v2 (piso_tierra/rezago_educ/lp_ingreso, diag~LogNormal, ceros arriba).

Veredictos que produce:
  1. R-hat/ESS sobre TODOS los parámetros (sin z no hay excusa rotacional para sigma/alpha).
  2. Estabilidad del SUBESPACIO: R-hat sobre los elementos de Lam Lam' (invariante a rotación)
     y comunalidades — la opción (b) del revisor, medida directamente.
  3. Scores con incertidumbre SIN muestrear z: E[z|Y] = Lam' Sigma^{-1} (y - mu) por draw
     (media y sd posterior) -> outputs/zscores_marginal_rung{2,3}.csv
  4. gamma_s convergidas para la tabla medición-vs-federalismo (frente 2).

Uso: python scripts/gllvm_marginal.py --rung 3 --draws 1000 --tune 1000 --chains 4
"""
import os, argparse
import numpy as np, pandas as pd
import pymc as pm, pytensor.tensor as pt, arviz as az
import gllvm_ladder as gl

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs")


def build(Y, ind, K, rural, X, state=None, free=False, contrastes=None, hyper=False):
    N, J = Y.shape
    IDX = {n: i for i, n in enumerate(ind)}
    facs = ["material", "educativo", "monetario"]
    # con K<3 solo caben los primeros K anclajes; con K>3 las columnas extra van sin ancla
    # (el objeto comparable entre K es LamLam', invariante a rotación)
    anchor_rows = [IDX[gl.ANCHOR[f]] for f in facs][:K]
    mask = np.ones((J, K))
    for r, ar in enumerate(anchor_rows):
        for c in range(r + 1, K):
            mask[ar, c] = 0.0
    A_cols = [np.ones(N), rural] + [X[:, j] for j in range(X.shape[1])]
    A = np.column_stack(A_cols)                         # (N, 2+P) diseño de la media
    with pm.Model() as mod:
        if free:
            # SIN anclas: Lam libre; lo identificado es LamLam' (ejes canónicos post-hoc por
            # eigen-descomposición). Se monitorea SOLO el subespacio.
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
            if hyper:
                # Bloque 4.2 de la revisión: hiperprior estándar sobre la escala estatal
                # en vez del sigma=0.5 fijo — ¿la partición medición/federalismo sobrevive?
                sg = pm.HalfNormal("sigma_gamma", 0.5)
                gam = pm.Deterministic("gamma", sg * pm.ZeroSumNormal(
                    "gamma_raw", sigma=1.0, shape=(J, S)))
            else:
                gam = pm.ZeroSumNormal("gamma", sigma=0.5, shape=(J, S))
            mu = mu + gam.T[pt.as_tensor_variable(state)]
        # MÉTODO COMO CONTRASTE INTER-AGENCIA (identificación): dirección FIJA ortogonal al
        # nivel (CONAPO + / CONEVAL −), solo magnitud libre. Con dirección uniforme el bloque
        # era casi colineal con las cargas del factor -> multimodalidad estructural.
        CONTRASTES = contrastes if contrastes is not None else {
            0: {"analf": .5, "sin_basica": .5, "rezago_educ": -1.0},              # educación
            1: {"lp_ingreso": 1.0, "lp_ingreso_ext": 1.0},                        # SAE-EBPH (misma agencia: suma)
            2: {"sin_drenaje": 1/3, "sin_electr": 1/3, "sin_agua": 1/3,
                "car_vivienda": -.5, "car_servbas": -.5},                          # vivienda-servicios
        }
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
        pm.MvNormal("Y", mu=mu, cov=Cov, observed=Y)
    return mod, facs


def scores_marginales(idata, Y, ind, facs, rural, X, state, thin=4):
    """E[z|Y] y Var[z|Y] por draw (GLS), promediados sobre el posterior (sin Procrustes:
    con Lam convergida los ejes están fijos por las anclas)."""
    post = idata.posterior
    C, D = post.dims["chain"], post.dims["draw"]
    A = np.column_stack([np.ones(len(Y)), rural] + [X[:, j] for j in range(X.shape[1])])
    zs_m, zs_v = [], []
    for c in range(C):
        for d in range(0, D, thin):
            Lam = post["Lam"].values[c, d]
            sig = post["sigma"].values[c, d]
            lms = post["mload"].values[c, d]
            W = post["W"].values[c, d]
            mu = A @ W
            if "gamma" in post:
                mu = mu + post["gamma"].values[c, d].T[state]
            Cov = Lam @ Lam.T + np.diag(sig ** 2)
            CONTR = {0: {"analf": .5, "sin_basica": .5, "rezago_educ": -1.0},
                     1: {"lp_ingreso": 1.0, "lp_ingreso_ext": 1.0},
                     2: {"sin_drenaje": 1/3, "sin_electr": 1/3, "sin_agua": 1/3,
                         "car_vivienda": -.5, "car_servbas": -.5}}
            for bi, cv in CONTR.items():
                v = np.zeros(len(ind))
                for n, w in cv.items():
                    v[ind.index(n)] = w
                v = v / np.linalg.norm(v)
                Cov += (lms[bi] ** 2) * np.outer(v, v)
            Si = np.linalg.inv(Cov)
            B = Lam.T @ Si                                  # (K, J)
            zs_m.append((Y - mu) @ B.T)                     # (N, K)
            zs_v.append(np.diag(np.eye(Lam.shape[1]) - B @ Lam))
    zm = np.mean(zs_m, axis=0)
    # varianza total = var de la media entre draws + media de la var condicional
    zv = np.var(zs_m, axis=0) + np.mean(zs_v, axis=0)[None, :]
    return zm, np.sqrt(zv)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rung", type=int, default=3, choices=[2, 3])
    ap.add_argument("--k", type=int, default=3, help="nº de factores (ELPD comparable entre K)")
    ap.add_argument("--draws", type=int, default=1000)
    ap.add_argument("--tune", type=int, default=1000)
    ap.add_argument("--chains", type=int, default=4)
    ap.add_argument("--free", action="store_true", help="Lam sin anclas; identificar LamLam'")
    ap.add_argument("--hyper", action="store_true", help="HalfNormal sobre sigma_gamma")
    a = ap.parse_args()
    Y, ind, rural, X, state, cvegeo = gl.load_data()
    mod, facs = build(Y, ind, a.k, rural, X, state if a.rung == 3 else None, free=a.free,
                      hyper=a.hyper)
    with mod:
        idata = pm.sample(nuts_sampler="numpyro", draws=a.draws, tune=a.tune,
                          chains=a.chains, random_seed=11, target_accept=0.9,
                          idata_kwargs={"log_likelihood": True})
    rh = az.rhat(idata)
    print("\n=== VEREDICTO DE CONVERGENCIA (marginalizado, peldaño", a.rung,
          "| free =", a.free, ") ===")
    for v in (["sigma", "W", "mload"] if a.free else ["Lam", "sigma", "W", "mload"]) + (["gamma"] if a.rung == 3 else []):
        print(f"R-hat max {v}: {float(rh[v].max()):.3f}")
    print(f"R-hat max LamLamT (subespacio, invariante a rotación): "
          f"{float(rh['LamLamT'].max()):.3f}")
    ess = az.ess(idata)
    print(f"ESS min Lam: {float(ess['Lam'].min()):.0f} | ESS min LamLamT: "
          f"{float(ess['LamLamT'].min()):.0f}")
    div = int(idata.sample_stats["diverging"].sum())
    bfmi = az.bfmi(idata)
    print(f"divergencias: {div} | BFMI min: {float(np.min(bfmi)):.2f}")
    print(f"ELPD-LOO: {float(az.loo(idata).elpd_loo):.1f}")
    sufk = (f"_K{a.k}" if a.k != 3 else "") + ("_hyper" if a.hyper else "")
    idata.to_netcdf(os.path.join(OUT, f"idata_marginal_rung{a.rung}{sufk}.nc"))  # variantes no pisan el canónico
    if a.rung == 3 and a.k == 3 and not a.hyper:
        # persistir la matriz gamma (media posterior) — insumo de validaciones sin depender del .nc
        gm = idata.posterior["gamma"].mean(("chain", "draw")).values
        pd.DataFrame(gm, index=ind).to_csv(os.path.join(OUT, "gamma_marginal_rung3.csv"))

    if a.free:
        # ejes canónicos: eigen-descomposición de E[LamLam'] (convención documentada)
        M = idata.posterior["LamLamT"].mean(("chain", "draw")).values
        w, V = np.linalg.eigh(M)
        orden = np.argsort(-w)
        print("eigenvalores de E[LamLam']:", np.round(w[orden], 3))
        top = orden[:3]
        eig = pd.DataFrame(V[:, top] * np.sqrt(np.maximum(w[top], 0)),
                           index=ind, columns=["eje1", "eje2", "eje3"])
        # convención de signo: el elemento de mayor magnitud de cada eje es positivo
        for c in eig.columns:
            if eig[c].iloc[eig[c].abs().argmax()] < 0:
                eig[c] = -eig[c]
        eig.round(3).to_csv(os.path.join(OUT, "ejes_canonicos_marginal.csv"))
        print(eig.round(2).to_string())
        return
    if a.k != 3 or a.hyper:
        return          # las variantes son para comparación; sin scores ni CSVs canónicos
    zm, zs = scores_marginales(idata, Y, ind, facs, rural, X, state)
    zc = pd.DataFrame(np.hstack([zm, zs]),
                      columns=[f"{f}_mean" for f in facs] + [f"{f}_sd" for f in facs])
    zc.insert(0, "cvegeo", cvegeo)
    zc.to_csv(os.path.join(OUT, f"zscores_marginal_rung{a.rung}.csv"), index=False)
    print(f"zscores_marginal_rung{a.rung}.csv listo | sd media por factor:",
          np.round(zs.mean(0), 3))
    # correlación con los scores del modelo con z muestreada (validación cruzada de método)
    old = pd.read_csv(os.path.join(OUT, f"zscores_rung{a.rung}_K3.csv"))
    for i, f in enumerate(facs):
        r = np.corrcoef(zm[:, i], old[f"{f}_mean"])[0, 1]
        print(f"corr(marginal, muestreado v2) {f}: {r:+.3f}")


if __name__ == "__main__":
    main()
