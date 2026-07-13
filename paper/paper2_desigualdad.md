# Desigualdad territorial en dos escalas: geografías disjuntas de la privación municipal en México

**Borrador de trabajo (Paper 2, sustantivo) — 2026-07-12**
*Objetivo editorial: World Development / Journal of Development Economics (español; traducción al enviar).*
*Versión unificada de referencia: `manuscrito.md`. Paper metodológico compañero: `paper1_metodo.md`.*

## Resumen

¿A qué escala opera la desigualdad territorial mexicana, y se acumulan sus dimensiones en los
mismos lugares? Usando un espacio latente municipal de privación estimado sobre los 17
indicadores elementales de las dos mediciones oficiales (CONAPO y CONEVAL; método en el paper
compañero), documentamos tres resultados. Primero, la desigualdad opera en **dos escalas**:
cerca de la mitad de la dispersión de los indicadores observados ocurre entre estados (Theil
entre-estados 48–59%), mientras la desigualdad residual — descontadas composición y
pertenencia estatal — es predominantemente intraestatal (76–87%). Segundo, las **geografías
residuales rara vez se superponen** (Jaccard 0.05–0.21 entre pares de dimensiones; la triple
severidad apenas excede la esperada bajo independencia): la acumulación multidimensional vive
en el nivel bruto, y los 48 municipios triple-severos del espacio residual — la mitad en
Oaxaca, mediana 5,430 habitantes, fuera de la economía de remesas y casi todos invisibles a la
tipología espacial estándar — son los olvidados de los olvidados. Tercero, existe una **brecha
de apropiación territorial**: municipios cuya actividad económica es visible desde satélite
pero cuya mejora social local es menor a la esperada; su predictor dominante es la precariedad
laboral (β = +0.23, t = 8.6), con las remesas operando en sentido inverso. Una escalera
predictiva de circunstancias (geografía heredada → demografía → inserción productiva →
composición indígena) alcanza R² = 0.78 sobre la privación bruta con validación espacialmente
bloqueada. Cinco validaciones externas independientes — homicidios, luces nocturnas,
exposición criminal documentada (incluida la coerción política histórica), transición INSABI e
incidencia fiscal — convergen: violencia y privación son dimensiones territorialmente
distintas, y las transferencias aún pagan a la vara vieja.

**Palabras clave:** desigualdad territorial; pobreza multidimensional; acumulación de
desventajas; remesas; luces nocturnas; México.

---

## 1. Introducción: más allá de "cuál índice"

El debate aplicado sobre la medición municipal de la pobreza en México suele plantearse como
una elección entre índices. Este paper toma otra ruta: dado un espacio latente de privación
que integra los indicadores elementales de ambas agencias oficiales — con efectos de método y
de estado explícitos, estimado con la maquinaria descrita en el paper compañero
(`paper1_metodo.md`) — pregunta por la **estructura** de la desigualdad territorial: a qué
escala opera, si sus dimensiones se acumulan en los mismos municipios, y si la actividad
económica visible implica inclusión social local. Las tres respuestas (dos escalas; geografías
disjuntas; brecha de apropiación) tienen implicaciones directas de focalización que ningún
índice sintético único puede satisfacer simultáneamente.

## 2. Datos y espacio latente (resumen)

Diecisiete indicadores elementales (9 CONAPO, 8 CONEVAL) para 2,469 municipios en 2020,
modelados en escala logit estandarizada dentro de un GLLVM marginalizado con K=3 factores,
efectos de método como contrastes inter-agencia, covariables de composición y efectos
estado×indicador; convergencia verificada sobre el subespacio de covarianza (R̂ ΛΛᵀ = 1.003).
Los ejes canónicos: 1 material-infraestructural, 2 educativo, 3 vivienda+ingreso contra
servicios de red. Cada municipio tiene media y desviación posterior por eje; toda inferencia
de este paper hereda esa incertidumbre (los modelos municipales van ponderados por 1/sd² y
la clasificación individual solo es sustantiva en 42/55/14% de los municipios según el eje;
`certeza_canonica.csv`). El detalle metodológico — incluida la advertencia de que las
comparaciones de ingreso intra-estado arrastran la firma del método SAE — está en el paper 1.

## 3. La desigualdad opera en dos escalas

En los indicadores observados, cerca de la mitad de la dispersión ponderada por población
ocurre entre estados (Theil entre-estados: 48–59% según indicador; 50.8% para el factor
material bruto), con las líneas de ingreso como lo más federalizado (58.8%) — consistente a la
vez con la calibración estatal del método de imputación y con el federalismo fiscal. Una vez
descontadas composición y pertenencia estatal, la desigualdad de los ejes canónicos es
predominantemente intraestatal (76–87%). No hay contradicción: los efectos estatales absorben
la parte interestatal antes de estimar el residuo — son dos objetos distributivos distintos y
los reportamos como tales.

La partición bruta es robusta al esquema de ponderación; la residual depende del objeto
distributivo: el componente interestatal del eje 1 casi desaparece al equiponderar municipios
(23.6% → 0.5%), es decir, es un fenómeno de personas concentradas en municipios grandes, no de
territorios. (Fuentes: `desigualdad_theil.csv`, `desigualdad_robustez.csv`.)

## 4. Las geografías residuales rara vez se superponen

Definiendo severidad como el cuartil superior de cada eje canónico, la proporción de
municipios severos en las tres dimensiones (2.0%) apenas excede la esperada bajo independencia
(1.6%; razón 1.25–1.43 según umbral, IC bootstrap rozando 1; Jaccard entre pares 0.05–0.21).
La acumulación multidimensional — el municipio "peor en todo" — es un fenómeno del nivel
bruto, donde domina el factor general; el espacio residual selecciona territorios distintos
por dimensión.

**Los 48 triple-severos, con nombre** (fuente: `veta_48_triple.csv`): el 2% que sí acumula
severidad residual en las tres dimensiones tiene un perfil nítido — 24 de 48 en Oaxaca,
pequeños (mediana 5,430 habitantes contra ~12,700 nacional), 75% rurales, fuera de la economía
de remesas (mediana 17 vs 92 USD per cápita), con *menos* presencia criminal documentada que
el promedio (27% vs 48%) y casi todos invisibles para la tipología espacial de discordancia
(44/48 no significativos en LISA). No son los municipios famosos de la pobreza mexicana ni los
de la violencia: son los olvidados de los olvidados, y ninguna de las lentes usuales — índice
agregado, mapa de clusters, registro de eventos — los selecciona.

## 5. La brecha de apropiación territorial

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
(IC95 14–28) la de los subestimados. **La actividad territorial no implica inclusión laboral
local.** (Fuentes: `reporte_satelital.md`, `satelital_oof.parquet`.)

## 6. Circunstancias y oportunidades

¿Cuánta de la privación bruta es predecible desde circunstancias estructurales que ningún
municipio elige? Una escalera incremental (gradient boosting, validación cruzada bloqueada por
estado; fuente: `desigualdad_robustez.csv`) responde: geografía heredada (rugosidad,
elevación, aislamiento, dispersión) 0.27; + composición demográfica 0.47; + inserción
productiva 0.73; + composición indígena (ITER 2020: % hablantes de lengua indígena y %
monolingüe; `vistaD_indigena.parquet`) **0.78**. La contribución condicional indígena es
moderada (Δ +0.04) no porque la dimensión étnica no importe, sino porque su huella ya viaja
dentro de la geografía, la demografía y la inserción — la desventaja indígena en México está
estructuralmente *incorporada* en las circunstancias territoriales. La pertenencia estatal
añade hasta 0.89 (validación no bloqueada, no comparable estrictamente). Formulación
disciplinada: predecible-desde, no causado-por.

## 7. Validaciones externas convergentes

Cinco rutas independientes, ninguna usada en la construcción del espacio latente, convergen
en la misma estructura:

1. **Homicidios** (100 mil registros oficiales; orden estable en siete variantes de
   sensibilidad; `sensibilidad_homicidios.csv`): la privación explica ~23% de la violencia
   municipal, casi todo vía composición; el residual no aporta. La señal es un contraste
   intra-familia casi ortogonal al nivel — un índice sintético único no puede focalizar
   privación y anticipar violencia a la vez.
2. **Luces nocturnas** (`reporte_satelital.md`): ven la privación material bruta (R² 0.41–0.43
   con bloqueo espacial no administrativo; sin transferencia entre macroregiones) y nada del
   residual (24/24 R² < 0). La relación log-lineal canónica se resuelve en regímenes: piso
   oscuro (14% de municipios), umbrales regionales con IC disjuntos, sin saturación urbana a
   escala municipal.
3. **Exposición criminal documentada** (OCVED, 65 mil eventos diario-municipales con actores;
   `reporte_crimen_desigualdad.md`): predice violencia — más bajo competencia entre
   organizaciones que bajo monopolio (+0.130 vs +0.083) — y es esencialmente ortogonal a la
   privación residual (resultado negativo documentado con robustez). La **coerción política
   histórica** (ataques a autoridades y candidatos 2007–2012, réplica de Trejo-Ley con DOI
   verificado; `g5_coercion.csv`) refuerza el patrón como exposición rezagada: no mueve la
   privación residual de 2020, pero predice homicidio 2019–21 una década después (+0.26,
   t = 2.7) y ocurrió donde competencia criminal y fragmentación política interactúan.
   Advertencia permanente: los datos de eventos observan O = R × D — presencia documentada no
   es control territorial y la ausencia de registro no es ausencia real; todos los modelos
   llevan proxies de observabilidad.
4. **Transición INSABI**: la varianza estatal máxima del sistema corresponde a la carencia de
   salud, con correlación +0.61 con la dependencia estatal del Seguro Popular/INSABI (máxima
   de los 17 indicadores; placebos 0.18–0.49) — el componente estatal captura política real,
   no solo ruido de medición.
5. **Incidencia fiscal**: a igual privación y tamaño, los municipios "más marginados que
   pobres" reciben +15.8% de transferencias del Ramo 33 per cápita (t = 4.3) — el piso
   heredado de la fórmula antigua de masa carencial sigue pagando al perfil de marginación.
   **La vara con que se mide un municipio vale dinero.**

La convergencia importa más que cada pieza: dimensionalidad latente, validación por
homicidios, lentes satelitales, acumulación disjunta y exposición criminal llegan por caminos
independientes a la misma conclusión — violencia y privación residual son dimensiones
territorialmente distintas, y la desigualdad tiene más de una geografía.

## 8. Implicaciones de política

1. **Focalización**: focalizar a los más pobres en todo (nivel bruto) y focalizar los peores
   residuos por dimensión produce listas casi disjuntas. La elección entre ambas es una
   decisión distributiva que hoy se toma implícitamente al elegir índice; conviene tomarla
   explícitamente. Los 48 triple-severos residuales — invisibles a todas las lentes usuales —
   son el caso de prueba concreto.
2. **La vara que paga**: mientras la fórmula de transferencias conserve pisos heredados de la
   masa carencial, el perfil de marginación seguirá cobrando prima sobre la pobreza vigente a
   igual privación. El diseño de fórmulas debería auditarse contra la circularidad
   medición→dinero→fenómeno (agenda del paper 3, con montos anuales).
3. **Ninguna lente única**: índice, satélite y registro de eventos ven dimensiones distintas y
   fallan en lugares distintos (la luz no ve pobreza urbana; los eventos no ven donde no hay
   prensa; el índice no ve el residuo). La política que use una sola lente hereda sus puntos
   ciegos — documentados aquí con su geografía.

---

*Materiales: todos los resultados, figuras y tablas son reproducibles desde el repositorio
(scripts numerados por capítulo, manifiesto de figuras y manifiesto de datos crudos con URLs y
advertencias de cada fuente). Cifras citadas y sus outputs: Theil y robustez
(`desigualdad_theil.csv`, `desigualdad_robustez.csv`), acumulación (`fig_acumulacion.png`),
triple-severos (`veta_48_triple.csv`), brecha (`reporte_satelital.md`), crimen y coerción
(`reporte_crimen_desigualdad.md`, `g5_coercion.csv`), fiscal (`reporte_dgp_dag.md` §4b).
Referencias con DOI verificado en `reports/revision_literatura.md`.*
