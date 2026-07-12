# Dos lentes sobre la privación: qué ve la actividad nocturna, qué explica la geografía y qué permanece invisible

**Encuadre.** Validación externa del espacio latente con lentes independientes del aparato
censal-social: luces nocturnas VIIRS 2020 (NPP-VIIRS-like v2, 500 m), relieve (GMTED2010:
elevación + rugosidad TRI) y accesibilidad (distancia a ciudad ≥50k). Vista F en
`data/processed/vistaF_satelital.parquet` (2,469 municipios, 0 NaN). Evaluación: R² con CV
**bloqueado por estado**, ponderado por 1/sd² posterior donde aplica.

## Tres resultados distintos — separados con disciplina

### 1. El hallazgo limpio: la privación material bruta es visible desde el espacio

R²(NTL → z_material bruto) = **0.41** extrapolando a estados no vistos. Robustez de bloqueo
(`satelital_robustez_bloqueo.csv`): con clusters espaciales KMeans-15 construidos sin usar
outcomes, **0.43** (peor fold 0.29) — no es un artefacto del bloqueo administrativo. Límite
de alcance: **no cruza macroregiones** (leave-one-macroregion-out: R²=−0.31) — el mapeo
luz↔privación se recalibra entre el norte y el sur del país; la lente funciona dentro de una
región, no como regla nacional transportable. En cambio, más luz NO equivale a mejor
educación (−0.11) ni a menor privación monetaria (0.02).

### 2. El 0.77 NO es mérito de las lentes: la fila decisiva es ΔR²

| (hgb, CV-estado) | M0 Vista D | M1 NTL | M2 geo | M3 lentes | M4 D+lentes | **ΔR² lentes** |
|---|---|---|---|---|---|---|
| z material bruto | 0.68 | 0.41 | 0.02 | 0.41 | 0.77 | **+0.09** |
| z educativo bruto | 0.25 | −0.11 | −0.12 | −0.07 | 0.32 | **+0.07** |
| z monetario bruto | 0.43 | 0.02 | 0.02 | 0.18 | 0.50 | **+0.07** |
| z (los tres) residual p.3 | ≈−0.1 | <0 | <0 | <0 | ≈−0.07 | **≈0** |

Vista D sola ya explica 0.68 del material; las lentes agregan +0.07–0.09 sobre el contexto
tabular. Ese es el número honesto del valor marginal de Vista F (`satelital_delta.csv`).

### 3. Validación contra indicadores OBSERVADOS (independiente del GLLVM)

El patrón replica sin pasar por la parametrización del factor model
(logit-z publicados, mismos modelos):

| indicador | M1 NTL | M0 Vista D | ΔR² lentes |
|---|---|---|---|
| car_servbas | 0.33 | 0.35 | **+0.20** |
| rezago_educ | 0.32 | 0.42 | +0.12 |
| piso_tierra | 0.05 | 0.09 | **+0.15** |
| car_vivienda | 0.14 | 0.30 | +0.08 |
| lp_ingreso | 0.13 | 0.51 | +0.06 |
| car_salud | 0.01 | −0.04 | +0.07 |

Las lentes agregan más exactamente donde el mecanismo físico lo predice (servicios básicos,
piso de tierra). Matiz fino: el `rezago_educ` observado sí es visible para las luces (0.32)
aunque el factor educativo latente no (−0.11) — el indicador crudo correlaciona con
urbanización; el factor latente es la parte que queda tras el eje material, y esa parte es
demográfica (cohortes), no luminosa.

## La geografía física: precisión en la conclusión

**No** concluimos "el relieve no explica la privación". Lo que muestra la evidencia:
*elevación media, TRI a 30 arcseg y distancia euclídea a ciudad no generalizan entre estados
como predictores suficientes de los factores latentes ni de los indicadores observados*
(M2 ≤ 0.02 en todo). Puede fallar por operacionalización (media municipal borra barrancas;
distancia euclídea ≠ tiempo de viaje; 30 arcseg es grueso), por heterogeneidad regional del
efecto, o porque la infraestructura estatal media el efecto del relieve. La arista
`rugosidad → z_infra` del DAG queda como **mecanismo plausible no respaldado de forma
generalizable por esta operacionalización** — no refutado (así está anotado en
`dag_edges.csv`).

## Remesas: el mejor hallazgo del capítulo, ahora con controles

Residual de lentes `e = z_obs − ẑ_M3` (bruto, out-of-fold), regresión con FE de estado +
ruralidad + log población, errores HC1 (`satelital_remesas_reg.csv`):

- **Material: β(log1p remesas) = −0.034, t = −5.1** — a más remesas, mejor vivienda/servicios
  de lo que sus luces y geografía predicen. No es solo un contraste de colas: sobrevive
  controles y FE.
- **Monetario: β = +0.027, t = +3.4** — signo opuesto: el ingreso (laboral) local sigue pobre
  relativo a su huella luminosa.
- Lectura conjunta: **las transferencias se materializan en paredes, no en salarios locales**.
  La economía de remesas rompe la equivalencia actividad-visible ↔ bienestar en las dos
  direcciones a la vez.
- Colas (titular calibrado): razón de medianas de remesas pc entre "mejor de lo esperado" y
  "subestimadas" = **~20× (IC95 bootstrap 14–28×)**, estable a umbral (5/10/15%) y al filtro
  pob≥5k. (El "40×" inicial era el punto con colas de 20 municipios; se reporta el rango.)

## Lo que nada ve: el residual del peldaño 3

24/24 combinaciones con R²<0 sobre los z condicionales, y ΔR² de las lentes ≈ 0. Tras remover
composición observable y efectos estatales, **las lentes espaciales no recuperan la desviación
municipal residual** — el residuo del GLLVM no es una versión escondida de urbanización o
brillo. Interpretación por factor, sin sobre-extender: en salud apunta a lo institucional
(consistente con γ_s/INSABI); en educación puede ser cohortes históricas, persistencia o
identificabilidad del factor; en lo monetario, informalidad y transferencias que el NTL no
registra. La etiqueta "invisibilidad institucional" se sostiene con fuerza para salud; para
el resto la afirmación precisa es *invisibilidad a lentes espaciales convencionales*.

## Síntesis en tres capas

| Capa | Contenido |
|---|---|
| **Visible** | vivienda, servicios básicos, urbanización, actividad material agregada (ΔR² máximo: `car_servbas`, `piso_tierra`; NTL→material 0.41–0.43 robusto a bloqueos) |
| **Parcialmente visible y regionalmente calibrada** | ingreso monetario, educación observada, accesibilidad — la relación luz↔privación es transferible entre bloques espaciales comparables pero NO invariante entre macroregiones (LORO −0.31): es una familia de calibraciones regionales f_r(NTL, geo), no una f nacional |
| **Invisible para estas lentes** | salud institucional, privación residual condicionada, transferencias sin actividad local equivalente, historia educativa de cohortes, heterogeneidad administrativa estatal |

**Cierre:** *el espacio observa bien la materialidad de la privación, pero no su arquitectura
institucional ni todas sus fuentes de ingreso. Las luces capturan actividad, no necesariamente
participación en ella; el relieve condiciona costos pero no genera una relación nacional
estable; y las remesas permiten mejorar vivienda e ingreso sin una huella productiva local
equivalente.*

Figuras: `fig_satelital_delta.png` (la fila decisiva, visualizada), `fig_satelital_mapa.png`
(la geografía de la discordancia: el cinturón azul "mejor de lo esperado" es el corredor
migratorio Zacatecas–Jalisco–Michoacán–Guanajuato–Mixteca), `fig_satelital_discordancia.png`
(municipios nombrados).

## Reproducibilidad

`build_vistaF.py` → `satelital_modelos.py` (M0–M4 × {rung1, rung3, 6 indicadores} × {ridge,
hgb}) → `satelital_robustez.py` (bloqueos alternativos + remesas) → `satelital_discordancia.py`.
Fuentes y advertencias (bug cvegeo, tiles GMTED, espejo Dataverse) en `RAW_DATA_MANIFEST.md`.
Pendientes: raster de accesibilidad Malaria Atlas, densidad vial OSM, SHAP.
