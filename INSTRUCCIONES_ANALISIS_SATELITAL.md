# Instrucciones — Análisis satelital como validación externa del espacio latente

**Objetivo.** Probar qué dimensiones de la privación municipal (`z_material`, `z_educativo`,
`z_monetario` del GLLVM peldaño 3 v2) son **visibles desde el espacio** (luces nocturnas),
cuáles están gobernadas por **geografía física / accesibilidad**, y cuáles solo aparecen en los
**instrumentos sociales** (invisibles a ambas lentes).

**Encuadre (importante).** Esto NO es "otro análisis". Es una **validación externa** del espacio
latente, análoga a la validación con homicidios que ya está en el repo. La hipótesis fuerte no es
el R²: es la **tríada de invisibilidad** (ver §6). Titúlalo:
*"Dos lentes sobre la privación: qué ve la actividad nocturna, qué explica la geografía y qué
permanece invisible."*

---

## 0. Contexto del repo (lo que YA existe y vas a consumir)

| Archivo | Qué es | Clave |
|---|---|---|
| `outputs/zscores_rung3_K3.csv` | **Outcomes.** 2455 munis × 3 factores, media Y sd posterior | `cvegeo` **int64** (`1001`) |
| `spatial/municipios_2020.geojson` | Geometría municipal, WGS84 (EPSG:4326), 2469 polígonos | `cvegeo` **str** (`"01008"`) |
| `data/processed/vistaD_v1.parquet` | Vista D (17 cofactores) = bloque de control para M₄ | `cvegeo` **str** |
| `data/processed/lisa_classes.parquet` | Régimen LISA (`AA`/`BB`/`ns`...) para errores por régimen | `cvegeo` **str** (`"01008"`) |

Columnas exactas de los outcomes:
`cvegeo, material_mean, educativo_mean, monetario_mean, material_sd, educativo_sd, monetario_sd`
(n=2455). Signo: **z alto = más privación.**

### ⚠️ BUG DE CLAVE — léelo antes de cualquier join
`cvegeo` está en **dos formatos distintos**:
- z-scores: `int64` sin cero a la izquierda → `1001`, `8008`
- geojson / vistaD / lisa: `str` de 5 chars con cero → `"01001"`, `"08008"`

Un `merge` directo **descarta en silencio los estados 01–09** (Aguascalientes…Jalisco). **Normaliza
SIEMPRE a string de 5 dígitos antes de unir:**
```python
df["cvegeo"] = df["cvegeo"].astype(str).str.zfill(5)
```
Verifica tras cada merge: `assert len(merged) >= 2450, merged.shape` (esperado ~2455).
La geometría tiene 2469 munis; los z solo 2455 (14 sin cofactores completos) — es correcto que
sobren 14 al unir con la geometría.

---

## 1. Entorno

```bash
# en el .venv del repo (o crea uno)
pip install rasterio rasterstats xarray rioxarray pystac-client planetary-computer \
            scikit-learn shap geopandas
```
`scikit-learn` ya está; `rasterio`/`rasterstats` NO — son los que faltan. `shap` es opcional (§5).

---

## 2. Adquisición de rasters — Vista F (las "lentes")

Cinco variables nuevas, agregadas por municipio. Fuentes recomendadas (ordenadas por facilidad):

**A. Luces nocturnas (NTL) — VIIRS 2020 anual, "average masked".**
- Fuente 1 (recomendada, sin bajar el mundo entero): **Microsoft Planetary Computer** STAC,
  colección relacionada `viirs`; o el producto anual VNL v2.1 de Earth Observation Group.
- Fuente 2: `https://eogdata.mines.edu/nighttime_light/annual/v21/2020/` →
  `VNL_v21_npp_2020_global_vcmslcfg_c202205302300.average_masked.dat.tif.gz` (~global, recorta MX).
- Agregado municipal: **media** y **suma** de radiancia por polígono; deriva `log1p(ntl_mean)` y
  `ntl_pc = ntl_sum / pob_tot`.

**B. Elevación y rugosidad — DEM.**
- Fuente: **OpenTopography** (SRTM GL1 30m o Copernicus GLO-30) API, o Copernicus DEM vía Planetary
  Computer. **No uses `s3.amazonaws.com/elevation-tiles-prod`** (bloqueado por denylist).
- Deriva: `elev_mean`, y **rugosidad TRI** (Terrain Ruggedness Index) = media de |z_centro − z_vecino|
  sobre ventana 3×3; agrega `tri_mean` por municipio. `gdaldem TRI` o cálculo manual con `rasterio`.

**C. Accesibilidad — tiempo de viaje a ciudad.**
- Fuente: **Malaria Atlas Project** "Accessibility to Cities 2015" (Weiss et al. 2018), raster global
  de minutos de viaje. Agregado: `acc_mean` (minutos) por municipio.
- Alternativa tabular si el raster no se alcanza: distancia euclídea del centroide municipal a la
  localidad ≥50k hab más cercana (se calcula solo con el geojson + un padrón de ciudades).

**D. (Opcional) Densidad vial** — OSM highways longitud/área municipal vía `osmnx` o extractos de
Geofabrik México. Si añade fricción, déjalo para una segunda iteración.

**Salida de esta fase:** `data/processed/vistaF_satelital.parquet` con
`cvegeo (str 5), ntl_mean, ntl_pc, log_ntl, elev_mean, tri_mean, acc_min[, dens_vial]`.
Todas las agregaciones zonales con `rasterstats.zonal_stats(gdf, raster, stats=["mean","sum"])`
tras reproyectar el raster al CRS del geojson (o el geojson al del raster — cuida el CRS).

**Congela** Vista F como checkpoint igual que Vista D (documenta fuente, versión y fecha de cada raster).

---

## 3. Los cuatro modelos (por cada factor k ∈ {material, educativo, monetario})

```
M1:  z_k ~ NTL                          (¿qué ve el satélite?)
M2:  z_k ~ geografía (elev, tri, acc)   (¿qué explica el relieve/aislamiento?)
M3:  z_k ~ NTL + geografía              (lentes espaciales combinadas)
M4:  z_k ~ NTL + geografía + Vista D    (¿qué añade el satélite sobre lo ya conocido?)
```

12 ajustes (4 modelos × 3 factores). Usa un regresor no lineal moderado (Random Forest o
HistGradientBoosting de sklearn) **y** un lineal (Ridge) como referencia interpretable — reporta ambos.

---

## 4. Evaluación — la parte que la vuelve rigurosa

Para cada (modelo, factor):
1. **R² con CV espacialmente bloqueado por estado.** GroupKFold con `grupo = cvegeo[:2]` (los 2
   primeros dígitos = CVE_ENT). Esto evita que la autocorrelación espacial infle el R² — es el mismo
   criterio que ya usa la validación de homicidios del repo. Reporta media ± sd sobre folds.
2. **MAE** en la misma partición.
3. **Moran I residual** de cada modelo (usa `spatial/icar_edges.npz` o reconstruye vecindad Queen
   desde el geojson con `libpysal`). Un modelo bueno deja Moran residual bajo.
4. **Importancia:** permutación (siempre) y SHAP (si instalaste shap) — por factor.
5. **Errores por régimen LISA:** une `lisa_classes.parquet` y reporta MAE dentro de `AA`, `BB`, `ns`.
   Aquí es donde se ven las discordancias sistemáticas.
6. **Estabilidad regional:** R² por macro-región (norte / centro / sur-sureste) para ver si una lente
   funciona solo en parte del país.

Pondera opcionalmente cada municipio por `1/z_k_sd²` (los outcomes traen incertidumbre posterior —
úsala, es una ventaja del enfoque bayesiano).

**Tabla de salida:** `outputs/satelital_modelos.csv` con
`factor, modelo, estimador, r2cv_media, r2cv_sd, mae, moran_resid, mae_AA, mae_BB, mae_ns`.

---

## 5. El hallazgo — discordancia bidireccional

Con M3 (solo lentes espaciales), calcula el residual **por factor** y busca los dos extremos:

**(a) "Las luces dicen riqueza, lo social dice privación"** → `ẑ_NTL < z_observado`
(el satélite subestima la privación): candidatos = mineras, polos industriales, corredores
logísticos, turísticas. Actividad económica visible con población local rezagada.

**(b) "La geografía predice rezago, pero están mejor de lo esperado"** → `ẑ_geo > z_observado`:
candidatos = municipios de **remesas** (crúzalo con `remesas_pc_usd` de Vista D — hipótesis directa),
localidades aisladas con integración económica externa.

**Salida:** `outputs/satelital_discordancia.csv` (cvegeo, municipio, factor, z_obs, z_pred_ntl,
z_pred_geo, residual, lisa, remesas_pc) + figura de dispersión ẑ vs z con los extremos etiquetados,
y un mapa de las dos colas.

---

## 6. La conclusión que amarra todo — tríada de invisibilidad

Esperado (y lo que hay que confirmar/refutar con los números):
1. **Material** → huella espacial fuerte: `tri + acc → z_material` mejor que hacia monetario
   (relieve encarece redes de agua/drenaje/luz). Corr(NTL, z_material) < 0.
2. **Monetario** → NTL lo captura parcialmente (actividad económica), pero sobreestima bienestar donde
   hay infraestructura sin población integrada.
3. **Institucional invisible:** NTL y relieve explican **poco** de `car_salud`, `car_segsoc`,
   `car_alim` y de los **efectos estatales**. Esto conecta con dos hallazgos ya establecidos del repo:
   `car_salud` es política estatal (transición Seguro Popular→INSABI 2020, ortogonal a lo material)
   y el análisis de red mostró que no hay palanca sustantiva única. Sería la **cuarta ruta
   independiente** a la misma conclusión.

Frase de cierre defendible: *"La privación material deja una huella espacial visible, pero la
privación institucional no emite luz ni sigue el relieve."*

---

## 7. Conexión con el DAG (NO al índice final)

Añade a `dict/dag_nodes.csv` cinco nodos `kind=estructural` (o crea `kind=satelital`):
`viirs_ntl, elevacion, rugosidad, acc_ciudad, dens_vial`.

Conéctalos en `dict/dag_edges.csv` como **causas contextuales de latentes/indicadores**, nunca al
índice final `im_conapo`/`pobreza_coneval`:
```
rugosidad  → z_infra        relation_type=causal_sustantivo   (costo de red → sin agua/drenaje/luz)
acc_ciudad → z_infra        relation_type=causal_sustantivo   (aislamiento → déficit servicios)
elevacion  → z_infra        relation_type=causal_sustantivo
actividad_economica → viirs_ntl   relation_type=medicion       (NTL es PROXY OBSERVADO de actividad)
actividad_economica → z_mon       relation_type=causal_sustantivo
```
**Ojo conceptual:** las luces son un **proxy observado de actividad económica**, no una causa de
menor pobreza. La flecha correcta es `actividad → NTL` (medición) y `actividad → z_mon` (sustantiva),
NO `NTL → z_mon`. Marca `viirs_ntl` como nodo observado, no latente.

Luego re-corre `scripts/` que pesan/dibujan el DAG (el pipeline `dag_edges_weighted.csv` +
`dag_centralidad.csv` + las dos figuras) para que las nuevas lentes aparezcan como causas
contextuales de `z_infra` y `z_mon`.

---

## 8. Orden de trabajo sugerido

1. Instala rasterio/rasterstats. Baja NTL 2020 → agrega a municipal → sanity (log_ntl correlaciona
   negativo con z_monetario y con loc_peq_pct). Es el quick win.
2. DEM → elev + TRI. Accesibilidad (raster MAP o distancia-a-ciudad tabular como fallback).
3. Congela `vistaF_satelital.parquet`.
4. Corre M1–M4 × 3 factores, tabla `satelital_modelos.csv`, con CV bloqueado por estado.
5. Discordancia bidireccional + figuras + mapa.
6. Nodos DAG + re-pesado + re-dibujo.
7. `reports/reporte_satelital.md` con la tríada de invisibilidad y las tablas.

**Entregables:** `data/processed/vistaF_satelital.parquet`, `outputs/satelital_modelos.csv`,
`outputs/satelital_discordancia.csv`, `figures/fig_satelital_*.png`, `reports/reporte_satelital.md`,
nodos+aristas nuevos en `dict/`.

**Coordinación:** si la re-corrida v2 / test de label switching sigue activa sobre `outputs/`, escribe
las salidas satelitales con prefijo `satelital_` para no colisionar, y no toques los `idata_*.nc`.
