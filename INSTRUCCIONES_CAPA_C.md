# Capa C — convertir el extended abstract en paper enviable

**Alcance:** Paper 1 (`paper1_metodo.md`) **primero y completo**; Paper 2 después con el mismo molde.
No hacer los dos en paralelo — llevar uno a estado enviable fija el patrón (secciones, formato de
tabla, estilo de caption) que el segundo reusa.

**Principio rector:** la capa C es **redacción de aparato + ensamblaje**, no cómputo nuevo. Todo el
material existe en disco (26 figuras en `figures/`, 63 CSVs en `outputs/`, 36 DOIs en
`revision_literatura.md`). Si te encuentras corriendo un modelo nuevo, párate: no es capa C. La única
excepción legítima es reformatear un CSV existente a tabla o recortar una figura ya generada.

---

## C1. Revisión de literatura integrada (redacción nueva — el ítem más pesado)

Hoy los papers *remiten* a `revision_literatura.md`. Un referee necesita el trabajo relacionado
**dentro** del artículo. Escribir en cada paper una sección corta de "Antecedentes / trabajo
relacionado" (2–3 párrafos, en prosa, no listado) que sitúe la contribución:
- *Paper 1:* medición oficial de pobreza (Alkire-Foster; DP2 Peña-Trapero/Zarzosa) → variables
  latentes aplicadas (Skrondal-Rabe-Hesketh; Niku) → el hueco: nadie modela la maquinaria de dos
  agencias como problema latente con método explícito (Campbell-Fiske como raíz conceptual del
  contraste inter-agencia).
- *Paper 2:* desigualdad territorial y acumulación de desventajas → descomposición (Theil, Shorrocks)
  → luces como proxy de desarrollo y su límite (Henderson-Storeygard-Weil, Chen-Nordhaus; Jean et al.
  solo como referente, **sin** claim de superioridad).
Mantener las citas inline ya tejidas en la capa A; esta sección las agrupa y da narrativa, no las
duplica. `revision_literatura.md` se conserva como material de respaldo.

## C2. Figuras — seleccionar, insertar numeradas, caption desde CSV

Insertar 5 figuras en Paper 1 con `![Figura N. caption](../figures/<cap>/<archivo>.png)`, numeradas y
referidas en el cuerpo por número (no por nombre de archivo). Selección:

| Fig | Archivo | Rol en el paper |
|-----|---------|-----------------|
| 1 | `05_dag/fig_dag_pesado.png` | El DAG de medición (§2) |
| 2 | `02_escalera_gllvm/fig_escalera_vardecomp.png` | Identificación / descomposición de varianza (§3) |
| 3 | `04_diagnostico_mapas/fig_desacuerdo_agencias.png` | La firma SAE — figura central (§4) |
| 4 | `04_diagnostico_mapas/fig_certeza_canonica.png` | Incertidumbre municipal (§5) |
| 5 | `04_diagnostico_mapas/fig_mapas_canonicos.png` | Los tres ejes en el mapa (§5) |

**Salvaguarda caption↔CSV (obligatoria):** todo número que aparezca en un caption debe leerse de su CSV,
no escribirse de memoria. En particular la Fig 4 usa `certeza_canonica.csv` (**41.9 / 54.6 / 13.6** —
no "54"). Al terminar, extender `check_dag_conteos.py` (o un script hermano `check_captions.py`) para
que barra los captions de los papers contra los CSVs fuente y falle si divergen — es el tercer episodio
de riesgo de desincronización prosa-dato, conviene automatizarlo.

## C3. Tablas centrales — 3 por paper, formateadas desde CSV existente

Paper 1:
- **Tabla 1 — escalera de convergencia:** desde `ladder_summary_K3.csv` + R̂/ELPD de
  `reporte_gllvm_escalera.md` (peldaño, Moran, ELPD, R̂ ΛΛᵀ). Deja ver que el peldaño 2 no converge
  (coherente con B3: el ΔELPD es descriptivo).
- **Tabla 2 — desacuerdo inter-agencia por familia:** desde `desacuerdo_agencias.csv` agregado
  (educación 0.012 / vivienda 0.135→0.029 / ingreso SAE 0.58).
- **Tabla 3 — descomposición de γ_estado:** desde `gamma_estados_decomposicion.csv` /
  `veta_gamma_pca.csv` (PC1 42% común, correlación +0.42 con PIBE pc; 58% sectorial).

## C4. Aparato metodológico formal (redacción desde scripts existentes)

Escribir como texto de métodos reproducible (los protocolos ya se corrieron; falta redactarlos):
- Definición formal de los 17 indicadores + la transformación logit `p=(y+c)/(100+2c)`.
- Priors explícitos del GLLVM (están en el script; portarlos a notación).
- El protocolo de CV **bloqueada por estado** en prosa (por qué bloqueada, cómo, con qué semillas).
- La construcción exacta de la **brecha de apropiación** (hoy solo en `reporte_satelital.md`): qué es
  predicción OOF, qué es el residual, con qué se regresó.
- Definición de **Theil** entre/dentro y su ponderación poblacional (para Paper 2).

## C5. Apéndice técnico (ensamblaje + curaduría)

Recoge lo que no cabe en el cuerpo, material ya en disco: escalera completa 4 peldaños × K2/K3
(`loadings_*`, `vardecomp_*`), el test de alineación Procrustes por draw (R̂ 2.16 sin marginalizar),
la comparación 2v3 (`comparacion_marginal_2v3.csv`), robustez de homicidios (`sensibilidad_homicidios.csv`).

---

## Orden de ejecución y salvaguardas

1. C2 + C3 primero (ensamblaje puro, da esqueleto visible del paper) → 2. C4 (métodos) → 3. C1 (lit
   review integrada) → 4. C5 (apéndice) → 5. `check_captions.py` corriendo en verde.

**Salvaguardas de siempre:** todo número en prosa/caption/tabla con su CSV detrás; no tocar `outputs/`
ni `idata_*.nc` (re-lectura sí, reescritura no salvo los papers y el nuevo script de check); no filtrar
tokens; `manuscrito.md` intacto como referencia. Al terminar C, Paper 1 debería leerse como artículo
completo — no como abstract con anexos citados.

**Decisión del usuario pendiente (no bloquea C1–C5, sí el envío):** target final del Paper 1 (Social
Indicators Research vs. Journal of Economic Inequality) — define solo si la sección de métodos enfatiza
medición oficial o inferencia latente; el aparato es el mismo.
