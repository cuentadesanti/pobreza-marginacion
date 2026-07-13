# La maquinaria de medición: por qué dos burocracias cuentan historias distintas del mismo territorio

**Borrador de trabajo (Paper 1, metodológico) — 2026-07-12**
*Objetivo editorial: Social Indicators Research / Journal of Economic Inequality (español; traducción al enviar).
Encuadre: contribución aplicada-metodológica — no una teoría general de GLLVM; eso exigiría un estudio de simulación (extensión declarada).*
*Versión unificada de referencia: `manuscrito.md`. Paper sustantivo compañero: `paper2_desigualdad.md`.*

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
secuencia diagnóstica de tres pasos — verosimilitud integrada, método parametrizado como
contraste inter-agencia de dirección fija, y monitoreo del subespacio ΛΛᵀ, la cantidad
identificada (R̂ = 1.003; tres eigenvalores sustantivos compatibles con rango efectivo 3).
Segunda, el resultado fundacional: el componente de método dominante en la discordancia entre
agencias es consistente con la firma del modelo de imputación de ingreso (SAE-EBPH; carga
0.58) y parte limpiamente los regímenes espaciales de discordancia, mientras que en educación
las agencias esencialmente acuerdan (0.012) y el desacuerdo de vivienda es un fenómeno estatal
(0.135 → 0.029 al condicionar en efectos de estado). Tercera, epistemológica: la incertidumbre
posterior municipal es parte del resultado — la clasificación individual es sustantiva en
42/55/14% de los municipios según el eje, y esa incertidumbre tiene geografía propia: la
representación es más precisa en municipios rurales y pequeños que en los urbanos y grandes.

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
sino de la maquinaria, y es consistente principalmente con la firma del método de imputación
de ingreso. Llegar a esa respuesta con garantías exige dos piezas que constituyen la
contribución metodológica: un DAG de medición que hace explícitas las dependencias mecánicas
que un análisis conjunto no debe confundir con estructura sustantiva (§2), y una estrategia de
estimación e identificación que resuelve el principal problema de identificación y
convergencia de esta aplicación en lugar de ocultarlo (§3).
El paper compañero (`paper2_desigualdad.md`) explota el espacio latente resultante para la
lectura sustantiva de la desigualdad territorial.

## 2. El proceso generador como DAG de medición

Trabajamos con los 17 indicadores elementales que alimentan ambas mediciones (9 de CONAPO,
8 de CONEVAL: 6 carencias — en la metodología de conteo de Alkire & Foster 2011 — y 2 líneas
de ingreso) para 2,469 municipios en 2020, deliberadamente sin usar los índices finales, que
son funciones deterministas de estos componentes. Los indicadores se modelan en escala logit
estandarizada; los cuatro indicadores modelados por CONEVAL vía áreas pequeñas (Rao & Molina
2015) no son conteos y una verosimilitud binomial les atribuiría precisión falsa.

El DAG de medición (Figura 1; objeto canónico en dos tablas versionadas — 56 nodos, 97
aristas en siete semánticas tipificadas — con validación automática de aciclicidad, de una
matriz de tipos permitidos y de sincronía prosa-tablas) explicita, entre otras relaciones:

- que la pobreza multidimensional **no es derivable de las prevalencias marginales
  municipales** — pasa por la distribución conjunta persona-hogar y una regla de
  identificación;
- que la estimación SAE y la calibración estatal son **operadores secuenciales**
  (SAE → preliminares → calibración → publicados), cada uno con su huella;
- que `loc_peq` (población en localidades pequeñas) es un solo nodo con **rol dual** —
  condición estructural de dispersión *y* componente del índice de marginación, lo que induce
  una endogeneidad estructural interna del propio índice;
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
fronterizas; y educación aparece en ambas agencias con cohortes distintas.

## 3. Método: el GLLVM marginalizado y la identificación del subespacio

El marco es un GLLVM (Skrondal & Rabe-Hesketh 2004; en su implementación aplicada moderna,
Niku et al. 2019) con especificación condicional η_ij = α_j + λ_j′z_i + β_r,j·rural_i +
β_D,j′x_i + γ_j,s(i) + m_ij + ε_ij, con z_i ∈ ℝ³ los factores latentes, γ_j,s efectos
estado×indicador (ZeroSum; la extensión espacial BYM2 — Besag, York & Mollié 1991, en la
reparametrización de Riebler et al. 2016 — se evaluó como peldaño adicional y su patología de
frontera se documenta en el repositorio) y m_ij efectos de método por familia. La estimación con scores muestreados exhibe la patología
conocida: cadenas en rotaciones distintas pese a anclas, y — demostrado con un test de
alineación Procrustes por draw — no-convergencia genuina más allá de la rotación (R̂ alineado
2.16), con las cadenas difiriendo en el reparto de varianza entre factores, bloques de método
y unicidades. Distinguimos por eso tres veredictos: estructural (sobre ΛΛᵀ, invariante a
rotación), no-rotacional (sobre parámetros de media y varianza) e interpretativo (sobre ejes
nombrados).

La solución tiene tres pasos, cada uno con su diagnóstico:

1. **Marginalizar.** Y_i ~ N(μ_i, ΛΛᵀ + Σ_b λ_b²v_bv_bᵀ + Ψ) elimina ~7,400 parámetros
   latentes; la estructura de medias converge de inmediato (R̂ ≤ 1.011) pero la descomposición
   de covarianza no (R̂ ΛΛᵀ = 2.05): la multimodalidad no era de los scores.
2. **El método como contraste inter-agencia.** Los bloques de método con dirección uniforme
   sobre su soporte son casi colineales con las cargas del factor; fijar la dirección como
   contraste inter-agencia (CONAPO+/CONEVAL−, ortogonal al nivel; solo la magnitud es libre)
   reduce la multimodalidad (R̂ 1.53) y es conceptualmente superior: el método *es* el
   desacuerdo entre instrumentos, no otra fuente de nivel — la lógica de la matriz
   multirrasgo-multimétodo (Campbell & Fiske 1959) llevada a parametrización.
3. **Liberar las anclas.** El modo restante era un conflicto anclas-verosimilitud (una cadena
   alcanzaba logp +106 pagando un prior extremo por colapsar el ancla monetaria). Sin anclas,
   monitoreando solo ΛΛᵀ: **R̂ = 1.003** con ESS 3,490, cero divergencias, BFMI 0.91, y tres
   eigenvalores sustantivos (1.23, 0.50, 0.34) con el resto cercanos a cero — compatibles con
   rango efectivo 3, condicionado a la especificación y escala.

Los ejes canónicos se definen por eigen-descomposición de E[ΛΛᵀ] con convención de signo
documentada: eje 1 material-infraestructural, eje 2 educativo, y eje 3 — la dimensión que las
anclas suprimían — un contraste de *vivienda e ingreso contra servicios de red*. Los scores
municipales E[z|Y] se obtienen por regresión GLS por draw, con media y desviación posterior.

Los efectos estatales no son decorativos, y el orden del argumento importa. (i) Sin γ_s el
modelo no identifica una posterior estable: el peldaño marginalizado sin efectos estatales
sigue estructuralmente multimodal — la multimodalidad no era solo label switching. (ii) En esa
especificación aparece una cuarta dirección latente débil y un eje rota 53° respecto de la
solución canónica. (iii) Al incluir γ_s, la reducción de unicidad por indicador es
proporcional a su share de varianza estatal — evidencia directa de que, sin γ_s, la
heterogeneidad estatal se reparte ambiguamente entre unicidad y covarianza latente. (iv) La
comparación de verosimilitud idéntica favorece al modelo con efectos estatales (ELPD
+5,410 ± 135), pero este contraste es descriptivo y se interpreta con cautela: uno de los dos
modelos comparados no está bien identificado.

## 4. Resultado fundacional: la discordancia es de método

El modelo estima el desacuerdo inter-agencia por familia con dirección fija y magnitud libre,
y produce scores municipales E[m|Y] con incertidumbre (fuente: `desacuerdo_agencias.csv`,
`fig_desacuerdo_agencias.png`). Tres hechos:

1. **En educación las agencias esencialmente acuerdan** (carga 0.012) — el desacuerdo aparente
   entre indicadores educativos vive en cargas y cohortes, no en método.
2. **El desacuerdo de vivienda-servicios es un fenómeno estatal** (carga 0.135 sin efectos
   estatales, 0.029 con ellos): huella de la calibración, no del territorio municipal.
3. **El componente de método dominante es la firma del modelo de ingreso SAE-EBPH** (0.58) —
   las dos líneas de pobreza moviéndose juntas más allá del factor monetario. Esa firma
   municipal parte los regímenes espaciales de discordancia: media de −0.325 en los municipios
   "más marginados que pobres" (LISA alto-alto de la discordancia) y +0.339 en los "más pobres
   que marginados", con 22.6% de municipios con firma sustantiva (|m|/sd ≥ 2) y sin
   correlación con composición.

La discordancia "más pobre que marginado" que originó el proyecto es, en buena parte,
consistente principalmente con la firma compartida del método de imputación de ingreso: el
componente de método asociado a las líneas SAE domina la discordancia estimada. La firma es
inferida — se identifica desde la covarianza residual y la estructura del DAG, no comparando
estimaciones con y sin SAE (§7) —, pero el resultado es fundacional y no una validación:
reordena qué preguntas territoriales son formulables con estas mediciones — las comparaciones
de ingreso entre municipios dentro de un estado arrastran la firma del modelo SAE, mientras
que las comparaciones educativas son limpias de método.

La lectura complementaria por indicador acota — como falsación posible, no como prueba — la
interpretación de los efectos estatales: los indicadores SAE-calibrados no dominan el
componente estatal (Δshare vs. directos de CONEVAL: −0.034, IC95 [−0.060, −0.007]) aunque
exhiben un piso de calibración respecto de los censales (+0.027, [+0.007, +0.049]).

## 5. Identificación del subespacio e incertidumbre municipal

La identificación es del subespacio, no de los ejes: reportamos por eso la certeza de
clasificación municipal como resultado (fuente: `certeza_canonica.csv`). La clasificación
individual es sustantiva (|z|/sd ≥ 2) en 42% de los municipios para el eje material, 55% para
el educativo y solo 14% para el tercero — el eje 3 existe como dirección de covarianza
nacional, pero su clasificación municipal individual es débil en la mayor parte del
territorio, y todo uso aplicado debe heredar esa distinción.

La incertidumbre tiene además geografía propia (fuente: `veta_ignorancia.csv`): la desviación
posterior municipal crece con el tamaño y la urbanización (correlación +0.32 con log población
en el eje 1; −0.26 con ruralidad). Condicionado en las covariables, la representación
municipal es más precisa en municipios rurales y pequeños que en los urbanos y grandes — un
patrón opuesto al de los diseños muestrales, que saben más donde hay más gente. Una
explicación plausible, no identificada, es la heterogeneidad urbana intra-municipal: la
desviación respecto de la composición es más idiosincrática precisamente donde el municipio
agrega realidades internas más diversas.

## 6. Qué hace γ_estado: federalismo sectorial y legibilidad institucional

El componente estatal estimado no es un gradiente único. La descomposición espectral de la
matriz γ (17 indicadores × 32 estados; fuente: `veta_gamma_pca.csv`) muestra que solo 42% de
su varianza es un factor común — interpretable como capacidad estatal: correlaciona +0.42 con
el PIB estatal per cápita — y el 58% restante es específico por dominio de política:
**federalismo sectorial**, no un ranking de estados.

Un episodio institucional vuelve legible esta lectura: la varianza estatal máxima corresponde
a la carencia de salud (0.27), cuya correlación con la dependencia estatal del sistema Seguro
Popular/INSABI (+0.61, la más alta de los 17 indicadores; placebos 0.18–0.49) la identifica
como huella de la transición sanitaria de 2020 (fuente: `validacion_insabi.csv`). El
componente estatal es compatible con heterogeneidad sustantiva, aunque sigue mezclando
política, composición y medición; esa mezcla es un límite declarado, no un defecto ocultable.

## 7. Discusión: qué significa modelar la maquinaria

Modelar la maquinaria en lugar de proponer otro índice cambia el tipo de conclusión
disponible. No decimos qué municipio "es" más pobre; decimos qué parte del desacuerdo entre
las mediciones oficiales es método (la firma SAE), qué parte es calibración (vivienda), qué
parte es federal (γ sectorial) y qué parte queda como estructura territorial — y con qué
certeza municipal (dicho en corto: el modelo sabe más del campo que de la ciudad, y lo
declara). Los límites: los resultados son asociativos; la separación entre las dos
rutas de los cofactores requiere restricciones de exclusión sustantivas que no imponemos; la
identificación del rango efectivo 3 está condicionada a especificación y escala; y la firma
SAE se estima desde la covarianza residual — medirla directamente exige replicar el SAE de
CONEVAL, extensión declarada.

Para la práctica estadística oficial la implicación es constructiva: las dependencias
mecánicas del DAG (secuencia SAE→calibración, rol dual de `loc_peq`, circularidad FAIS
temporalizada) son propiedades documentables del sistema de medición que cualquier usuario
serio de estos datos — académico o gubernamental — necesita conocer para no confundir
maquinaria con territorio.

## Referencias

- Alkire, S. & Foster, J. (2011). Counting and multidimensional poverty measurement. *Journal
  of Public Economics*. doi:10.1016/j.jpubeco.2010.11.006
- Besag, J., York, J. & Mollié, A. (1991). Bayesian image restoration, with two applications
  in spatial statistics. *Annals of the Institute of Statistical Mathematics*.
  doi:10.1007/bf00116466
- Campbell, D.T. & Fiske, D.W. (1959). Convergent and discriminant validation by the
  multitrait-multimethod matrix. *Psychological Bulletin*. doi:10.1037/h0046016
- Niku, J., Hui, F.K.C., Taskinen, S. & Warton, D.I. (2019). gllvm: Fast analysis of
  multivariate abundance data with generalized linear latent variable models. *Methods in
  Ecology and Evolution*. doi:10.1111/2041-210x.13303
- Peña-Trapero, B. (2021). La medición del Bienestar Social: una revisión crítica. *Studies of
  Applied Economics*. doi:10.25115/eea.v27i2.4919
- Rao, J.N.K. & Molina, I. (2015). *Small Area Estimation*, 2ª ed. Wiley.
  doi:10.1002/9781118735855
- Riebler, A., Sørbye, S.H., Simpson, D. & Rue, H. (2016). An intuitive Bayesian spatial model
  for disease mapping that accounts for scaling. *Statistical Methods in Medical Research*.
  doi:10.1177/0962280216660421
- Skrondal, A. & Rabe-Hesketh, S. (2004). *Generalized Latent Variable Modeling*. Chapman &
  Hall/CRC. doi:10.1201/9780203489437
- Zarzosa Espina, P. (2021). Estimación de la pobreza en las comunidades autónomas españolas
  mediante la distancia DP2. *Studies of Applied Economics*. doi:10.25115/eea.v27i2.4923

(La literatura sustantiva mexicana — Cortés, Boltvinik, Lustig, Székely, CONEVAL, CONAPO — se
integrará desde `reporte_literatura.md` en la versión de envío.)

---

*Materiales: todos los resultados, figuras y tablas son reproducibles desde el repositorio
(scripts numerados por capítulo, manifiesto de figuras, DAG canónico en tablas versionadas con
validación automática de aciclicidad y de sincronía prosa-tablas, y manifiesto de datos crudos
con URLs y advertencias). Cifras citadas y sus outputs: R̂ y eigenvalores
(`reporte_gllvm_escalera.md`), firma SAE (`desacuerdo_agencias.csv`), certeza
(`certeza_canonica.csv`), ignorancia (`veta_ignorancia.csv`), γ-PCA (`veta_gamma_pca.csv`),
INSABI (`validacion_insabi.csv`), medición-vs-federalismo (`tabla_medicion_federalismo.csv`).*
