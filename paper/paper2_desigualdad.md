# Desigualdad territorial en México: escalas, dimensiones y límites de la focalización municipal

**Borrador de trabajo (Paper 2, sustantivo) — 2026-07-13**
*Objetivo editorial: World Development (alternativas alineadas: Regional Studies, Journal of Regional Science, World Development Perspectives; español; traducción al enviar).*

## Resumen

México cuenta con dos sistemas oficiales de medición de la privación municipal — el índice de
marginación de CONAPO y la pobreza multidimensional de CONEVAL — que capturan dimensiones
distintas del mismo fenómeno. Este trabajo pregunta cómo se distribuye la desigualdad
territorial entre estados y municipios, y si las distintas dimensiones de privación se
concentran en los mismos lugares. Para responderlo construimos un espacio latente municipal de
privación a partir de los 17 indicadores elementales de ambos sistemas, con efectos de método
y de estado explícitos e incertidumbre municipal cuantificada. Tres resultados. Primero, medido con
la misma descomposición de varianza, el peso de las diferencias entre estados cae de 50.8% en
la privación material observada a 23.6% en su contraparte residual — y a 13–14% en las
dimensiones educativa y de vivienda-ingreso —: una vez descontadas la composición del
municipio y su pertenencia estatal, la heterogeneidad se concentra dentro de los estados (en
los indicadores publicados, la fracción interestatal del índice de Theil va del 31% al
59%<!-- src: desigualdad_theil.csv --> según el indicador). Segundo, las distintas
dimensiones residuales de privación seleccionan municipios diferentes: la coincidencia de
desventaja severa en las tres dimensiones apenas excede la esperada bajo independencia.
Tercero, la actividad económica visible desde satélite no se traduce de forma uniforme en
bienestar local: los municipios que están peor de lo que su actividad sugiere se caracterizan
por precariedad laboral, y los que están mejor, por recepción de remesas. Documentamos
además que la fórmula de transferencias federales, al conservar como piso una asignación
calculada con el instrumento de medición anterior, introduce una diferencia distributiva
entre municipios de igual privación. La implicación central para la política: la focalización depende de qué dimensión de la privación y qué
escala territorial se quiera intervenir, y ningún indicador único resuelve ambas elecciones a
la vez.

**Palabras clave:** desigualdad espacial; pobreza municipal; privación multidimensional;
federalismo fiscal; luces nocturnas; México.

---

## 1. Introducción

Un municipio puede ser pobre de maneras distintas: puede carecer de infraestructura básica,
de escolaridad, o de ingresos suficientes, y esas carencias no siempre llegan juntas. Las dos
mediciones oficiales mexicanas — el índice de marginación de CONAPO y la pobreza
multidimensional municipal de CONEVAL — resumen ese vector de carencias en índices distintos,
y el debate aplicado suele reducirse a cuál de los dos usar. Ese debate deja sin responder
dos preguntas previas que importan más para la política pública: **a qué escala territorial
vive la desigualdad** (¿las brechas relevantes están entre estados o entre municipios del
mismo estado?) y **si las dimensiones de la privación se concentran en los mismos lugares**
(¿el municipio con peor infraestructura es también el de peor escolaridad y menor ingreso?).
De las respuestas depende qué nivel de gobierno puede cerrar cada brecha y si una sola lista
de municipios prioritarios puede servir a programas de naturaleza distinta.

Este trabajo responde ambas preguntas con un espacio latente municipal de privación que
integra los indicadores elementales de los dos sistemas oficiales, en lugar de elegir entre
sus índices. Sus tres contribuciones: (i) documentar que la desigualdad territorial opera en
dos escalas — buena parte de la desigualdad observada coincide con fronteras estatales, pero
la heterogeneidad que queda tras descontar composición y pertenencia estatal es
predominantemente intraestatal; (ii) mostrar que las dimensiones residuales de la privación
seleccionan municipios diferentes, de modo que la concentración multidimensional de
desventaja es un fenómeno del nivel observado, no del residuo; y (iii) medir el desacople
entre la actividad económica visible desde satélite y el bienestar social local, e
identificar sus correlatos (precariedad laboral y remesas). Una batería de análisis externos
— violencia, sensores remotos, instituciones y transferencias fiscales — delimita el alcance
de cada resultado.

El artículo procede así: §2 describe los datos y la construcción del espacio de privación; §3
responde dónde vive la desigualdad territorial (Figura 1, Tabla 1); §4, si las dimensiones de
privación se solapan (Tabla 2, Figura 2); §5 analiza actividad visible y bienestar local
(Figura 3); §6, qué características territoriales predicen la privación (Tabla 3); §7 agrupa
las validaciones externas por la pregunta que responden (Figuras 4 y 5); §8 deriva
implicaciones para la focalización; §9 concluye y §10 discute limitaciones. El apéndice documenta las
baterías de robustez.

## 2. Datos y construcción del espacio de privación

Trabajamos con los 17 indicadores elementales que alimentan ambas mediciones oficiales — 9 de
CONAPO (censales: educación, vivienda, servicios, dispersión, ingreso salarial) y 8 de
CONEVAL (rezago educativo, cinco carencias sociales y dos líneas de pobreza por ingreso) —
para 2,469 municipios en 2020 (2,455 en la matriz de estimación; el paper metodológico
compañero documenta el descarte, que no selecciona por tamaño ni por nivel de privación).

Los 17 indicadores se modelan como realizaciones ruidosas de un espacio común de privación
con tres dimensiones latentes, estimado con un modelo de variables latentes que incluye,
además de los factores: covariables de composición municipal (demografía, mezcla sectorial,
remesas), efectos estado×indicador, y efectos de método que absorben las dependencias
mecánicas entre indicadores que comparten instrumento o modelo estadístico — en particular,
las dos líneas de ingreso de CONEVAL comparten el modelo de imputación de áreas pequeñas, y
su co-movimiento se modela explícitamente. La convergencia se verifica sobre la matriz de
covarianza latente (R̂ = 1.003). Las tres dimensiones resultantes: **material-infraestructural**,
**educativa**, y un contraste de **vivienda e ingreso frente a servicios de red**.

Fijamos la terminología: llamamos *privación* al nivel (observado o latente) de carencia de
un municipio en una dimensión, y *desigualdad territorial* a la dispersión de esa privación
entre municipios. Dos propiedades del espacio estimado gobiernan todo lo que sigue. Primera, cada municipio
tiene una media y una desviación posterior por dimensión, y la inferencia las hereda: los
modelos municipales se ponderan por el inverso de la varianza posterior, y la clasificación
individual de un municipio solo es estadísticamente firme en 42%, 55% y 14% de los casos
según la dimensión<!-- src: certeza_canonica.csv -->. Segunda, distinguimos dos objetos: el
**nivel observado** de privación (los indicadores publicados, o el factor material estimado
sin condicionar) y la **heterogeneidad residual** (las dimensiones del modelo completo, que
descuentan composición y pertenencia estatal). Responden preguntas distintas — "¿dónde está
la privación?" y "¿dónde hay más privación de la que la estructura del municipio explica?" —
y los resultados de §3 y §4 dependen de cuál se mire.

## 3. La distribución territorial de la desigualdad

Parte de las diferencias de privación entre municipios coincide con las fronteras estatales
— los municipios de Chiapas se parecen entre sí y difieren de los de Nuevo León — pero una
fracción importante persiste entre municipios del mismo estado. La pregunta es cuánto pesa
cada componente, y la respuesta cambia según el objeto que se mire (Figura 1).

![Figura 1. Buena parte de la desigualdad observada coincide con fronteras estatales; la heterogeneidad residual vive dentro de los estados. Panel (a): fracción del índice de Theil de cada indicador publicado atribuible a diferencias entre estados (ponderación poblacional). Panel (b): fracción de la varianza del factor material sin condicionar y de las tres dimensiones residuales atribuible a diferencias entre estados. Cada panel usa su propio estadístico; los niveles no se comparan entre paneles.](../figures/09_desigualdad/fig_theil_escalas.png)

El contraste central se mide con un solo estadístico. La fracción de la varianza atribuible
a diferencias entre estados es de 50.8% para el factor material observado y de 23.6% para su
contraparte residual — 13.8% y 13.1% en las dimensiones educativa y de vivienda-ingreso
(Tabla 1, panel B)<!-- src: desigualdad_theil.csv -->. Con la misma medida, el peso
interestatal cae marcadamente — a menos de la mitad — al descontar composición y pertenencia
estatal, y del 76% al 87% de la varianza residual es intraestatal. La textura por indicador
(panel A, índice de Theil) va en la misma dirección y añade un orden informativo: las
diferencias entre estados explican del 31.1% (sin electricidad) al 58.8% (línea de pobreza
por ingreso) de la desigualdad de cada indicador publicado, con mediana de 47.8%. Los
servicios de red — electricidad, drenaje, dispersión — son lo menos alineado con fronteras
estatales (31–35%), mientras que las dos líneas de pobreza por ingreso son lo más
(55.9–58.8%), un patrón consistente tanto con el federalismo fiscal como con el hecho de que
esas líneas se estiman con un modelo calibrado a totales estatales (la huella de método
documentada en el paper compañero). No hay contradicción entre las dos lecturas del factor
material: los efectos estatales absorben la parte interestatal antes de estimar el residuo.
Que la desigualdad del ingreso en México se sostiene predominantemente dentro de las
entidades es un hallazgo recurrente de la literatura distributiva nacional (Cortés & Valdés
Cruz 2023); aquí mostramos que esa escala depende del objeto: en el nivel observado de la
privación el componente interestatal pesa cerca de la mitad, y es la heterogeneidad residual
la que reproduce el predominio intraestatal.

**Tabla 1. Fracción atribuible a diferencias entre estados, por objeto y método de
descomposición** (panel A: fracción del índice de Theil; panel B: fracción de la varianza).<!-- src: desigualdad_theil.csv -->

| Objeto | % entre estados | Método |
|---|---|---|
| línea de pobreza por ingreso | 58.8 | Theil, ponderación poblacional |
| piso de tierra | 54.7 | Theil, ponderación poblacional |
| analfabetismo | 53.1 | Theil, ponderación poblacional |
| sin agua entubada | 40.4 | Theil, ponderación poblacional |
| sin electricidad | 31.1 | Theil, ponderación poblacional |
| factor material (sin condicionar) | 50.8 | varianza entre/dentro |
| dimensión material (residual) | 23.6 | varianza entre/dentro |
| dimensión educativa (residual) | 13.8 | varianza entre/dentro |
| dimensión vivienda-ingreso vs redes (residual) | 13.1 | varianza entre/dentro |

Los resultados del nivel observado cambian poco al ponderar municipios por población o
tratarlos con el mismo peso (50.8 vs 47.6 para el factor material). En el residuo, en cambio,
la contribución de las diferencias entre estados es mucho menor cuando cada municipio recibe
el mismo peso (23.6% → 0.5% en la dimensión material), lo que indica que ese componente
interestatal está impulsado por municipios grandes: es un fenómeno de personas concentradas,
no de territorios.<!-- src: desigualdad_robustez.csv bloque A -->

## 4. Solapamiento entre dimensiones de privación

Los municipios con desventaja severa en una dimensión no suelen ser los mismos que presentan
desventaja severa en las otras. Definiendo desventaja severa como el cuartil superior de cada
dimensión residual, el 43% de los municipios no es severo en ninguna, el 47% lo es en una o
dos, y solo el 2.0% (48 municipios) lo es en las tres — apenas por encima del 1.6% que se
esperaría si las tres dimensiones fueran independientes (Tabla 2, Figura 2). La coincidencia
por pares es igualmente baja (índices de Jaccard de 0.05 a 0.21 según el umbral). En el nivel
observado ocurre lo contrario: ahí domina un factor general y el municipio con carencias
simultáneas en todo sí es la norma entre los más pobres. La concentración simultánea de desventaja es
fuerte en el nivel observado; en el espacio residual, en cambio, no encontramos solapamiento
extremo adicional claramente distinto de la independencia.

**Tabla 2. Coincidencia de desventaja severa entre las tres dimensiones residuales** (razón
entre la proporción observada de municipios severos en las tres y la esperada bajo
independencia; IC bootstrap de 1,000 réplicas).<!-- src: desigualdad_robustez.csv bloque C -->

| Umbral de severidad | obs/esp 3 severas | IC95 | Jaccard (1,2) | Jaccard (1,3) | Jaccard (2,3) |
|---|---|---|---|---|---|
| q70 | 1.25 | [1.00, 1.51] | 0.19 | 0.21 | 0.18 |
| q75 | 1.25 | [0.94, 1.62] | 0.15 | 0.18 | 0.14 |
| q80 | 1.43 | [0.97, 1.99] | 0.13 | 0.15 | 0.10 |
| q90 | 2.44 | [0.80, 4.48] | 0.06 | 0.10 | 0.05 |

![Figura 2. Municipios por número de dimensiones residuales con desventaja severa simultánea (cuartil superior de cada dimensión). La coincidencia en las tres dimensiones — 48 municipios, 2.0% — no difiere claramente de la esperada bajo independencia.](../figures/04_diagnostico_mapas/fig_acumulacion.png)

Los 48 municipios severos en las tres dimensiones — concentrados en Oaxaca, pequeños, rurales
y con baja recepción de remesas — se describen en el suplemento; el grupo es sensible al
umbral y a la dimensión menos precisa del sistema, por lo que se reporta como caracterización
descriptiva.<!-- src: veta_48_triple.csv -->

**Nota metodológica.** Las tres dimensiones residuales se construyen como direcciones
ortogonales de la covarianza latente, de modo que parte del bajo solapamiento es atribuible a
la construcción y no solo a la geografía. Por eso el contraste relevante de la Tabla 2 es
contra la independencia — y la razón observado/esperado cercana a 1 indica que, incluso
tomado con esa cautela, no hay concentración extrema adicional que reportar. El resultado
tampoco depende de la dimensión menos precisa: restringiendo el cálculo a las dos dimensiones
firmes (material y educativa), la razón observado/esperado es 1.07
[0.91, 1.23]<!-- src: solapamiento_2dim.csv --> — aún más cerca de la independencia.

## 5. Actividad económica visible y bienestar local

Las luces nocturnas son el proxy estándar de actividad económica local (Henderson,
Storeygard & Weil 2012; Chen & Nordhaus 2011). Usamos esa señal en sentido inverso al
habitual: en lugar de predecir pobreza para sustituir encuestas, medimos el **desacople**
entre lo que la actividad visible sugiere y lo que la medición social observa.

La medida se construye en tres pasos, todos fuera de muestra: (i) se predice la privación
material de cada municipio a partir de sus luces nocturnas y su geografía física, con
validación cruzada agrupada por estado (la predicción de cada municipio proviene de un modelo
que no vio ningún municipio de su estado); (ii) el desacople es el residual entre privación
observada y predicha; (iii) ese residual se regresa sobre características municipales con
efectos fijos estatales, errores robustos y coeficientes estandarizados. Un valor positivo
significa que el municipio está *peor* socialmente de lo que su actividad visible sugiere.
Dos límites de diseño: el modelo predictivo ya incluye luz y geografía (no es un contraste
puro de luz contra bienestar), y se usa la predicción puntual sin propagar su incertidumbre.

El correlato dominante del desacople es la precariedad laboral (β = +0.23, t = 8.6)<!-- src:
desigualdad_brecha_apropiacion.csv -->: municipios donde hay actividad económica visible pero
la inserción de los trabajadores es por cuenta propia, por jornal o sin remuneración. Le
sigue el tamaño urbano (+0.15): la pobreza de las ciudades es poco visible en la luz
agregada. Las remesas operan en sentido contrario (−0.07, t = −5.3): mejoran vivienda e
ingreso sin una huella productiva local equivalente — y el efecto tiene el signo esperado en
cada dimensión (−0.034 sobre la material, +0.027 sobre la monetaria<!-- src:
satelital_remesas_reg.csv -->). El contraste entre colas resume el patrón: la mediana de
remesas en los municipios que están mejor de lo que sus luces sugieren es unas 20 veces la de
los municipios subestimados — 440 contra 21 USD per cápita; IC95 bootstrap de la razón
14–28 — (Figura 3). Interpretamos el desacople como evidencia compatible con una traducción incompleta de la
actividad visible en bienestar local; la etiqueta **brecha de apropiación territorial** es una
lectura interpretativa de esos coeficientes, no una identificación causal. La regresión completa está
en el apéndice E.

![Figura 3. Privación observada contra predicha por luces nocturnas y geografía (predicción fuera de muestra, bloqueada por estado). Los municipios por encima de la diagonal están peor de lo que su actividad visible sugiere y se caracterizan por precariedad laboral; los municipios por debajo, mejor, y se caracterizan por recepción de remesas.](../figures/07_satelital/fig_satelital_discordancia.png)

## 6. Predictores territoriales de la privación

¿Qué características del territorio se asocian con el nivel de privación? Estimamos la
capacidad predictiva de cuatro bloques de variables sobre la privación material, con
validación cruzada bloqueada por estado (la evaluación siempre ocurre en estados que el
modelo no vio; Tabla 3). La geografía física heredada — rugosidad del terreno, elevación,
aislamiento, dispersión poblacional — explica por sí sola una parte real pero limitada. La
composición demográfica y, sobre todo, la estructura productiva — qué sectores emplean a la
población y cuán precaria es esa inserción — aumentan mucho la capacidad predictiva. La
composición indígena añade poca señal adicional una vez incluidos los bloques anteriores, lo
que no indica irrelevancia causal ni histórica: es compatible con que la desventaja indígena
esté fuertemente superpuesta con la geografía, la demografía y la inserción productiva que ya
están en el modelo. Dos disciplinas de lectura: la contribución marginal de cada bloque
depende del orden en que entra (los incrementos no son atribuciones), y todo el ejercicio es
predictivo, no causal.

La lectura sustantiva: la privación material no es principalmente una consecuencia del
relieve o del aislamiento. Su predictibilidad aumenta de forma marcada cuando se incorpora la
forma en que el territorio está poblado e integrado productivamente — lo que sugiere que la
desigualdad material combina restricciones geográficas con procesos históricos de
urbanización y empleo.

**Tabla 3. Capacidad predictiva de bloques de características territoriales sobre la
privación material** (R² de validación cruzada bloqueada por estado; los bloques entran
acumulativamente en el orden mostrado).<!-- src: desigualdad_robustez.csv capa3 -->

| Bloque (acumulativo) | Variables | R²cv |
|---|---|---|
| geografía heredada | rugosidad, elevación, aislamiento, dispersión | 0.265 |
| + composición demográfica | estructura etaria, dependencia | 0.469 |
| + estructura productiva | mezcla sectorial, precariedad laboral | 0.732 |
| + composición indígena | % hablantes de lengua indígena, % monolingüe | 0.775 |

*Nota: añadir la pertenencia estatal eleva el ajuste a 0.891, pero con validación no
bloqueada por estado; no es comparable con las filas de la tabla.*

## 7. Validaciones externas

Tres grupos de análisis externos — ninguno usado en la construcción del espacio de privación
— delimitan qué es y qué no es la heterogeneidad residual.

### 7.1 ¿La desigualdad residual coincide con la geografía de la violencia?

Los tres análisis siguientes producen el mismo patrón general: no.

*Homicidios.* Para medir si la privación anticipa violencia, usamos 103 mil registros
oficiales de homicidio (2019–2021) y comparamos la capacidad de cinco conjuntos de
información municipal para predecir la tasa suavizada, con validación cruzada (Figura 4). La
privación explica alrededor del 23% de la variación municipal de la violencia, pero casi todo
proviene de las características de composición del municipio; los factores residuales no
aportan capacidad predictiva adicional<!-- src: validacion_homicidios.csv -->. El orden es
estable en siete variantes de diseño (ventana temporal, lugar de registro, suavizamiento,
exclusión de metrópolis), y la diferencia entre composición y residuo es positiva en todos
los pliegues de todas las variantes (0.06–0.21)<!-- src: sensibilidad_homicidios.csv -->.

*Exposición criminal documentada.* Para evaluar si la desigualdad residual coincide con la
presencia del crimen organizado, agregamos 65 mil eventos documentados a nivel municipal
(2000–2018) y distinguimos la presencia de una sola organización de la competencia entre
varias. La competencia se asocia más fuertemente con homicidios que la presencia simple
(+0.130, t = 4.0, contra +0.083, t = 3.1)<!-- src: g_monopolio_competencia.csv -->, pero
ninguna medida de exposición explica de forma robusta los factores residuales de privación.
Dado que los registros dependen de cobertura y detección, todas las especificaciones incluyen
proxies de observabilidad, e interpretamos estas variables como exposición documentada, no
como control territorial real.

*Coerción política histórica.* Los ataques del crimen organizado contra autoridades y
candidatos municipales (2007–2012; Trejo & Ley 2021) tampoco muestran una ruta robusta hacia
la privación residual de 2020 — el indicador es nulo en dos dimensiones y contradictorio en
la tercera —, pero sí predicen homicidio una década después (+0.26, t = 2.7)<!-- src:
g5_coercion.csv --> y ocurrieron donde coincidían competencia criminal y fragmentación
política. La coerción política histórica conserva asociación con la violencia posterior, pero no con
las dimensiones residuales de privación.

La lectura conjunta: violencia y privación son dimensiones territorialmente distintas. Un
índice de privación — observado o residual — no sirve como mapa de riesgo de violencia, y
viceversa.

![Figura 4. Capacidad de cinco conjuntos de información municipal para predecir la tasa de homicidios 2019–2021 (R² de validación cruzada). Las características de composición del municipio concentran la señal; los factores residuales de privación no aportan.](../figures/06_validacion_homicidios/fig_validacion_homicidios.png)

### 7.2 ¿Qué dimensiones de la privación pueden observarse desde el espacio?

Solo el nivel material observado. Las luces nocturnas predicen la privación material sin
condicionar (R² de 0.41–0.43 incluso con bloqueo espacial no administrativo), pero
esencialmente nada de la heterogeneidad residual: ninguna combinación de modelo, dimensión y
estimador supera un R² de 0.03, y 26 de 30 son negativas<!-- src: satelital_modelos.csv -->.
La relación luz-privación tampoco es la log-lineal simple de la literatura global (Jean et
al. 2016, como referente): a escala municipal se resuelve en regímenes — un piso oscuro (14%
de municipios con luz cercana a cero y privación muy variable) y umbrales regionales con
intervalos disjuntos. Implicación: los sensores remotos sirven para mapear el nivel material
de la privación donde no hay datos, no para sustituir la medición social fina.

### 7.3 ¿Los efectos estatales y las diferencias de medición tienen correlatos institucionales y fiscales?

Sí, y de dos tipos. *Institucional:* la varianza estatal máxima del sistema corresponde a la
carencia de acceso a la salud, y su correlación con la dependencia estatal del extinto Seguro
Popular (+0.61, la más alta de los 17 indicadores; placebos entre 0.18 y 0.49)<!-- src:
validacion_insabi.csv --> es compatible con la huella de la transición al INSABI en 2020 — el
componente estatal contiene señal de política institucional real, no únicamente calibración
estadística, aunque la correlación es sugestiva y no una identificación.

*Fiscal:* las transferencias federales responden al perfil de medición del municipio. A igual
nivel de privación y tamaño, los municipios clasificados como más marginados que pobres
reciben +15.8% de transferencias del Ramo 33 per cápita (t = 4.3), y los clasificados como
más pobres que marginados, −3.0% (no significativo)<!-- src: gap_aportaciones_regimen.csv -->
(Figura 5). La brecha entre ambos perfiles (≈19 puntos) descansa sobre el brazo positivo: el
intervalo al 95% de la *diferencia* entre perfiles, con remuestreo por conglomerado estatal,
va de −2.0% a +47.4%<!-- src: b_fism_descomposicion.csv --> — la asociación concentra su masa
en brechas positivas, pero la diferencia en sí pierde significancia convencional cuando se
reconoce que los regímenes de medición se agrupan por estado.

El correlato institucional es conocido en su mecánica y nuevo en la lectura que proponemos.
La fórmula vigente del fondo de infraestructura social (art. 34 de la Ley de Coordinación
Fiscal, reforma de diciembre de 2013) asigna a cada unidad lo que recibió en 2013 — el piso —
más una participación en el crecimiento del fondo que sí se reparte por las carencias de la
población en pobreza extrema medida por CONEVAL. Ese piso de 2013 se calculó con la fórmula
anterior, construida sobre el Índice Global de Pobreza: cinco necesidades básicas censales
(ingreso, educación, espacio de la vivienda, drenaje y electricidad-combustible) homólogas a
los insumos del índice de marginación, y de ahí que el perfil del piso se aproxime a la vara
de marginación y no a la de pobreza. Que el piso congela la distribución previa a la reforma
está documentado: CONEVAL (2015) cuantificó la diferencia entre repartir el fondo 2014 con la
fórmula nueva y conservar la asignación de 2013, la Auditoría Superior de la Federación
(2013) describió la práctica inercial y la opacidad del reparto federalizado, y la literatura
del FAIS encontraba desde antes una focalización débil (Díaz Cayeros & Silva Castañeda 2004;
Chiapa & Velázquez 2011). Lo que esos antecedentes no formulan es la consecuencia entre
varas: como el piso hereda un instrumento (≈marginación) discordante del que gobierna el
incremento (pobreza CONEVAL), dos municipios de igual privación latente cobran distinto según
cuál de las dos mediciones oficiales los pinte peor. Y el piso todavía domina el fondo: en
términos reales (INPC, factor 1.310), la asignación de 2013 equivalía en 2020 a 81.0% del
FISM municipal<!-- src: b_fism_descomposicion.csv -->.

Para probar el mecanismo descompusimos la transferencia de 2020 en piso más incremento en los
municipios con FISM rastreable en ambos años en los reportes trimestrales de la SHCP (SRFT):
249 municipios, 10.1% del modelo — una intersección sesgada hacia municipios más grandes,
menos rurales y menos privados que el resto (apéndice G, Figura A1), aunque dentro de ella
la brecha del Ramo 33 agregado se reproduce (+17.2%,
t = 2.4)<!-- src: b_fism_descomposicion.csv -->. El resultado apunta en la dirección del
mecanismo sin cerrarlo: la brecha entre perfiles se concentra en el piso (+600 pesos por
habitante) y no en el incremento (−149), pero el intervalo de la diferencia cruza cero
([−1,221, +2,838]) (Figura 6). El brazo con potencia estadística es el espejo del perfil
favorecido: los municipios más pobres que marginados parten de un piso 32.9% menor que el de
municipios comparables (IC 95% [−46.6%, 0.0%]) y el incremento — repartido con la vara de
pobreza — los compensa parcialmente (+342 pesos por habitante, t = 2.2): la fórmula nueva
corrige en el margen lo que la vieja les negó. Con efectos fijos estatales todas las brechas
se disuelven; la variación del piso es interestatal, consistente con que el reparto municipal
de 2013 fue decisión de cada estado (art. 35 LCF) sobre un perfil federal común. La lectura
conjunta es la de un legado en erosión, no un estado estacionario: el peso del piso cae
mecánicamente con cada ejercicio en que el fondo crece, y la brecha de 2020 es la fotografía
de un sesgo que se diluye. La evidencia es asociativa y de un solo corte; la descomposición
es sugestiva, con la cobertura declarada como su límite. El análisis de incidencia de la
política fiscal sobre la desigualdad tiene un marco establecido (Lustig 2018); nuestro
hallazgo es anterior a esa etapa: la fórmula de asignación misma, al heredar el instrumento
de medición, puede introducir una diferencia distributiva antes de cualquier análisis de
incidencia del gasto.

![Figura 5. Transferencias federales por habitante según el nivel de privación y el perfil de medición del municipio. A igual privación y tamaño, el perfil "más marginado que pobre" recibe +15.8% respecto de lo esperado (t = 4.3) y el perfil "más pobre que marginado" −3.0% (n.s.); la brecha entre ambos perfiles es ≈19%, con IC 95% de la diferencia (bootstrap por conglomerado estatal) de −2.0% a +47.4%.](../figures/05_dag/fig_dos_varas_dinero.png)

![Figura 6. Descomposición de la transferencia FISM 2020 en piso 2013 (fórmula del Índice Global de Pobreza) e incremento (fórmula de pobreza extrema CONEVAL), en los 224 municipios con dato en ambos años y controles completos (privación y su cuadrado, población, ruralidad, FORTAMUN per cápita). La brecha entre perfiles se concentra en el piso (+600 pesos por habitante) y no en el incremento (−149), con intervalo de la diferencia que cruza cero; el perfil "más pobre que marginado" parte de un piso 32.9% menor y el incremento lo compensa parcialmente (+342 pesos per cápita, t = 2.2). Evidencia sugestiva: cobertura de 10.1% del modelo, sesgada hacia municipios grandes.](../figures/05_dag/fig_b_piso_incremento.png)

## 8. Implicaciones para la focalización

1. **La medición asigna dinero antes que el gasto.** El hallazgo con mayor alcance general
   es fiscal: cuando una fórmula de transferencias hereda — como piso o como insumo — el
   instrumento con que se midió la carencia, puede introducir una diferencia distributiva
   entre territorios de igual privación *antes* de cualquier decisión de gasto. En México ese
   mecanismo se asocia con +15.8% de Ramo 33 per cápita para el perfil favorecido, y la
   descomposición piso/incremento apunta en la misma dirección sin cerrarla; el diseño de
   fórmulas debería auditarse contra esta circularidad medición→asignación — una hipótesis
   exportable a cualquier sistema de transferencias basado en fórmula (las cláusulas de
   *hold harmless* son comunes en los sistemas de igualación), ilustrada aquí con México.
2. **La focalización depende de la dimensión y de la escala.** Ordenar municipios por
   privación observada y ordenarlos por sus peores residuos dimensionales produce listas casi
   disjuntas. La primera lista concentra la desventaja acumulada; la segunda identifica
   municipios que están peor de lo que su estructura explica en una dimensión específica.
   Elegir un índice es elegir implícitamente una de las dos; conviene que esa elección sea
   explícita y responda al instrumento de política en cuestión.
3. **La escala señala al nivel de gobierno.** La parte de la desigualdad observada que
   coincide con fronteras estatales — mayor en ingreso, menor en servicios de red — es
   materia de coordinación federal-estatal; la heterogeneidad residual, predominantemente
   intraestatal, requiere capacidad de discriminación fina dentro de cada estado, que las
   fórmulas nacionales agregadas difícilmente capturan con precisión.
4. **Ningún indicador único cubre todos los usos.** El nivel observado no anticipa violencia;
   los sensores remotos no ven el residuo ni la pobreza urbana; los registros de crimen
   dependen de la detección; y las fórmulas de transferencia heredan los sesgos del
   instrumento con que se midió. Cada fuente de información cubre dimensiones distintas y tiene errores de
   medición propios, documentados aquí; la política que use una sola hereda sus puntos
   ciegos.

## 9. Conclusión

La desigualdad territorial mexicana no puede reducirse a una sola jerarquía municipal. Una
parte importante de la privación observada sigue fronteras estatales — más en el ingreso,
menos en los servicios de red — pero las diferencias residuales, las que quedan una vez
descontado lo que la composición y la pertenencia estatal explican, se concentran dentro de
los estados. Las dimensiones residuales de la privación, además, rara vez identifican los
mismos municipios, y la actividad económica visible desde satélite no garantiza un bienestar
local proporcional: donde el desacople es mayor, la constante es la precariedad laboral.

Los tres hallazgos trascienden el caso mexicano: el patrón de dos escalas aplica a cualquier
país cuya medición en áreas pequeñas se calibre a unidades administrativas; el desacople
entre luminosidad y bienestar es replicable dondequiera que coexistan sensores nocturnos y
medición social; y el sesgo de fórmula heredado del instrumento de medición es un mecanismo
general de reproducción de desigualdad que precede al análisis fiscal estándar.

Para la política pública, estos resultados implican que la focalización debe especificar
tanto la dimensión de la privación como la escala territorial de la intervención: ninguna
lista única de municipios prioritarios sirve simultáneamente a programas de infraestructura,
educación e ingreso, y ningún nivel de gobierno puede cerrar por sí solo brechas que viven a
escalas distintas. El límite principal del ejercicio es su naturaleza asociativa y de corte
transversal: describe la estructura de la desigualdad, no sus mecanismos.

## 10. Limitaciones

Los resultados son de corte transversal (2020) y de naturaleza asociativa; ninguna relación
reportada se identifica causalmente. Las dimensiones residuales son scores latentes con
incertidumbre municipal — firme en 42%, 55% y 14% de los municipios según la dimensión — y
toda inferencia la hereda por ponderación, pero la clasificación individual de municipios
específicos debe leerse con esa cautela. Las dimensiones se construyen como direcciones
ortogonales, lo que contribuye por construcción al bajo solapamiento de §4; el contraste
contra independencia mitiga pero no elimina esa objeción. La medida de desacople de §5 usa
predicciones puntuales fuera de muestra sin propagar su incertidumbre. Los datos de crimen
documentan exposición filtrada por detección, no presencia real. Y la distinción entre
desigualdad observada y residual, central al argumento, depende de la especificación del
modelo de medición (paper compañero): otros condicionamientos producirían otros residuos.

## Apéndice: baterías de robustez

**A. Ponderación de la partición.** El porcentaje entre estados del nivel observado es
estable a ponderar por población, equiponderar municipios o excluir municipios de menos de
1,000 habitantes (50.8 / 47.6 / 50.7 para el factor material); el de la dimensión material
residual cae de 23.6 a 0.5 al equiponderar — la sensibilidad es del objeto distributivo y se
declara en §3.<!-- src: desigualdad_robustez.csv A -->

**B. Umbrales de coincidencia** (Tabla 2): la razón observado/esperado y los índices de
Jaccard se reportan en los umbrales q70/q75/q80/q90 con bootstrap; ninguna configuración
aleja la triple severidad de la independencia.

**C. Homicidios, siete variantes**: ventana temporal, ocurrencia vs residencia,
suavizamiento, transformación, exclusión de metrópolis, pesos y pliegues — el orden de los
conjuntos predictores (composición > nivel observado > residuo ≈ 0) es estable en las siete;
la diferencia composición−residuo es positiva en todos los pliegues de todas las variantes
(0.06–0.21).<!-- src: sensibilidad_homicidios.csv -->

**D. Crimen, escenarios de cobertura**: los resultados nulos sobre privación sobreviven sin
proxies de observabilidad, sin las cinco metrópolis y en las tres ventanas de exposición; el
contraste competencia>monopolio sobre homicidio sobrevive las tres ventanas (competencia
0.130 / 0.152 / 0.237 contra monopolio 0.083 / 0.021 / 0.110)<!-- src:
g_monopolio_competencia.csv --> y se atenúa sin la descomposición por número de
organizaciones; la coerción histórica mantiene su asociación con homicidio (t 2.4–2.7) en
todos los escenarios.<!-- src: g5_coercion.csv -->

**E. Regresión completa del desacople de §5** (coeficientes estandarizados, efectos fijos
estatales, errores robustos HC1; el cuerpo reporta los tres coeficientes
interpretados).<!-- src: desigualdad_brecha_apropiacion.csv -->

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

La regresión es estable a estimar el desacople sobre el factor material o sobre los seis
indicadores observados directamente; el signo opuesto de las remesas por dimensión (−0.034
material / +0.027 monetaria) replica con ambos.

**F. Los 48 municipios severos en las tres dimensiones** (suplemento): 24 de 48 en Oaxaca;
mediana de 5,430 habitantes contra ~13,550 nacional; 79% con al menos la mitad de su
población en localidades pequeñas; recepción de remesas mediana de 17 contra 92 USD per
cápita; 27% con presencia criminal documentada contra 48% nacional; 44 de 48 no
significativos en la tipología espacial de discordancia.<!-- src: veta_48_triple.csv -->

**G. Cobertura del test piso/incremento del FISM (§7.3).** La intersección de municipios con
FISM rastreable en 2013 y 2020 en el SRFT (249; 10.1% del modelo) difiere sistemáticamente
del resto: más poblada (SMD +0.59), menos rural (−0.28) y menos privada (−0.36), con Hidalgo
y Puebla sobrerrepresentados y sin Oaxaca ni Veracruz<!-- src: b_fism_cobertura.csv -->. Este
sesgo de cobertura es la razón por la que la descomposición del §7.3 se reporta como
sugestiva y no como evidencia de mecanismo.

![Figura A1. Chequeo de sesgo de cobertura del test piso/incremento: municipios de la intersección SRFT 2013∩2020 contra los excluidos del modelo, en población, ruralidad, privación total, los tres ejes canónicos y composición por estado (diferencias de medias estandarizadas, SMD).](../figures/05_dag/fig_b_cobertura_sesgo.png)

## Referencias

- Alkire, S. & Foster, J. (2011). Counting and multidimensional poverty measurement. *Journal
  of Public Economics*. doi:10.1016/j.jpubeco.2010.11.006
- Auditoría Superior de la Federación (2013). *Diagnóstico sobre la opacidad en el gasto
  federalizado*. ASF, Cámara de Diputados.
  https://www.asf.gob.mx/uploads/56_Informes_especiales_de_auditoria/Diagnostico_sobre_la_Opacidad_en_el_Gasto_Federalizado_version_final.pdf
- Boltvinik, J. (2012). Treinta años de medición de la pobreza en México. *Estudios
  Sociológicos* 30(núm. extra): 79–110. doi:10.24201/es.2012v30nextra.186
- Chen, X. & Nordhaus, W.D. (2011). Using luminosity data as a proxy for economic statistics.
  *PNAS*. doi:10.1073/pnas.1017031108
- Chiapa, C. & Velázquez, C. (coords.) (2011). *Estudios del Ramo 33*. El Colegio de México,
  Centro de Estudios Económicos / CONEVAL. https://libros.colmex.mx/tienda/estudios-del-ramo-33/
- CONEVAL (2015). *Análisis del uso de los recursos del Fondo de Aportaciones para la
  Infraestructura Social (FAIS)*. Consejo Nacional de Evaluación de la Política de Desarrollo
  Social.
  https://www.coneval.org.mx/EvaluacionDS/PP/CEIPP/ERG33/Documents/Analisis_Recursos_FAIS_2015.pdf
- Cortés, F. & Valdés Cruz, S. (2023). Desigualdad en la distribución del ingreso: México 2016
  a 2020. En *Los derroteros del desarrollo*. UNAM-PUED.
  doi:10.22201/pued.9786073078337e.2023.c9
- Cortés, F. & Vargas, D. (2011). Marginación en México a través del tiempo: a propósito del
  índice de Conapo. *Estudios Sociológicos* 29(86): 361–387. doi:10.24201/es.2011v29n86.228
- Díaz Cayeros, A. & Silva Castañeda, S. (2004). *Descentralización a escala municipal en
  México: la inversión en infraestructura social*. CEPAL, Serie Estudios y Perspectivas 15,
  Sede Subregional en México. https://repositorio.cepal.org/handle/11362/4935
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
tabla de este artículo están disponibles en el repositorio del proyecto (https://github.com/cuentadesanti/pobreza-marginacion; archivo
permanente: doi:10.5281/zenodo.21344720), junto con el manifiesto de datos crudos (URLs y advertencias de cada fuente
oficial) y las verificaciones automáticas de consistencia entre texto y resultados. La tabla
suplementaria S1 mapea cada figura y tabla a su script generador y a su archivo de
resultados. Material suplementario adicional: los mapas de medias y desviaciones posteriores
de las tres dimensiones, el mapa de presencia y competencia criminal documentada, la
caracterización de los 48 municipios triple-severos, y el chequeo de sesgo de cobertura del
test piso/incremento del FISM (`fig_b_cobertura_sesgo`).
