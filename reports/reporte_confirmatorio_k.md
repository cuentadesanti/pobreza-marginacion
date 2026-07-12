# Sprint 3a — Confirmación formal: K=2 vs K=3, robustez y salud

Batería solicitada por ambos revisores. No es más EDA: es prueba confirmatoria.

## 1. ¿El 3er factor es real o artefacto de duplicados? (Modelo B)
Repetí Horn con **una variable por familia** (9 indicadores: rezago_educ, car_vivienda, car_servbas, lp_ingreso, loc_peq, car_salud, car_segsoc, car_alim, ing_2sm).

| Conjunto | Horn retiene |
|---|---|
| 17 indicadores completos | **K=3** |
| 9 deduplicados | **K=2** (3er eigenvalor 0.82 < umbral 1.06) |

**Conclusión:** el 3er factor de la solución completa está inflado por los pares casi duplicados que el revisor señaló — sobre todo `sin_basica`~`rezago_educ` (ρ=0.95) y las dos líneas de ingreso (ρ=0.98). El eje educativo se disuelve al deduplicar (cargas 0.36/0.30/0.25 sin hogar claro). **La dimensionalidad honesta del dato está entre 2 y 3, no fija en 3.**

## 2. K=2 vs K=3: validación predictiva formal
**Holdout-por-variable** (predecir cada indicador desde los otros 16, 5-fold):

| Método | MAE medio (logit-z) |
|---|---|
| Ridge (predictor externo, baseline fuerte) | **0.386** |
| Factor K=3 | 0.459 |
| Factor K=2 | 0.550 |

- **K=3 gana a K=2 en 15/17 indicadores** → si se elige factor model, es K=3.
- **PERO ridge gana al factor model en 17/17.** Confirma lo advertido: *un modelo latente no gana en precisión puntual*. Su valor no es predictivo puntual sino: incertidumbre coherente multidimensional, dimensiones interpretables y análisis de residuos/discordancia. Vender eso, no MAE.
- Reconstrucción de celdas al azar (15% oculto): KNN 0.42 < FA K=3 0.51 < col-mean 0.81. El masking aleatorio es "demasiado fácil" (KNN explota correlación intra-fila), como el propio plan anticipó.

## 3. Estabilidad de cargas (Tucker/congruencia bootstrap)
Congruencia del peor factor, 100 réplicas, alineación Procrustes:
- K=2: 0.998 (p5=0.997) · K=3: 0.998 (p5=0.996). **Ambas soluciones son altamente reproducibles** — la inestabilidad no es el problema; la redundancia sí.

## 4. Modelo C — ¿F2 era educación o ruralidad?
Residualicé los 16 indicadores sobre `loc_peq` (ruralidad como cofactor) y re-factoricé.

**Resultado clave:** con ruralidad removida, **la educación sobrevive como factor propio** (F3: rezago_educ 1.02, sin_basica 0.92, analf 0.58) e ingreso separa limpio (F2: lp_ingreso 0.96). Es decir, F2 en la solución original **no era "solo ruralidad"**: educación y ruralidad son dimensiones genuinamente distinguibles una vez que se residualiza. Esto respalda modelar **ruralidad como cofactor, no como indicador del latente** (Modelo C del revisor).

## 5. Carencia de salud — análisis específico (no eliminar)
- Distribución: media 25.1%, sd 12.5, sesgo 0.66 — no degenerada.
- **Varianza entre-estados η²=0.17**, comparable a indicadores estructurales (sin_agua 0.15; muy por debajo de lp_ingreso 0.55). No es ruido administrativo puro.
- Gradiente geográfico **no** sigue privación material: alto en Michoacán (38%), Jalisco, Edomex, Guerrero, Chiapas; bajo en el norte (Chihuahua 13%, NL 15%). Patrón consistente con la disrupción de afiliación 2020 (Seguro Popular→INSABI), no con pobreza material.
- **Veredicto:** dimensión verdaderamente distinta. Tratar como **factor específico / indicador con su propia varianza**, no forzarla al latente común ni eliminarla.

## Decisión para el MVP generativo
1. **Correr K=2 y K=3 en paralelo** como especificaciones competidoras; reportar ambas. No fijar K=3.
2. **Ruralidad (`loc_peq`) como cofactor**, no indicador.
3. **Bloque de método / residuos correlacionados** para: par de líneas de ingreso, par educativo (sin_basica/rezago_educ), y solapamiento vivienda-servicios CONAPO/CONEVAL.
4. **`car_salud` como específico** (uniqueness alta), posiblemente su propio factor si se justifica con un 2º indicador de salud.
5. Enmarcar el entregable en incertidumbre + dimensiones + residuos, **no** en MAE puntual (ridge lo supera).
