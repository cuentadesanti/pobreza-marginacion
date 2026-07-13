# Tabla maestra de resultados — qué es principal, qué es validación, qué es apéndice

**Regla editorial**: cuatro resultados principales; todo lo demás los apoya o los acota.
(El riesgo ya no es falta de análisis sino exceso de hallazgos compitiendo.)

## Los cuatro resultados principales

| # | Resultado | Número clave | Robustez | Fuente |
|---|---|---|---|---|
| 1 | **La desigualdad territorial opera en dos escalas**: ~mitad entre estados en los indicadores observados; predominantemente intraestatal en los factores condicionales (γ_s absorbe la parte interestatal antes del residuo) | 50.8% entre (z bruto) vs 13–24% (ejes canónicos) | ✓ ponderación (bruto); sensibilidad al objeto distributivo declarada (eje1: 23.6%→0.5% equiponderado) | `reporte_desigualdad.md` A; `desigualdad_theil.csv` |
| 2 | **Las geografías de privación residual se solapan débilmente**: la acumulación multidimensional vive en el nivel bruto, no en el residuo | obs/esp 1.25–1.43 (IC≈1); Jaccard 0.05–0.21; 3-severas = 2.0% munis / 0.8% pob | ✓ umbrales 70/75/80/90 + bootstrap | `reporte_desigualdad.md` C; `fig_acumulacion.png` |
| 3 | **Brecha de apropiación territorial**: la actividad visible coexiste con precariedad laboral y mejora social local menor a la que sugiere la luminosidad | β precariedad +0.23 (t=8.6) > log pob +0.15 > remesas −0.07 (t=−5.3) | ✓ FE estado + HC1; coherente con colas de remesas ~20× [14–28] | `reporte_desigualdad.md` B; `reporte_satelital.md` |
| 4 | **La discordancia fundacional es de método**: la firma SAE-EBPH (las dos líneas de ingreso moviéndose juntas más allá del factor monetario) parte los regímenes LISA — la discordancia "más pobre que marginado" está mediada por el método de imputación de ingreso | mload SAE 0.58 (vs educación 0.012: las agencias casi acuerdan); AA −0.325 vs BB +0.339; 22.6% con firma sustantiva; sin correlación con composición | ✓ scores E[m∣Y] con incertidumbre; desacuerdo viv-servicios identificado como ESTATAL (0.135→0.029 con γ_s) | `desacuerdo_agencias.csv`; `fig_desacuerdo_agencias.png` |

## Validaciones y piezas de soporte

| Pieza | Número | Rol | Fuente |
|---|---|---|---|
| Identificación del subespacio (marginalizado libre) | R-hat ΛΛᵀ 1.003; eigen 1.23/0.50/0.34 (rango efectivo 3) | fundamento del espacio latente | `reporte_gllvm_escalera.md` cierre |
| γ_estado estabiliza la descomposición | p2 vs p3: ELPD +5,410±135; un eje rota 53°; Δσ²ⱼ∝shareⱼ | por qué el peldaño 3 es canónico | `comparacion_marginal_2v3.csv` |
| Medición vs federalismo | ΔSAE−directos −0.034 [−0.060,−0.007]; ΔSAE−censal +0.027 [+0.007,+0.049] | acota la lectura de γ_s | `tabla_medicion_federalismo.csv` |
| `car_salud` = huella INSABI | corr +0.61 con dependencia SP/INSABI (máx de 17); placebos 0.18–0.49 | interpretación institucional puntual | `validacion_insabi.csv` |
| Luces ven lo material bruto | R² 0.41–0.43 (bloqueos); nada ve el residual (24/24 <0) | alcance de las lentes | `reporte_satelital.md` |
| Curva luz-privación con regímenes | canónico 0.005; piso oscuro 14%; umbral sur vs norte IC disjuntos | límite del modelo simple | corte B |
| La vara vale dinero | AA +15.8% Ramo 33 pc (t=4.3) vs BB −3% | política/circularidad FAIS | `reporte_dgp_dag.md` §4b |
| Homicidios: el residual no predice violencia | orden estable en 7 variantes; dif +0.06–0.21 todos los folds | validación externa 1 | `sensibilidad_homicidios.csv` |
| Certeza municipal por eje | sustantivo: 41.9/54.6/13.6% de municipios | anti-sobreinterpretación | `certeza_canonica.csv`; `fig_certeza_canonica.png` |
| Circunstancias → privación bruta (incremental) | 0.27→0.47→0.73→0.78 (+indígena Δ0.04; +estado 0.89 no bloqueado) | capa de oportunidades (predictivo) | `desigualdad_robustez.csv`; `vistaD_indigena.parquet` |
| Federalismo sectorial | PC1 de γ = 42% (común, = capacidad: +0.42 PIBE pc); 58% específico por dominio | refina la lectura de γ_s | `veta_gamma_pca.csv` |
| La geografía de la ignorancia | sd posterior mayor en municipios grandes/urbanos (+0.32 pob, −0.26 ruralidad): el modelo sabe más del campo que de la ciudad | sección de incertidumbre | `veta_ignorancia.csv` |
| Los 48 triple-severos | mitad Oaxaca; mediana 5,430 hab; remesas 17 vs 92 USD; 27% presencia criminal vs 48%; 44/48 invisibles al LISA | el rostro del resultado 2 | `veta_48_triple.csv` |
| Exposición criminal ⊥ privación residual (Vista G) | G1/G2 negativos con robustez; G4: competencia +0.130 > monopolio +0.083 sobre homicidio | quinta ruta de dimensiones distintas | `reporte_crimen_desigualdad.md` |
| Coerción política (Trejo-Ley, rezagada 2007–12) | privación residual: nulo; homicidio 2019–21: +0.26 (t 2.7) robusto; coerción donde competencia×fragmentación (t 3.4) | cierra criterio 5 Vista G; persistencia de violencia, no de privación | `g5_coercion.csv` |

## Apéndices / extensiones declaradas

DAG canónico verificado (56 nodos/97 aristas, acíclico); DGP y 5 dependencias mecánicas;
FAIS dinámico (otro paper); multi-escala del corte B;
raster de accesibilidad MAP; DENUE (Vista F2); serie 2010–2020.
