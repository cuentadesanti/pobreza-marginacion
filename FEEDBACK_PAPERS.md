# Feedback sobre paper1_metodo.md y paper2_desigualdad.md

Dos capas: **(A) correcciones factuales verificadas contra outputs en disco** — no negociables antes
de enviar; **(B) revisión editorial** (acotar claims, estructura, targets, lo que falta físicamente).
Los 14 archivos citados por ambos papers existen en disco y los números centrales verificados salen
clavados de sus outputs (firma SAE 0.58, LISA −0.325/+0.339, certeza 41.9/54.6/13.6, γ-PC1 42%,
triple-severos 24/48 Oaxaca, remesas 17 vs 92, escalera indígena 0.27→0.47→0.73→0.78). La prosa es
de calidad; el trabajo pendiente es de aparato, no de contenido.

---

## A. Correcciones factuales (verificadas en disco — corregir antes de considerar enviable)

**A1. (Grande) Falta el aparato de citas inline — hueco #1 para las revistas objetivo.** Ambos papers
describen métodos con nombre propio pero tienen **cero citas autor-año en el cuerpo**; remiten a
`revision_literatura.md` al final, y eso no basta. Los DOIs ya están verificados ahí; solo hay que
tejerlos. Mapeo:
- *paper1* §1/§2 índice DP2 → (Peña-Trapero 2021; Zarzosa Espina 2021); §2 carencias → (Alkire &
  Foster 2011); §2/§3 GLLVM → (Skrondal & Rabe-Hesketh 2004; Niku et al. 2019); §2 SAE → (Rao &
  Molina 2015); §3 efectos estado/espacial → (Besag, York & Mollié 1991; Riebler et al. 2016); §4
  método como contraste inter-agencia → (Campbell & Fiske 1959, el antecedente MTMM).
- *paper2* §3 Theil → (Theil 1979; Shorrocks 1984); §5/§7 luces → (Henderson, Storeygard & Weil 2012;
  Chen & Nordhaus 2011); §5 gancho no-lineal → (Jean et al. 2016, sin afirmar que le ganamos); §7.3
  coerción → Trejo-Ley (DOI 10.7910/DVN/VIXNNE).

**A2. (Numérico) Mediana poblacional nacional mal en paper2 §4.** Dice "mediana 5,430 hab contra
**~12,700 nacional**". La mediana real es **13,552** (`vistaD_v1.parquet`, `municipal_components_2020.parquet`,
n=2469). Corregir a "~13,550 nacional". El 5,430 de los triple-severos es correcto.

**A3. (Claim sobredicho) paper2 §7.3 aplana el hallazgo G5a que el reporte maneja con más honestidad.**
El paper dice que la coerción histórica "no mueve la privación residual de 2020". Pero `g5_coercion.csv`
muestra en G5a: eje3 `coercion_any` β=+0.372 (t=4.0) y `log_coercion_r100k` β=−0.157 (t=−3.3) —
**signos opuestos entre dummy y tasa**; y eje1 tasa β=+0.141 (t=2.3). El `reporte_crimen_desigualdad.md`
(líneas 45–47) ya lo lee bien: nulo con el dummy en eje1/eje2, y en eje3 los signos contradictorios
son **colinealidad dummy/tasa, no una ruta**, por eso no se promueve. **Portar esa redacción del
reporte al paper**: no "no mueve la privación", sino "no se identifica una ruta robusta hacia la
privación residual (el dummy es nulo en eje1/eje2 y en eje3 dummy y tasa se contradicen), mientras sí
predice homicidio". Es un matiz que da credibilidad, no que resta.

**A4. (Menor, no bloqueante)** El "75% rurales" de los 48 es 79% con umbral loc_peq≥50% (73% con =100%).
Definir el umbral en el texto o redondear a "~80%".

---

## B. Revisión editorial (acotar claims y madurez de manuscrito)

**B1. Acotar la afirmación de multimodalidad.** "resuelve la multimodalidad endémica de estos modelos"
es demasiado universal — el peldaño 2 marginalizado siguió multimodal, y no se demostró una receta
general. Cambiar en resumen e intro por: "resuelve el principal problema de identificación y
convergencia **de esta aplicación**".

**B2. La firma SAE es inferida, no observada.** "la discordancia tiene nombre y apellido: el método de
imputación de ingreso" es demasiado fuerte: la firma se identifica desde covarianza residual +
estructura del DAG, no comparando estimaciones con/sin SAE (medirla directo exige replicar el SAE,
como el propio paper reconoce). Usar: "es **consistente principalmente** con la firma compartida del
método SAE-EBPH" / "el componente de método asociado a las líneas SAE domina la discordancia estimada".

**B3. El ΔELPD +5,410 no debe encabezar la prueba de los efectos estatales.** El peldaño 2 no converge,
así que el contraste no es entre dos modelos bien identificados. Reordenar §3: (1) el peldaño 2 no
identifica una posterior estable → (2) cuarta dirección débil + rotación 53° → (3) la heterogeneidad
estatal se filtra a uniqueness/covarianza → (4) el ΔELPD es **descriptivo**, interpretarse con cautela.

**B4. "El modelo sabe más del campo que de la ciudad" es antropomórfico para un hallazgo principal.**
En el cuerpo: "la representación municipal es más precisa en municipios rurales/pequeños que
urbanos/grandes, condicionado en las covariables". La explicación de heterogeneidad urbana
intra-municipal es plausible, no identificada. El hook puede quedarse en discusión/figura.

**B5. Sacar los 48 "olvidados de los olvidados" del resumen.** Hay fragilidad estadística (triple
severidad apenas sobre independencia; IC bootstrap rozando 1; depende del umbral; eje3 de baja
certeza). En el cuerpo: "municipios severos en las tres dimensiones residuales"; el hook memorable va a
discusión/comunicación pública.

**B6. Las cinco validaciones no validan la misma cantidad.** "convergen en la misma estructura" es
atractivo pero impreciso: homicidios prueba ortogonalidad con violencia; satélite, visibilidad
material; INSABI interpreta un efecto estatal; crimen valida violencia con negativo en privación;
fiscalidad muestra consecuencias distributivas. Mejor: "cinco análisis externos **delimitan distintas
implicaciones y límites** del espacio estimado".

---

## C. Lo que falta físicamente (siguiente sprint, no este)

Hoy es un extended abstract excelente, no todavía un paper. Faltan, por paper: revisión de literatura
**integrada** (no remitida a archivo), definición formal de variables, priors, estrategia de
estimación, definición de Theil y ponderación, construcción exacta de la brecha de apropiación,
protocolo de validación cruzada, tablas centrales, figuras numeradas e insertadas, robustez con
jerarquía, referencias y apéndice técnico.

---

## D. Targets (realista) y orden

**Paper 1** — Social Indicators Research / Journal of Economic Inequality. Para venderlo como
contribución metodológica *general* (Sociological Methods & Research) haría falta una **simulación**
que controle método compartido, efectos estatales, anclas mal especificadas, número de factores y
recuperación de ΛΛᵀ. Sin ella, es una excelente contribución aplicada-metodológica, no una teoría
general de GLLVM — enmarcar como tal.

**Paper 2** — World Development plausible si se profundizan mecanismos, focalización, población
indígena, federalismo y fiscal. **Journal of Development Economics poco realista** en esta versión
(suele exigir identificación causal); el paper es asociativo/transversal/de medición. Alternativas
alineadas: Regional Studies, Journal of Regional Science, World Development Perspectives, Journal of
Economic Geography (si se fortalece lo espacial).

**Orden inmediato (no agregar más análisis todavía):** (1) congelar cuál paper va primero — recomendado
**Paper 1**, porque fija la validez del objeto que Paper 2 explota; (2) integrar literatura y
referencias [A1]; (3) elegir 4–5 figuras y 3 tablas por paper; (4) convertir claims fuertes en claims
identificados [A3, B1–B6]; (5) métodos reproducibles; (6) lectores externos; (7) solo después, análisis
que un lector pida.

*manuscrito.md se conserva como working paper largo / síntesis del proyecto — no como artículo enviable.*
