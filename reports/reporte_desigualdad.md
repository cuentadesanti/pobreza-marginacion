# El giro a desigualdad: peor respecto de quién, por qué mecanismos, y qué tan desigual

**Reencuadre.** El proyecto deja de preguntar solo *quién está peor* y pregunta: peor respecto
de quién, por qué mecanismos, y cómo se distribuye la desigualdad dentro y entre territorios.
Cinco capas; aquí las tres priorizadas (A/B/C) con resultados, más la capa de oportunidades
exprés. Insumos: ejes canónicos del modelo convergido, indicadores en escala natural, residual
satelital. Scripts: `desigualdad.py`.

## A. La desigualdad bruta es mitad federal; la residual es local

Descomposición entre/dentro de estados, ponderada por población (`desigualdad_theil.csv`):

| Medida | % entre estados |
|---|---|
| `lp_ingreso` (Theil) | **58.8** |
| `lp_ingreso_ext` | 55.9 |
| `piso_tierra` | 54.7 |
| `car_servbas` | 54.3 |
| z material **bruto** (varianza) | **50.8** |
| **eje canónico 1 (condicional)** | **23.6** |
| eje 2 educativo | 13.8 |
| eje 3 vivienda-vs-redes | 13.1 |

Lectura: en la escala en que se publican los indicadores, **la mitad de la desigualdad
territorial mexicana es un fenómeno entre estados** (y las líneas de ingreso son lo más
federalizado que hay — coherente con la calibración estatal Y con el federalismo fiscal).
Una vez descontadas composición y pertenencia estatal, la desigualdad restante es
**intra-estatal en ~80%**: el residuo es un fenómeno de vecindades y municipios, no de
fronteras estatales.

## B. La brecha de apropiación territorial: actividad visible sin bienestar apropiado

`B_i = z_obs − ẑ_lentes` (material bruto; B>0 = más privado de lo que su actividad luminosa y
geografía sugieren). Regresión con FE de estado, β estandarizadas
(`desigualdad_brecha_apropiacion.csv`):

| Explicador | β | t |
|---|---|---|
| **empleo precario** | **+0.226** | 8.6 |
| log población | +0.151 | 8.3 |
| ruralidad (loc_peq) | +0.140 | 9.1 |
| rugosidad | −0.135 | −9.1 |
| % secundario | +0.085 | 8.1 |
| **remesas pc (log)** | **−0.072** | −5.3 |

El hallazgo reordena la historia: la brecha de apropiación es **ante todo un fenómeno de
precariedad laboral** — municipios donde la actividad existe y brilla pero la inserción es por
cuenta propia/jornal/sin pago — con el tamaño urbano como segundo factor (pobreza urbana
invisible a la luz agregada). Las remesas operan en la dirección opuesta (apropiación vía
transferencias, confirmando el capítulo satelital) pero con un tercio de la fuerza de la
precariedad. *Brecha de apropiación territorial* es el concepto de desigualdad; "discordancia
satelital" era su nombre de medición.

## C. La acumulación multidimensional vive en el nivel bruto, no en el residual

`A_i = #{k: z_ik > q75}` sobre los tres ejes canónicos condicionales
(`desigualdad_acumulacion.csv`, `fig_acumulacion.png`):

| Dimensiones severas | % municipios | % población |
|---|---|---|
| 0 | 43.3 | 49.0 |
| 1 | 40.3 | 37.9 |
| 2 | 14.4 | 12.3 |
| 3 | **2.0** | 0.8 |

Bajo independencia, P(3 severas) = 0.25³ = 1.6% ≈ el 2.0% observado: **las tres geografías
residuales casi no se superponen**. La privación acumulada — el municipio "peor en todo" — es
un fenómeno del nivel bruto (donde el factor general concentra), no del espacio residual: cada
dimensión condicional produce su propia geografía. Consecuencia de política: focalizar "los
más pobres en todo" y focalizar "los peores residuales por dimensión" son listas casi
disjuntas.

## Capa 3 exprés — desigualdad asociada a circunstancias estructurales

R²cv(rugosidad + aislamiento + ruralidad + estructura etaria + elevación → z material bruto)
= **0.47** bajo CV bloqueado por estado. Asociación, no causal; falta la composición indígena
(pendiente señalado — el censo la trae, próxima iteración de Vista D).

## Capa 5 — fiscal (referencia)

Ya medido en el repo: los municipios AA reciben +19% de Ramo 33 pc a igual privación
(`reporte_dgp_dag.md` §4b) — la fórmula responde a la pobreza *medida* y al piso heredado, no
a la privación residual. El análisis dinámico completo (FISM anual 2016–2020) queda como
extensión longitudinal.

## La narrativa, reescrita

Antes: *CONAPO y CONEVAL miden cosas distintas de la privación municipal.*

Ahora: **la desigualdad territorial mexicana no es un único gradiente — se compone de brechas
materiales, monetarias, educativas, institucionales y de apropiación económica que se
superponen de manera desigual entre regiones y estados**: la mitad de la desigualdad publicada
es federal; el residuo es local y sus dimensiones casi no se tocan; y la brecha entre actividad
visible y bienestar apropiado es un fenómeno de calidad del empleo antes que de geografía.

Y la frase fuerte, ahora con números detrás: *dos municipios pueden mostrar la misma
marginación agregada y ocupar posiciones opuestas en la estructura de desigualdad — uno carece
de infraestructura, otro de ingresos, otro queda fuera de la actividad que ilumina su
territorio.*
