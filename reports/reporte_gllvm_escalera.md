# Escalera GLLVM: resultados K=3 (peldaños 1–4)

**Corrida:** 2026-07-11, NumPyro NUTS, 4 cadenas × (1000 tune + 1000 draws), semilla 1,
N=2,455 municipios × J=17 indicadores (logit-z). K=3 y K=2 completos.
Figuras: `../figures/02_escalera_gllvm/fig_escalera_cargas.png`, `../figures/02_escalera_gllvm/fig_escalera_vardecomp.png`, `../figures/02_escalera_gllvm/fig_escalera_metricas.png`,
`../figures/02_escalera_gllvm/fig_gamma_estados.png`.

## Resumen por peldaño

| Peldaño | Moran I resid. | ELPD-LOO | sd latente media | ρ BYM2 |
|---|---|---|---|---|
| 1 base | 0.422 | −26,229 | 0.80 | — |
| 2 +Vista D | 0.336 | −15,730 | 0.78 | — |
| 3 +estado | **0.225** | −15,118 | 0.70 | — |
| 4 +BYM2 (sin estado) | 0.294 | **−12,876** | **0.42** | 1.00 en los 3 factores |

*(R-hat de α es ~1.00 en todos los peldaños; el R-hat alto reportado (2.0–2.6) viene de σ y del
bloque factorial y refleja multimodalidad rotacional — ver §Diagnóstico. Las cantidades a nivel
ajuste (η, ELPD, Moran, α) coinciden entre cadenas; cargas, scores y descomposiciones están
alineadas por Procrustes por cadena.)*

## Hallazgo 1 — El "factor general" del peldaño 1 era, en su mayoría, composición observable

La fracción media de varianza atribuida a los factores latentes cae de **0.60 → 0.15** al
entrar Vista D (+ruralidad); los cofactores absorben **0.48**. Las cargas que más caen
(post-Procrustes, 1→2): `ing_2sm` (−0.59), `car_servbas` (−0.52), `sin_electr` (−0.48),
`lp_ingreso`/`lp_ingreso_ext` (−0.44/−0.47) sobre el factor material (`loc_peq` −0.68 es
mecánico: ruralidad ES la covariable). El ELPD salta +10,500 — por mucho el peldaño que más
aporta. Esto confirma con maquinaria bayesiana lo que el baseline ridge/KNN del reporte
confirmatorio ya insinuaba: **la privación municipal es ante todo una función del perfil
territorial-demográfico observable**; el espacio latente "puro" es la desviación respecto a esa
composición, no el fenómeno completo. La lectura correcta de los factores de los peldaños 2–4
es condicional: *privación no explicada por composición*.

## Hallazgo 2 — La geografía discreta es real, y `car_salud` es su caso extremo

Los efectos estatales (peldaño 3) absorben en promedio **0.17** de la varianza y bajan el Moran
residual a 0.225. El caso dramático: **`car_salud`**, el indicador "casi ortogonal" de los
reportes previos (uniqueness 0.94 en el peldaño 1), resulta ser **~22% estado**: su uniqueness
cae de 0.82 → 0.53 al entrar γ_s. En 2020 — año de la transición Seguro Popular→INSABI — el
acceso a salud es un fenómeno de *política estatal*, no de municipio. Su "ortogonalidad" era
federalismo, no ruido.

**Test del DAG (directo vs modelado):** la predicción era |γ_s| mayor en los indicadores SAE
(calibrados a totales estatales). Resultado matizado: SAE 0.322 > CONAPO censal 0.269 ✓, pero
los CONEVAL *directos* son los más altos (0.340), arrastrados por `car_salud` (0.438, el máximo
de los 17) y `car_servbas` (0.363). Es decir: **ambos bloques CONEVAL (universo personas,
muestra censal) cargan más estado que los CONAPO censales**, y el componente estatal mezcla
política real (salud) con posible artefacto de calibración (las dos líneas de ingreso SAE están
en el top-5: 0.359 y 0.353, mientras `car_segsoc` SAE queda abajo, 0.267). El artefacto de
calibración no queda descartado ni confirmado en bloque: hay que mirarlo indicador por
indicador (`outputs/dag_test_directo_vs_modelado.csv`).

**Descomposición fiscal de γ̄_s** (`../figures/02_escalera_gllvm/fig_gamma_estados.png`, `outputs/gamma_estados_decomposicion.csv`):
el efecto estatal medio correlaciona r = −0.46 con log PIBE pc y r = +0.48 con gasto estatal/PIBE.
Los estados con efecto positivo (más privación de la que su composición municipal predice) son
pobres y con gobiernos grandes relativo a su economía (Chiapas 07, Guerrero 12, Oaxaca 20,
Veracruz 30, Yucatán 31); los negativos son el norte rico (NL 19, Coahuila 05, BCS, Sonora).
Con 32 puntos y CDMX sin gasto EFIPEM esto es descriptivo, no causal — pero deja los efectos
estatales anclados a algo medido, no como cajón residual. (Nota: gasto/PIBE alto en estados
pobres es en parte mecánico — transferencias federales sobre PIB chico.)

## Hallazgo 3 — Lo espacial suave predice mejor y angosta la incertidumbre, pero NO sustituye al estado

El peldaño 4 (BYM2 sobre z, sin estado) da el mejor ELPD (−12,876, +2,242 sobre el peldaño 3) y
**la incertidumbre municipal se reduce a la mitad** (sd media 0.70 → 0.42; por factor:
material 0.15→0.10, educativo 0.52→0.33, monetario 0.26→0.12) — el "préstamo de fuerza" de los
vecinos es real y cuantificado. Pero dos señales dicen que la especificación espacial actual es
insuficiente como geografía única:

1. **ρ = 1.00 en los tres factores** — el posterior se apila en la frontera (ICAR puro). Con un
   campo por factor tan flexible, ρ pierde su papel de "métrica 4" y ya no discrimina.
2. **El Moran residual SUBE respecto al peldaño 3** (0.294 vs 0.225): un campo espacial
   *compartido* (vía z) no puede absorber autocorrelación *específica por indicador* (salud,
   drenaje), que los γ_s por indicador sí capturan. → La geografía residual del sistema es
   **indicador-específica, no un continuo compartido**. La comparación 3-vs-4 respondió algo
   más interesante que "¿cuál gana?": son geografías de naturaleza distinta.

## K=2 vs K=3: la dimensión extra paga en los cuatro peldaños

| Peldaño | ELPD K=2 | ELPD K=3 | Δ (K=3 − K=2) |
|---|---|---|---|
| 1 base | −30,341 | −26,229 | +4,112 |
| 2 +Vista D | −21,076 | −15,730 | +5,346 |
| 3 +estado | −16,538 | −15,118 | +1,420 |
| 4 +BYM2 | −19,443 | −12,876 | **+6,567** |

Dos lecturas: (i) **K=3 domina en todos los peldaños** — cierra la duda del reporte
confirmatorio ("K=3 en el borde") a favor de K=3, ahora con covariables, geografía e
incertidumbre en la ecuación; (ii) en K=2 el peldaño espacial es *peor* que el estatal
(−19,443 < −16,538), mientras en K=3 lo espacial gana: con pocos factores el campo BYM2
compartido no tiene canales suficientes para la geografía específica por indicador — refuerza
el Hallazgo 3. El Moran residual de K=2 replica el patrón de K=3 (mínimo en el peldaño 3:
0.237; sube a 0.341 con BYM2).

## Diagnóstico técnico (leer antes de citar números finos)

- **Label switching real entre cadenas en los 4 peldaños** (diagnóstico max|R−I| ≈ 1.1–1.5).
  Causa raíz: **las anclas se apagan** — `diag` (carga ancla) tiene modos en ~0 en algunas
  cadenas (p.ej. material→`sin_agua` en el peldaño 2: a `sin_agua` casi no le queda contenido
  factorial tras condicionar en composición; HalfNormal permite diag→0 y la rotación queda
  libre). Consecuencias contenidas: cargas/scores/descomposiciones se reportan alineadas por
  Procrustes por cadena (`analyze_ladder.py::recompute_from_idata`), y α/η/ELPD/Moran son
  invariantes (desacuerdo entre cadenas: α ≤ 0.007; σ ≤ 0.17 en el peor peldaño).
- **Respecificación recomendada para la siguiente corrida:**
  1. Re-anclar material en un indicador con carga parcial fuerte (`piso_tierra` o `hacinam`),
     no `sin_agua`;
  2. `diag ~ LogNormal(log 0.5, 0.4)` (acotada lejos de 0) en vez de HalfNormal;
  3. para ρ: prior penalizada hacia 0 (tipo PC prior) o reportar en su lugar el Moran de z;
  4. peldaño 4b exploratorio: BYM2 **por indicador** solo para `car_salud` y `sin_drenaje`
     (los de mayor γ_s), que es donde la geografía específica vive.
- ELPD-LOO: Pareto-k altos (esperado con latentes por observación); usar solo como ordenamiento
  grueso entre peldaños, no como diferencia calibrada.

## Re-corrida con anclas v2 (2026-07-12): qué se sostiene y qué no

Se re-corrió K=3 completo con material→`piso_tierra` y `diag ~ LogNormal(log .5, .4)`.

| Peldaño | Moran resid. | ELPD v2 | ELPD v1 | sd latente v2 |
|---|---|---|---|---|
| 1 | 0.413 | −25,834 | −26,229 | 0.55 |
| 2 | 0.346 | −15,624 | −15,730 | 0.41 |
| 3 | **0.223** | **−13,555** | −15,118 | 0.40 |
| 4 | 0.323 | −16,855 | −12,876 | 0.35 |

1. **Los hallazgos sustantivos replican**: test DAG (0.32/0.34/0.27), correlaciones fiscales de
   γ̄_s (−0.45/+0.47), Moran mínimo en el peldaño 3, `car_salud` estatal. Los scores municipales
   correlacionan 0.83–0.91 entre corridas sin intercambio de factores (matriz cruzada diagonal),
   el top-25 material comparte 17/25 y Batopilas sigue #1 con la misma media y sd más angosta
   (0.46→0.28).
2. **La ventaja de ELPD del peldaño 4 NO replica**: en v2 el espacial cae por debajo del estatal
   (−16,855 vs −13,555), igual que en K=2. La ordenación 3>4 es la robusta; la 4>3 de la v1 era
   dependiente del modo. Conclusión reforzada: **la geografía por indicador (estado) es la
   especificación defendible; el BYM2 compartido en z no lo es** (ρ sigue clavado en 1.00).
3. **Las anclas v2 no eliminaron el label switching y el test decisivo
   (`scripts/test_label_switching.py`, peldaño 2, 4 cadenas) mostró que NO es solo rotación**:
   R-hat sobre cantidades alineadas draw a draw con Procrustes sigue alto (Λ alineada 2.16,
   z alineada 1.54, σ 2.16; α 1.04). Hay **multimodalidad genuina**: las cadenas encuentran
   soluciones de cargas parecidas pero no reconciliables por un mapa ortogonal (difieren en el
   reparto de varianza entre factores, bloques de método y σ). Consecuencias:
   - Lo que publicamos son **promedios sobre modos**; su validez empírica descansa en la
     replicación entre corridas independientes (v1 vs v2 = multi-arranque de facto): scores
     r≈0.9, mismas conclusiones de escalera, mismos hallazgos fiscales. Lo que NO replicó
     (ELPD del peldaño 4) queda correctamente descartado por este mismo criterio.
   - La ruta de fondo para la siguiente iteración es **marginalizar z** (verosimilitud
     integrada: Y ~ N(μ, ΛΛ' + Ψ) con bloques de método), que elimina 7,365 parámetros
     latentes y típicamente funde los modos; no más cirugía de priors.

## CIERRE DEL FRENTE 1 (2026-07-12): la multimodalidad resuelta — y era autoinfligida

Secuencia de diagnóstico (cada paso con su veredicto formal en tres niveles):

| Modelo | R-hat ΛΛᵀ | R-hat σ/mload | media (W, γ) | ELPD-LOO |
|---|---|---|---|---|
| z muestreada (escalera) | — (alineación) | ~2 | ~1–2.6 | — |
| marginalizado + anclas + bloques uniformes | 2.05 | 1.7 / 1.9 | 1.011 / 1.022 | — |
| + método como CONTRASTE inter-agencia | 1.53 | 1.5 | 1.007 / 1.006 | −24,183 |
| **+ Λ libre (sin anclas), identificar ΛΛᵀ** | **1.003** (ESS 3,490) | **1.006 / 1.002** | 1.005 / 1.005 | **−24,106** |

Tres causas apiladas, todas de especificación: (i) los z muestreados fabricaban geometría
multimodal; (ii) el bloque de método con dirección uniforme era casi colineal con las cargas
del factor (se intercambiaban) — resuelto definiendo el método como **contraste inter-agencia**
(dirección fija CONAPO+/CONEVAL−, ortogonal al nivel; conceptualmente superior: el método ES el
desacuerdo entre instrumentos); (iii) **las anclas peleaban con la verosimilitud** — una cadena
encontraba un modo con logp +106 pagando prior enorme por colapsar el ancla monetaria. Sin
anclas, todo converge (0 divergencias, BFMI 0.91) y los **eigenvalores de E[ΛΛᵀ] = 1.23, 0.50,
0.34, ≈0…** confirman K=3 desde dentro del modelo.

**Convención de orientación documentada** (`outputs/ejes_canonicos_marginal.csv`,
`zscores_canonicos_rung3.csv`): ejes = eigen-descomposición de E[ΛΛᵀ], signo del elemento
mayor positivo, ejes por draw alineados al canónico. Lectura: eje1 = privación
material-infraestructural general; eje2 = educativo; **eje3 = vivienda+líneas de ingreso
CONTRA servicios de red** — la tercera dimensión que el ancla "monetaria" no dejaba emerger.
Los criterios de cierre del revisor: (1) R-hat<1.01 + ESS en no-rotacionales ✓; (2) ΛΛᵀ
estable ✓; (3) partición de varianza estable ✓; (4) scores estables tras alineación ✓;
(5) conclusiones sustantivas replican (tabla estatal, abajo) ✓.

## CIERRE DEL FRENTE 2: medición vs federalismo, con incertidumbre posterior

Con las γ del modelo convergido (`outputs/tabla_medicion_federalismo.csv`): `car_salud` domina
el share de varianza estatal (0.27), seguido de `sin_drenaje` (0.23) y `car_servbas` (0.19);
`loc_peq` ≈ 0.01. Contrastes de grupo (posterior): **Δshare SAE − CONEVAL directo = −0.034,
IC95 [−0.060, −0.007]** (los calibrados NO dominan — muere "todo es SAE") y **Δshare SAE −
CONAPO censal = +0.027, IC95 [+0.007, +0.049]** (el piso de calibración existe, y es chico).
Conclusión calibrada: el componente estatal no está dominado por la arquitectura SAE; es
compatible con heterogeneidad sustantiva estatal, aunque sigue mezclando política, composición
y medición.

## Implicación integradora

La pregunta central del repo ("¿cuándo cuentan historias distintas?") queda reformulada por la
escalera: la discordancia marginación-pobreza vive en tres capas separables — (i) composición
territorial (la mayor parte, y compartida), (ii) política estatal (salud sobre todo, con mezcla
de calibración SAE no resuelta), y (iii) desviaciones municipales espacialmente suaves (reales
pero menores, con incertidumbre ya cuantificada municipio por municipio en
`outputs/zscores_rung4_K3.csv`). El producto diagnóstico prometido — "no un índice nuevo" —
ya tiene forma empírica.

*Pendiente: respecificación de anclas y re-corrida; mapas de z ± sd (falta geojson — ver
inegi-client en el manifiesto). Nota K=2: el label switching también aparece (salvo el peldaño
3, único con cadenas coincidentes); los CSVs de ambos K están regenerados con la alineación
por cadena.*
