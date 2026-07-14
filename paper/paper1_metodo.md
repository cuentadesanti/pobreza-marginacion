# La maquinaria de medición: por qué dos burocracias cuentan historias distintas del mismo territorio

**Borrador de trabajo (Paper 1, metodológico) — 2026-07-13**
*Objetivo editorial: Social Indicators Research (español; traducción al enviar).
Encuadre: contribución aplicada-metodológica con validación de identificación por simulación reducida (apéndice F) — no una teoría general de GLLVM.*

## Resumen

México publica dos mediciones oficiales de la privación municipal — el índice de marginación
(CONAPO, agregación DP2 sobre el censo) y la pobreza multidimensional (CONEVAL, estimación en
áreas pequeñas calibrada a totales estatales) — que con frecuencia cuentan historias distintas
del mismo territorio. En lugar de proponer un índice adicional, modelamos la *maquinaria de
medición*: formalizamos el proceso generador de ambas mediciones como un DAG de medición a
nivel de variable (56 nodos, 97 aristas tipificadas, aciclicidad verificada
computacionalmente) y estimamos un modelo de variables latentes (GLLVM) marginalizado que
trata los 17 indicadores elementales de ambas agencias como vistas ruidosas de un espacio
común de privación, con efectos de método explícitos y efectos estatales. Tres contribuciones.
Primera, técnica: el principal problema de identificación y convergencia de esta aplicación —
la multimodalidad entre factores, bloques de método y unicidades — se resuelve con una
secuencia diagnóstica de tres pasos — verosimilitud integrada, efectos de método sobre
direcciones de dependencia metodológica predefinidas, y monitoreo del subespacio ΛΛᵀ, la
cantidad identificada (R̂ = 1.003; tres eigenvalores sustantivos compatibles con rango
efectivo 3). Segunda, el resultado fundacional, en dos afirmaciones de estatus distinto: las dos
líneas de pobreza por ingreso — dos umbrales sobre la misma variable de ingreso estimada en
áreas pequeñas (correlación municipal 0.984) — comparten un componente que los indicadores
censales directos no tienen (carga 0.58), la huella del modelo de ingreso y de su calibración
estatal, que parte limpiamente los regímenes espaciales de discordancia; y la evidencia de
método identificada con claridad es la calibración estatal: el desacuerdo de vivienda-servicios
— indicadores censales directos, sin modelo de ingreso de por medio — cae de 0.135 a 0.029 al
condicionar en efectos de estado, mientras que en educación las agencias esencialmente
acuerdan (0.012). Tercera, epistemológica:
la incertidumbre posterior municipal es parte del resultado — la clasificación individual es
sustantiva en 42/55/14% de los municipios según el eje, y esa incertidumbre tiene geografía
propia: la representación es más precisa en municipios rurales y pequeños que en los urbanos y
grandes, un patrón que sobrevive a incorporar el error estándar oficial de las estimaciones de
áreas pequeñas. Un estudio de simulación de identificación y una capa de error de medición
heteroscedástica acotan el alcance de las dos afirmaciones de método.

**Palabras clave:** pobreza multidimensional; marginación; variables latentes; error de
medición; pequeñas áreas; México.

---

## 1. Introducción: dos mediciones, una pregunta de estructura

Dos municipios mexicanos pueden mostrar la misma marginación agregada y ocupar posiciones
opuestas en la estructura de la desigualdad: uno carece de infraestructura, otro de ingresos,
otro queda fuera de la actividad económica que ilumina su territorio. Las dos mediciones
oficiales que deberían distinguir estos casos — el índice de marginación de CONAPO y la
pobreza multidimensional municipal de CONEVAL — difieren por construcción: constructos
distintos (territorio vs. personas), instrumentos distintos (censo completo vs. muestra censal
y encuesta), y maquinarias estadísticas distintas (agregación DP2, en la tradición de Peña
Trapero — véanse Peña-Trapero 2021 y Zarzosa Espina 2021 — vs. modelos de áreas pequeñas
calibrados a totales estatales; Rao & Molina 2015). La pregunta que organiza este trabajo no
es cuál medición es mejor, sino qué estructura — dimensional, de método, estatal — explica
cuándo y por qué cuentan historias distintas.

La respuesta corta de este paper: una parte sustancial de la discordancia no es del territorio
sino de la maquinaria — la huella del modelo de ingreso en áreas pequeñas y, con la
identificación más limpia, la de su calibración a totales estatales. Llegar a esa respuesta
con garantías exige dos piezas que constituyen la
contribución metodológica: un DAG de medición que hace explícitas las dependencias mecánicas
que un análisis conjunto no debe confundir con estructura sustantiva (§3), y una estrategia de
estimación e identificación que resuelve el principal problema de identificación y
convergencia de esta aplicación en lugar de ocultarlo (§4). El paper compañero explota el
espacio latente resultante para la lectura sustantiva de la desigualdad territorial.

El resto del artículo procede así: §2 sitúa la contribución en la literatura; §3 presenta los
datos y el DAG de medición (Figura 1); §4 desarrolla el método — especificación, priors,
estimación y la secuencia de identificación (Tabla 1, Figura 2); §5 presenta el resultado
fundacional (Tabla 2, Figura 3); §6 la certeza municipal y su geografía (Figuras 4 y 5); §7 la
descomposición de los efectos estatales (Tabla 3); §8 discute. El apéndice técnico documenta
la escalera completa con scores muestreados, el test de alineación Procrustes y la comparación
formal con y sin efectos estatales.

## 2. Antecedentes y trabajo relacionado

La medición oficial de la pobreza multidimensional mexicana pertenece a la familia de conteo
de Alkire & Foster (2011): carencias dicotomizadas por persona, agregadas con una regla de
identificación. El índice de marginación de CONAPO viene de otra tradición — la distancia DP2
de Peña Trapero, diseñada para agregar indicadores territoriales continuos sin ponderaciones
arbitrarias (Peña-Trapero 2021; Zarzosa Espina 2021, para su uso regional en España, el molde
del uso mexicano). Ambas tradiciones producen *índices*; la literatura comparada suele
preguntarse cuál ordena mejor. Nuestra pregunta es anterior: qué proceso generador conjunto
explica que dos agregaciones defendibles del mismo territorio diverjan donde divergen. Para
los cuatro indicadores municipales que CONEVAL no observa sino estima, la maquinaria relevante
es la estimación en áreas pequeñas — el emparejamiento censo-encuesta con predicción empírica
mejor (Elbers, Lanjouw & Lanjouw 2003; Molina & Rao 2010; el marco de producción oficial en
Tzavidis et al. 2018) y calibración a totales estatales (Deville & Särndal 1992) que
sintetizan Rao & Molina (2015) — y esa maquinaria, mostramos,
deja una huella en la covarianza inter-agencia: identificable con claridad en el caso de la
calibración estatal, y como co-movimiento del bloque de ingreso cuya atribución exacta entre
método y estructura discutimos en §5.

El instrumento natural para modelar vistas múltiples y ruidosas de un constructo común es el
modelo de variables latentes generalizado (GLLVM; Skrondal & Rabe-Hesketh 2004), cuya
aplicación moderna a matrices multivariadas de gran escala está estandarizada en ecología
(Niku et al. 2019) pero sigue siendo rara en medición de pobreza. La dificultad práctica que
esta literatura reporta — multimodalidad posterior, sensibilidad a anclas, label switching —
suele tratarse como estorbo computacional; aquí la tratamos como información: distinguir qué
parte es rotación inocua y qué parte es no-identificación real es precisamente lo que permite
separar factores, método y federalismo. La raíz conceptual de nuestro efecto de método es la
matriz multirrasgo-multimétodo de Campbell & Fiske (1959): dos instrumentos que miden los
mismos rasgos comparten varianza de método además de varianza de rasgo. Nuestro aporte a esa
tradición es de parametrización — direcciones de dependencia metodológica *predefinidas* y de
dirección fija, ortogonales al nivel, que resuelven la colinealidad método-factor que las
direcciones uniformes inducen — y de objeto: hasta donde sabemos, nadie ha modelado la
maquinaria conjunta de dos agencias estadísticas del mismo país como problema latente con
método explícito y proceso generador documentado como grafo.

En la literatura mexicana, la crítica canónica al índice de marginación es la de Cortés &
Vargas (2011), continuada en su análisis longitudinal (Cortés & Vargas 2013): el índice de
CONAPO confunde constructo con método y no es comparable en el tiempo sin reconstrucción. La
propia CONAPO respondió a esa línea crítica en el eje temporal: el índice 2020 — el objeto que
aquí modelamos — ya no es el PCA histórico sino la agregación DP2, adoptada precisamente para
mejorar la comparabilidad (Peláez Herreros 2022, quien muestra además que la migración tampoco
resuelve por completo la comparabilidad intertemporal). Nuestro aporte es la pieza que ninguno
de los dos movimientos cubre: la separación formal constructo (z) / método (m) / heterogeneidad
federal (γ) en el corte transversal. El debate de larga data sobre umbrales y agregación de la
pobreza multidimensional (Boltvinik 2012) y la tradición de series comparables de pobreza y
desigualdad bajo cambio de instrumento (Székely 2005) son el trasfondo sustantivo: dos
mediciones oficiales del mismo fenómeno con maquinarias en disputa. Las metodologías oficiales
que aquí se modelan están documentadas por las propias agencias (CONEVAL 2021a para la
medición municipal de pobreza; CONAPO 2021 para el índice de marginación 2020), y el DAG de §3
es, en buena medida, su lectura formalizada.

Dos precisiones de mapa completan el encuadre. Primera, el comparador que un lector mexicano
echará de menos: el índice de rezago social de CONEVAL (IRS), censal, municipal y construido
por componentes principales (CONEVAL 2021c) — es decir, de las mismas unidades y la misma
tradición territorial que la marginación. No lo usamos como tercera vista por una razón de
diseño: el contraste que este paper explota es el de *constructo y maquinaria* (territorio
agregado por DP2 contra persona-derechos estimada por áreas pequeñas); el IRS está, por
construcción, del lado CONAPO de ese contraste — un PCA censal territorial más — y añadirlo
aportaría instrumento redundante, no información de método nueva. Segunda, la posición
ontológica del modelo. Un GLLVM es *reflectivo*: postula un espacio latente del que los
indicadores son realizaciones ruidosas. Los objetos que modelamos no lo son: la pobreza
multidimensional es axiomático-normativa (carencias de derechos definidas por regla, no rasgo
descubierto) y la DP2 es formativa (el índice se define por sus componentes). Tratar sus
indicadores elementales como reflexiones de z es por tanto una decisión de estrategia
analítica — leer z como "el espacio de privación común que generan los indicadores que ambas
agencias comparten" — y no una afirmación de que z sea lo que las agencias miden o deban
medir. El caso más delicado es la población en localidades pequeñas, que es condición
estructural de dispersión además de componente del índice (el rol dual del DAG, §3.2): su
lectura reflectiva es la más discutible de las 17 y el modelo la señala en lugar de ocultarla.

## 3. Datos y el proceso generador como DAG de medición

### 3.1 Indicadores

Trabajamos con los 17 indicadores elementales que alimentan ambas mediciones para 2,469
municipios en 2020; la matriz del modelo tiene 2,455 tras exigir covariables completas. Los
14 excluidos son en su mayoría municipios de creación reciente (los seis nuevos de Chiapas,
tres de Morelos, San Quintín, Seybaplaya, Bacalar, Puerto Morelos) que las series fuente de
covariables — en particular la de remesas — aún no incorporan; van de 4,315 a 117,568
habitantes en siete estados, de modo que el descarte no selecciona por tamaño ni por nivel de
privación. Los indicadores: 9 de CONAPO desde el censo (analfabetismo, sin educación básica,
sin drenaje, sin electricidad, sin agua entubada, piso de tierra, hacinamiento, población en
localidades pequeñas, ingresos hasta 2 salarios mínimos) y 8 de CONEVAL (rezago educativo y
las carencias de salud, seguridad social, vivienda, servicios básicos y alimentación — en la
metodología de conteo de Alkire & Foster 2011 — más las dos líneas de pobreza por ingreso).
Deliberadamente no usamos los índices finales, que son funciones deterministas de estos
componentes. Los cuatro indicadores que CONEVAL modela vía áreas pequeñas (las dos líneas de
ingreso, y las carencias estimadas con el emparejamiento censo-ENIGH; Rao & Molina 2015) no
son conteos: una verosimilitud binomial les atribuiría precisión falsa, por lo que toda la
matriz se modela en escala logit estandarizada (§4.1).

### 3.2 El DAG de medición

El DAG — cuyo objeto canónico son dos tablas versionadas de 56 nodos y 97 aristas en siete
semánticas tipificadas, con validación automática de aciclicidad y de una matriz de tipos
permitidos — explicita, entre otras relaciones:

- que la pobreza multidimensional **no es derivable de las prevalencias marginales
  municipales** — pasa por la distribución conjunta persona-hogar y una regla de
  identificación;
- que la estimación SAE y la calibración estatal son **operadores secuenciales**
  (SAE → preliminares → calibración → publicados), cada uno con su huella;
- que la población en localidades pequeñas es un solo nodo con **rol dual** — condición
  estructural de dispersión *y* componente del índice de marginación, lo que induce una
  endogeneidad estructural interna del propio índice;
- que el lazo de política FAIS es acíclico solo al **versionarse temporalmente** (pobreza
  medida en t−1 → asignación → inversión → privación en t): la fórmula asigna recursos usando
  la propia medición de pobreza, y esa circularidad es una propiedad del sistema de medición,
  no un artefacto del análisis;
- y que los cofactores contextuales entran con **dos rutas** cada uno — hacia la privación
  latente y directamente hacia indicadores específicos por canales que no son privación
  (costo de red por dispersión, composición de cohortes, estructura ocupacional,
  transferencias) — de las cuales la especificación identifica la suma, límite que se declara.

De este grafo se derivan cinco dependencias mecánicas entre indicadores que el modelo debe
absorber en bloques de método y no en factores: las dos líneas de ingreso comparten el modelo
SAE; los cuatro indicadores SAE comparten la calibración estatal; los indicadores censales de
CONAPO comparten instrumento; las carencias de vivienda y servicios comparten definiciones
fronterizas; y educación aparece en ambas agencias con cohortes distintas. La Figura 1
presenta la vista conceptual del grafo; la versión completa a nivel de variable, con las 97
aristas auditables, está en el material suplementario.

![Figura 1. El proceso generador de las dos mediciones, vista conceptual (25 nodos; las placas ×N indican repetición sobre la familia de indicadores). El grafo canónico completo — 56 nodos y 97 aristas tipificadas, aciclicidad verificada computacionalmente — está en el suplemento. El lazo de política FAIS aparece temporalizado (t−1…t+2); el borde grueso indica el nodo con rol dual.](../figures/05_dag/fig_dag_main.png)

## 4. Método

### 4.1 Transformación de escala

Cada indicador municipal se observa como porcentaje y_j ∈ [0, 100]. Se transforma con
corrección de continuidad c = 0.5, p_j = (y_j + c) / (100 + 2c), luego logit(p_j) y
estandarización por indicador ("escala logit-z"). La corrección evita ±∞ en los ceros
estructurales (p. ej., municipios sin viviendas con piso de tierra) sin recortar información;
la estandarización hace comparables las cargas entre indicadores de dispersión muy distinta.
Una nota de consistencia: aplicar la corrección a los cuatro indicadores estimados por áreas
pequeñas los trata como observados cuando son estimaciones con error propio — es coherente
con la limitación declarada de unicidad homoscedástica (§8) y se levanta en la capa de error
de medición de §5.3.

### 4.2 Especificación y priors

El marco es un GLLVM (Skrondal & Rabe-Hesketh 2004; en su implementación aplicada moderna,
Niku et al. 2019) con verosimilitud gaussiana en escala logit-z y scores marginalizados. La
media condicional del indicador j en el municipio i es

  η_ij = α_j + λ_j′z_i + β_r,j·rural_i + β_D,j′x_i + γ_j,s(i) + m_ij + ε_ij,

con z_i ∈ ℝ³ los factores latentes, x_i las covariables de composición (demografía, mezcla
sectorial, remesas), γ_j,s efectos estado×indicador y m_ij efectos de método por familia.
Marginalizando z y m, la verosimilitud integrada es

  Y_i ~ MvN(μ_i, Σ),  Σ = ΛΛᵀ + Σ_b λ_b² v_b v_bᵀ + Ψ,

donde Λ (17×3) apila las cargas, v_b son las tres direcciones de dependencia metodológica
*fijas* (§4.4) con magnitud λ_b libre, y Ψ = diag(σ_j²) las unicidades. Priors: λ_jk ~ N(0, 1)
sin restricciones (especificación libre); coeficientes de media W ~ N(0, 1); efectos estatales
γ_j,· ~ ZeroSumNormal(σ = 0.5) por indicador (la restricción de suma cero separa nivel
nacional de desviación estatal; la robustez a un hiperprior sobre esa escala se examina en el
apéndice E); magnitudes de método λ_b ~ HalfNormal(0.5); unicidades
σ_j ~ HalfNormal(1). La extensión espacial BYM2 (Besag, York & Mollié 1991, en la
reparametrización de Riebler et al. 2016) se evaluó como especificación adicional de la
escalera; su patología de frontera (ρ → 1) se documenta en el apéndice A.

### 4.3 Estimación y diagnósticos

NUTS con 4 cadenas, 1,000 de calentamiento + 1,000 draws por cadena, target_accept 0.9,
semilla fija. La cantidad monitoreada es ΛΛᵀ — el subespacio, invariante a rotación — no Λ.
Distinguimos tres veredictos de convergencia: **estructural** (R̂ y ESS sobre ΛΛᵀ y funciones
invariantes), **no-rotacional** (parámetros de media y varianza: W, γ, σ, λ_b) e
**interpretativo** (estabilidad de los ejes nombrados tras la convención de orientación).
Un modelo puede pasar el segundo y fallar el primero; reportar solo R̂ de parámetros de media
oculta exactamente la patología que importa.

### 4.4 La secuencia de identificación

Denotamos la escalera con scores muestreados como especificaciones S1–S4: S1 (GLLVM base), S2
(+covariables de composición), S3 (+efectos estatales), S4 (+BYM2 espacial); y los modelos de
verosimilitud integrada como M−γ (marginalizado sin efectos estatales) y M+γ (con ellos). La
estimación con scores muestreados exhibe la patología conocida: cadenas en rotaciones
distintas pese a anclas y — demostrado con un test de alineación Procrustes por draw
(apéndice B) — no-convergencia genuina más allá de la rotación (R̂ alineado 2.16), con las
cadenas difiriendo en el reparto de varianza entre factores, bloques de método y unicidades.
La solución tiene tres pasos, cada uno con su diagnóstico (Tabla 1):

1. **Marginalizar.** La verosimilitud integrada elimina ~7,400 parámetros latentes; la
   estructura de medias converge de inmediato (R̂ ≤ 1.011) pero la descomposición de
   covarianza no (R̂ ΛΛᵀ = 2.05): la multimodalidad no provenía únicamente de los scores
   municipales.
2. **Direcciones de dependencia metodológica predefinidas.** Los bloques de método con
   dirección uniforme sobre su soporte son casi colineales con las cargas del factor; fijar
   cada dirección desde el DAG — con solo la magnitud libre — reduce la multimodalidad
   (R̂ 1.53 — medido *aún con las anclas puestas*, el paso intermedio de esta secuencia en la
   especificación con γ_s; la coincidencia con el R̂ = 1.530 del modelo sin efectos estatales
   de la Tabla 1 es un accidente numérico entre dos corridas distintas) y es conceptualmente
   superior — la lógica de la matriz multirrasgo-multimétodo de Campbell & Fiske (1959)
   llevada a parametrización. Dos de las tres direcciones son contrastes inter-agencia
   (CONAPO+/CONEVAL−, ortogonales al nivel): educación {analf +½, sin_basica +½, rezago_educ
   −1} y vivienda-servicios {drenaje, electricidad, agua +⅓ cada uno; car_vivienda,
   car_servbas −½ cada uno}. La tercera es un **bloque intra-agencia**: las dos líneas de
   ingreso {+1, +1}, que captura su co-movimiento más allá del factor monetario — el bloque
   donde se espera la huella del modelo de ingreso compartido, no un desacuerdo entre
   agencias (qué puede y qué no puede atribuirse a ese bloque se discute en §5). Cada v_b se
   normaliza a norma 1. La sensibilidad de las cargas a los pesos exactos de las direcciones
   se examina en el apéndice E (barrido de ±20%).
3. **Liberar las anclas.** El modo restante era un conflicto anclas-verosimilitud (una cadena
   alcanzaba logp +106 pagando un prior extremo por colapsar el ancla monetaria). Sin anclas,
   monitoreando solo ΛΛᵀ: **R̂ = 1.003** con ESS 3,490, cero divergencias, BFMI 0.91, y tres
   eigenvalores sustantivos de E[ΛΛᵀ] (1.23, 0.50, 0.34) con el resto cercanos a cero —
   compatibles con rango efectivo 3, condicionado a la especificación y escala; no es una
   prueba de K (la comparación formal de K = 2, 3, 4 — que favorece *predictivamente* a
   K=4 — está en §4.6).

**Tabla 1. La escalera de convergencia.** Nomenclatura: S1–S4 = escalera con scores
muestreados; M−γ / M+γ = verosimilitud integrada sin/con efectos estatales — dos ejes
distintos (muestreado/marginalizado × sin/con γ_s), no una sola escalera. Los ELPD solo se
comparan dentro del mismo bloque de verosimilitud: la escalera muestreada usa verosimilitud
condicional puntual; los marginalizados, MvN integrada — el objeto predictivo
cambia.<!-- src: tabla1_escalera.csv -->

| Modelo | Moran I resid. | R̂ | ELPD-LOO | ¿Converge? |
|---|---|---|---|---|
| S1 (base, z muestreada) | 0.413 | 2.19 | −25,833.6 | no (multimodal) |
| S2 (+ covariables de composición) | 0.345 | 2.70 | −15,624.4 | no (multimodal) |
| S3 (+ efectos estatales) | 0.223 | 1.90 | −13,554.7 | no (multimodal) |
| S4 (+ BYM2 espacial) | 0.323 | 2.50 | −16,855.0 | no (multimodal) |
| M−γ (marginalizado sin γ_s) | 0.345 | 1.530 | −29,516.1 | no (multimodal) |
| **M+γ (marginalizado con γ_s, canónico)** | **0.223** | **1.003** | **−24,106.1** | **sí** |

El Moran de los marginalizados se calcula sobre el residuo condicional Y − E[Y|Y] — el
análogo exacto del residuo con z muestreada<!-- src: moran_marginal.csv -->. El del modelo
canónico (0.223) no es cero: queda estructura espacial en los residuos, de modo que las
desviaciones posteriores de z y de las cargas de método deben leerse como cotas inferiores
de la incertidumbre — una calificación que heredan la geografía de la incertidumbre de §6 y
los intervalos del apéndice. Descartar BYM2 por su patología de frontera (apéndice A) no
exime de este diagnóstico; por eso se reporta.

Los ejes canónicos se definen por eigen-descomposición de E[ΛΛᵀ] con convención de signo
documentada (elemento mayor positivo; ejes por draw alineados al canónico): eje 1
material-infraestructural, eje 2 educativo, y eje 3 — la dimensión que las anclas suprimían —
el contraste de *vivienda e ingreso contra servicios de red*. Los scores municipales E[z|Y] se
obtienen por regresión GLS por draw — ẑ_i = E[Λᵀ Σ⁻¹ (Y_i − μ_i)] sobre el posterior — con
media y desviación posterior por municipio y eje (Figura 2 muestra la descomposición de
varianza resultante por indicador).

![Figura 2. Descomposición de varianza por indicador a lo largo de la escalera S1–S4: factor común, método, covariables, estado y unicidad. La reducción de unicidad al añadir efectos estatales es proporcional al share de varianza estatal de cada indicador.](../figures/02_escalera_gllvm/fig_escalera_vardecomp.png)

### 4.5 Qué hacen los efectos estatales

Los efectos estatales no son decorativos, y el orden del argumento importa. (i) Sin γ_s el
modelo no identifica una posterior estable: el marginalizado sin efectos estatales sigue
estructuralmente multimodal — la multimodalidad no era solo label switching. (ii) En esa
especificación aparece una cuarta dirección latente débil y un eje rota 53° respecto de la
solución canónica (apéndice C). (iii) Al incluir γ_s, la reducción de unicidad por indicador
es proporcional a su share de varianza estatal — evidencia directa de que, sin γ_s, la
heterogeneidad estatal se reparte ambiguamente entre unicidad y covarianza latente. (iv) La
comparación de verosimilitud idéntica favorece al modelo con efectos estatales (ELPD
+5,410 ± 135), pero este contraste es descriptivo y se interpreta con cautela: uno de los dos
modelos comparados no está bien identificado.

### 4.6 Selección formal del número de factores

"Rango efectivo 3" era, hasta esta versión, una decisión de especificación apoyada en los
eigenvalores; la comparación formal la convierte en resultado calificado. Estimamos M+γ con
K = 2, 3 y 4 en el mismo bloque de verosimilitud marginalizada<!-- src: seleccion_k.csv -->.
K=2 empeora el ajuste (ΔELPD −1,337 ± 55) y ni siquiera identifica el subespacio (R̂ ΛΛᵀ =
1.530): dos factores no bastan. K=4 mejora la predicción sobre K=3 (ΔELPD +331 ± 32, con el
subespacio convergido, R̂ = 1.003) — lo declaramos sin atenuantes. Dos hechos califican esa
mejora. Primero, el espacio canónico no se mueve: los ángulos principales entre los tres
primeros eigen-ejes de K=3 y K=4 son 1.2°, 2.6° y 15.2° — los ejes que el paper interpreta
son los mismos. Segundo, el cuarto eje es pequeño (7.3% de la varianza común) y su patrón de
cargas — las dos líneas de ingreso (+0.38, +0.37), el ingreso censal (+0.33) y la carencia
alimentaria (+0.31) contra la carencia de vivienda (−0.57) — es un contraste de instrumento
de ingreso, no una dimensión sustantiva nueva: exactamente la vecindad donde §5 localiza la
huella del modelo de ingreso. La elección de K=3 es por tanto de parsimonia interpretable —
tres ejes con lectura sustantiva y un subespacio que K=4 no altera — no de ajuste: el ELPD
favorece a K=4 y así queda dicho; quien prefiera el criterio predictivo puro debe añadir un
cuarto eje que refracciona el bloque monetario-instrumental, no una dimensión nueva de
privación.

## 5. Resultado fundacional: la huella de la maquinaria en la discordancia

### 5.1 El componente de método por familia

El modelo estima el componente de método por familia sobre su dirección predefinida, con
magnitud libre, y produce scores municipales E[m|Y] con incertidumbre — la proyección GLS del
residuo sobre la dirección correspondiente, escalada por su carga posterior, análoga a E[z|Y].
La Tabla 2 resume; la Figura 3 mapea.

**Tabla 2. El componente de método por familia.** M−γ/M+γ = marginalizado sin/con efectos
estatales (Tabla 1); cargas = desviación estándar del componente de método. "% sustantivo" =
municipios con |m|/sd ≥ 2. Medias por régimen espacial de la discordancia observada (AA =
"más marginado que pobre").<!-- src: desacuerdo_familias.csv -->

| Familia | Carga M−γ | Carga M+γ | % sustantivo | media AA | media BB |
|---|---|---|---|---|---|
| educación (contraste inter-agencia) | 0.012 | 0.012 | 0.0 | 0.000 | 0.000 |
| líneas de ingreso (huella del modelo de ingreso) | **0.582** | **0.574** | **22.6** | **−0.325** | **+0.339** |
| vivienda-servicios (contraste inter-agencia) | 0.135 | 0.029 | 0.0 | 0.021 | 0.012 |

Tres hechos:

1. **En educación las agencias esencialmente acuerdan** (carga 0.012) — el desacuerdo aparente
   entre indicadores educativos vive en cargas y cohortes, no en método.
2. **El desacuerdo de vivienda-servicios es huella de la calibración estatal** (carga 0.135
   sin efectos estatales, 0.029 con ellos). Esta es la evidencia de método identificada con
   más limpieza del paper: los cinco indicadores del contraste son censales *directos* — no
   pasan por el modelo de ingreso — y sin embargo su desacuerdo inter-agencia se disuelve al
   condicionar en estado. El único operador de la maquinaria que actúa a esa escala es la
   calibración de los resultados municipales a las estimaciones estatales directas (CONEVAL
   2021a, §4.5, que aplica la calibración de Deville & Särndal 1992): el operador induce
   correlación intra-estatal en indicadores que no comparten ninguna otra mecánica.
3. **El componente dominante es la huella del modelo de ingreso en áreas pequeñas** (0.58) —
   las dos líneas de pobreza moviéndose juntas más allá del factor monetario. Esa huella
   municipal parte los regímenes espaciales de discordancia: media de −0.325 en los municipios
   "más marginados que pobres" y +0.339 en los "más pobres que marginados", con 22.6% de
   municipios con componente sustantivo y sin correlación con composición (|r| ≤ 0.001 con
   dispersión rural, envejecimiento y tamaño poblacional<!-- src: desacuerdo_familias.csv
   corr_* -->).

### 5.2 Qué es atribuible a la maquinaria y qué no

La carga de 0.58 admite dos lecturas que conviene separar porque tienen estatus probatorio
distinto. La afirmación **(a)**, que este diseño sí identifica: *las dos líneas de ingreso
comparten un componente municipal que los indicadores censales directos no tienen*, y ese
componente — no un residuo difuso — es el que parte los regímenes espaciales de discordancia.
La afirmación **(b)**, que este diseño por sí solo no separa: *cuánto de ese componente es
método de estimación y cuánto es estructura genuina de la distribución del ingreso*. La razón
es mecánica y hay que decirla: las dos líneas son dos umbrales sobre la misma variable de
ingreso estimada (correlación municipal 0.984 en escala del modelo; 0.942 condicionando en
los otros 15 indicadores<!-- src: corr_lineas.csv -->), de modo que su co-movimiento más allá
de un factor monetario unidimensional se esperaría incluso sin maquinaria compartida — si la
distribución del ingreso tiene más de una dimensión efectiva, ese exceso también aparecería.
Por eso el argumento de método del paper no descansa en el 0.58 sino en la calibración
(hecho 2), donde la explicación distribucional no está disponible: los indicadores del
contraste de vivienda no comparten variable de ingreso alguna. La huella del ingreso queda
como el componente *descriptivamente* dominante — real, municipal, espacialmente estructurado
— cuya atribución fina entre modelo de áreas pequeñas y estructura del ingreso exige el error
estándar oficial del SAE como capa de error de medición (§5.3) y, para el reparto
factor/método en general, el estudio de simulación del apéndice F.

El resultado sigue siendo fundacional en el sentido que importa: reordena qué preguntas
territoriales son formulables con estas mediciones — las comparaciones de ingreso entre
municipios dentro de un estado arrastran el componente compartido de las líneas (sea cual sea
su origen último), mientras que las comparaciones educativas son limpias de método y las de
vivienda-servicios solo requieren condicionar en estado.

![Figura 3. La anatomía del método. (a) La huella del modelo de ingreso en áreas pequeñas (carga 0.58): rojo = las dos líneas de ingreso se desvían juntas hacia más pobreza de lo que el factor monetario explica. (b) El desacuerdo vivienda-servicios CONAPO vs CONEVAL (0.135 sin efectos estatales; 0.029 con ellos: fenómeno estatal — huella de la calibración estatal).](../figures/04_diagnostico_mapas/fig_desacuerdo_agencias.png)

La lectura complementaria por indicador acota — como falsación posible, no como prueba — la
interpretación de los efectos estatales: los indicadores SAE-calibrados no dominan el
componente estatal (Δshare vs. directos de CONEVAL: −0.034, IC95 [−0.060, −0.007]) aunque
exhiben un piso de calibración respecto de los censales (+0.027,
[+0.007, +0.049]).<!-- src: tabla_medicion_federalismo.csv -->

### 5.3 Una capa de error de medición sobre los indicadores estimados

La objeción de método más directa es que la unicidad homoscedástica trata las cuatro
estimaciones de áreas pequeñas como si fueran observadas. CONEVAL publica el error estándar
municipal de esos indicadores; lo incorporamos como una capa de unicidad *heteroscedástica* —
la diagonal de Σ deja de ser constante entre municipios y suma, indicador por indicador, la
varianza de estimación oficial (propagada a la escala logit por el método delta), agrupando
los municipios en bandas de precisión para mantener tratable la verosimilitud. El modelo así
ampliado converge (R̂ ΛΛᵀ = 1.004, cero divergencias)<!-- src: nivel1_hetero_resumen.csv -->
y responde dos preguntas.

Primera, si la carga de las líneas era un artefacto de tratar estimaciones como datos: no lo
es. La carga del bloque de ingreso pasa de 0.574 a 0.572 al reconocer el error oficial —
prácticamente inalterada—, y las de educación y vivienda tampoco se mueven. El componente
compartido de las líneas sobrevive a descontar la imprecisión de su estimación.

Segunda, si la "geografía de la incertidumbre" de §6 era ese artefacto. Aquí el dato del
propio insumo orienta la lectura antes que el modelo: el error estándar del SAE es *menor* en
los municipios grandes (correlación −0.56 con el log de la población para la línea de ingreso;
negativa en siete de los ocho indicadores<!-- src: sae_se_municipal.parquet, ver manifiesto -->),
de modo que reconocerlo devuelve algo de imprecisión a los municipios pequeños y debería
atenuar — no crear — el patrón de mayor precisión rural. Es justo lo que ocurre: la correlación
de la desviación posterior con el tamaño baja de 0.34 a 0.31 en el eje material y de 0.26 a
0.19 en el eje de vivienda-ingreso — donde el error del SAE pesa más— sin invertirse ni
desaparecer<!-- src: nivel1_hetero_resumen.csv -->. La geografía de la incertidumbre se atenúa
al corregir por el error de medición, pero persiste: no es un subproducto de la
homoscedasticidad. (El ELPD del modelo heteroscedástico no es comparable con el homoscedástico
—fija por fuera una parte de la varianza en lugar de estimarla— y no se usa como contraste de
ajuste.)

## 6. Identificación del subespacio e incertidumbre municipal

La identificación es del subespacio, no de los ejes. Las etiquetas "material", "educativo" y
"vivienda-ingreso contra redes" nombran la base de ejes principales de E[ΛΛᵀ] — una elección
matemática con convención documentada, no constructos identificados por rotación sustantiva —
y toda lectura aplicada debe anclarse en la certeza de clasificación, que reportamos por eso
como resultado. La clasificación individual es sustantiva (|z|/sd ≥ 2)
en 41.9% de los municipios para el eje material, 54.6% para el educativo y solo 13.6% para el
contraste de vivienda-ingreso contra servicios de red<!-- src: certeza_canonica.csv --> — ese
tercer eje existe como dirección de covarianza nacional, pero su clasificación municipal
individual es débil en la mayor parte del territorio, y todo uso aplicado debe heredar esa
distinción (Figuras 4 y 5).

![Figura 4. Certeza posterior por eje canónico: |E[z]|/SD[z] clasificado en indistinguible de cero (<1), sugerente (1–2) y sustantivo (≥2). Sustantivo: 41.9% (eje material), 54.6% (educativo), 13.6% (vivienda-ingreso vs redes).](../figures/04_diagnostico_mapas/fig_certeza_canonica.png)

![Figura 5. Los tres ejes canónicos del espacio latente condicional: media posterior E[z|Y] (arriba) y desviación posterior (abajo) por municipio, modelo marginalizado convergido (R̂ ΛΛᵀ = 1.003).](../figures/04_diagnostico_mapas/fig_mapas_canonicos.png)

La incertidumbre tiene además geografía propia: la desviación posterior municipal crece con el
tamaño y la urbanización (correlación +0.322 con log población en el eje material; −0.259 con
ruralidad<!-- src: veta_ignorancia.csv -->). Condicionado en las covariables, la
representación municipal es más precisa en municipios rurales y pequeños que en los urbanos y
grandes — un patrón opuesto al de los diseños muestrales, que saben más donde hay más gente.
Antes de interpretarlo hay que descartar el artefacto obvio: que el patrón sea un subproducto
de tratar con una sola varianza de unicidad a indicadores SAE cuyo error de estimación es
heteroscedástico. La capa de error de medición de §5.3 es el test directo, y lo descarta —el
patrón se atenúa pero persiste al incorporar el error oficial, que además es *menor* en los
municipios grandes, de modo que empuja en contra del patrón, no a su favor. Superado ese
descarte, una explicación plausible — no identificada — es la
heterogeneidad urbana intra-municipal: la desviación respecto de la composición es más
idiosincrática precisamente donde el municipio agrega realidades internas más diversas. Ambas
lecturas heredan, además, la calificación del Moran residual (§4.4): las desviaciones
posteriores son cotas inferiores.

## 7. Qué hacen los efectos estatales: federalismo sectorial y legibilidad institucional

El componente estatal estimado no es un gradiente único. La descomposición espectral de la
matriz γ (17 indicadores × 32 estados) muestra que solo 42% de su varianza es un factor
común — interpretable como capacidad estatal: correlaciona +0.42 con el log del PIB estatal
per cápita, IC95 de Fisher [0.08, 0.67] con n = 32 — y el 58% restante es específico por
dominio de política: **federalismo sectorial**, no un ranking de estados (valores exactos en
la Tabla 3; en prosa redondeamos; la partición es robusta a liberar la escala de γ con un
hiperprior — 40.7% contra 41.8% del PC1, apéndice E). Las correlaciones estatales de esta sección son puntos
sobre 32 observaciones: distinguibles de cero pero anchas — la de gasto/PIBE, −0.48, lleva
IC [−0.71, −0.16]<!-- src: ic_fisher_estatales.csv --> — y deben leerse hacia la
incertidumbre, no hacia el punto.

**Tabla 3. Descomposición espectral de los efectos estatales** (SVD de la matriz γ 17×32
centrada por indicador).<!-- src: tabla3_gamma.csv, veta_gamma_pca.csv -->

| Medida | Valor |
|---|---|
| Share de varianza del PC1 (gradiente común) | 41.8% |
| Share de varianza del PC2 | 14.9% |
| Share específico por dominio (sectorial) | 58.2% |
| corr(PC1 estatal, log PIBE per cápita) | +0.42 |
| corr(PC1 estatal, gasto estatal / PIBE) | −0.48 |
| Indicadores con mayor peso en PC1 | carencia serv. básicos (−0.40), hacinamiento (−0.38), línea de pobreza (−0.34) |

Un episodio institucional vuelve legible esta lectura — y es, en su mecanismo más probable,
un episodio *del instrumento*, no solo del acceso. La varianza estatal máxima corresponde a
la carencia de salud (0.27), cuya correlación con la dependencia estatal del sistema Seguro
Popular/INSABI (+0.61, la más alta de los 17 indicadores, IC95 [0.33, 0.79]; placebos
0.18–0.49<!-- src: validacion_insabi.csv -->) es compatible con la huella de la transición
sanitaria de 2020. La propia CONEVAL (2021b) documenta que el reactivo de afiliación quedó a
caballo de la transición — la pregunta pasó de "¿está afiliado al Seguro Popular?" a incluir
el derecho a los servicios del INSABI — y que parte del salto nacional de la carencia (su
cifra, de la ENIGH nacional, no de la serie censal municipal que usamos) podría deberse a que
la población no reconoció su nueva adscripción. Nuestro +0.61 se lee entonces como
reclasificación diferencial por estado en el instrumento de captación — los estados más
dependientes del esquema saliente son donde el reactivo pierde más cobertura nominal — antes
que como pérdida real de atención proporcional; señal sugestiva en ambos casos, no una
identificación. El componente estatal es compatible con heterogeneidad sustantiva, aunque
sigue mezclando política, composición y medición; esa mezcla es un límite declarado, no un
defecto ocultable.

## 8. Discusión: qué significa modelar la maquinaria

Modelar la maquinaria en lugar de proponer otro índice cambia el tipo de conclusión
disponible. No decimos qué municipio "es" más pobre; decimos qué parte del desacuerdo entre
las mediciones oficiales es huella de la maquinaria del ingreso (el bloque de las líneas),
qué parte es calibración estatal (vivienda), qué
parte es federal (γ sectorial) y qué parte queda como estructura territorial — y con qué
certeza municipal (dicho en corto: el modelo sabe más del campo que de la ciudad, y lo
declara).

Los límites: los resultados son asociativos; la separación entre las dos rutas de los
cofactores requiere restricciones de exclusión sustantivas que no imponemos; la identificación
del rango efectivo 3 está condicionada a especificación y escala — y la selección formal
(§4.6) favorece predictivamente a K=4, con K=3 conservado por parsimonia interpretable; y la
huella del modelo de ingreso se estima desde la covarianza residual — medirla directamente
exigiría replicar el SAE de CONEVAL, que sigue declarada como extensión. Dos peticiones
previsibles de un referee de métodos sí se ejecutan en esta versión: el estudio de simulación
que controla método compartido, efectos estatales, anclas mal especificadas y número de
factores (apéndice F — la separación factor/método/estado es recuperable al rango correcto,
no se fabrica bajo colinealidad pura, y hereda sesgo al alza solo de la sub-extracción de
factores), y la incorporación del error estándar oficial del SAE como capa de unicidad
heteroscedástica (§5.3).

Para la práctica estadística oficial la implicación es constructiva: las dependencias
mecánicas del DAG (secuencia SAE→calibración, rol dual de la población en localidades
pequeñas, circularidad FAIS temporalizada) son propiedades documentables del sistema de
medición que cualquier usuario serio de estos datos — académico o gubernamental — necesita
conocer para no confundir maquinaria con territorio.

## Apéndice técnico

**A. La escalera con scores muestreados.** Cuatro especificaciones (S1 base → S2 +covariables
de composición → S3 +efectos estatales → S4 +BYM2 espacial), cada una estimada con K=2 y K=3.
Ninguna converge en el sentido estructural (R̂ 1.9–2.7; Tabla 1), aunque las cantidades de
ajuste (α, η, ELPD, Moran) coinciden entre cadenas — la ilustración exacta de por qué el
veredicto no-rotacional no basta. La especificación espacial (BYM2 sobre z, sin estado)
exhibe la patología de frontera ρ → 1 y su ventaja aparente de ELPD no replica al reestimar
con la verosimilitud corregida; queda correctamente descartada por el criterio de
comparabilidad.

**B. El test de alineación Procrustes.** Para separar rotación inocua de no-identificación
real: por cadena, se alinean los draws de Λ (y de z) al primer draw por rotación Procrustes y
se recomputa R̂ sobre lo alineado. Resultado en S3: R̂ alineado = 2.16 — las cadenas difieren
en el *reparto de varianza* entre factores, método y unicidades, no solo en la orientación.
Este test es el que justifica marginalizar en lugar de post-procesar.

**C. La comparación M−γ vs M+γ.** Con verosimilitud idéntica (MvN sobre la misma Y):
(i) eigenestructura de E[ΛΛᵀ], recomputada de los posteriores archivados — M−γ = (1.804,
0.628, 0.371, 0.087, ≈0) vs M+γ = (1.230, 0.501, 0.344, ≈0)<!-- src: eigen_marginal_2v3.csv -->:
sin efectos estatales aparece una cuarta dirección latente débil; (ii) ángulos principales
entre los subespacios top-3: (52.9°, 6.3°, 3.8°) — dos ejes esencialmente compartidos, uno se
reorganiza 53°; (iii) la caída de unicidad por indicador Δσ_j² es proporcional al share de
varianza estatal del indicador en M+γ<!-- src: comparacion_marginal_2v3.csv --> — el test
elegante de que γ_s absorbe heterogeneidad que antes se repartía ambiguamente. ELPD:
+5,410 ± 135 a favor de M+γ (descriptivo; el posterior de M−γ es de mezcla).

**D. Detalle de estimación.** PyMC con NUTS de numpyro; 4 cadenas × (1,000 + 1,000),
target_accept 0.9, semilla fija; log-verosimilitud puntual almacenada para LOO; scores E[z|Y]
y E[m|Y] por draw (submuestreo 1:4) con varianza total = var(medias) + media(varianzas
condicionales). Los posteriores completos están archivados en el repositorio.

**E. Sensibilidad a las direcciones v_b y al prior de σ_γ.** Barrido de ±20% en los pesos de
las direcciones de método, una perturbación por corrida (corridas reducidas de 500+500 × 2
cadenas)<!-- src: sensibilidad_vb.csv -->. La carga del bloque de líneas es estable ante
perturbaciones de los *otros* bloques (0.59 con educación o vivienda a ±20%, contra 0.57
base) y ante la asimetría que sube el peso de la línea extrema ({0.8, 1}: 0.53). La
perturbación que sí importa es desviar la propia dirección de las líneas hacia la línea
general ({1, 0.8}): la posterior se vuelve inestable (media 0.32, banda 90% [0.02, 0.57]) —
la dirección simétrica {+1, +1} no es una elección arbitraria sino la única de la familia
explorada con posterior estable, y las conclusiones deben leerse como condicionales a ella
(Figura E1). Sobre σ_γ: sustituir el σ = 0.5 fijo por un hiperprior HalfNormal produce
σ_γ posterior 0.38 ± 0.01, una matriz γ prácticamente idéntica (correlación 0.998 con la
canónica) y una partición espectral que se mueve un punto (share del PC1: 40.7% contra
41.8%)<!-- src: hyper_sigma_gamma.csv --> — la descomposición de §7 no es artefacto del
prior. El costo es diagnóstico: con la escala libre, el bloque de covarianza pierde la
convergencia estructural (R̂ ΛΛᵀ = 1.53), de modo que fijar σ_γ es parte de la estrategia de
identificación de §4.4, documentada aquí en vez de silenciosa.

![Figura E1. Sensibilidad de las cargas de método a los pesos de las direcciones v_b: la carga del bloque de líneas (rojo) es estable salvo cuando se desvía su propia dirección hacia la línea general ({1, 0.8}), donde la posterior se desestabiliza.](../figures/02_escalera_gllvm/fig_sensibilidad_vb.png)

**F. Estudio de simulación de identificación.** Para acotar el riesgo de que el reparto
factor/método/estado sea un artefacto de la parametrización, generamos datos sintéticos con la
estructura del modelo (N = 1,000 municipios, J = 17, dos réplicas por escenario, semillas
fijas) y verdades tomadas del posterior real — ΛΛᵀ canónica, unicidades y estructura de media
estimadas — variando la carga de método verdadera sobre la dirección de las líneas
(λ ∈ {0, 0.3, 0.6}), la escala de los efectos estatales (σ_γ ∈ {0, 0.5}), la fuerza de las
anclas y el número de factores. Cada escenario se ajustó en las dos parametrizaciones —
anclada y libre (la canónica de este trabajo, con ΛΛᵀ como único objeto identificado)<!-- src:
sim_identificacion_resumen.csv -->. La lectura descansa en la variante libre, que converge
limpiamente en los ocho escenarios (R̂ máximo 1.03, cero divergencias); la anclada despierta
ocasionalmente el modo de colapso del ancla (R̂ ≈ 1.85 en varios ajustes), sin que ello altere
las cargas de método ni las comunalidades — otra ilustración de por qué se identifica ΛΛᵀ y
no Λ.

Con el modelo bien especificado el reparto es recuperable: la carga de método se estima sin
sesgo apreciable (λ̂ = 0.020, 0.304 y 0.587 para verdades 0, 0.3 y 0.6, variante libre), ΛΛᵀ
se recupera con error de Frobenius relativo de 0.12–0.13 y correlación de comunalidades ≥ 0.99,
y los efectos estatales se recuperan con correlación ≥ 0.98 sin fabricarse cuando σ_γ = 0. Dos escenarios
adversariales fijan el alcance. El primero encarna la objeción previsible: datos generados
**sin** componente de método (λ = 0) pero con las dos líneas de ingreso casi colineales a
través de los factores (correlación residual 0.98, la observada en los datos reales). El
modelo no fabrica el componente: λ̂ = 0.064, con banda del 90% acotada por 0.13 — un orden de
magnitud por debajo del 0.574 estimado en los datos reales. La carga de las líneas no es, por
tanto, atribuible a la mera colinealidad del par: exige covarianza compartida más allá del
subespacio factorial. El segundo escenario es el que sí sesga, y por eso lo declaramos como el
supuesto operativo del resultado: la **sub-extracción** de factores (generar con tres, ajustar
con dos) filtra parte del factor omitido al bloque de método (λ̂ = 0.36 para λ = 0.3, con
intervalo que excluye la verdad) y degrada ΛΛᵀ (Frobenius ≈ 0.32); la sobre-extracción, en
cambio, es benigna. La huella del ingreso heredaría sesgo al alza solo de una eventual
sub-extracción — lo que hace de la selección de K (§4.6), y no de la parametrización de método,
el supuesto del que depende la magnitud del resultado.

![Figura F1. Simulación de identificación (N=1,000, J=17, verdades del posterior real). (a) Recuperación de la carga de método por escenario, parametrización anclada y libre, con la verdad marcada; el escenario del referee (colinealidad 0.98, λ=0) no fabrica la carga. (b) Error de Frobenius relativo de ΛΛᵀ. (c) Correlación de comunalidades. La sub-extracción (K 3→2) es el único escenario que sesga materialmente.](../figures/02_escalera_gllvm/fig_sim_identificacion.png)

## Referencias

- Alkire, S. & Foster, J. (2011). Counting and multidimensional poverty measurement. *Journal
  of Public Economics*. doi:10.1016/j.jpubeco.2010.11.006
- Besag, J., York, J. & Mollié, A. (1991). Bayesian image restoration, with two applications
  in spatial statistics. *Annals of the Institute of Statistical Mathematics*.
  doi:10.1007/bf00116466
- Boltvinik, J. (2012). Treinta años de medición de la pobreza en México. *Estudios
  Sociológicos* 30(núm. extra): 79–110. doi:10.24201/es.2012v30nextra.186
- Campbell, D.T. & Fiske, D.W. (1959). Convergent and discriminant validation by the
  multitrait-multimethod matrix. *Psychological Bulletin*. doi:10.1037/h0046016
- CONAPO (2021). *Índice de marginación por entidad federativa y municipio 2020*. Consejo
  Nacional de Población, nota técnico-metodológica.
- CONEVAL (2021a). *Metodología para la medición de la pobreza en los municipios de México,
  2020*. Consejo Nacional de Evaluación de la Política de Desarrollo Social.
  https://www.coneval.org.mx/Medicion/Documents/Pobreza_municipal/2020/Metodologia_pobreza_municipal_2020.pdf
- CONEVAL (2021b). *Nota técnica sobre la carencia por acceso a los servicios de salud,
  2018-2020*. Consejo Nacional de Evaluación de la Política de Desarrollo Social.
  https://www.coneval.org.mx/Medicion/MP/Documents/MMP_2018_2020/Notas_pobreza_2020/Nota_tecnica_sobre_la_carencia_por_acceso_a_los_servicios_de_salud_2018_2020.pdf
- CONEVAL (2021c). *Índice de Rezago Social 2020: principales resultados*. Consejo Nacional
  de Evaluación de la Política de Desarrollo Social.
  https://www.coneval.org.mx/Medicion/Documents/IRS_2020/Nota_principales_resultados_IRS_2020.pdf
- Cortés, F. & Vargas, D. (2011). Marginación en México a través del tiempo: a propósito del
  índice de Conapo. *Estudios Sociológicos* 29(86): 361–387. doi:10.24201/es.2011v29n86.228
- Cortés, F. & Vargas, D. (2013). La dependencia temporal de la marginación municipal en
  México 1990-2010: una tercera mirada al índice de marginación. Documento de trabajo núm. 1,
  PUED-UNAM. https://www.pued.unam.mx/export/sites/default/archivos/documentos-trabajo/001.pdf
- Deville, J.-C. & Särndal, C.-E. (1992). Calibration estimators in survey sampling. *Journal
  of the American Statistical Association* 87(418): 376–382. doi:10.1080/01621459.1992.10475217
- Elbers, C., Lanjouw, J.O. & Lanjouw, P. (2003). Micro-level estimation of poverty and
  inequality. *Econometrica* 71(1): 355–364. doi:10.1111/1468-0262.00399
- Molina, I. & Rao, J.N.K. (2010). Small area estimation of poverty indicators. *Canadian
  Journal of Statistics* 38(3): 369–385. doi:10.1002/cjs.10051
- Niku, J., Hui, F.K.C., Taskinen, S. & Warton, D.I. (2019). gllvm: Fast analysis of
  multivariate abundance data with generalized linear latent variable models. *Methods in
  Ecology and Evolution*. doi:10.1111/2041-210x.13303
- Peláez Herreros, Ó. (2022). El Índice de Marginación del Conapo transformado en indicador
  cardinal. *EconoQuantum* 20(1). doi:10.18381/eq.v20i1.7294
- Peña-Trapero, B. (2021). La medición del Bienestar Social: una revisión crítica. *Studies of
  Applied Economics*. doi:10.25115/eea.v27i2.4919
- Rao, J.N.K. & Molina, I. (2015). *Small Area Estimation*, 2ª ed. Wiley.
  doi:10.1002/9781118735855
- Riebler, A., Sørbye, S.H., Simpson, D. & Rue, H. (2016). An intuitive Bayesian spatial model
  for disease mapping that accounts for scaling. *Statistical Methods in Medical Research*.
  doi:10.1177/0962280216660421
- Skrondal, A. & Rabe-Hesketh, S. (2004). *Generalized Latent Variable Modeling*. Chapman &
  Hall/CRC. doi:10.1201/9780203489437
- Székely, M. (2005). Pobreza y desigualdad en México entre 1950 y 2004. *El Trimestre
  Económico* 72(288): 913–931. doi:10.20430/ete.v72i288.566
- Tzavidis, N., Zhang, L.-C., Luna, A., Schmid, T. & Rojas-Perilla, N. (2018). From start to
  finish: A framework for the production of small area official statistics. *Journal of the
  Royal Statistical Society: Series A* 181(4): 927–979. doi:10.1111/rssa.12364
- Zarzosa Espina, P. (2021). Estimación de la pobreza en las comunidades autónomas españolas
  mediante la distancia DP2. *Studies of Applied Economics*. doi:10.25115/eea.v27i2.4923

## Disponibilidad de datos y código

Todos los datos derivados, el código de estimación, los posteriores archivados y los scripts
que generan cada figura y tabla de este artículo están disponibles en el repositorio del
proyecto (https://github.com/cuentadesanti/pobreza-marginacion; archivo
permanente: doi:10.5281/zenodo.21344720), junto con las tablas canónicas del DAG (nodos y
aristas versionados con validación automática de aciclicidad), el manifiesto de datos crudos
(URLs y advertencias de cada fuente oficial) y las verificaciones automáticas de consistencia
entre texto y resultados. La tabla suplementaria S1 mapea cada figura y tabla a su script
generador y a su archivo de resultados. Material suplementario adicional: el DAG completo a
nivel de variable (56 nodos, 97 aristas).
