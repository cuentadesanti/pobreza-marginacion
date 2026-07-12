# Marginación vs. Pobreza multidimensional — espacio latente municipal (México 2020)

Modelo de un **espacio latente municipal de privación** que integra dos mediciones oficiales
como vistas parciales y ruidosas del mismo fenómeno subyacente:

- **CONAPO — Índice de Marginación 2020** (constructo territorial, método DP2): 9 componentes.
- **CONEVAL — Pobreza multidimensional 2020** (constructo de personas, estimado vía SAE): 6 carencias + 2 líneas de ingreso.

El producto **no es un nuevo índice** sino un modelo generativo diagnóstico: una descomposición
probabilística de dimensiones comunes, efectos de método y desviaciones municipales, con
incertidumbre explícita.

## Pregunta central
¿Cuándo marginación y pobreza cuentan historias distintas del mismo territorio, y qué estructura
(dimensional, de método, espacial) explica esa discordancia?

## Estructura del repositorio

```
data/
  processed/    datasets analíticos listos (parquet/csv)
  raw/          insumos crudos moderados (ITER censo, export Banxico)
dict/           diccionarios de variables (fuente, universo, directa/modelada, oficial/proxy)
figures/        figuras de cada sprint
reports/        reportes por hito (markdown)
scripts/        gllvm_ladder.py (escalera), analyze_ladder.py (análisis/figuras),
                build_finanzas_2020.py (Vista E fiscal)
outputs/        posteriores (.nc, no versionados) y resúmenes csv de la escalera
spatial/        grafo de contigüidad (edge list ICAR)
RAW_DATA_MANIFEST.md   URLs de origen de los crudos grandes NO versionados
GLLVM_REPLICACION.md   guía de corrida e interpretación de la escalera
```

## Datasets analíticos clave (`data/processed/`)

| Archivo | Contenido |
|---|---|
| `municipal_components_2020.parquet` | Matriz base 2,469 × 17 indicadores **elementales** (9 CONAPO + 6 carencias + 2 líneas de ingreso). Sin índices finales ni derivados, para evitar circularidad. |
| `indicators_logit.parquet` | Los 17 indicadores en escala logit, estandarizados (2,466 municipios con estimación CONEVAL completa). |
| `vistaD_v1.parquet` | **Vista D congelada** — cofactores contextuales: ruralidad, metropolitaneidad, demografía, empleo, remesas per cápita, mezcla sectorial (2,455 completos). |
| `crosswalk_banxico_cvegeo.csv` | Crosswalk 2,456 series de remesas Banxico ↔ CVEGEO, con banderas de confianza de match. |
| `lisa_classes.parquet` | Clases LISA de discordancia (Alto-Alto, Bajo-Bajo, no significativo). |
| `gllvm_Y.parquet`, `gllvm_covars.parquet` | Matriz de diseño alineada (2,455) para el GLLVM: 17 indicadores + cofactores Vista D. |
| `estatales_2020.csv` | **Vista E estatal**: PIBE 2020, gasto estatal EFIPEM, per cápita y gasto/PIB (CDMX sin EFIPEM 2020). |
| `finanzas_mun_2020.parquet` | **Vista E municipal**: ingresos/egresos, participaciones, aportaciones (⚠ FAIS circular — solo validación), autonomía fiscal (2,250 municipios, 91%). |

## Hallazgos por hito (`reports/`)

1. **Dimensionalidad** (`reporte_dimensionalidad.md`): el dato soporta **2–3 factores** (Horn=3, Velicer MAP=2, bootstrap estable). Factor general fuerte (eigenvalor 9.28). `car_salud` casi ortogonal (comunalidad 0.02). Educación y ruralidad se funden en la solución MARGINAL; la especificación condicional (peldaños 2+, ruralidad como cofactor) las distingue — resuelto, no reabrir salvo lectura causal del factor educativo.
2. **Confirmación K** (`reporte_confirmatorio_k.md`): un baseline ridge/KNN gana al factor model en precisión puntual (el latente NO es predictor superior); entre factor models, K=3 > K=2 en 15/17 indicadores. Modelo deduplicado colapsa a K=2 → K=3 está en el borde.
3. **Regímenes LISA** (`reporte_regimenes_lisa.md`): régimen AA (más marginado que pobre) es rural, con remesas; BB (más pobre que marginado) es urbano. La composición explica la magnitud pero no la geografía.
4. **Modelo externo** (`reporte_modelo_externo.md`): con cofactores externos (sin insumos CONAPO/CONEVAL), la dependencia espacial residual persiste (Moran I 0.51→0.46, p=0.001) → el componente espacial del GLLVM está justificado empíricamente.
5. **DGP como DAG de medición** (`reporte_dgp_dag.md`): los dos pipelines oficiales (DP2 censal;
   SAE = 12 logísticos + EBPH + calibración estatal) como grafo dirigido, con 5 dependencias
   mecánicas y sus implicaciones de especificación (bloques de método, lectura doble de los
   efectos estatales, circularidad FAIS).
6. **Mapa de literatura** (`reporte_literatura.md`): el proyecto en el cruce economía de la
   desigualdad × ciencia social computacional; el hueco que ocupa.
7. **Escalera GLLVM** (`reporte_gllvm_escalera.md`): la composición absorbe el grueso del
   factor general (0.60→0.15); `car_salud` es ~22% estado (federalismo INSABI, no ruido);
   lo espacial reduce la incertidumbre municipal a la mitad pero la geografía residual es
   específica por indicador; K=3 domina a K=2 en ELPD en los 4 peldaños.
8. **Validación externa — homicidios** (`reporte_validacion_homicidios.md`): la privación
   explica ~23% de la violencia municipal, casi todo vía composición; el residual latente no
   aporta (R²=0.016). La señal es un *contraste* intra-familia de indicadores, casi ortogonal
   al nivel — un índice sintético único no puede focalizar privación y anticipar violencia a
   la vez.
9. **Validación satelital — Vista F** (`reporte_satelital.md`): la privación material bruta es
   visible desde el espacio (NTL solo: R² 0.41–0.43 bajo bloqueos espaciales; no cruza
   macroregiones); las lentes agregan ΔR²≈+0.07–0.20 sobre Vista D (máximo en servicios
   básicos/piso de tierra, replicado en indicadores observados); nada ve el residual
   condicional; las remesas se materializan en paredes, no en salarios locales (β opuestas
   por factor, colas ~20×).
10. **Diagnóstico municipal** (`data/processed/diagnostico_municipal_v1.parquet`,
   `outputs/top_discordantes.csv`): z ± sd por factor y municipio + régimen LISA + fiscal;
   los top residual-material (Sierra Tarahumara) son todos régimen AA — dos rutas
   independientes, misma historia.

## Especificación del GLLVM

```
η_ij = α_j + λ_j'·z_i + β_r,j·ruralidad_i + β_D,j'·x_i + m_ij + s_ij
```

- `z_i`: factores latentes. K=2 = (material, monetario); K=3 = (material, educativo, monetario).
- `ruralidad_i` = `loc_peq_pct` como **único** eje urbano-rural (urbano_pct ≡ 100−loc_peq exactamente).
- `x_i`: cofactores Vista D (remesas pc log, empleo precario, demografía, mezcla sectorial, log población).
- `m_ij`: bloques de método (familia educación / líneas de ingreso / vivienda-servicios).
- `s_ij`: uniqueness específica (especialmente `car_salud`).
- Identificación: anclas de diagonal positiva (material→sin_agua, educativo→rezago_educ, monetario→lp_ingreso) + multi-cadena + alineación Procrustes por cadena antes de agrupar.

**Escalera de especificaciones** (para medir cuánto absorbía el latente antes de contexto y espacio):
1. GLLVM base → 2. + Vista D → 3. + efectos estatales → 4. + estructura espacial (ICAR).

Comparación crítica: GLLVM no espacial vs. espacial (autocorrelación de residuos posteriores,
calibración, estabilidad de cargas, incertidumbre municipal).

## Fuentes de datos
- CONAPO, Índice de Marginación por entidad y municipio 2020.
- CONEVAL, Medición de la pobreza municipal 2020 (estimaciones SAE).
- INEGI, Censo de Población y Vivienda 2020 (ITER + cuestionario ampliado).
- Banxico, Remesas familiares por municipio (cuadro CE166, API SIE).
- Geometrías municipales INEGI Marco Geoestadístico 2020.

Ver `RAW_DATA_MANIFEST.md` para las URLs exactas de los crudos grandes.
