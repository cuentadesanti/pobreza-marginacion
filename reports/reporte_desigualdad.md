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

**Por qué no es contradicción** que los indicadores observados y el z bruto den ~50% entre
estados mientras los ejes canónicos del peldaño 3 dan solo 13–24%: son **dos objetos de
desigualdad distintos**. Los efectos estatales del modelo absorben parte de la desigualdad
interestatal ANTES de estimar los factores residuales municipales — los ejes condicionales
miden, por construcción, lo que queda después de esa absorción.

**Sensibilidad al objeto distributivo** (`desigualdad_robustez.csv`): la partición bruta es
robusta al esquema de ponderación (z material bruto: 50.8% con población, 47.6%
equiponderando municipios, 50.7% excluyendo <1,000 hab). La del eje residual NO: eje 1 pasa
de 23.6% (población) a **0.5%** (municipios equiponderados) — su componente federal es un
fenómeno de *personas concentradas en municipios grandes*, no de territorios. La elección
del objeto distributivo (personas vs territorios) es parte de la conclusión, no un detalle
técnico.

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

Definición formal: la *brecha de apropiación territorial* es la **discordancia residual entre
la actividad económica visible y la privación social observada** (constructo interpretativo
sobre una cantidad medida, no una variable observada directa). El hallazgo reordena la
historia: la brecha es **ante todo un fenómeno de precariedad laboral** — municipios donde la actividad existe y brilla pero la inserción es por
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

Robustez (`desigualdad_robustez.csv`): razón observado/esperado de 3-severas = 1.25 en q70 y
q75 (IC95 bootstrap [1.00, 1.51] y [0.94, 1.62]), 1.43 en q80, 2.44 en q90 con IC muy ancho;
Jaccard entre pares de conjuntos de alta privación: 0.05–0.21. Afirmación calibrada: **las
tres geografías residuales se solapan débilmente** (dependencia positiva leve, lejos de la
acumulación automática). La privación acumulada — el municipio "peor en todo" — es un
fenómeno del nivel bruto (donde el factor general concentra), no del espacio residual.
Consecuencia de política: focalizar "los más pobres en todo" y focalizar "los peores
residuales por dimensión" producen listas mayormente distintas (tabla completa de
intersecciones en el CSV).

## Capa 3 — desigualdad asociada a circunstancias estructurales (incremental)

Formulación correcta: *el X% de la variación territorial del outcome puede predecirse a partir
del conjunto definido de circunstancias* — no "es causada por". Escalera incremental
(hgb, CV bloqueado por estado; z material bruto):

| Bloque de circunstancias | R²cv | Δ |
|---|---|---|
| geografía heredada (rugosidad, elevación, aislamiento, dispersión) | 0.27 | +0.27 |
| + composición demográfica | 0.47 | +0.20 |
| + inserción productiva (sectores, precariedad) | **0.73** | +0.26 |
| + pertenencia estatal (KFold simple — NO bloqueado, no comparable estrictamente) | 0.88 | — |

La inserción productiva aporta tanto como la geografía heredada. "Estado" se reporta aparte:
no es una circunstancia elemental del mismo tipo. Falta composición indígena (el censo la
trae; pendiente de Vista D).

## Capa 5 — fiscal (referencia)

Ya medido en el repo: los municipios AA reciben +19% de Ramo 33 pc a igual privación
(`reporte_dgp_dag.md` §4b) — la fórmula responde a la pobreza *medida* y al piso heredado, no
a la privación residual. El análisis dinámico completo (FISM anual 2016–2020) queda como
extensión longitudinal.

## La narrativa, reescrita

Antes: *CONAPO y CONEVAL miden cosas distintas de la privación municipal.*

Ahora (tesis central): **la desigualdad territorial mexicana opera en dos escalas. En los
indicadores observados, aproximadamente la mitad de la dispersión ocurre entre estados y la
otra mitad dentro de ellos. Una vez descontada la heterogeneidad estatal, los factores
latentes revelan desigualdades predominantemente intraestatales y geografías de privación
material, educativa y monetaria que rara vez se superponen. Además, la actividad económica
visible puede coexistir con precariedad laboral y con mejoras sociales locales menores de las
que sugeriría la luminosidad del territorio.**

Y la frase fuerte, ahora con números detrás: *dos municipios pueden mostrar la misma
marginación agregada y ocupar posiciones opuestas en la estructura de desigualdad — uno carece
de infraestructura, otro de ingresos, otro queda fuera de la actividad que ilumina su
territorio.*
