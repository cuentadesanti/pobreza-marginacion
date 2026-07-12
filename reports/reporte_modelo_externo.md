# Modelo externo de discordancia — Vista D v1

Especificación priorizada por el revisor: predecir la discordancia D usando **solo cofactores externos**
(remesas, estructura sectorial, precariedad, demografía, metropolitaneidad) — SIN insumos que alimenten
CONAPO o CONEVAL. Esto evita la circularidad del `lp_ingreso` mecánico del modelo interno anterior.

## Vista D v1 (congelada)
2,469 municipios, 2,455 completos. Seis familias de cofactores:
- **Ruralidad/metropolitaneidad**: % urbano, log población
- **Demografía**: razón de dependencia, % 60+
- **Empleo**: tasa ocupación, participación, **% empleo precario (PROXY de informalidad)**
- **Remesas**: per cápita 2020 (Banxico CE166, validado: suma municipal 41,676 MUSD = 103% del total nacional)
- **Estructura productiva**: % primario/secundario/terciario (censo ampliado, ponderado por factores de expansión)

**Distinción medida oficial vs. proxy** (documentada en el diccionario):
- Medidas oficiales directas: demografía, empleo, remesas, sector (este último ponderado con factores de expansión del ampliado).
- **`empleo_precario_pct` es PROXY, NO la tasa oficial de informalidad.** La informalidad oficial (ENOE: ocupados sin acceso a seguridad social vía empleo) no se capta en el censo. El proxy = % en clases precarias (cuenta propia + sin pago + jornalero + ayudante, SITTRA 2/3/5/6). Es un correlato estructural de precariedad, tratado como cofactor **con análisis de sensibilidad**.

## Resultado del modelo externo
| Especificación | R² | Moran I residual |
|---|---:|---:|
| D sin ajustar | — | 0.506 |
| Composición interna (previo) | 0.46 | 0.521 |
| **Contexto externo** | **0.31** | **0.462** |
| Contexto externo + FE estado | 0.47 | 0.344 |

Coeficientes externos significativos (estandarizados, SE agrupado por estado):
- **% urbano −12.6** (p<0.001): municipios rurales → más marginado que pobre (régimen AA).
- **% empleo precario −7.0** (p=0.001): precariedad laboral → régimen AA.
- **log población +4.6**, **razón dependencia +2.9** (p<0.01).
- **Remesas per cápita +2.3** (p=0.004): **confirma el mecanismo del régimen AA** — el ingreso por remesas baja la pobreza por ingresos mientras la marginación material persiste. Esta vez sobre terreno externo, no mecánico.

## Conclusión que refuerza el GLLVM espacial
El contexto externo explica **MENOS** que la composición interna (R²=0.31 vs 0.46), y el Moran residual apenas baja (0.506→0.462, p=0.001). Incluso con efectos fijos de estado (R²=0.47), I=0.344 sigue siendo altamente significativo.

**Ni la composición ni el contexto externo borran la geografía de la discordancia.** La dependencia espacial no explicada es robusta a ambos tipos de control → el componente espacial del GLLVM está justificado de forma independiente. (Interpretación calibrada: "persiste dependencia espacial no explicada", no "estructura causal genuina".)

## Próximo hito
GLLVM K=2 vs K=3 con Vista D como cofactores `x_i`, salud como componente específico, bloques de método,
y estructura espacial en los factores/residuos — comparado contra la versión no espacial. La infraestructura
está validada (test de recuperación de parámetros: cargas |r|≈0.88, cofactor β≈1.0, con anclas + Procrustes por cadena).
