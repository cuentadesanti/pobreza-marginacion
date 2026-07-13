# La desigualdad territorial mexicana en dos escalas: un modelo de la maquinaria de medición de la privación municipal

**Borrador de trabajo — 2026-07-12**
*Objetivo editorial: Social Indicators Research / World Development (traducción al inglés tras congelar contenido).*

## Resumen

México publica dos mediciones oficiales de la privación municipal — el índice de marginación
(CONAPO, método DP2 sobre el censo) y la pobreza multidimensional (CONEVAL, estimación en áreas
pequeñas) — que con frecuencia cuentan historias distintas del mismo territorio. En lugar de
proponer un índice adicional, modelamos la *maquinaria de medición*: un modelo de variables
latentes (GLLVM) marginalizado que trata los 17 indicadores elementales de ambas agencias como
vistas ruidosas de un espacio común de privación, con efectos de método explícitos, efectos
estatales y una descomposición formal del proceso generador de datos como grafo acíclico
dirigido de 56 nodos verificado computacionalmente. La marginalización de los scores resuelve
la multimodalidad que afecta a estos modelos (R̂ de ΛΛᵀ = 1.003; tres eigenvalores sustantivos
compatibles con rango efectivo 3), y una parametrización del método como contraste
inter-agencia identifica la descomposición de covarianza. Cuatro resultados: (1) la
desigualdad territorial opera en dos escalas — cerca de la mitad de la dispersión de los
indicadores observados ocurre entre estados, mientras la desigualdad residual es
predominantemente intraestatal; (2) las geografías de privación material, educativa y
monetaria residual rara vez se superponen (Jaccard ≤ 0.21) — la acumulación multidimensional
vive en el nivel bruto; (3) existe una brecha de apropiación territorial — actividad económica
visible desde satélite con mejora social local menor a la esperada — explicada ante todo por
precariedad laboral y, en sentido inverso, por remesas; y (4) la discordancia fundacional
entre agencias está mediada por el método: la firma del modelo de imputación de ingreso (SAE)
parte los regímenes de discordancia, mientras que en educación las agencias esencialmente
acuerdan. Cinco validaciones externas independientes (homicidios, luces nocturnas, transición
INSABI, exposición criminal documentada, incidencia fiscal) convergen en la misma estructura.

**Palabras clave:** pobreza multidimensional; marginación; variables latentes; desigualdad
territorial; pequeñas áreas; México.

---

## 1. Introducción

Dos municipios mexicanos pueden mostrar la misma marginación agregada y ocupar posiciones
opuestas en la estructura de la desigualdad: uno carece de infraestructura, otro de ingresos,
otro queda fuera de la actividad económica que ilumina su territorio. Las dos mediciones
oficiales que deberían distinguir estos casos — el índice de marginación de CONAPO y la
pobreza multidimensional municipal de CONEVAL — difieren por construcción: constructos
distintos (territorio vs. personas), instrumentos distintos (censo completo vs. muestra censal
y encuesta), y maquinarias estadísticas distintas (agregación DP2 vs. modelos de áreas
pequeñas calibrados a totales estatales). La pregunta que organiza este trabajo no es cuál
medición es mejor, sino qué estructura — dimensional, de método, estatal, espacial — explica
cuándo y por qué cuentan historias distintas, y qué implica esa estructura para la lectura de
la desigualdad territorial.

Nuestra contribución es triple. Primero, metodológica: formalizamos el proceso generador de
ambas mediciones como un DAG de medición a nivel de variable (56 nodos, 97 aristas tipificadas
en siete semánticas, aciclicidad verificada computacionalmente), del cual se derivan cinco
dependencias mecánicas entre indicadores que cualquier análisis conjunto debe modelar y no
confundir con estructura sustantiva — incluida la circularidad de política del fondo FAIS,
cuya fórmula asigna recursos usando la propia medición de pobreza. Segundo, técnica:
mostramos que la multimodalidad endémica de los GLLVM aplicados (label switching y, más
profundamente, intercambiabilidad entre factores, bloques de método y unicidades) se resuelve
con verosimilitud integrada — marginalizando los scores y monitoreando el subespacio ΛΛᵀ, que
es la cantidad identificada — junto con una parametrización del método como contraste
inter-agencia de dirección fija. Tercero, sustantiva: el modelo convergido produce una lectura
de la desigualdad territorial en dos escalas y cuatro resultados principales, cada uno con su
batería de robustez y su validación externa.

## 2. Datos y el proceso generador como grafo

Trabajamos con los 17 indicadores elementales que alimentan ambas mediciones (9 de CONAPO,
8 de CONEVAL: 6 carencias y 2 líneas de ingreso) para 2,469 municipios en 2020, deliberadamente
sin usar los índices finales, que son funciones deterministas de estos componentes. Los
indicadores se modelan en escala logit estandarizada; los cuatro indicadores modelados por
CONEVAL vía áreas pequeñas no son conteos y una verosimilitud binomial les atribuiría
precisión falsa.

El DAG de medición (Figura 1; objeto canónico en dos tablas versionadas con validación
automática de aciclicidad y de una matriz de tipos permitidos) explicita, entre otras
relaciones: que la pobreza multidimensional no es derivable de las prevalencias marginales
municipales — pasa por la distribución conjunta persona-hogar y una regla de identificación —;
que la estimación SAE y la calibración estatal son operadores secuenciales; que `loc_peq`
(población en localidades pequeñas) es un solo nodo con rol dual — condición estructural de
dispersión *y* componente del índice de marginación, lo que induce una endogeneidad
estructural interna del propio índice —; y que el lazo de política FAIS es acíclico solo al
versionarse temporalmente (pobreza medida en t−1 → asignación → inversión → privación en t).
Los cofactores contextuales (Vista D: ruralidad, demografía, mezcla sectorial, remesas;
Vista E: fiscal; Vista F: lentes satelitales; Vista G: exposición criminal documentada) entran
con dos rutas cada uno — hacia la privación latente y directamente hacia indicadores
específicos por canales que no son privación (costo de red por dispersión, composición de
cohortes, estructura ocupacional, transferencias) — y la especificación identifica la suma de
ambas rutas, límite que se declara.

## 3. Método: el GLLVM marginalizado y la identificación del subespacio

La especificación condicional es η_ij = α_j + λ_j′z_i + β_r,j·rural_i + β_D,j′x_i + γ_j,s(i) +
m_ij + ε_ij. La estimación con scores muestreados exhibe la patología conocida: cadenas en
rotaciones distintas pese a anclas, y — demostrado con un test de alineación Procrustes por
draw — no-convergencia genuina más allá de la rotación (R̂ alineado 2.16), con las cadenas
difiriendo en el reparto de varianza entre factores, bloques de método y unicidades.

La solución tiene tres pasos, cada uno con su diagnóstico. (i) *Marginalizar*: Y_i ~
N(μ_i, ΛΛᵀ + Σ_b λ_b²v_bv_bᵀ + Ψ) elimina ~7,400 parámetros latentes; la estructura de medias
converge de inmediato (R̂ ≤ 1.011) pero la descomposición de covarianza no (R̂ ΛΛᵀ = 2.05).
(ii) *Método como contraste*: los bloques de método con dirección uniforme sobre su soporte
son casi colineales con las cargas del factor; fijar la dirección como contraste inter-agencia
(CONAPO+/CONEVAL−, ortogonal al nivel; solo la magnitud es libre) reduce la multimodalidad
(R̂ 1.53) y es conceptualmente superior: el método *es* el desacuerdo entre instrumentos.
(iii) *Liberar las anclas*: el modo restante era un conflicto anclas-verosimilitud (una cadena
alcanzaba logp +106 pagando un prior extremo por colapsar el ancla monetaria). Sin anclas,
monitoreando solo ΛΛᵀ: R̂ = 1.003 con ESS 3,490, cero divergencias, BFMI 0.91, y tres
eigenvalores sustantivos (1.23, 0.50, 0.34) con el resto cercanos a cero — compatibles con
rango efectivo 3, condicionado a la especificación y escala. Los ejes canónicos se definen por
eigen-descomposición de E[ΛΛᵀ] con convención de signo documentada: eje 1
material-infraestructural, eje 2 educativo, y eje 3 — la dimensión que las anclas suprimían —
un contraste de *vivienda e ingreso contra servicios de red*. Los scores municipales E[z|Y] se
obtienen por regresión GLS por draw, con media y desviación posterior.

Los efectos estatales no son decorativos: la comparación de verosimilitud idéntica entre
peldaños muestra que su inclusión transforma una posterior multimodal en una solución bien
identificada (ELPD +5,410 ± 135; sin γ_s aparece una cuarta dirección latente débil y un eje
rota 53°), y la reducción de unicidad por indicador es proporcional a su share de varianza
estatal — evidencia directa de que, sin γ_s, la heterogeneidad estatal se reparte
ambiguamente entre unicidad y covarianza latente.

## 4. Resultados

### 4.1 La desigualdad opera en dos escalas

En los indicadores observados, cerca de la mitad de la dispersión ponderada por población
ocurre entre estados (Theil entre-estados: 48–59% según indicador; 50.8% para el factor
material bruto), con las líneas de ingreso como lo más federalizado (58.8%) — consistente a la
vez con la calibración estatal del SAE y con el federalismo fiscal. Una vez descontadas
composición y pertenencia estatal, la desigualdad de los ejes canónicos es predominantemente
intraestatal (76–87%). No hay contradicción: los efectos estatales absorben la parte
interestatal antes de estimar el residuo. La partición bruta es robusta al esquema de
ponderación; la residual depende del objeto distributivo — el componente interestatal del
eje 1 casi desaparece al equiponderar municipios (23.6% → 0.5%), es decir, es un fenómeno de
personas concentradas en municipios grandes, no de territorios.

### 4.2 Las geografías residuales rara vez se superponen

Definiendo severidad como el cuartil superior de cada eje canónico, la proporción de
municipios severos en las tres dimensiones (2.0%) apenas excede la esperada bajo independencia
(1.6%; razón 1.25–1.43 según umbral, IC bootstrap rozando 1; Jaccard entre pares 0.05–0.21).
La acumulación multidimensional — el municipio "peor en todo" — es un fenómeno del nivel
bruto, donde domina el factor general; el espacio residual selecciona territorios distintos
por dimensión. Los 48 municipios triple-severos tienen un perfil nítido: la mitad en Oaxaca,
pequeños (mediana 5,430 habitantes), 75% rurales, fuera de la economía de remesas (mediana
17 vs 92 USD pc), con *menos* presencia criminal documentada que el promedio (27% vs 48%) y
casi todos invisibles para la tipología de discordancia (44/48 no significativos en LISA):
los olvidados de los olvidados.

### 4.3 La brecha de apropiación territorial

Definimos la brecha como la discordancia residual entre la actividad económica visible
(predicción de privación material a partir de luces nocturnas y geografía física, fuera de
muestra y con validación espacialmente bloqueada) y la privación social observada. Con efectos
fijos estatales y errores robustos, el predictor dominante es la precariedad laboral
(β = +0.23, t = 8.6) — municipios donde la actividad existe y brilla pero la inserción es por
cuenta propia, jornal o sin pago — seguido del tamaño urbano (+0.15; pobreza urbana invisible
a la luz agregada); las remesas operan en sentido contrario (−0.07, t = −5.3): mejoran
vivienda e ingreso sin huella productiva local equivalente (β de signo opuesto por factor:
−0.034 material, +0.027 monetario). El contraste descriptivo entre colas es elocuente: la
mediana de remesas en los municipios "mejor de lo esperado por sus luces" es ~20 veces
(IC95 14–28) la de los subestimados. La actividad territorial no implica inclusión laboral
local.

### 4.4 La discordancia fundacional es de método

El modelo estima el desacuerdo inter-agencia por familia con dirección fija y magnitud libre.
Tres hechos: en educación las agencias esencialmente acuerdan (carga 0.012) — el desacuerdo
aparente entre indicadores educativos vive en cargas y cohortes, no en método; el desacuerdo
de vivienda-servicios es un fenómeno estatal (carga 0.135 sin efectos estatales, 0.029 con
ellos: huella de la calibración); y el componente de método dominante es la firma del modelo
de ingreso SAE (0.58) — las dos líneas de pobreza moviéndose juntas más allá del factor
monetario. Esa firma municipal parte los regímenes de discordancia: media de −0.325 en los
municipios "más marginados que pobres" y +0.339 en los "más pobres que marginados", con 22.6%
de municipios con firma sustantiva y sin correlación con composición. La discordancia que
motivó el proyecto está, en buena parte, mediada por el método de imputación de ingreso.

La lectura complementaria por indicador acota la interpretación de los efectos estatales: los
indicadores SAE-calibrados no dominan el componente estatal (Δshare vs. directos de CONEVAL:
−0.034, IC95 [−0.060, −0.007]) aunque exhiben un piso de calibración respecto de los censales
(+0.027, [+0.007, +0.049]); la varianza estatal máxima corresponde a la carencia de salud
(0.27), cuya correlación con la dependencia estatal del sistema Seguro Popular/INSABI (+0.61,
la más alta de los 17; placebos 0.18–0.49) la vuelve legible como huella de la transición
sanitaria de 2020. El componente estatal es compatible con heterogeneidad sustantiva —
sectorial además: solo 42% de la varianza de γ es un gradiente común de capacidad — aunque
sigue mezclando política, composición y medición.

## 5. Validaciones externas convergentes

Cinco rutas independientes, ninguna usada en la construcción del espacio latente, convergen:
(i) *homicidios* (100 mil registros oficiales, orden estable en siete variantes de
sensibilidad): la privación explica ~23% de la violencia municipal casi todo vía composición;
el residual no aporta — la señal es un contraste intra-familia casi ortogonal al nivel, por lo
que un índice sintético único no puede focalizar privación y anticipar violencia a la vez;
(ii) *luces nocturnas*: ven la privación material bruta (R² 0.41–0.43 con bloqueo espacial no
administrativo; sin transferencia entre macroregiones) y nada del residual (24/24 R² < 0), con
la relación log-lineal canónica resolviéndose en piso oscuro (14% de municipios), umbrales
regionales con IC disjuntos y sin saturación urbana a escala municipal; (iii) *INSABI* (arriba);
(iv) *exposición criminal documentada* (65 mil eventos diario-municipales con actores):
predice violencia — más bajo competencia que bajo monopolio (+0.130 vs +0.083) — y es
esencialmente ortogonal a la privación residual (resultado negativo documentado con robustez);
y (v) *incidencia fiscal*: a igual privación y tamaño, los municipios "más marginados que
pobres" reciben +15.8% de transferencias del Ramo 33 per cápita (t = 4.3) — el piso heredado
de la fórmula antigua de masa carencial sigue pagando al perfil de marginación, y la vara con
que se mide un municipio vale dinero.

## 6. Incertidumbre y alcance

La desviación posterior municipal es parte del resultado, no una nota: la clasificación
individual es sustantiva (|z|/sd ≥ 2) en 42% de los municipios para el eje material, 55% para
el educativo y solo 14% para el tercero (41.9/54.6/13.6; `certeza_canonica.csv`) — el eje existe como dirección de covarianza nacional,
pero su clasificación municipal individual es débil en la mayor parte del territorio. La
incertidumbre además tiene geografía: es mayor en municipios grandes y urbanos (correlación
+0.32 con población), donde la desviación respecto de la composición es más idiosincrática —
el modelo sabe más del campo que de la ciudad. Los límites se declaran: los resultados son
asociativos; la separación entre las dos rutas de los cofactores requiere restricciones de
exclusión sustantivas; los datos de eventos criminales observan O = R × D y la ausencia de
registro no es ausencia real; y la afirmación multi-escala sobre la relación luz-desarrollo
exige reproducir el análisis en varias escalas sobre los mismos datos.

## 7. Conclusión

La desigualdad territorial mexicana opera en dos escalas. En los indicadores observados,
aproximadamente la mitad de la dispersión ocurre entre estados y la otra mitad dentro de
ellos. Una vez descontada la heterogeneidad estatal, los factores latentes revelan
desigualdades predominantemente intraestatales y geografías de privación material, educativa y
monetaria que rara vez se superponen. La actividad económica visible puede coexistir con
precariedad laboral y con mejoras sociales locales menores de las que sugeriría la luminosidad
del territorio. Y una parte sustancial de la discordancia entre las dos mediciones oficiales
no es del territorio sino de la maquinaria: la firma del método de imputación de ingreso.
Para la política pública las implicaciones son directas: focalizar a los más pobres en todo y
focalizar los peores residuos por dimensión produce listas casi disjuntas; las transferencias
aún pagan a la vara vieja; y ninguna lente única — índice, satélite o registro de eventos —
ve todas las dimensiones a la vez.

La agenda siguiente está declarada: el estudio longitudinal de la circularidad FAIS
(medición → dinero → fenómeno) con montos anuales; la serie 2010–2020; y la réplica del SAE
de CONEVAL para medir — no solo predecir — la correlación inducida por construcción.

---

*Materiales: todos los resultados, figuras y tablas de este manuscrito son reproducibles desde
el repositorio (scripts numerados por capítulo, manifiesto de figuras, DAG canónico en tablas
versionadas con validación automática, y manifiesto de datos crudos con URLs y advertencias de
cada fuente). Las referencias completas con DOI verificado están en
`reports/revision_literatura.md` y se integrarán en la versión de envío.*
