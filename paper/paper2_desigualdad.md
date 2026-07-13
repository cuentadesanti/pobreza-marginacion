# Desigualdad territorial en dos escalas: geografías débilmente solapadas de la privación municipal en México

**Borrador de trabajo (Paper 2, sustantivo) — 2026-07-13**
*Objetivo editorial: World Development (alternativas alineadas: Regional Studies, Journal of Regional Science, World Development Perspectives; español; traducción al enviar).*

## Resumen

¿A qué escala opera la desigualdad territorial mexicana, y se acumulan sus dimensiones en los
mismos lugares? Usando un espacio latente municipal de privación estimado sobre los 17
indicadores elementales de las dos mediciones oficiales (CONAPO y CONEVAL; método en el paper
compañero), documentamos tres resultados. Primero, la desigualdad opera en **dos escalas**: en
los indicadores observados, el componente interestatal del índice de Theil va de 31% a
59%<!-- src: desigualdad_theil.csv --> según el indicador (mediana 48%; 50.8% para el factor
material bruto), con los servicios de red como lo menos federalizado y las líneas de ingreso
como lo más; la desigualdad residual — descontadas composición y pertenencia estatal — es en
cambio predominantemente intraestatal (76–87% de la varianza). Segundo, las **severidades
residuales se solapan débilmente** (Jaccard 0.05–0.21 entre pares de dimensiones; la triple
severidad apenas excede la esperada bajo independencia): el municipio "peor en todo" es un
fenómeno del nivel observado, mientras que en el espacio residual — ortogonal en parte por
construcción — hay poco solapamiento extremo adicional al esperado. Tercero, existe una
**brecha entre la privación observada y la predicha por lentes espaciales** — que
interpretamos como brecha de apropiación territorial: municipios cuya actividad económica es
visible desde satélite pero cuya mejora social local es menor a la esperada; su predictor
dominante es la precariedad laboral (β estandarizado = +0.23, t = 8.6), con las remesas
operando en sentido inverso. Una escalera predictiva de condiciones estructurales e
inserciones históricas alcanza R² = 0.78 sobre la privación bruta con validación espacialmente
bloqueada. Cinco análisis externos independientes — homicidios, luces nocturnas, exposición
criminal documentada (incluida la coerción política histórica), transición INSABI e incidencia
fiscal — delimitan distintas implicaciones y límites del espacio estimado; donde se
superponen, apuntan a que violencia y privación son dimensiones territorialmente distintas, y
a que las transferencias aún pagan a la vara vieja.

**Palabras clave:** desigualdad territorial; pobreza multidimensional; acumulación de
desventajas; remesas; luces nocturnas; México.

---

## 1. Introducción: más allá de "cuál índice"

El debate aplicado sobre la medición municipal de la pobreza en México suele plantearse como
una elección entre índices. Este paper toma otra ruta: dado un espacio latente de privación
que integra los indicadores elementales de ambas agencias oficiales — con efectos de método y
de estado explícitos, estimado con la maquinaria descrita en el paper compañero — pregunta por
la **estructura** de la desigualdad territorial: a qué escala opera, si sus dimensiones se
acumulan en los mismos municipios, y si la actividad económica visible implica inclusión
social local. Las tres respuestas (dos escalas; severidades débilmente solapadas; brecha de
apropiación) tienen implicaciones directas de focalización que ningún índice sintético único
puede satisfacer simultáneamente.

El artículo procede así: §2 sitúa la contribución; §3 resume datos y espacio latente y define
los objetos distributivos; §4 presenta la partición en dos escalas (Figura 1, Tabla 1); §5 el
solapamiento de severidades residuales (Tabla 2, Figura 2); §6 la brecha de apropiación
(Figura 3); §7 la capa de condiciones estructurales (Tabla 3); §8 los cinco análisis externos
(Figuras 4 y 5); §9 discute implicaciones de política. El apéndice documenta las baterías de
robustez y la regresión completa de la brecha.

## 2. Antecedentes y trabajo relacionado

Tres literaturas convergen aquí. Primera, la descomposición de la desigualdad: usamos el
índice de Theil (1979) porque es el miembro canónico de la familia aditivamente descomponible
que Shorrocks (1984) axiomatizó — la partición exacta entre/dentro de estados que la tesis de
dos escalas necesita, y que un Gini no ofrece sin residuo. La pregunta de a qué escala vive la
desigualdad territorial tiene tradición larga en economía regional — para México, la agenda de
convergencia regional estancada tras la apertura comercial es el trasfondo macro — y la
crítica metodológica a los índices territoriales oficiales es también mexicana: Cortés &
Vargas (2011) mostraron que el índice de marginación confunde constructo con método. Este
trabajo se inscribe en la tradición de medición de pobreza y desigualdad en México (Lustig &
Székely 1997; Boltvinik 2012). Nuestra contribución es hacer la pregunta de escala
*condicional*: separar la partición del nivel bruto (lo que las agencias publican) de la
partición del residuo (lo que queda tras composición y pertenencia estatal), y mostrar que
son objetos distributivos distintos con respuestas distintas. Que la desigualdad del ingreso
en México se sostiene predominantemente *dentro* de las entidades y no entre ellas es un
hallazgo recurrente de la literatura distributiva nacional (Cortés & Valdés Cruz 2023); aquí
mostramos que esa escala depende del objeto: en el nivel bruto de la privación el componente
interestatal pesa cerca de la mitad, y solo el residuo condicional reproduce el predominio
intraestatal.

Segunda, la acumulación de desventajas: la literatura de pobreza multidimensional (Alkire &
Foster 2011, la base de la medición mexicana) presupone que las carencias se cuentan porque se
acumulan. Medimos directamente cuánto se acumulan las severidades — en el nivel observado y en
el residual — con razones observado/esperado bajo independencia e índices de Jaccard.

Tercera, los sensores remotos como lente de desarrollo: las luces nocturnas como proxy de
actividad económica (Henderson, Storeygard & Weil 2012; con la advertencia de ruido de Chen &
Nordhaus 2011) y el salto predictivo con imágenes de Jean et al. (2016), que citamos como
referente sin benchmark propio de imágenes. Nuestro uso es inverso al habitual: no predecimos
pobreza con luces para sustituir encuestas, sino que usamos la *discordancia* entre lo que la
luz predice y lo que la medición social observa como objeto de estudio.

## 3. Datos y espacio latente (resumen)

Diecisiete indicadores elementales (9 CONAPO, 8 CONEVAL) para 2,469 municipios en 2020 (2,455
en la matriz del modelo; el paper compañero documenta el descarte), modelados en escala logit
estandarizada dentro de un modelo de variables latentes marginalizado con tres factores,
efectos de método sobre direcciones de dependencia metodológica predefinidas, covariables de
composición (demografía, mezcla sectorial, remesas) y efectos estado×indicador; convergencia
verificada sobre el subespacio de covarianza (R̂ ΛΛᵀ = 1.003). Los ejes canónicos: 1
material-infraestructural, 2 educativo, 3 el contraste de vivienda e ingreso contra servicios
de red. Cada municipio tiene media y desviación posterior por eje; toda inferencia de este
paper hereda esa incertidumbre — los modelos municipales van ponderados por el inverso de la
varianza posterior, y la clasificación individual solo es sustantiva en 42/55/14% de los
municipios según el eje<!-- src: certeza_canonica.csv -->. El detalle metodológico — incluida
la advertencia de que las comparaciones de ingreso intra-estado arrastran la firma del método
de imputación — está en el paper compañero.

Dos objetos distributivos, definidos con precisión porque §4 los contrasta: el **nivel bruto**
(los indicadores publicados, o el factor material estimado sin covariables ni efectos
estatales) y el **residuo condicional** (los ejes canónicos del modelo completo, que
descuentan composición y pertenencia estatal). Ambos son legítimos; responden preguntas
distintas — "¿dónde está la privación?" versus "¿dónde hay más privación de la que la
estructura del municipio explica?".

## 4. La desigualdad opera en dos escalas

La Figura 1 muestra la partición entre/dentro de estados para ambos objetos — con una
advertencia de lectura que la tabla hereda: los indicadores observados se descomponen con el
índice de Theil y los ejes con descomposición de varianza; son funcionales distintos y **sus
niveles porcentuales no se comparan entre paneles**, solo el patrón dentro de cada uno.

![Figura 1. Las dos escalas: componente interestatal por indicador observado (panel a, descomposición de Theil, ponderación poblacional) y por factor bruto/ejes condicionales (panel b, descomposición de varianza). Los funcionales difieren entre paneles y sus niveles no son comparables; el patrón sí: el nivel observado es ~mitad interestatal, el residuo condicional es predominantemente intraestatal.](../figures/09_desigualdad/fig_theil_escalas.png)

En los indicadores observados, el componente interestatal va de 31.1% (sin electricidad) a
58.8% (línea de pobreza por ingreso), con mediana 47.8% y 50.8% para el factor material bruto
ponderado por población<!-- src: desigualdad_theil.csv -->. El orden no es aleatorio: **lo
menos federalizado son los servicios de red** (electricidad, drenaje, dispersión: 31–35%) —
infraestructura cuya variación es local — **y lo más federalizado son las dos líneas de
ingreso** (55.9–58.8%), consistente a la vez con la calibración estatal del método de
imputación de ingreso (la firma documentada en el paper compañero) y con el federalismo
fiscal. Una vez descontadas composición y pertenencia estatal, la desigualdad de los ejes
canónicos es predominantemente intraestatal (76–87% de la varianza; Tabla 1). No hay
contradicción: los efectos estatales absorben la parte interestatal antes de estimar el
residuo — son dos objetos distributivos distintos y los reportamos como tales.

**Tabla 1. La partición entre/dentro de estados, en dos paneles no comparables entre sí**
(panel A: descomposición de Theil, ponderación poblacional; panel B: descomposición de
varianza).<!-- src: desigualdad_theil.csv -->

*Panel A — indicadores observados (Theil)*

| Indicador | % entre estados | % dentro |
|---|---|---|
| línea de pobreza por ingreso | 58.8 | 41.2 |
| piso de tierra | 54.7 | 45.3 |
| analfabetismo | 53.1 | 46.9 |
| sin agua entubada | 40.4 | 59.6 |
| sin electricidad | 31.1 | 68.9 |

*Panel B — factor bruto y ejes condicionales (varianza)*

| Objeto | % entre estados | % dentro |
|---|---|---|
| factor material bruto | 50.8 | 49.2 |
| eje material (condicional) | 23.6 | 76.4 |
| eje educativo (condicional) | 13.8 | 86.2 |
| eje vivienda+ingreso vs redes (condicional) | 13.1 | 86.9 |

La partición bruta es robusta al esquema de ponderación; la residual depende del objeto
distributivo: el componente interestatal del eje material casi desaparece al equiponderar
municipios (23.6% → 0.5%), es decir, es un fenómeno de personas concentradas en municipios
grandes, no de territorios.<!-- src: desigualdad_robustez.csv bloque A -->

## 5. Las severidades residuales se solapan débilmente

Una advertencia algebraica antes del resultado: los ejes canónicos provienen de una
eigen-descomposición, así que son **ortogonales por construcción** — sus extremos tienden a
solaparse poco por álgebra, no solo por geografía. La pregunta empírica bien planteada no es
"¿se solapan?" sino "¿se solapan *más de lo esperado bajo independencia*?". La respuesta:
apenas. Definiendo severidad como el cuartil superior de cada eje, la proporción de municipios
severos en las tres dimensiones (2.0%) apenas excede la esperada bajo independencia (1.6%), y
la razón observado/esperado roza 1 en todos los umbrales (Tabla 2). En el nivel observado, en
cambio, el factor general domina y el municipio "peor en todo" sí existe. La lectura
calibrada: **hay poco solapamiento extremo adicional al esperado en el espacio residual** — la
concentración multidimensional es un fenómeno del nivel, y las geografías residuales de cada
dimensión son, en lo esencial, distintas (Figura 2).

**Tabla 2. Acumulación residual: razón observado/esperado de triple severidad y solapamiento
por pares** (IC bootstrap de 1,000 réplicas).<!-- src: desigualdad_robustez.csv bloque C -->

| Umbral de severidad | obs/esp 3 severas | IC95 | Jaccard (1,2) | Jaccard (1,3) | Jaccard (2,3) |
|---|---|---|---|---|---|
| q70 | 1.25 | [1.00, 1.51] | 0.19 | 0.21 | 0.18 |
| q75 | 1.25 | [0.94, 1.62] | 0.15 | 0.18 | 0.14 |
| q80 | 1.43 | [0.97, 1.99] | 0.13 | 0.15 | 0.10 |
| q90 | 2.44 | [0.80, 4.48] | 0.06 | 0.10 | 0.05 |

![Figura 2. Acumulación multidimensional de privación residual: municipios por número de dimensiones severas simultáneas (cuartil superior de cada eje canónico condicional). Las geografías severas se solapan débilmente; 48 municipios (2.0%) son severos en las tres.](../figures/04_diagnostico_mapas/fig_acumulacion.png)

Como viñeta descriptiva — no como estrato estadísticamente robusto: los **48 municipios
severos en las tres dimensiones residuales** tienen un perfil nítido<!-- src: veta_48_triple.csv -->
— 24 de 48 en Oaxaca, pequeños (mediana 5,430 habitantes contra ~13,550 nacional), 79% rurales
(≥50% de su población en localidades pequeñas; 75% con umbral ≥80%), fuera de la economía de
remesas (mediana 17 vs 92 USD per cápita), con *menos* presencia criminal documentada que el
promedio (27% vs 48%) y casi todos no significativos para la tipología espacial de
discordancia (44/48). No son los municipios prominentes de la pobreza mexicana ni los de la
violencia. Las dos cautelas que esta viñeta hereda: el grupo es pequeño y sensible al umbral
(la razón observado/esperado roza 1), y el tercer eje — vivienda+ingreso contra redes — tiene
la certeza municipal más baja del sistema.

## 6. La brecha entre privación observada y predicha por lentes espaciales

**El objeto formal primero.** Se construye en tres pasos, todos fuera de muestra: (i) se
predice la privación material bruta de cada municipio a partir de sus luces nocturnas — el
proxy de actividad de Henderson, Storeygard & Weil (2012) y Chen & Nordhaus (2011) — y su
geografía física (gradient boosting, validación cruzada agrupada por estado: la predicción de
cada municipio proviene de un modelo que no vio ningún municipio de su estado); (ii) la
*brecha* es el residual entre privación observada y predicha de esa predicción out-of-fold;
(iii) la brecha se regresa sobre candidatos a explicación con efectos fijos estatales y
errores robustos HC1, con covariables estandarizadas (los β son estandarizados). Brecha
positiva = el municipio está *peor* socialmente de lo que su actividad visible sugiere. Dos
límites declarados: el modelo base ya incluye luz *y* geografía física (no es un contraste
puro luz-vs-bienestar), y la brecha usa la predicción puntual out-of-fold sin propagar su
incertidumbre.

**Resultado.** El predictor dominante es la precariedad laboral (β = +0.23, t = 8.6)<!-- src:
desigualdad_brecha_apropiacion.csv --> — municipios donde la actividad existe y brilla pero la
inserción es por cuenta propia, jornal o sin pago — seguido del tamaño urbano (+0.15; pobreza
urbana invisible a la luz agregada); las remesas operan en sentido contrario (−0.07, t = −5.3):
mejoran vivienda e ingreso sin huella productiva local equivalente (β de signo opuesto por
factor: −0.034 material, +0.027 monetario<!-- src: satelital_remesas_reg.csv -->). La
regresión completa está en el apéndice E. El contraste descriptivo entre colas es elocuente:
la mediana de remesas en los municipios "mejor de lo esperado por sus luces" es ~20 veces
(IC95 bootstrap 14–28) la de los subestimados (Figura 3). La interpretación que proponemos —
**brecha de apropiación territorial**: la actividad visible no implica inclusión laboral
local — es una lectura de esos coeficientes, no una identificación causal.

![Figura 3. La brecha entre privación observada y predicha por las lentes satelitales (out-of-fold, bloqueado por estado), con las colas etiquetadas. Los municipios "mejor de lo esperado" son territorios de remesas; los "peor de lo esperado", de precariedad laboral.](../figures/07_satelital/fig_satelital_discordancia.png)

## 7. Condiciones estructurales e inserciones históricas

¿Cuánta de la privación bruta es predecible desde las condiciones de partida del territorio?
Una escalera incremental (gradient boosting, validación cruzada bloqueada por estado, cinco
pliegues de estados completos; Tabla 3) responde: la geografía heredada — rugosidad,
elevación, aislamiento, dispersión — predice 0.27; sumando composición demográfica, 0.47;
sumando la inserción productiva — que a diferencia de la geografía es un outcome histórico e
institucional, no una condición predeterminada —, 0.73; sumando composición indígena (%
hablantes de lengua indígena y % monolingüe, del censo), **0.78**.<!-- src:
desigualdad_robustez.csv capa3 --> La composición indígena aporta poca señal predictiva
*incremental* una vez incluidas geografía, demografía e inserción — compatible con una fuerte
superposición entre la dimensión étnica y las demás condiciones territoriales. Dos disciplinas
de lectura: el incremento de cada bloque depende del orden de entrada (sin una descomposición
tipo Shapley, los Δ no son atribuciones), y toda la escalera es predecible-desde, no
causado-por.

**Tabla 3. Escalera predictiva → privación material bruta** (R² de validación cruzada
bloqueada por estado).<!-- src: desigualdad_robustez.csv capa3 -->

| Bloque | R²cv | Δ (según orden de entrada) |
|---|---|---|
| geografía heredada (rugosidad, elevación, aislamiento, dispersión) | 0.265 | +0.265 |
| + composición demográfica | 0.469 | +0.204 |
| + inserción productiva (sectores, precariedad) | 0.732 | +0.263 |
| + composición indígena | **0.775** | +0.042 |
| + pertenencia estatal (validación NO bloqueada, no comparable) | 0.891 | — |

## 8. Cinco análisis externos

Cinco análisis externos independientes, ninguno usado en la construcción del espacio latente,
delimitan distintas implicaciones y límites del espacio estimado:

1. **Homicidios** (103 mil registros oficiales 2019–2021; orden estable en siete variantes de
   sensibilidad; Figura 4): la privación explica ~23% de la violencia municipal, casi todo vía
   composición; el residual no aporta.<!-- src: validacion_homicidios.csv,
   sensibilidad_homicidios.csv --> La señal es un contraste intra-familia casi ortogonal al
   nivel — un índice sintético único no puede focalizar privación y anticipar violencia a la
   vez.
2. **Luces nocturnas**: ven la privación material bruta (R² 0.41–0.43 con bloqueo espacial no
   administrativo; sin transferencia entre macroregiones) y esencialmente nada del residual —
   ninguna combinación modelo×factor×estimador supera R²cv = 0.03 sobre los ejes condicionales
   y 26 de 30 son negativas.<!-- src: satelital_modelos.csv --> La relación log-lineal
   canónica de esta literatura (y el salto predictivo de Jean et al. 2016, aquí solo como
   referente, sin benchmark propio de imágenes) se resuelve a escala municipal en regímenes:
   piso oscuro (14% de municipios), umbrales regionales con IC disjuntos, sin saturación
   urbana.
3. **Exposición criminal documentada** (65 mil eventos diario-municipales con actores,
   2000–2018): predice violencia — más bajo competencia entre organizaciones que bajo
   monopolio (+0.130, t = 4.0, vs +0.083, t = 3.1)<!-- src: g_monopolio_competencia.csv --> —
   y es esencialmente ortogonal a la privación residual (resultado negativo documentado con
   robustez). La **coerción política histórica** (ataques a autoridades y candidatos
   2007–2012; Trejo & Ley 2021) refuerza el patrón como exposición rezagada: no se identifica
   una ruta robusta hacia la privación residual de 2020 (el indicador de coerción es nulo en
   los ejes material y educativo, y en el tercero indicador y tasa se contradicen —
   colinealidad entre ambas medidas, no una ruta), mientras que sí predice homicidio 2019–21
   una década después (+0.26, t = 2.7)<!-- src: g5_coercion.csv --> y ocurrió donde
   competencia criminal y fragmentación política interactúan. Advertencia permanente: los
   datos de eventos observan lo real filtrado por la detección — presencia documentada no es
   control territorial y la ausencia de registro no es ausencia real; todos los modelos llevan
   proxies de observabilidad.
4. **Transición INSABI**: la varianza estatal máxima del sistema corresponde a la carencia de
   salud, con correlación +0.61 con la dependencia estatal del Seguro Popular/INSABI (máxima
   de los 17 indicadores; placebos 0.18–0.49)<!-- src: validacion_insabi.csv --> — el
   componente estatal contiene señal compatible con política institucional real, no únicamente
   con calibración; la correlación es sugestiva, no una identificación.
5. **Incidencia fiscal** (Figura 5): a igual privación y tamaño, los municipios "más
   marginados que pobres" reciben +15.8% de transferencias del Ramo 33 per cápita (t = 4.3) y
   los "más pobres que marginados" −3.0% (n.s.)<!-- src: gap_aportaciones_regimen.csv --> — el
   piso heredado de la fórmula antigua de masa carencial sigue pagando al perfil de
   marginación. El análisis de incidencia de la política fiscal sobre la desigualdad tiene
   marco establecido (Lustig 2018); nuestro hallazgo es que la *fórmula de asignación misma* —
   al heredar la vara de medición — introduce una brecha distributiva antes de cualquier
   análisis de incidencia del gasto. **La vara con que se mide un municipio vale dinero.**

![Figura 4. Validación por homicidios: R² de validación cruzada de cada conjunto predictor sobre la tasa municipal de homicidios 2019–2021. La composición carga la señal; el residuo latente no aporta.](../figures/06_validacion_homicidios/fig_validacion_homicidios.png)

![Figura 5. Dos varas y dinero: a igual nivel de privación y tamaño, los municipios "más marginados que pobres" (AA) reciben +15.8% de Ramo 33 per cápita respecto de lo esperado (t = 4.3) y los "más pobres que marginados" (BB) −3.0% (n.s.); la brecha AA–BB que anota la figura es ≈19%.](../figures/05_dag/fig_dos_varas_dinero.png)

Las cinco piezas no validan la misma cantidad, y conviene decirlo: homicidios prueba la
ortogonalidad del residuo con la violencia; el satélite, la visibilidad de lo material bruto;
INSABI interpreta un efecto estatal puntual; la exposición criminal aporta un resultado
negativo robusto sobre privación; y la fiscalidad muestra consecuencias distributivas de la
medición. Juntas delimitan qué es — y qué no es — el espacio estimado. En lo único en que sí
se superponen (violencia y privación residual como dimensiones territorialmente distintas)
llegan por caminos independientes, y ahí la convergencia importa más que cada pieza.

## 9. Implicaciones de política

1. **Focalización**: focalizar a los más pobres en todo (nivel bruto) y focalizar los peores
   residuos por dimensión produce listas casi disjuntas. La elección entre ambas es una
   decisión distributiva que hoy se toma implícitamente al elegir índice; conviene tomarla
   explícitamente. Los 48 municipios triple-severos del residuo — que ninguna de las lentes
   usuales selecciona — ilustran lo que la segunda lista vería y la primera no.
2. **La vara que paga**: mientras la fórmula de transferencias conserve pisos heredados de la
   masa carencial, el perfil de marginación seguirá cobrando prima sobre la pobreza vigente a
   igual privación. El diseño de fórmulas debería auditarse contra la circularidad
   medición→dinero→fenómeno (agenda del tercer paper, con montos anuales).
3. **Ninguna lente única**: índice, satélite y registro de eventos ven dimensiones distintas y
   fallan en lugares distintos (la luz no ve pobreza urbana; los eventos no ven donde no hay
   prensa; el índice no ve el residuo). La política que use una sola lente hereda sus puntos
   ciegos — documentados aquí con su geografía.

## Apéndice: baterías de robustez

**A. Ponderación de la partición.** El % entre estados del nivel bruto es estable a población
/ municipio equiponderado / exclusión de municipios <1,000 habitantes (50.8 / 47.6 / 50.7 para
el factor material); el del eje material condicional cae de 23.6 a 0.5 al equiponderar — la
sensibilidad es del objeto distributivo, y se declara.<!-- src: desigualdad_robustez.csv A -->

**B. Umbrales de acumulación** (Tabla 2): la razón observado/esperado y los Jaccard se
reportan en q70/q75/q80/q90 con bootstrap; ninguna configuración lleva la triple severidad
lejos de la independencia.

**C. Homicidios, siete variantes**: ventana temporal, ocurrencia vs residencia, suavizamiento,
transformación, exclusión de metrópolis, pesos y pliegues — el orden de los conjuntos
predictores (composición > bruto > residuo ≈ 0) es estable en las siete; la diferencia
composición−residuo es positiva en todos los pliegues de todas las variantes
(0.06–0.21).<!-- src: sensibilidad_homicidios.csv -->

**D. Crimen: escenarios de cobertura**: los negativos de privación sobreviven sin proxies de
observabilidad, sin las 5 metrópolis y en las tres ventanas de exposición; el contraste
competencia>monopolio sobre homicidio sobrevive las tres ventanas (competencia 0.130 / 0.152 /
0.237 vs monopolio 0.083 / 0.021 / 0.110)<!-- src: g_monopolio_competencia.csv --> y se
atenúa sin la descomposición por número de organizaciones; la coerción histórica mantiene su
asociación con homicidio (t 2.4–2.7) en todos los escenarios.<!-- src: g5_coercion.csv -->

**E. La regresión completa de la brecha** (β estandarizados, efectos fijos estatales, errores
HC1; el cuerpo reporta los tres coeficientes interpretados).<!-- src:
desigualdad_brecha_apropiacion.csv -->

| Regresor | β | t |
|---|---|---|
| empleo precario (%) | +0.226 | 8.6 |
| población en localidades pequeñas (%) | +0.140 | 9.1 |
| log población | +0.151 | 8.3 |
| rugosidad del terreno | −0.135 | −9.1 |
| sector secundario (%) | +0.085 | 8.1 |
| remesas per cápita (log) | −0.072 | −5.3 |
| sector primario (%) | −0.024 | −2.0 |
| sector terciario (%) | −0.023 | −1.6 |
| accesibilidad (km) | −0.010 | −0.8 |

La regresión es además estable a estimar sobre el factor bruto o sobre los seis indicadores
observados directamente; el signo opuesto de remesas por factor (−0.034 material / +0.027
monetario) replica con ambos outcomes.

## Referencias

- Alkire, S. & Foster, J. (2011). Counting and multidimensional poverty measurement. *Journal
  of Public Economics*. doi:10.1016/j.jpubeco.2010.11.006
- Boltvinik, J. (2012). Treinta años de medición de la pobreza en México. *Estudios
  Sociológicos* 30(núm. extra): 79–110. doi:10.24201/es.2012v30nextra.186
- Chen, X. & Nordhaus, W.D. (2011). Using luminosity data as a proxy for economic statistics.
  *PNAS*. doi:10.1073/pnas.1017031108
- Cortés, F. & Valdés Cruz, S. (2023). Desigualdad en la distribución del ingreso: México 2016
  a 2020. En *Los derroteros del desarrollo*. UNAM-PUED.
  doi:10.22201/pued.9786073078337e.2023.c9
- Cortés, F. & Vargas, D. (2011). Marginación en México a través del tiempo: a propósito del
  índice de Conapo. *Estudios Sociológicos* 29(86): 361–387. doi:10.24201/es.2011v29n86.228
- Henderson, J.V., Storeygard, A. & Weil, D.N. (2012). Measuring Economic Growth from Outer
  Space. *American Economic Review*. doi:10.1257/aer.102.2.994
- Jean, N., Burke, M., Xie, M., Davis, W.M., Lobell, D.B. & Ermon, S. (2016). Combining
  satellite imagery and machine learning to predict poverty. *Science*.
  doi:10.1126/science.aaf7894
- Lustig, N. (ed.) (2018). *Commitment to Equity Handbook: Estimating the Impact of Fiscal
  Policy on Inequality and Poverty*, vol. 1. Brookings/CEQ Institute.
  doi:10.5040/9780815753834
- Lustig, N. & Székely, M. (1997). *México: evolución económica, pobreza y desigualdad*.
  Banco Interamericano de Desarrollo. doi:10.18235/0009827
- Shorrocks, A.F. (1984). Inequality Decomposition by Population Subgroups. *Econometrica*.
  doi:10.2307/1913511
- Theil, H. (1979). World income inequality and its components. *Economics Letters*.
  doi:10.1016/0165-1765(79)90213-1
- Trejo, G. & Ley, S. (2021). High-Profile Criminal Violence: Why Drug Cartels Murder
  Government Officials and Party Candidates in Mexico. *British Journal of Political Science*
  51(1): 203–229. doi:10.1017/S0007123418000637. Datos de réplica: Harvard Dataverse,
  doi:10.7910/DVN/VIXNNE.

## Disponibilidad de datos y código

Todos los datos derivados, el código de estimación y los scripts que generan cada figura y
tabla de este artículo están disponibles en el repositorio del proyecto [URL / DOI Zenodo al
depositar], junto con el manifiesto de datos crudos (URLs y advertencias de cada fuente
oficial) y las verificaciones automáticas de consistencia entre texto y resultados. La tabla
suplementaria S1 mapea cada figura y tabla a su script generador y a su archivo de resultados.
Material suplementario adicional: los mapas de medias y desviaciones posteriores de los tres
ejes canónicos, y el mapa de presencia y competencia criminal documentada.
