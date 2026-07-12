# Semillas — "El modelo simple que ¿daba para más?" (luz → desarrollo)

**No es una receta. Son semillas.** Explora con libertad; lo de abajo son ganchos, sospechas ya
medidas y trampas conocidas para que arranques con grasa y no desde cero. Si encuentras algo mejor
que las preguntas que dejo, síguelo.

**Doble entrega, como pediste:**
1. **Integrado al capítulo satelital** — una subsección de `reporte_satelital.md` (no un reporte aparte).
2. **Corte transversal propio** — su figura estrella (la curva luz→desarrollo con su quiebre) y su
   tabla simple-vs-sofisticado, que se sostienen solas.

---

## La semilla que le da la vuelta a la premisa (empieza por aquí)

El paper de Jean et al. (Science 2016) asume una relación **log-lineal** luz↔desarrollo que el deep
learning refina. **En México municipal esa premisa se cae**, y ya hay evidencia en el repo:

`outputs/satelital_modelos.csv`, modelo `M1_ntl`, factor material bruto:
- **ridge (log-lineal): R²cv = −0.03** → el modelo lineal en log(NTL) no captura NADA.
- **hgb (no-lineal): R²cv = 0.41** → la misma información, leída no-linealmente, captura mucho.

**El titular de B se invierte:** no es "lo simple llega sorprendentemente lejos", es *"a escala
municipal la luz sí informa desarrollo, pero sólo si respetas su no-linealidad; el OLS log-lineal
canónico apenas ve"*. Ese contraste es el corazón del corte transversal. **Verifícalo, no lo
asumas** — puede que ridge suba con la transformación correcta (ver semilla de saturación), y ESE
sería el hallazgo aún más fino: *cuál* transformación rescata al modelo simple.

---

## Insumos listos (no re-descargar nada)

| Archivo | Qué tiene | Clave |
|---|---|---|
| `data/processed/vistaF_satelital.parquet` | `ntl_mean, ntl_sum, ntl_pc, log_ntl, elev_mean, tri_mean, acc_km, pob_tot` (n=2469) | `cvegeo` str 5 |
| `outputs/zscores_rung3_K3.csv` | z material/educativo/monetario ± sd (n=2455) | `cvegeo` **int64** ⚠️ |
| `data/processed/municipal_components_2020.parquet` | los 17 indicadores + población; medida de desarrollo alterna | `cvegeo` |
| `data/processed/estatales_2020.csv` | PIBE estatal (`pibe_mdp`, `pibe_pc_mxn`) para repartir a municipal | `cve_ent` |
| `outputs/satelital_modelos.csv` | M1–M4 × ridge/hgb ya corridos (r2cv, mae, moran, por región y LISA) | — |

⚠️ **Bug de clave ya conocido:** `cvegeo` es int64 sin cero (`1001`) en los z-scores, str con cero
(`"01001"`) en todo lo demás. Normaliza a `str.zfill(5)` antes de cualquier join, o pierdes en
silencio los estados 01–09. `assert len(merge) >= 2450`.

**Sobre la NTL:** `ntl_mean` está brutalmente sesgada a la derecha (mediana 0.13, p90 3.2, p99 31.9).
Esa cola es la ciudad; el piso de ceros es el campo profundo. Ahí viven los dos quiebres.

---

## Semillas de exploración (persíguelas con libertad)

**1. La curva y sus dos quiebres.** Grafica desarrollo vs `log_ntl` (usa como "desarrollo": el z
material bruto, y en paralelo IMN de CONAPO o marginación — compara cuál se comporta mejor). Busca:
- **saturación urbana:** arriba, ¿la luz deja de discriminar entre municipios ricos? (todos brillan)
- **piso rural:** abajo, ¿un mar de municipios con NTL≈0 que NO son igual de privados? (la luz no baja
  de cero, pero la privación sí varía)
Ajusta y compara: lineal, log-lineal, spline/segmentada con **detección de breakpoint** (`pwlf`,
o segmented por grid-search de nodo). Reporta *dónde* cae el quiebre en unidades de radiancia y qué
fracción de municipios vive en cada régimen.

**2. Simple vs sofisticado, cuantificado como tesis.** Extiende la comparación ridge↔hgb de M1 a una
escalera de complejidad y mide el ΔR² de cada salto:
`OLS(log_ntl)` → `OLS(log_ntl + ntl_pc)` → `+ poly/spline de NTL` → `+ 2 covariables (loc_peq, acc)`
→ `hgb full`. La pregunta de B bien planteada: **¿cuántas variables/qué transformación bastan para
alcanzar el 90% del R² del modelo sofisticado?** Si un OLS con log_ntl + spline + 2 covariables ya
llega, ESE es el "modelo simple que daba para más" — versión mexicana, honesta.

**3. ¿El quiebre es de nivel o de región?** Ya sabemos (`satelital_robustez_bloqueo.csv`) que
NTL→material se desploma en leave-one-macroregion-out (−0.31): la relación se **recalibra
norte↔sur**. Semilla fina: ¿la curva luz→desarrollo tiene *distinto breakpoint por macroregión*?
Si el norte satura antes (más urbano) y el sur tiene piso más alto, la "relación log-lineal única"
es un promedio de curvas regionales distintas — el mensaje metodológico más potente de B.

**4. Dónde miente la luz (cruce con lo que ya se encontró).** El capítulo satelital ya tiene la
discordancia bidireccional. Aquí, específicamente: los residuales grandes de la curva simple, ¿son
los mismos municipios mineros/turísticos (luz sobreestima) y de remesas (luz subestima)? Si sí, B
refuerza el hallazgo de remesas con otra ruta; si no, hay estructura nueva.

**5. Población como confusor honesto.** log(NTL) y log(población) están muy correlacionados. Parte de
"la luz predice desarrollo" puede ser "la luz predice tamaño de ciudad". Semilla: ¿cuánto R² sobrevive
al controlar por log_pob? Lo que quede es la señal de intensidad lumínica *neta de urbanización* —
más defendible y más interesante.

---

## Trampas conocidas (para que no las repitas)

- **CV espacialmente bloqueado, siempre.** GroupKFold por `cvegeo[:2]` (estado). El R² sin bloquear
  está inflado por autocorrelación — ya lo confirmamos con los otros modelos.
- **No afirmes "OLS le gana a Jean/CNN".** No hay benchmark de deep learning en el repo. El contraste
  legítimo es log-lineal vs no-lineal / pocas vs muchas variables, NO vs un CNN que no corriste.
- **NTL no es causa de desarrollo.** Es proxy observado de actividad económica. Lenguaje: "la luz
  *predice/indexa* desarrollo", nunca "la luz *causa*". (Coherente con el DAG: `actividad→NTL`.)
- **Signo de z:** z alto = MÁS privación. Entonces Corr(log_ntl, z_material) debe ser **negativa**.
  Si te sale positiva, revisa el join (probable bug de clave).

---

## Entregables sugeridos (ajústalos a lo que encuentres)

- `outputs/b_luz_desarrollo_escalera.csv` — R²cv por peldaño de complejidad × medida de desarrollo.
- `outputs/b_breakpoints.csv` — nodo(s) del quiebre, global y por macroregión, con % de municipios
  en cada régimen.
- `figures/07_satelital/fig_b_curva_quiebre.png` — la curva luz→desarrollo con breakpoint(s) y bandas
  de saturación/piso resaltadas. **La figura estrella del corte.**
- `figures/07_satelital/fig_b_escalera_complejidad.png` — ΔR² acumulado simple→sofisticado.
- Subsección nueva en `reports/reporte_satelital.md`: "¿Hasta dónde llega el modelo simple?"

**Estilo:** importa `scripts/plotstyle.py` (`import plotstyle as ps; ps.use()` al final del setup;
`ps.figdir("07_satelital")`). No inventes hex nuevos.

**Coordinación:** escribe salidas con prefijo `b_`; no toques `outputs/idata_*.nc` ni la corrida v2.
Añade tus figuras al `figures/MANIFIESTO_FIGURAS.csv` (una fila c/u).

---

## Lo que haría que valiera la pena (la vara alta)

B es "meta/metodológico". Lo que lo eleva de ejercicio a hallazgo: mostrar que **la relación
log-lineal canónica es un artefacto de escala/agregación** — a nivel país-continente (Jean) parece
log-lineal porque promedia sobre regiones y niveles; a nivel municipal mexicano se resuelve en
**saturación urbana + piso rural + recalibración regional**, y por eso el modelo simple falla donde
más importa (el campo profundo, que es justo donde vive la privación material que sí quieres focalizar).
Ese es el puente con el resto del proyecto: la luz ve la actividad, no la privación — y la diferencia
es geográficamente sistemática.
