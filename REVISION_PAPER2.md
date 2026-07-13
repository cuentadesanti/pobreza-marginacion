# Revisión de referee — Paper 2 (`paper2_desigualdad.md`)

**Dictamen:** revisión menor-a-moderada. La arquitectura es sólida (dos objetos distributivos
definidos antes de contrastarlos; cautelas de fragilidad en los 48; el cierre "las cinco piezas
no validan la misma cantidad" es exactamente el hedge correcto), el aparato está completo
(6 figuras, 3 tablas ancladas, construcción de la brecha en 3 pasos, apéndice de robustez).
Pero esta pasada encontró **dos números centrales contradichos por sus propios CSVs** (F1, F2)
y una afirmación cuantitativa sin output reproducible (F3) — los tres del mismo tipo que un
referee de World Development cazaría en la primera lectura seria.

## Mayores (verificados contra disco en esta pasada)

**F1 — El rango "Theil entre-estados 48–59%" es falso; el real es 31.1–58.8%.** Aparece en el
resumen y en §4. `desigualdad_theil.csv` (los 17 indicadores): mínimo `sin_electr` 31.1%,
máximo `lp_ingreso` 58.8%, mediana 47.8%. El "48–59%" describe solo la mitad superior de la
distribución (8 de 17 indicadores caen por debajo de 48). La tesis "cerca de la mitad" se
sostiene — mediana 47.8%, factor material bruto ponderado 50.8% — pero el rango citado no.
Corrección propuesta: "31–59% según indicador (mediana 48%; 50.8% para el factor material
bruto), con los servicios de red como lo menos federalizado (31–35%) y las líneas de ingreso
como lo más (56–59%)". Ese contraste servicios-vs-ingreso además *fortalece* el argumento:
lo más federalizado es exactamente lo SAE-calibrado.

**F2 — "nada del residual (24/24 R² < 0)" contradice `satelital_modelos.csv`.** El CSV
archivado da, sobre los ejes condicionales (rung3): 26/30 combinaciones negativas contando
todo; 20/24 contando solo modelos con lentes (M1–M4 × 3 factores × 2 estimadores); las 4
no-negativas son todas ridge con R²cv 0.005–0.030 (≈0, sd 0.026–0.033). La conclusión
sustantiva ("las lentes no ven el residual") sobrevive intacta, pero el conteo citado no
corresponde al output vigente — probablemente quedó de una corrida anterior. Corrección:
"ninguna combinación supera R²cv = 0.03 y 26/30 son negativas". El mismo "24/24" vive en
`reporte_satelital.md` (L84) y en `manuscrito.md` — barrerlos juntos.

**F3 — El contraste monopolio/competencia (+0.083 vs +0.130) no tiene CSV.** Es el número
titular de la validación por crimen (§8.3, también en TABLA_MAESTRA y
`reporte_crimen_desigualdad.md`), pero el bloque que lo produce (`g_modelos.py`, sección
"7.6") solo lo imprime a stdout — no está en `g_modelos_principales.csv` ni en
`g_robustez.csv` (el 0.083 que aparece ahí es un error estándar de otra fila). Mismo defecto
que el M5 del Paper 1: afirmación cuantitativa sin output reproducible. Corrección: extender
`g_modelos.py` para persistir las filas N=1 / N≥2 (y sus variantes de ventana) y cubrirlas
con `check_captions.py`.

## Verificado y correcto (esta pasada, contra disco)

- Perfil completo de los 48 triple-severos: 24/48 Oaxaca, mediana 5,430 vs 13,539 nacional,
  79%/75% rural según umbral, remesas 17 vs 92, presencia criminal 27%, 44/48 LISA ns ✓
- 2.0% observado vs 1.6% bajo independencia (1.96 / 1.56 exactos) ✓
- Regresión de la brecha (`desigualdad_brecha_apropiacion.csv`): precariedad +0.226 (t 8.6),
  log_pob +0.151, remesas −0.072 (t −5.3) ✓; por factor −0.034/+0.027
  (`satelital_remesas_reg.csv`) ✓
- INSABI 0.606, placebos 0.178–0.489 (`validacion_insabi.csv`) ✓
- Homicidios: ~23% (0.228/0.230), composición 0.204 vs residual 0.027, diferencia positiva
  en 100% de folds (0.06–0.21), "100 mil registros" = 103,022 ✓
- G5 coerción: 0.26/2.7 y robustez t 2.4–2.7 (`g5_coercion.csv`) ✓
- Fiscal: AA 15.78 / BB −2.97 (`gap_aportaciones_regimen.csv`) ✓
- Escalera 0.265→0.469→0.732→0.775 (+estado 0.891) ✓ (bindings)
- Tabla 1, Tabla 2, R² satelital bruto 0.41–0.43, piso oscuro 14%, Jaccard 0.05–0.21 ✓

## Menores

**f1 — La regresión de la brecha reporta 3 de 10 coeficientes.** El CSV tiene además
`loc_peq_pct` +0.140 (t 9.1) y `tri_mean` −0.135 (t −9.1), tan grandes como el tamaño urbano,
y `pct_secundario` +0.085 (t 8.1). "Predictor dominante" para precariedad es correcto (es el
mayor), pero un referee querrá la tabla completa — añadirla como tabla del apéndice E.

**f2 — El "~20× (IC95 14–28)" de colas vive solo en el reporte.** Documentado con método
(bootstrap, estable a umbrales 5/10/15%) en `reporte_satelital.md` L79, pero sin CSV. Menor
porque el método está declarado; ideal persistirlo si la frase sobrevive al recorte.

**f3 — El t = 4.3 fiscal no está en el CSV.** `gap_aportaciones_regimen.csv` trae los gaps
pero no los t; el 4.3 vive en `reporte_dgp_dag.md` §4b y en los píxeles de la Figura 6.
Añadir la columna t al CSV al regenerar.

**f4 — La Figura 1 es la misma imagen que la Figura 5 del Paper 1** (fig_mapas_canonicos).
Legítimo entre papers compañeros, pero si van coordinados a revistas distintas conviene
variar (p. ej. solo medias, sin panel de sd) o declarar el reúso.

**f5 — Literatura mexicana igual de anunciada que estaba en P1 antes de m3.** §2 tiene tres
literaturas internacionales; falta el anclaje mexicano que P1 ya integró (Cortés & Vargas
2011 con DOI verificado está disponible; la tradición de convergencia regional post-TLCAN
— Esquivel — es el hueco natural del §2 primer párrafo). Cerrar antes de envío.

**f6 — Tabla 1 mezcla dos estadísticos en una columna** (Theil para indicadores, varianza
para ejes). La nota lo declara — suficiente para borrador — pero un referee puede pedir el
mismo estadístico en ambos bloques o dos columnas separadas.

## No tocar (está muy bien)

- La definición explícita de los dos objetos distributivos en §3 *antes* del contraste de §4
  — desactiva la objeción "no hay contradicción entre 50.8% y 76–87%" antes de que nazca.
- Las dos cautelas del párrafo de los 48 (sensibilidad al umbral; certeza del eje 3) y el
  hook desterrado a §9 — exactamente lo que pedía B5.
- La construcción de la brecha en tres pasos OOF, con la dirección del signo definida.
- El cierre de §8: "las cinco piezas no validan la misma cantidad" con el mapa de qué prueba
  cada una.
- El O = R × D con proxies declarado dentro del punto 3 — la disciplina del steer sobrevivió
  hasta el paper.

## Veredicto

Con F1–F3 resueltos (F1 y F2 son reescritura + barrido de reportes; F3 pide ~15 líneas en
`g_modelos.py` y un rerun barato de WLS) y f1/f5 cerrados, el Paper 2 queda listo para
traducción y envío a World Development. F1 tiene premio escondido: el rango real, bien
contado, refuerza la tesis de la firma SAE del paper compañero.

*Nota de método: en esta pasada TODAS las cifras listadas en "Verificado y correcto" se
comprobaron contra sus CSVs/parquets en `outputs/` y `data/processed/` (no de memoria ni del
reporte); F1–F3 son los tres puntos donde esa comprobación falló. Los puntos f4–f6 y "no
tocar" salen de lectura directa del paper.*
