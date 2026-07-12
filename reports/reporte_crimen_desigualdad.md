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
| 5. Coerción política como ruta específica | pendiente (Fase 3: Trejo-Ley descargable; PAIAMEX por pedir) |

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

## Interpretación (calibrada)

La exposición criminal documentada en México es, territorialmente, **un fenómeno de violencia
más que de privación**: asociación compatible con disputa→violencia (más fuerte bajo
competencia que bajo monopolio), y esencialmente ortogonal a la desigualdad residual de
privación una vez descontadas composición y estado. El resultado negativo de G1/G2 se
documenta y **la Vista G no se fuerza dentro de la tesis principal** — queda como capítulo de
validación con un hallazgo propio (criterio 4) y una agenda de Fase 3 (coerción política:
Trejo-Ley 1995–2012 descargable; PAIAMEX y MCO por gestionar con autores; eventos ACLED
municipales pendientes de credencial).

**Advertencias vigentes**: OCVED termina en 2018 (la "ventana pre-2020" es 2015–2018);
sin-registro ≠ ausencia real (los modelos llevan proxies de observabilidad; sin ellos, β_C
del eje1 se infla a −0.14 — ilustración directa del sesgo de detección); homicidio ≠ crimen
organizado (validación, no equivalencia).
