# Cómo replicar el GLLVM (para Claude Code)

Todo lo necesario está en el repo. El script `scripts/gllvm_ladder.py` corre la escalera completa
de 4 peldaños para K=2 y K=3. Los insumos ya están en `data/processed/` y `spatial/`.

## 1. Entorno

```bash
cd /Users/cuentadesanti/code/pobreza-marginacion
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` incluye `numpyro` como sampler NUTS rápido. En tu máquina (fuera del sandbox)
NumPyro con JAX aprovecha bien la CPU/Metal y hace factible el BYM2 del peldaño 4. Si prefieres el
sampler nativo de PyMC, usa `--sampler pymc` (más lento pero sin dependencias extra).

> **Nota sobre PyTensor**: el script detecta automáticamente si `$HOME/.pytensor` es escribible y,
> si no, redirige el compiledir al directorio local. En tu Mac esto no hace nada — usa tu HOME real
> y el compilador del sistema. Solo importa dentro del sandbox de Claude Science.

## 2. Correr la escalera

```bash
# K=3 completo (los 4 peldaños), sampler NumPyro
python scripts/gllvm_ladder.py --K 3 --rung all --sampler numpyro --draws 1000 --tune 1000 --chains 4

# K=2 completo
python scripts/gllvm_ladder.py --K 2 --rung all --sampler numpyro --draws 1000 --tune 1000 --chains 4

# un solo peldaño (p.ej. el espacial), para iterar
python scripts/gllvm_ladder.py --K 3 --rung 4 --sampler numpyro
```

Tiempos esperados (M-series, NumPyro, 4 cadenas): peldaños 1–3 unos minutos cada uno;
el peldaño 4 (BYM2 sobre z, +2,455×K parámetros espaciales) es el caro — de decenas de minutos
a ~1 h según draws. Empieza con `--draws 500 --tune 500` para una corrida de prueba.

### Correcciones aplicadas en la corrida (2026-07-11)

- `h5py`/`netcdf4` agregados a requirements (el `to_netcdf` de arviz los necesita; sin ellos el
  guardado del posterior falla al final del peldaño).
- **ELPD-LOO**: PyMC no guarda la log-verosimilitud pointwise por defecto → `az.loo` daba NaN.
  El script ahora llama `pm.compute_log_likelihood` tras muestrear (y la descarta antes de
  escribir el `.nc`, que si no pesaría GBs).
- **Descomposición de varianza**: se calcula sobre `E[zΛ']` draw a draw (invariante a rotación),
  no `E[z]·E[Λ]'` — el promedio ingenuo entre cadenas se cancela si hay label switching.
- **z-scores**: alineados por cadena (Procrustes de la media de Λ por cadena contra la referencia)
  antes de promediar. `scripts/analyze_ladder.py` puede regenerar ambos desde los `.nc`
  (`recompute_from_idata`) y reporta un diagnóstico de rotaciones entre cadenas.

## 3. Qué produce (en `outputs/`)

| Archivo | Contenido |
|---|---|
| `idata_rungN_K{K}.nc` | Traza posterior completa (arviz InferenceData) — para diagnóstico y figuras. |
| `loadings_rungN_K{K}.csv` | Cargas λ **alineadas por Procrustes al peldaño 1** (comparables entre peldaños). |
| `zscores_rungN_K{K}.csv` | Score latente por municipio: `{factor}_mean` y `{factor}_sd` (ancho de incertidumbre). |
| `ladder_summary_K{K}.csv` | Una fila por peldaño: Moran I residual, R-hat, ELPD-LOO, sd latente media, ρ espacial (BYM2). |

## 4. Cómo leer el resultado

La comparación clave está en `ladder_summary_K{K}.csv`:

- **Moran I residual** debe **bajar** al avanzar de peldaño. Si el peldaño 4 (BYM2) lo lleva cerca de 0
  mientras el 3 (efectos estatales) no, la estructura espacial suave era real y el ICAR valió la pena.
- **ρ espacial (BYM2)** en el peldaño 4: es la proporción de varianza latente que es espacialmente
  estructurada, POR factor. Un ρ alto en el factor material y bajo en el monetario diría que la
  privación material es geográficamente suave y la monetaria no. Ésta es directamente la métrica 4.
- **ELPD-LOO** sube = mejor ajuste predictivo fuera de muestra. Válido comparar entre peldaños porque
  la verosimilitud (gaussiana logit) no cambia.
- **sd latente media** debería **angostarse** al agregar geografía si los vecinos aportan información.
- **Cargas** (`loadings_rung*`): comparar peldaño 1 vs 2 dice cuánto de cada carga era composición
  observable (ruralidad + cofactores) y cuánto es privación latente genuina.

## 5. Decisiones de diseño ya tomadas (no re-litigar)

1. **Verosimilitud gaussiana en escala logit** para los 17 indicadores. Los indicadores SAE de CONEVAL
   (car_segsoc, car_alim, lp_ingreso, lp_ingreso_ext) son estimaciones modeladas, NO conteos —
   binomial/beta-binomial les daría precisión falsa. `sigma_j` libre por indicador absorbe la
   heterocedasticidad y la uniqueness específica (incluida `car_salud`, casi ortogonal).
2. **Anclas fijas** en los 4 peldaños: material→sin_agua, educativo→rezago_educ, monetario→lp_ingreso.
   Diagonal positiva + Procrustes contra el peldaño 1 → cargas comparables (mide cambio, no rotación).
3. **Ruralidad = `loc_peq_pct` es el único eje urbano-rural** (urbano_pct ≡ 100−loc_peq, corr −1.00).
   Entra como cofactor `beta_r`, NO como factor latente.
4. **Peldaños 3 y 4 NO se apilan**: efectos estatales y BYM2 compiten por la misma varianza geográfica.
   Son dos geografías alternativas sobre el peldaño 2. La comparación limpia es 3 vs 4.
5. **BYM2 sobre los scores `z`** (no un campo por indicador — serían 17×2,455, no identificado contra
   sigma_j). El factor de escala se calcula por componente conexo (hay 2: 2,450 + 5 municipios).
6. **Restricción suma-cero por componente conexo** (no global) — el grafo tiene un enclave de 5
   municipios además del bloque principal.

## 6. Siguiente figura (sugerida)
Panel de la escalera: (a) Moran I residual por peldaño, (b) cargas peldaño 1 vs 4 lado a lado,
(c) mapa del score latente material con su incertidumbre, (d) ρ espacial por factor.
Los `outputs/*.csv` ya traen todo lo necesario.
