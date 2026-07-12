# Validación externa: el espacio latente contra la violencia municipal

**Outcome:** tasa de homicidios por 100 mil hab., municipio de *ocurrencia*, promedio 2019–2021
(INEGI, defunciones registradas; espejo abierto datos.gob.mx/Salud). Control de calidad: los
totales nacionales reproducen las cifras oficiales al registro exacto (34,503 / 34,825 / 33,695;
PRESUNTO=2 e ICD-10 X85–Y09 coinciden al 99.99%). Datos: `homicidios_mun_2019_2021.parquet`.

**Pregunta:** un outcome externo, no usado en ninguna parte de la construcción del espacio
latente, ¿qué versión de la privación lo predice? Ridge, R² de 5-fold CV sobre
log1p(tasa), N=2,455.

| Conjunto predictor | R² CV | sd |
|---|---|---|
| 17 indicadores elementales | **0.228** | 0.021 |
| Vista D (composición observable) | 0.204 | 0.017 |
| Vista D + z peldaño 3 + discordancia | 0.222 | 0.018 |
| z peldaño 1 (3 factores, no condicionales) | 0.104 | 0.020 |
| z peldaño 3 + discordancia (residual puro) | 0.016 | 0.009 |

## Tres lecturas

**1. La violencia no es un fenómeno de privación residual.** Quitada la composición
territorial, el latente condicional y la discordancia no predicen casi nada (R²=0.016). Lo
poco que la privación sabe de la violencia (≈23%) vive en el perfil observable del territorio
— ruralidad, demografía, sectores — no en la desviación municipal. Consistente con la
literatura mexicana de violencia (economía criminal con geografía propia: rutas, disputas,
no pobreza per se).

**2. La compresión 17→3 pierde justo la señal que importa aquí** (0.228 → 0.104). Los
coeficientes ridge explican por qué: la dirección predictiva es un **contraste intra-familia**,
no un nivel — `rezago_educ` +0.49 pero `sin_basica` −0.26 (misma familia educativa);
`piso_tierra` +0.43 pero `car_servbas` −0.44 (misma familia material). El perfil violento
característico: municipios con rezago educativo y piso de tierra *pero* servicios básicos y
educación básica relativamente cubiertos — serranías conectadas, no los márgenes profundos.
Un espacio de 3 factores de *nivel* es casi ortogonal a ese contraste por construcción.

**3. Para el modelo del repo esto es una validación de alcance, no un fracaso.** El espacio
latente fue diseñado para modelar la maquinaria de medición de la privación (común, método,
residuo), no para maximizar predicción de outcomes arbitrarios; el hallazgo delimita qué es:
los factores capturan el nivel común (que sí predice mortalidad por composición), y los
*contrastes* informativos para otros fenómenos (violencia hoy; movilidad social o salud
mañana) requieren mirar el espacio completo de residuos por indicador — exactamente lo que
`s_ij` y los bloques de método preservan. Corolario metodológico para CONAPO/CONEVAL: **un
índice sintético único no puede servir simultáneamente para focalizar privación y para
anticipar violencia** — son direcciones distintas del mismo espacio de indicadores.

## Reproducibilidad
`python scripts/validacion_homicidios.py <dir_con_defunciones_csv>` — descarga documentada en
`RAW_DATA_MANIFEST.md`. Figura: `figures/fig_validacion_homicidios.png`; tabla:
`outputs/validacion_homicidios.csv`.

*Sensibilidad pendiente: tasa por municipio de residencia (vs ocurrencia), y ventana 2018–2022.*
