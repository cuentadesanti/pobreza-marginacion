# Sprint 3b — Regímenes territoriales de la discordancia (Pasos 1 y 2)

Puente entre el análisis descriptivo de dos índices y la necesidad del componente espacial del GLLVM.

## Definición
Discordancia D_i = percentil(marginación) − percentil(pobreza). D>0 = territorio más marginado que pobre; D<0 = lo inverso. 2,466 municipios con estimación CONEVAL completa.

## Paso 1 — Caracterización de los regímenes LISA
Pesos: contigüidad Queen (1 componente conexo, 0 islas — geometrías pre-disueltas). Moran global **I=0.507, p=0.001** (reproduce la sesión paralela). LISA local con corrección **FDR-BH 5%**:
- **Alto-Alto (138)**: marginación relativa > pobreza. Centro-norte, occidente.
- **Bajo-Bajo (203)**: pobreza relativa > marginación. Sur, periferias.
- Outliers locales: 13 BA + 6 AB.

### Perfil vs. municipios no significativos (desviación estandarizada)
| Variable | AA | BB |
|---|---:|---:|
| Ruralidad | +0.27 | **−0.72** |
| Car. calidad viv. | +0.37 | −0.48 |
| Car. serv. básicos | +0.11 | **−0.73** |
| LP ingreso | −0.38 | +0.40 |
| Car. seg. social | +0.24 | +0.10 |
| Car. alimentación | +0.22 | +0.03 |

- **BB** se desvía fuerte del centro: **menos rural, materialmente consolidado, pero pobre por ingreso**.
- **AA**: más privación material y menos pobreza por ingreso de la esperada — territorios físicamente rezagados pero menos pobres monetariamente (patrón compatible con remesas/autoconsumo, hipótesis H4).
- Modelo multinomial (SE agrupados por estado): pseudo-R²=0.29. **Advertencia clave**: los coeficientes enormes de `lp_ingreso` (−1.67 AA / +2.69 BB) **no son descubrimiento explicativo** — `lp_ingreso` alimenta la pobreza de CONEVAL y por tanto D mecánicamente. Es *validación del signo* de la discordancia, no una explicación.

## Paso 2 — Residualización: I(D) vs I(D−D̂)
| Especificación | R² | Moran I del residual |
|---|---:|---:|
| D sin ajustar | — | 0.507 |
| Cofactores observables (rural+ss+ingreso+metro) | 0.46 | **0.521** |
| Cofactores + efectos fijos de estado | 0.57 | **0.405** |

**Hallazgo (título de la figura):** *la composición explica la magnitud pero no la geografía de la discordancia.* Los covariables explican **qué** municipios discrepan (R²=0.46–0.57), pero **no eliminan** que municipios vecinos discrepen de forma parecida — el Moran residual se mantiene alto y significativo (p=0.001).

### Interpretación calibrada
No es "estructura territorial genuina" en sentido causal. Es: **persiste dependencia espacial no explicada**. Puede reflejar mercados laborales regionales, políticas estatales, accesibilidad, remesas, estructura productiva, historia de infraestructura, variables omitidas, o el propio suavizado del SAE de CONEVAL. El patrón es real estadísticamente; su mecanismo queda abierto.

## Limitación y próximo paso
El **modelo externo** que el revisor recomienda —D ~ remesas + informalidad + estructura productiva + accesibilidad + metropolitaneidad + estructura etaria, excluyendo variables que alimentan CONAPO/CONEVAL— es la especificación sustantivamente defendible, pero **requiere los cofactores de la Vista D que aún no se han adquirido**. Aquí se usó un proxy metropolitano (log población > ~200k) marcado como provisional. Adquirir Vista D es prerequisito para cerrar el Paso 2 de forma defendible.

## Decisión para el GLLVM
Justificado el componente espacial. Correr:
- K=2 y K=3 competidoras; ruralidad cofactor; factores material/monetario/(educativo); salud específico; bloques de método; índices finales fuera del ajuste.
- **Prueba decisiva del componente espacial**: ¿reduce la autocorrelación posterior residual y mejora la calibración predictiva espacial **sin borrar** municipios realmente atípicos?
