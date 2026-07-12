#!/usr/bin/env python
"""
Test decisivo de convergencia módulo rotación (peldaño 2, K=3, anclas v2).

Muestrea el peldaño 2 y calcula R-hat DOS veces:
  (a) ingenuo, sobre Lam y z crudos  -> alto si hay label switching
  (b) sobre Lam y z ALINEADOS draw a draw (Procrustes contra una referencia común)

Veredicto:
  - R-hat alineado ~1.0  => el modelo converge módulo rotación; el label switching queda
    resuelto por post-procesamiento (no hace falta re-especificar).
  - R-hat alineado alto  => no-convergencia genuina más allá de la rotación.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, arviz as az, xarray as xr
from scipy.linalg import orthogonal_procrustes
import gllvm_ladder as gl
import pymc as pm

DRAWS, TUNE, CHAINS = 500, 500, 4

def main():
    data = gl.load_data()
    Y, ind, rural, X, state, cvegeo = data
    mod, facs = gl.build_gllvm(Y, ind, 3, rural=rural, X=X)
    with mod:
        idata = pm.sample(nuts_sampler="numpyro", draws=DRAWS, tune=TUNE, chains=CHAINS,
                          random_seed=7, target_accept=0.9, progressbar=True)
    L = idata.posterior["Lam"].values      # (C, D, J, K)
    Z = idata.posterior["z"].values        # (C, D, N, K)
    C, D, J, K = L.shape

    # (a) R-hat ingenuo
    rh_raw_L = float(az.rhat(idata, var_names=["Lam"])["Lam"].max())
    rh_sig = float(az.rhat(idata, var_names=["sigma"])["sigma"].max())
    rh_alp = float(az.rhat(idata, var_names=["alpha"])["alpha"].max())

    # (b) alineación draw a draw contra la media alineada de la cadena 0
    ref = L[0].mean(0)
    La = np.empty_like(L)
    sub = np.linspace(0, Z.shape[2] - 1, 200).astype(int)   # submuestra de municipios
    Za = np.empty((C, D, len(sub), K))
    for c in range(C):
        for d in range(D):
            R, _ = orthogonal_procrustes(L[c, d], ref)
            La[c, d] = L[c, d] @ R
            Za[c, d] = Z[c, d][sub] @ R
    def rhat_arr(a, name):
        da = xr.Dataset({name: (("chain", "draw") + tuple(f"d{i}" for i in range(a.ndim - 2)),
                                a)})
        return float(az.rhat(da)[name].max())
    rh_ali_L = rhat_arr(La, "Lam_alineada")
    rh_ali_Z = rhat_arr(Za, "z_alineada")

    print("\n================ VEREDICTO ================")
    print(f"R-hat ingenuo   Lam: {rh_raw_L:.3f}   (label switching visible)")
    print(f"R-hat ALINEADO  Lam: {rh_ali_L:.3f}   z: {rh_ali_Z:.3f}")
    print(f"R-hat sigma: {rh_sig:.3f}   alpha: {rh_alp:.3f}")
    if rh_ali_L < 1.05 and rh_ali_Z < 1.05:
        print("=> CONVERGE MÓDULO ROTACIÓN: el label switching muere con alineación por draw.")
    elif rh_ali_L < 1.1 and rh_ali_Z < 1.1:
        print("=> converge módulo rotación con holgura marginal (<1.1).")
    else:
        print("=> NO-CONVERGENCIA GENUINA más allá de la rotación: re-especificar.")

if __name__ == "__main__":
    main()
