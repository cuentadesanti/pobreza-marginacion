# El proceso generador de datos: DAG estructural de marginación y pobreza municipal 2020

**Propósito.** Hacer explícito el proceso generador de datos (DGP) detrás de los 17 indicadores
elementales, como grafo acíclico dirigido. No es un DAG causal en sentido fuerte (Pearl): es un
**DAG de medición** — qué instrumento produce qué número, con qué insumos, y por dónde se filtran
dependencias mecánicas que el modelo puede confundir con estructura sustantiva. Cada arista está
documentada en las notas técnicas oficiales (CONAPO dic. 2021; CONEVAL dic. 2021).

---

## 1. Pipeline CONAPO — Índice de Marginación 2020

**Fuente:** una sola — Censo de Población y Vivienda 2020 (INEGI).

| Insumo | Indicadores |
|---|---|
| Cuestionario básico (tabulados) | `analf`, `sin_basica`, `sin_drenaje`, `sin_electr`, `sin_agua`, `piso_tierra`, `loc_peq` |
| Laboratorio de Microdatos INEGI | `hacinam` (nuevo criterio 2020: >2.5 ocupantes por dormitorio) |
| Cuestionario ampliado (microdatos, muestra) | `ing_2sm` |

Detalles del cálculo que importan para el modelo:

- **Denominadores excluyen "no especificado"** en cada indicador; los no especificados de
  educación se redistribuyen proporcionalmente antes de calcular `sin_basica`.
- **Universos distintos por indicador**: población 15+ (educación), ocupantes de viviendas
  (servicios), viviendas (hacinamiento), población total (`loc_peq`), población ocupada (`ing_2sm`).
  El "municipio" no es una sola población: es cuatro.
- `ing_2sm` es el único indicador CONAPO que viene de la **muestra** (ampliado), no del censo
  completo → tiene error muestral que los otros 8 no tienen; comparte instrumento con las
  covariables censales de los modelos SAE de CONEVAL.
- **Agregación DP2 (Pena Trapero)**: `DP2 = Σ_j (d_ij/σ_j)(1 − R²_{j·j−1,…,1})`, con base de
  referencia = peor escenario 2010–2020 y orden de entrada de variables por contenido
  informativo (coeficiente de discriminación de Ivanovic; el algoritmo canónico itera el orden
  hasta convergencia vía correlación con el índice previo). Después: estratificación
  Dalenius–Hodges (21 clases a nivel municipal) → 5 grados.
- **Implicación**: el índice final es una función determinista, *casi lineal por tramos*, de los
  9 componentes. Todo lo que el índice sabe está en los componentes → trabajar con los
  componentes (como hace este repo) no pierde información y evita heredar los pesos `(1−R²)`,
  que son un artefacto del orden de entrada.

## 2. Pipeline CONEVAL — Pobreza municipal 2020

**Dos fuentes que no se tocan al mismo nivel:**

1. **MEC del MCS-ENIGH 2020** — representativa nacional y estatal. Mide TODO (ingreso, 6
   carencias) pero no baja a municipio.
2. **Muestra del Censo 2020 (cuestionario ampliado)** — representativa municipal. Mide 4
   carencias directamente; NO mide ingreso, alimentación ni seguridad social completa.

| Indicador | Cómo se obtiene a nivel municipal |
|---|---|
| `rezago_educ`, `car_salud`, `car_vivienda`, `car_servbas` | **Directo** de la muestra censal (estimación de diseño) |
| `car_segsoc` | **12 modelos logísticos** (6 grupos de estados por k-medias sobre incidencia de pobreza × urbano/rural), ajustados en MEC-ENIGH, predichos sobre la muestra censal. Umbral de dicotomización = media estatal de carencia en MEC-ENIGH. Con "rescate de información" (asigna no-carencia a quien declara acceso directo en censo). Criterios de aceptación: ≥90% casos bien clasificados; diferencia ≤1% nacional, ≤3% estatal |
| `car_alim` | Igual (12 logísticos, stepwise dos vías p<0.1), sin rescate; tolerancias 3%/5% |
| `lp_ingreso`, `lp_ingreso_ext` | **EBPH**: modelo lineal mixto `Y_ij = x'_ij β + γ_i + ε_ij` sobre log-ingreso (γ_i = efecto aleatorio municipal), con heterocedasticidad estilo ELL (un "modelo alfa" para la varianza por hogar), estimado en MEC-ENIGH por los mismos 12 grupos, **100 simulaciones** del ingreso por hogar censal → proporción bajo LPI/LPEI |
| Integración | Cuadrantes pobreza = f(carencias, ingreso) promediados sobre las 100 simulaciones |
| **Calibración** | Ponderadores recalibrados (logit, Deville–Särndal) para que los agregados municipales **cuadren exactamente con los estatales del MEC-ENIGH**; solo en municipios >10 mil hab. no censados |

## 3. El DAG (a nivel de variable)

![DAG de medición](../figures/fig_dag_dgp.png)

**El objeto canónico son dos tablas**: `dict/dag_nodes.csv` (50 nodos: `node_id, label, kind,
observed_level, time_index, dual_role, definition`) y `dict/dag_edges.csv` (91 relaciones
tipificadas). La figura se genera desde ellas (`scripts/fig_dag.py`), que antes de renderizar
**valida formalmente**: aciclicidad con networkx, consistencia nodos↔aristas, y una matriz
permitida de tipos `relation_type × (source_kind, target_kind)`. Estado: acíclico, 0
violaciones. Reglas de construcción (revisión conceptual 2026-07-12, dos rondas):

- **Un nodo = una variable empírica, un constructo latente, un instrumento, un operador
  estadístico, un índice publicado o un objeto de política.** Sin cajas colectivas.
- **`loc_peq` es UN solo nodo** con rol dual declarado (`dual_role=structural_and_indicator`):
  condición estructural de dispersión *y* componente del IM. Consecuencia que el índice hereda:
  un componente del IM causa otros componentes del mismo índice (endogeneidad estructural
  interna — ver §4c).
- **La pobreza multidimensional NO se deriva de las prevalencias marginales municipales**: dos
  municipios con las mismas ocho prevalencias pueden tener distinta pobreza según el
  solapamiento persona a persona. El grafo pasa por `dist_conjunta` (vector de carencias ×
  ICTPC simulado, nivel persona) → regla de identificación → agregación municipal.
- **SAE y calibración son secuenciales, no padres paralelos**: `op_sae → estimaciones
  preliminares (*_raw) → op_calib → indicadores publicados`. Queda visible qué parte es modelo
  y qué parte es reconciliación estatal.
- **El lazo FAIS está temporalizado** (t−1, t, t+1, t+2): pobreza 2015 y piso 2013 → FAIS
  2016–2020 → inversión pasada → privación ACTUAL; y la medición 2020 → FAIS 2021+ →
  privación futura (t+2). El CSV es acíclico sin notas externas.
- **Relación definicional como tipo propio**: `dep_ratio → lp_ingreso` es acoplamiento por el
  denominador del ICTPC (per cápita), no un efecto económico como `remesas → lp_ingreso`.
  `remesas → piso_tierra` se podó (el canal documentado es calidad/espacios: `car_vivienda`).
- **Siete semánticas de arista** por color; operadores dibujados como operadores; los índices
  publicados (IM-DP2, pobreza CONEVAL) explícitos antes de la fórmula FAIS.


### Los cofactores tienen DOS rutas, no una

Los cofactores no operan solo "causando privación" (x → z). Cada familia tiene **canales
directos sobre indicadores específicos que no son privación** — y el GLLVM los modela
explícitamente: eso son los `β_D,j` (un coeficiente POR indicador, no un efecto común):

| Cofactor | Ruta vía z (privación) | Ruta directa β_D,j (no-privación) |
|---|---|---|
| ruralidad (`loc_peq`) | dispersión → menos acceso efectivo | **costo de ingeniería de red**: agua/drenaje faltan en localidades dispersas a igual privación; además **identidad definicional**: ruralidad ≡ `loc_peq`, uno de los 9 indicadores CONAPO |
| demografía (`dep_ratio`, `pct_60mas`) | dependencia económica real | **composición de cohortes**: los mayores estudiaron menos (`rezago_educ`, `analf` suben sin que la privación actual cambie); pensiones → `car_segsoc` |
| sectores (`pct_primario`) | economías agrícolas más pobres | **estructura ocupacional**: autoempleo agrícola sin seguridad social por diseño (`car_segsoc`) e ingreso en especie/subreportado (`ing_2sm`, `lp_ingreso`) |
| remesas | aliviana la privación de largo plazo | **transferencia directa al ingreso corriente** (`lp_ingreso*`) y a calidad de vivienda financiada, sin mover educación/servicios |

**Consecuencia de identificación (honesta):** la escalera identifica la SUMA de ambas rutas,
no su separación — el peldaño 2 mide "cuánto de la varianza va por composición en total"
(β_D,j capta la ruta directa *y* la parte de z correlacionada con x). Separar x→z de x→η
requeriría restricciones de exclusión (p. ej. "las remesas no afectan rezago educativo de
adultos en el corto plazo") que están disponibles pero son supuestos sustantivos, no
estadísticos. Por eso los factores de los peldaños 2–4 se leen como *privación condicional* y
no como "la privación verdadera". El DAG dibuja ambas rutas para que ese límite quede a la
vista.

## 4c. Endogeneidad estructural interna del IM (consecuencia del rol dual de loc_peq)

`loc_peq` es simultáneamente componente del índice de marginación y determinante causal de
otros componentes del mismo índice (`sin_agua`, `sin_drenaje`, `sin_electr`, vía costo de red;
y de las privaciones educativa e infraestructural vía z). El IM mezcla así una privación con
un *determinante territorial de otras privaciones* — al agregarlas, el DP2 cuenta parte del
mismo fenómeno dos veces por rutas distintas, y su corrección (1−R²) trata esa redundancia
como duplicidad informativa, no como estructura causal. No es un error de CONAPO: es una
propiedad del diseño que cualquier análisis del índice debería declarar.

## 4. Las cinco dependencias mecánicas son CAMINOS del grafo, no aristas

Cada "dependencia" es un patrón de padres compartidos o un camino que la edge-list induce —
por eso no aparecen como flechas extra:

1. **Bloques de método** = dos indicadores con el mismo padre instrumento (p.ej. `sin_agua` ←
   censo → ... y `car_servbas` ← muestra censal, con las mismas preguntas de fondo).
2. **Correlación inducida por SAE** = camino `muestra censal → op.SAE → car_alim` junto a
   `muestra censal → rezago_educ`: el mismo instrumento es padre directo de unos e insumo del
   operador que genera otros.
3. **Suavizamiento/calibración estatal** = camino `MEC-ENIGH → op.calibración → indicadores
   modelados`: el nivel estatal es ancestro común de los 4 modelados.
4. **`ing_2sm` puente** = único indicador CONAPO cuyo padre instrumental es la muestra censal
   (no el censo básico), compartiendo instrumento con el pipeline CONEVAL y constructo con
   `lp_ingreso`.
5. **Circularidad FAIS** = ciclo entre cortes: `pobreza 2015 → fórmula → FISM → inversión →
   z_infra (futuro) → indicadores 2020 → pobreza 2020 → fórmula 2021+`. En un corte es DAG;
   entre cortes es un lazo de control.

## 4a. Detalle de las cinco dependencias

**(1) Bloques de método por instrumento compartido.** Los pares casi-duplicados
(`sin_drenaje`/`sin_electr`/`sin_agua` vs `car_servbas`; `piso_tierra`/`hacinam` vs
`car_vivienda`; `analf`/`sin_basica` vs `rezago_educ`) no son mediciones independientes del
mismo constructo: salen de las **mismas preguntas censales**, agregadas con universos y
umbrales distintos. Su correlación residual es de instrumento, no de fenómeno →
justifica los bloques `m_ij` del GLLVM exactamente como están (educación / líneas de ingreso /
vivienda-servicios).

**(2) Correlación inducida por los modelos SAE.** `car_segsoc`, `car_alim`, `lp_ingreso*` a
nivel municipal son *predicciones* construidas con covariables de la muestra censal — el mismo
instrumento que genera los indicadores CONAPO. Si el logístico de alimentación usa educación y
vivienda del censo como predictores, parte de la correlación observada entre `car_alim` y
`sin_basica` es **mecánica** (comparten x), no evidencia de un factor común. El GLLVM no puede
distinguirla de estructura real; lo honesto es reconocer que las cargas de los indicadores SAE
sobre el factor material están *infladas por construcción*. Dirección del sesgo: hacia
sobre-estimar la comunalidad de los indicadores modelados. (Verificable: contrastar la
comunalidad de `car_alim` — modelado — contra `car_salud` — directo; la ortogonalidad casi
total de `car_salud`, comunalidad 0.02 en el reporte de dimensionalidad, es consistente con que
lo directo trae señal propia y lo modelado trae señal prestada.)

**(3) Suavizamiento y umbral estatal.** Los 12 modelos se ajustan por *grupos de estados* y el
umbral de dicotomización es la **media estatal**; la calibración fuerza los agregados estatales.
Consecuencia: la varianza intra-estatal de los indicadores SAE está atenuada y su nivel estatal
está anclado a la ENIGH. Los **efectos estatales del peldaño 3 tienen entonces doble lectura**:
geografía sustantiva *y* artefacto de calibración — para los indicadores SAE, γ_s absorbe el
benchmarking. Predicción comprobable: γ_s debería ser mayor (en magnitud) para
`car_segsoc`/`car_alim`/`lp_ingreso*` que para los indicadores censales directos.

**(4) `ing_2sm` es el puente.** Es CONAPO pero viene del cuestionario ampliado (la misma
muestra censal que alimenta los SAE de CONEVAL) y mide ingreso laboral — conceptualmente cercano
a `lp_ingreso`. Comparte instrumento con un lado y constructo con el otro. Cualquier "factor
monetario" que los junte hereda ambas cosas; el bloque de método de líneas de ingreso no lo
incluye (correcto: no comparte el paso SAE), pero su carga en el factor monetario debe leerse
con esta ambigüedad.

**(5) Circularidad de política: FAIS.** El Fondo de Aportaciones para la Infraestructura Social
se distribuye por la fórmula del art. 34 de la Ley de Coordinación Fiscal usando **la medición
municipal de pobreza extrema de CONEVAL** (2015 para ejercicios ~2020). El gasto FAIS financia
justo agua/drenaje/piso/electricidad — los indicadores del lado izquierdo del DAG. Usar FAIS (o
totales municipales de aportaciones, que lo contienen) como *covariable* condicionaría sobre un
descendiente del outcome medido: sesgo de colisionador/mediador garantizado. FAIS entra al
análisis solo como **variable de validación o de política**, jamás como cofactor del espacio
latente.

## 4b. La dependencia 5, cuantificada: la vara vale dinero

![Dos varas, un presupuesto](../figures/fig_dos_varas_dinero.png)

Condicional al **mismo nivel de privación total y tamaño poblacional**, los municipios en
régimen AA (más marginados que pobres) recibieron en 2020 **+15.8% de aportaciones federales
per cápita** (t=4.3) y los BB −3.0% (n.s.) — brecha AA−BB ≈ **+19%**, del orden de 1.2 mmdp/año
sobre la masa AA (`outputs/gap_aportaciones_regimen.csv`). Interpretación propuesta (hipótesis,
no demostrada): la fórmula vigente del FAIS conserva como piso la asignación 2013, heredada de
la fórmula *vieja* de masa carencial (perfil marginación: drenaje, electricidad, piso,
educación); solo el excedente se reparte por pobreza extrema CONEVAL (0.8z+0.2e) → **el dinero
de hoy aún lleva la huella de la vara vieja**. Caveats: aportaciones EFIPEM = FAIS+FORTAMUN
(FORTAMUN ~per cápita, diluye pero no invierte el signo), cobertura 91%, un solo año,
asociación no causal. El diseño con montos FISM reales 2016–2020 (tarea abierta) convierte
esto en el estudio de identificación central.

## 5. Implicaciones directas para la escalera GLLVM

| Decisión de especificación | Arista del DAG que la justifica |
|---|---|
| Verosimilitud gaussiana en logit, no binomial | Los SAE no son conteos: son predicciones con error de modelo; una binomial les daría precisión falsa (n_efectivo ≫ información real) |
| Bloques de método `m_ij` | Dependencia (1): instrumento compartido |
| Uniqueness libre por indicador (`s_ij`), esp. `car_salud` | Indicadores directos traen señal propia no compartida |
| Efectos estatales (peldaño 3) con lectura de medición | Dependencia (3): calibración estatal de los SAE |
| No apilar estado + BYM2 | Ambos son proxies de la misma geografía; además γ_s ya carga el artefacto de calibración |
| Excluir FAIS/aportaciones como cofactor | Dependencia (5): circularidad de política |
| Cofactores limpios: remesas (Banxico), demografía, sectores | Medidos por instrumentos ajenos a ambos pipelines |

**Dos análisis nuevos que el DAG sugiere** (implementables con lo que ya hay en `outputs/`):

- **A. Contraste directo-vs-modelado**: comparar comunalidades y |γ_s| entre los 4 indicadores
  CONEVAL directos y los 4 modelados. Si (2) y (3) son ciertas, los modelados tendrán mayor
  comunalidad en el factor material y mayor varianza estatal.
- **B. Descomposición de γ_s con covariables estatales medidas** (PIBE pc, gasto estatal/PIB,
  dependencia de transferencias): regresión jerárquica post-hoc sobre los efectos del peldaño 3
  — responde "¿la geografía discreta es capacidad fiscal estatal o es artefacto de calibración?"
  sin refit del GLLVM.

## Fuentes

- CONAPO (2021), *Índice de marginación por entidad federativa y municipio 2020. Nota
  técnico-metodológica* — [PDF](https://www.gob.mx/cms/uploads/attachment/file/685354/Nota_te_cnica_IMEyM_2020.pdf)
- CONEVAL (2021), *Metodología para la medición de la pobreza en los municipios de México,
  2020* — [PDF](https://www.coneval.org.mx/Medicion/Documents/Pobreza_municipal/2020/Metodologia_pobreza_municipal_2020.pdf);
  réplica: [Programas de cálculo](https://www.coneval.org.mx/Medicion/Paginas/Programas_BD_municipal_2010_2020.aspx)
- Ley de Coordinación Fiscal, art. 34 (fórmula FAIS); CONEVAL, *Análisis de los Fondos de
  Aportaciones del Ramo 33* — [PDF](https://www.coneval.org.mx/coordinacion/Documents/monitoreo/Ramo33/Analisis_Ramo_33_a_traves_de_sus_indicadores.pdf)
- Pena Trapero (1977); Zarzosa (1996, 2009); Somarriba y Pena (2009) — método DP2.
- Rao y Molina (2015); Molina, Nandram y Rao (2014); Elbers, Lanjouw y Lanjouw (2003) — SAE/EBPH/ELL.
- Deville y Särndal (1992, 1993) — calibración.
