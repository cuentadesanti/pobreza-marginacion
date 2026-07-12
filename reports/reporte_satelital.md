# Dos lentes sobre la privación: qué ve la actividad nocturna, qué explica la geografía y qué permanece invisible

**Encuadre.** Validación externa del espacio latente con lentes independientes de todo el
aparato censal-social: luces nocturnas VIIRS 2020 (NPP-VIIRS-like v2, 500 m), relieve
(GMTED2010: elevación y rugosidad TRI) y accesibilidad (distancia a ciudad ≥50k, ITER).
Vista F congelada en `data/processed/vistaF_satelital.parquet` (2,469 municipios, 0 NaN).
Evaluación: R² con **CV bloqueado por estado** (GroupKFold sobre CVE_ENT — el mismo criterio
anti-autocorrelación de la validación de homicidios), ponderado por 1/sd² posterior.

## La tabla central (HistGradientBoosting; Ridge da el mismo patrón)

| Lente | material | educativo | monetario |
|---|---|---|---|
| **Privación bruta (peldaño 1)** | | | |
| M1 solo luces | **0.41** | −0.11 | 0.02 |
| M2 solo geografía (elev+TRI+acc) | 0.02 | −0.12 | 0.02 |
| M3 lentes combinadas | 0.41 | −0.07 | 0.18 |
| M4 + Vista D | 0.77 | 0.32 | 0.50 |
| **Privación residual (peldaño 3)** | | | |
| M1–M4 (todos) | **< 0** | **< 0** | **< 0** |

(`outputs/satelital_modelos.csv` trae MAE, Moran residual, MAE por régimen LISA y R² por
macro-región para las 48 combinaciones.)

## Tríada de invisibilidad (confirmada, con una sorpresa)

1. **La privación material bruta SÍ es visible desde el espacio** — las luces solas explican
   0.41 fuera de muestra entre estados. Corr(log NTL, z_material) < 0 ✓; corr(log NTL,
   loc_peq) = −0.57 (la lente nocturna es, ante todo, un urbanómetro).
2. **La sorpresa: la geografía física NO agrega poder predictivo bajo CV bloqueado** (M2 ≈ 0.02;
   M3 ≈ M1). El relieve "explica" privación solo mientras se le permite memorizar diferencias
   entre estados; obligado a extrapolar a estados no vistos, no viaja. La arista causal
   `rugosidad → z_infra` del DAG queda como mecanismo plausible con señal empírica débil a
   escala municipal-nacional (así se anotó en `dag_edges.csv`).
3. **Nada ve el espacio residual.** Sobre los z condicionales del peldaño 3, las 24
   combinaciones dan R² negativo. Ni luces ni relieve ni accesibilidad saben nada de la
   privación que queda tras composición y estado — **cuarta ruta independiente** a la misma
   conclusión (dimensionalidad → `car_salud` ortogonal; escalera → γ_s estatal; homicidios →
   residual sin señal; satélite → residual invisible). La privación educativa además es
   invisible a TODAS las lentes espaciales incluso en bruto (solo la demografía la ve, M4):
   es un fenómeno de cohortes, no de territorio luminoso.

**Frase de cierre:** *la privación material deja huella espacial visible; la privación
institucional no emite luz ni sigue el relieve.*

## Discordancia bidireccional (`outputs/satelital_discordancia.csv`, fig_satelital_discordancia)

Con M3 out-of-fold sobre la privación bruta:

- **(a) El satélite subestima la privación** (z_obs ≫ ẑ): municipios indígenas adyacentes a
  corredores luminosos — San Mateo del Mar (Istmo), Chenalhó/Mitontic/Zinacantán (Altos de
  Chiapas), Valles Centrales de Oaxaca — más las sierras profundas (Batopilas, Cochoapa el
  Grande). Actividad luminosa cercana, población excluida de ella: la lente confunde
  *proximidad a la economía* con *participación en ella*.
- **(b) Mejor de lo esperado por sus luces/geografía**: la hipótesis de remesas se confirma
  con contundencia — mediana de **600 USD pc** en esta cola vs **92** general y **14** en la
  cola (a). Economías de transferencias: integración económica externa que ni la luz local ni
  el relieve registran.

## Conexión con el DAG

Cinco nodos nuevos (`kind=satelital` + el latente `actividad_economica`) y cinco aristas en el
canónico (56 nodos, 97 aristas, acíclico verificado). Punto conceptual cuidado: las luces son
**proxy observado de actividad** — la flecha es `actividad → NTL` (medición) y `actividad →
z_mon` (causal), nunca `NTL → privación`. Los nodos satelitales van como causas contextuales
de latentes; jamás tocan `im_conapo`/`pobreza_coneval`.

## Reproducibilidad

`scripts/build_vistaF.py <scratch>` (fuentes en `RAW_DATA_MANIFEST.md`; ⚠ bug de clave cvegeo
int/str documentado y verificado con asserts) → `scripts/satelital_modelos.py` →
`scripts/satelital_discordancia.py`. Pendientes de segunda iteración: raster de accesibilidad
Malaria Atlas (hoy distancia euclídea a ciudad), densidad vial OSM, y SHAP (la importancia por
permutación ya está en `outputs/satelital_importancias.csv`).
