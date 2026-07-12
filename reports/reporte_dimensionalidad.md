# Sprint 1–2 — Matriz de componentes y diagnóstico de dimensionalidad

## Datos
- **Matriz municipio–indicador 2020**: 2,469 municipios × 17 indicadores elementales.
- 9 componentes CONAPO (directos, censo) + 6 carencias CONEVAL + 2 líneas de ingreso.
- **Excluidos por diseño**: índices finales (IM, GM, pobreza total/extrema/moderada), población con ≥1 y ≥3 carencias, carencias promedio → todos son funciones de las variables elementales (evita circularidad e inflado de dimensionalidad).
- 2,466 municipios con estimación CONEVAL completa (3 sin SAE; marcados `coneval_completo=False`).
- Transformación: proporción con corrección de continuidad c=0.5, luego logit; correlaciones Spearman sobre % crudos.

## Auditoría de correlación
- **KMO = 0.893** (factorabilidad excelente), Bartlett p ≈ 0.
- Correlación media |ρ| within-block = 0.486, between-block = 0.493 → los indicadores de CONAPO y CONEVAL **se entremezclan**, no se separan por institución. Sustrato favorable a un latente compartido.
- **Pares casi duplicados** (|ρ|>0.85):
  - `lp_ingreso` ~ `lp_ingreso_ext`  ρ=0.984 (casi colineales — candidatos a colapsar o modelar como bloque)
  - `sin_basica` ~ `rezago_educ`  ρ=0.947 (misma señal educativa, distinta institución)
  - `analf` ~ `rezago_educ`  ρ=0.856

## Dimensionalidad (4 criterios, no solo Horn)
| Criterio | K retenido |
|---|---|
| Scree / Kaiser (eigenvalor>1) | 3 |
| Parallel analysis de Horn (p95, 500 sims) | **3** |
| Velicer MAP | 2 |
| Estabilidad bootstrap (200 réplicas, Procrustes) | K=3 estable (SD máx=0.038, media=0.018) |

Primer eigenvalor = 9.28 (factor general de privación, ~55% de varianza), luego caída abrupta. **Veredicto: 2–3 factores**, como se anticipó — no 4–5.

## Estructura de cargas (K=3, oblimin ML)
- **F1 — Material / vivienda-servicios**: agua, electricidad, drenaje, piso de tierra, hacinamiento, calidad y servicios básicos de vivienda, alimentación. Mezcla indicadores de ambas instituciones.
- **F2 — Educación / ruralidad**: analfabetismo, sin educación básica, rezago educativo, localidades pequeñas. (El eje educativo y el rural se funden — a vigilar.)
- **F3 — Ingreso monetario**: líneas de pobreza por ingreso (CONEVAL) + ingreso ≤2 SM (CONAPO). Es la dimensión que CONAPO capta solo parcialmente.

## Hallazgos que condicionan el modelo latente
1. **`car_salud` es un outlier casi ortogonal** (comunalidad = 0.02): la carencia de acceso a salud no correlaciona con ninguna otra dimensión. No pertenece al latente común; tratarla aparte o como su propio factor específico.
2. **Educación y ruralidad no se separan** con K=3 — F2 los funde. Es el tipo de "fuga conceptual" que el plan advertía: si se quiere un factor territorial puro, hará falta anclaje o cofactores.
3. **`car_segsoc` carga débil y difuso** (comunalidad 0.27): la seguridad social —también modelada por SAE— no se explica bien por el latente material. Consistente con la hipótesis H2 del documento Fase 0.
4. **Las dos líneas de ingreso son casi redundantes** (ρ=0.98) → riesgo de doble conteo; colapsar a una o imponer bloque de método.

## Implicación para K
El MVP generativo debe correr con **K=3**, comparándolo contra K=2. K=4 no gana estructura interpretable (el 4º factor aísla `car_salud`+`loc_peq`, ya explicables como específicos). No usar K≥4 sin justificación.
