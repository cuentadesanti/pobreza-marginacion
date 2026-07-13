# Vista G — gobernanza criminal y desigualdad territorial: resultados (incluido el negativo)

**Disciplina aplicada** (steer maestro): fuentes auditadas antes de modelar
(`auditoria_fuentes_crimen.md`, 13 fuentes); presencia documentada ≠ control territorial;
O = R × D con proxies de observabilidad SIEMPRE en la especificación; lenguaje de *asociación
compatible con*; ningún resultado sube a la tabla maestra sin sensibilidad completa.

**Datos**: OCVED 2.0 (verificado: 64,895 eventos diario-municipales 2000–2018, actores,
match de claves 100%) → taxonomía P/N/C/F/V/WC por 4 ventanas
(`vistaG_crimen_municipal.parquet`); ACLED agregado ADMIN1 como contexto estatal 2018+
(`vistaG_crimen_estatal.parquet`); BACRIM = state_context pendiente de plataforma.
Exposición principal: ventana pre-2020 (2015–2018).

## Los criterios de éxito del steer, evaluados

| Criterio | Veredicto |
|---|---|
| 1. Competencia importa más que presencia simple | **✓ solo para violencia** (G4): homicidio EB 2019–21 — monopolio N=1 β=+0.083 (t=3.1) vs competencia N≥2 **β=+0.130 (t=4.0)**; el contraste sobrevive ventanas (Calderón t=3.4; 2018 t=2.7), se atenúa sin la descomposición por N |
| 2. Exposición criminal explica desigualdad intraestatal residual | **✗ NEGATIVO** (G1): sobre los ejes canónicos, P y C no son robustos (β_C en eje1 voltea de −0.14 a +0.01 entre especificaciones); solo WC vecinal es sugerente (t 2.0–2.5) sin sobrevivir la ventana histórica |
| 3. Brecha de apropiación mayor bajo coerción/competencia | **✗ NEGATIVO** (G2): C t=1.2; WC t=2.2 no sobrevive Calderón. La brecha sigue siendo un fenómeno de precariedad laboral, no de exposición criminal documentada |
| 4. Violencia organizada y privación son dimensiones territorialmente distintas | **✓ el hallazgo del capítulo**: la misma exposición que predice homicidio (t 3–4.5) no mueve la privación residual — **quinta ruta independiente** a la conclusión (dimensionalidad, homicidios-validación, satélite, acumulación disjunta, y ahora exposición criminal) |
| 5. Coerción política como ruta específica | **✓ como violencia, ✗ como privación** (G5, Trejo-Ley 2007–2012 rezagado): la coerción histórica no mueve los ejes residuales 2020 (eje1 t −0.3; eje3 con signos contradictorios dummy/tasa → no se promueve), pero predice homicidio 2019–21 una década después (+0.26, t 2.7; sobrevive sin proxies, sin metrópolis y condicionando en C_calderon) y ocurrió donde competencia × fragmentación partidista interactúan (CxJ t 3.4 — réplica transversal de la tesis Trejo-Ley con OCVED independiente) |

## Detalle de estimaciones (FE estado, WLS 1/sd², HC1; `g_modelos_principales.csv`, `g_robustez.csv`)

- **G1** — eje3 muestra el único patrón con forma (P −0.10 t=−2.3; C +0.12 t=+2.6: monopolio
  asociado a *menos* privación vivienda-vs-redes, competencia a más), pero el eje3 tiene la
  clasificación municipal más débil del sistema (14% sustantivo) → se reporta como sugerente,
  no se promueve.
- **G2** — brecha: nada robusto; la exposición vecinal (WC +0.09, t=2.2) es lo único que
  respira y muere en la ventana histórica.
- **G4** — homicidio: P solo +0.106 (t=4.5); descompuesto, el gradiente por N es la pieza:
  competencia > monopolio > sin registro, estable entre ventanas. Consistente con la
  literatura (la violencia sube con la disputa, no con el control).

## G5 — coerción política (Fase 3, cerrada con Trejo-Ley)

**Fuente verificada**: réplica de Trejo & Ley, *High-Profile Criminal Violence* (Dataverse
doi:10.7910/DVN/VIXNNE; codebook leído). Panel municipio-año 2007–2012, 2,018 municipios;
CAPAM: 311 ataques del crimen organizado contra autoridades, candidatos y activistas (204
municipios con ≥1). **Exposición histórica rezagada** — nunca contemporánea a los outcomes
2020. CAPAM se construye de prensa: O = R × D aplica y los proxies de observabilidad van en
toda especificación (`g5_coercion.csv`).

- **G5a** (privación residual 2020): nulo en eje1/eje2 (dummy t −0.3 / −0.1); en eje3 el
  dummy y la tasa dan signos opuestos (+0.372 vs −0.157) — colinealidad dummy/tasa, no ruta;
  no se promueve. La coerción política se suma a P/C/WC: **ninguna cara de la exposición
  criminal documentada explica la desigualdad residual de privación.**
- **G5b** (persistencia de violencia): coerción 2007–12 → homicidio EB 2019–21 **+0.26
  (t 2.7)**, estable sin proxies (t 2.5), sin metrópolis (t 2.4) y condicionando en la
  competencia OCVED de la misma era (+0.25, con C_calderon +0.14 t 4.2): canal propio,
  no reducible a la mera presencia de organizaciones.
- **G5c** (¿dónde ocurrió?): coerción ~ competencia × fragmentación partidista vertical
  (juxtaposition): interacción **+0.056 (t 3.4)** — la lectura transversal reproduce el
  mecanismo del paper original con una fuente de presencia criminal independiente (OCVED).
- **G5d** (estatal, descriptivo, n=31): tasa de coerción ⊥ PC1 de γ (corr +0.08; corregida
  una desalineación posicional de columnas detectada en capa C) — el gradiente común de
  capacidad estatal no está asociado a la coerción histórica.

## Interpretación (calibrada)

La exposición criminal documentada en México es, territorialmente, **un fenómeno de violencia
más que de privación**: asociación compatible con disputa→violencia (más fuerte bajo
competencia que bajo monopolio), y esencialmente ortogonal a la desigualdad residual de
privación una vez descontadas composición y estado. El resultado negativo de G1/G2 se
documenta y **la Vista G no se fuerza dentro de la tesis principal** — queda como capítulo de
validación con dos hallazgos propios (criterio 4: dimensiones distintas; G5b: la coerción
política de 2007–12 deja una huella de violencia medible una década después, pero no de
privación). Agenda restante: PAIAMEX y MCO por gestionar con autores; eventos ACLED
municipales pendientes de credencial.

**Advertencias vigentes**: OCVED termina en 2018 (la "ventana pre-2020" es 2015–2018);
sin-registro ≠ ausencia real (los modelos llevan proxies de observabilidad; sin ellos, β_C
del eje1 se infla a −0.14 — ilustración directa del sesgo de detección); homicidio ≠ crimen
organizado (validación, no equivalencia).
