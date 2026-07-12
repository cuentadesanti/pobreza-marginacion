# Revisión de literatura — fundamentos metodológicos y sustantivos

Esta revisión ancla cada pieza del proyecto en la literatura publicada. Complementa a
`reporte_literatura.md` (que mapea a los investigadores mexicanos y el nicho): aquí el eje son los
**métodos** —variables latentes, estructura espacial, estimación en áreas pequeñas, luces
nocturnas, descomposición de desigualdad, medición multidimensional— y **cómo el proyecto los usa
y extiende**. Todas las referencias tienen DOI verificado (Crossref).

---

## 1. Modelos de variables latentes y efectos de método

El corazón del proyecto —tratar marginación y pobreza como vistas ruidosas de un latente común—
es un **modelo lineal generalizado de variable latente (GLLVM)**. La formulación general (variable
latente + enlace por indicador + verosimilitud arbitraria) es de Skrondal & Rabe-Hesketh (2004),
*Generalized Latent Variable Modeling* (DOI: 10.1201/9780203489437), que unifica análisis factorial,
IRT y modelos de medición bajo un mismo marco. La implementación moderna eficiente y la práctica de
estimar el subespacio **ΛΛᵀ** en vez de las cargas individuales viene de la literatura ecológica de
abundancia multivariada: Niku et al. (2019), *gllvm: Fast analysis of multivariate abundance data
with GLLVMs*, Methods in Ecology and Evolution (DOI: 10.1111/2041-210x.13303) y Niku et al. (2017),
*Generalized Linear Latent Variable Models for Multivariate Count and Biomass Data*, JABES
(DOI: 10.1007/s13253-017-0304-7).

**Conexión con el proyecto.** La escalera de especificaciones y, sobre todo, la resolución del
label switching por **marginalización de los scores e identificación de ΛΛᵀ** (R̂ 1.003, eigenvalores
1.23/0.50/0.34) son exactamente la práctica que esta literatura recomienda: los ejes individuales no
están identificados sin restricciones, pero el subespacio de covarianza sí. La distinción
**constructo vs. método** que el modelo hace explícita (factores z vs. efectos de agencia/método m)
se remonta a la matriz multirrasgo-multimétodo de Campbell & Fiske (1959), *Convergent and
discriminant validation by the multitrait-multimethod matrix*, Psychological Bulletin
(DOI: 10.1037/h0046016) — el antecedente conceptual de "dos burocracias midiendo el mismo territorio
con instrumentos distintos".

## 2. Estructura espacial bayesiana

El componente espacial (efectos estatales y la variante BYM2 explorada en la escalera) se apoya en
el modelo canónico de Besag, York & Mollié (1991), *Bayesian image restoration, with two applications
in spatial statistics*, Ann. Inst. Statist. Math. (DOI: 10.1007/bf00116466) — el CAR/ICAR con
componente estructurado + no estructurado. La reparametrización **BYM2**, que hace interpretable y
escala-invariante la mezcla entre ambos, es de Riebler, Sørbye, Simpson & Rue (2016), *An intuitive
Bayesian spatial model for disease mapping that accounts for scaling*, Statistical Methods in Medical
Research (DOI: 10.1177/0962280216660421). Los priors PC que esa parametrización usa vienen de
Simpson, Rue et al. (2017), *Penalising Model Component Complexity*, Statistical Science
(DOI: 10.1214/16-sts576).

**Conexión con el proyecto.** El hallazgo de que los **efectos estatales estabilizan la
descomposición de covarianza** (peldaño 2 no converge, R̂≈1.53; peldaño 3 sí) y de que el BYM2
compartido sobre z tiene ρ clavado en 1.00 es precisamente el tipo de diagnóstico de identificación
que la reparametrización de Riebler et al. fue diseñada para exponer: cuando la señal espacial no es
separable de la estructura de efectos fijos, la mezcla degenera. La lectura calibrada del reporte
("persiste dependencia espacial no explicada", no "estructura causal") es fiel a la naturaleza
descriptiva de estos modelos.

## 3. Estimación en áreas pequeñas (SAE)

La pobreza municipal de CONEVAL 2020 **no es un conteo directo**: es una estimación por área pequeña
(SAE) que combina censo y encuesta. La referencia canónica es Rao & Molina (2015), *Small Area
Estimation*, 2ª ed. (DOI: 10.1002/9781118735855), y para medidas de pobreza específicamente la
predicción empírica mejor (EBP) desarrollada en Molina & Rao y sintetizada en Rao (2016), *Empirical
Bayes and Hierarchical Bayes Estimation of Poverty Measures* (DOI: 10.1002/9781118814963.ch17).

**Conexión con el proyecto.** Esta literatura justifica dos decisiones centrales: (i) la
**verosimilitud gaussiana en escala logit** para los 17 indicadores (los SAE son estimaciones
modeladas con error, no conteos), y (ii) el test **directo-vs-modelado** del reporte DGP, que trata
el suavizado del SAE como una fuente potencial de autocorrelación espacial artificial. El pendiente
declarado de incorporar el **SE del SAE de CONEVAL como capa de error de medición** es la extensión
natural que esta literatura pide: propagar la incertidumbre de la estimación de área pequeña al
modelo latente.

## 4. Luces nocturnas y desarrollo (corte B / capítulo satelital)

El uso de luces nocturnas como proxy de actividad económica arranca con Henderson, Storeygard & Weil
(2012), *Measuring Economic Growth from Outer Space*, American Economic Review
(DOI: 10.1257/aer.102.2.994) y Chen & Nordhaus (2011), *Using luminosity data as a proxy for economic
statistics*, PNAS (DOI: 10.1073/pnas.1017031108), que establecen tanto el valor como los límites de la
señal. El salto a predicción de pobreza con aprendizaje automático sobre imágenes es Jean, Burke, Xie
et al. (2016), *Combining satellite imagery and machine learning to predict poverty*, Science
(DOI: 10.1126/science.aaf7894) — el paper que el corte B interroga directamente.

**Conexión con el proyecto.** El corte B **invierte la premisa log-lineal** de esta literatura a
escala municipal mexicana: el OLS canónico en log(NTL) da R²cv≈0.005 mientras el modelo no lineal
llega a 0.40. El hallazgo defendible —la relación no es aproximadamente log-lineal a esta escala,
se recalibra por macroregión (umbrales norte vs. sur con IC disjuntos) y falla en el piso oscuro
rural— matiza a Jean et al. sin sobreafirmar (no hay benchmark de deep learning en el repo, y el
lenguaje es de proxy, coherente con Chen-Nordhaus: la luz indexa actividad, no la causa). Chen &
Nordhaus ya advertían que el valor informativo de la luminosidad es mayor donde faltan otras
estadísticas —justo lo contrario del piso oscuro rural donde el proyecto encuentra que la lente es
ciega.

## 5. Descomposición de la desigualdad (resultado principal 1)

El resultado "dos escalas" descompone la desigualdad en componentes entre y dentro de estados. La
familia de índices aditivamente descomponibles y el índice de Theil provienen de Theil (información
y economía; ver Theil 1979, *World income inequality and its components*, Economics Letters,
DOI: 10.1016/0165-1765(79)90213-1) y la caracterización axiomática de las descomposiciones por
subgrupos es de Shorrocks (1984), *Inequality Decomposition by Population Subgroups*, Econometrica
(DOI: 10.2307/1913511), complementada por su descomposición por factores (Shorrocks 1982,
DOI: 10.2307/1912537).

**Conexión con el proyecto.** La descomposición Theil entre/dentro de estados es la herramienta
exacta que la tesis "dos escalas" necesita, y la elección de Theil (no Gini) se justifica
precisamente por la descomponibilidad aditiva que Shorrocks axiomatizó. El matiz que el proyecto
añade —que los **indicadores brutos** se reparten ~mitad y mitad pero los **factores latentes
condicionales a estado** son predominantemente intraestatales— es una lectura que la literatura
clásica no aborda porque opera sobre variables observadas, no sobre scores latentes descontados de
efectos fijos.

## 6. Pobreza multidimensional y el índice DP2 (los dos instrumentos)

Los dos constructos que el proyecto integra tienen cada uno su literatura. La pobreza multidimensional
de CONEVAL se apoya en la metodología de conteo de Alkire & Foster (2011), *Counting and
multidimensional poverty measurement*, Journal of Public Economics
(DOI: 10.1016/j.jpubeco.2010.11.006). La marginación de CONAPO usa la **distancia DP2** de Pen͂a
Trapero (1977, *Problemas de la medición del bienestar y conceptos afines*), cuya revisión crítica
reciente es Pen͂a-Trapero (2021), *La medición del Bienestar Social: una revisión crítica*,
Studies of Applied Economics (DOI: 10.25115/eea.v27i2.4919), y cuya aplicación a áreas subnacionales
españolas —el molde del uso mexicano— es Zarzosa Espina (2021)
(DOI: 10.25115/eea.v27i2.4923).

**Conexión con el proyecto.** El proyecto no adopta ninguno de los dos índices agregados: los
**descompone** a sus indicadores elementales (9 CONAPO + 8 CONEVAL) y los trata como manifestaciones
de un latente común. Esto responde formalmente a la crítica de comparabilidad del DP2 (que el índice
confunde constructo con método y no es comparable intertemporalmente — Cortés y Vargas 2011, ver
`reporte_literatura.md`) separando explícitamente z (constructo), m (método/agencia) y s (residuo
espacial).

## 7. Dónde se para el proyecto (síntesis del hueco)

Ninguna de estas literaturas, por separado, hace lo que el repo hace: **modelar la maquinaria de
medición misma**. La econometría de la desigualdad mide incidencia; la SAE produce las estimaciones
pero no las contrasta entre agencias; la literatura de variables latentes vive en ecología y
psicometría, no en medición oficial de pobreza; la de luces nocturnas predice desarrollo pero no lo
cruza con un espacio latente de privación. El aporte es la **intersección**: un GLLVM espacial que
toma dos mediciones oficiales del mismo territorio como vistas parciales, separa constructo de método,
propaga incertidumbre municipal (ausente en ambas fuentes oficiales) y usa lentes externas
(satélite, homicidios, fiscal) como validación del espacio latente, no como regresión decorativa.

---

## Referencias (DOI verificado)

**Variables latentes / método**
- Skrondal, A. & Rabe-Hesketh, S. (2004). *Generalized Latent Variable Modeling*. Chapman & Hall/CRC. 10.1201/9780203489437
- Niku, J. et al. (2019). gllvm: Fast analysis of multivariate abundance data with GLLVMs. *Methods Ecol. Evol.* 10.1111/2041-210x.13303
- Niku, J. et al. (2017). GLLVMs for Multivariate Count and Biomass Data. *JABES*. 10.1007/s13253-017-0304-7
- Campbell, D.T. & Fiske, D.W. (1959). Convergent and discriminant validation by the MTMM matrix. *Psychol. Bull.* 10.1037/h0046016

**Estructura espacial**
- Besag, J., York, J. & Mollié, A. (1991). Bayesian image restoration… *Ann. Inst. Statist. Math.* 10.1007/bf00116466
- Riebler, A., Sørbye, S.H., Simpson, D. & Rue, H. (2016). An intuitive Bayesian spatial model… (BYM2). *Stat. Methods Med. Res.* 10.1177/0962280216660421
- Simpson, D., Rue, H. et al. (2017). Penalising Model Component Complexity (PC priors). *Statist. Sci.* 10.1214/16-sts576

**Estimación en áreas pequeñas**
- Rao, J.N.K. & Molina, I. (2015). *Small Area Estimation*, 2nd ed. Wiley. 10.1002/9781118735855
- Rao, J.N.K. (2016). Empirical Bayes and Hierarchical Bayes Estimation of Poverty Measures. 10.1002/9781118814963.ch17

**Luces nocturnas / desarrollo**
- Henderson, J.V., Storeygard, A. & Weil, D.N. (2012). Measuring Economic Growth from Outer Space. *Am. Econ. Rev.* 10.1257/aer.102.2.994
- Chen, X. & Nordhaus, W.D. (2011). Using luminosity data as a proxy for economic statistics. *PNAS*. 10.1073/pnas.1017031108
- Jean, N., Burke, M., Xie, M. et al. (2016). Combining satellite imagery and machine learning to predict poverty. *Science*. 10.1126/science.aaf7894

**Descomposición de desigualdad**
- Theil, H. (1979). World income inequality and its components. *Econ. Lett.* 10.1016/0165-1765(79)90213-1
- Shorrocks, A.F. (1984). Inequality Decomposition by Population Subgroups. *Econometrica*. 10.2307/1913511
- Shorrocks, A.F. (1982). Inequality Decomposition by Factor Components. *Econometrica*. 10.2307/1912537

**Pobreza multidimensional / DP2**
- Alkire, S. & Foster, J. (2011). Counting and multidimensional poverty measurement. *J. Public Econ.* 10.1016/j.jpubeco.2010.11.006
- Peña-Trapero, B. (2021). La medición del Bienestar Social: una revisión crítica. *Stud. Appl. Econ.* 10.25115/eea.v27i2.4919
- Zarzosa Espina, P. (2021). Estimación de la pobreza en las CCAA españolas mediante DP2. *Stud. Appl. Econ.* 10.25115/eea.v27i2.4923

*Nota: la literatura sustantiva mexicana (Cortés, Boltvinik, Lustig, Székely, Prieto-Curiel, CEEY,
CONEVAL, CONAPO) está en `reporte_literatura.md`; esta revisión cubre los fundamentos metodológicos
internacionales. La DP2 se origina en Peña Trapero (1977), obra sin DOI; se cita la revisión con DOI verificado (2021).*
