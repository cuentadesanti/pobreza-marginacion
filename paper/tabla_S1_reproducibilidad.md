# Tabla suplementaria S1 — reproducibilidad: figura/tabla → script generador → resultado

Complemento de la sección "Disponibilidad de datos y código" de ambos papers. Cada fila mapea
un elemento del manuscrito a su script y a su archivo de resultados en el repositorio. Las
verificaciones automáticas de consistencia texto↔resultados son `scripts/check_captions.py`
(valores numéricos) y `scripts/check_dag_conteos.py` (conteos del DAG).

## Paper 1 — La maquinaria de medición

| Elemento | Script | Resultado |
|---|---|---|
| Figura 1 (DAG conceptual) | `scripts/fig_dag_main.py` | `figures/05_dag/fig_dag_main.png` |
| DAG completo (suplemento) | `scripts/fig_dag.py` | `figures/05_dag/fig_dag_full.png` + `dict/dag_nodes.csv`, `dict/dag_edges.csv` |
| Figura 2 (descomposición de varianza) | `scripts/analyze_ladder.py` | `figures/02_escalera_gllvm/fig_escalera_vardecomp.png` |
| Figura 3 (anatomía del método) | `scripts/desacuerdo_agencias.py` | `figures/04_diagnostico_mapas/fig_desacuerdo_agencias.png`, `outputs/desacuerdo_agencias.csv` |
| Figura 4 (certeza posterior) | `scripts/mapas_canonicos.py` | `figures/04_diagnostico_mapas/fig_certeza_canonica.png`, `outputs/certeza_canonica.csv` |
| Figura 5 (ejes canónicos) | `scripts/mapas_canonicos.py` | `figures/04_diagnostico_mapas/fig_mapas_canonicos.png`, `outputs/zscores_canonicos_rung3.csv` |
| Tabla 1 (escalera de convergencia) | `scripts/tablas_paper.py` | `outputs/tabla1_escalera.csv` |
| Tabla 2 (método por familia) | `scripts/tablas_paper.py` | `outputs/desacuerdo_familias.csv` |
| Tabla 3 (descomposición de γ) | `scripts/tablas_paper.py` | `outputs/tabla3_gamma.csv`, `outputs/veta_gamma_pca.csv` |
| Modelo canónico (M±γ) | `scripts/gllvm_marginal.py` | `outputs/idata_marginal_rung{2,3}.nc` |
| Apéndice A (escalera S1–S4) | `scripts/gllvm_ladder.py`, `scripts/analyze_ladder.py` | `outputs/ladder_summary_K3.csv` |
| Apéndice B (Procrustes) | `scripts/test_label_switching.py` | reporte de escalera |
| Apéndice C (M−γ vs M+γ) | `scripts/comparacion_marginal_2v3.py`, `scripts/tablas_paper.py` | `outputs/comparacion_marginal_2v3.csv`, `outputs/eigen_marginal_2v3.csv` |
| Contrastes SAE/federalismo (§5) | `scripts/tabla_medicion_federalismo.py` | `outputs/tabla_medicion_federalismo.csv` |
| INSABI (§7) | `scripts/validacion_insabi.py` | `outputs/validacion_insabi.csv` |
| Geografía de la incertidumbre (§6) | `scripts/vetas_finales.py` | `outputs/veta_ignorancia.csv` |

## Paper 2 — Desigualdad territorial en dos escalas

| Elemento | Script | Resultado |
|---|---|---|
| Figura 1 (dos escalas, barras) | `scripts/fig_theil_escalas.py` | `figures/09_desigualdad/fig_theil_escalas.png`, `outputs/desigualdad_theil.csv` |
| Figura 2 (acumulación) | `scripts/desigualdad.py` | `figures/04_diagnostico_mapas/fig_acumulacion.png` |
| Figura 3 (brecha, dispersión) | `scripts/satelital_discordancia.py` | `figures/07_satelital/fig_satelital_discordancia.png` |
| Figura 4 (homicidios) | `scripts/validacion_homicidios.py` | `figures/06_validacion_homicidios/fig_validacion_homicidios.png`, `outputs/validacion_homicidios.csv` |
| Figura 5 (dos varas y dinero) | `scripts/fig_dos_varas.py` | `figures/05_dag/fig_dos_varas_dinero.png`, `outputs/gap_aportaciones_regimen.csv` |
| Figura 6 (piso/incremento FISM) | `scripts/build_b_fism_piso.py` + `scripts/b_fism_descomposicion.py` | `figures/05_dag/fig_b_piso_incremento.png`, `outputs/b_fism_descomposicion.csv`, `outputs/fism_2013_municipal.parquet`, `outputs/fism_fortamun_2020_municipal.parquet` |
| Suplemento: cobertura del test piso/incremento | `scripts/b_fism_descomposicion.py` | `figures/05_dag/fig_b_cobertura_sesgo.png`, `outputs/b_fism_cobertura.csv` |
| Tabla 1 (partición dos paneles) | `scripts/desigualdad.py` | `outputs/desigualdad_theil.csv` |
| Tabla 2 (acumulación por umbral) | `scripts/desigualdad_robustez.py` | `outputs/desigualdad_robustez.csv` (bloque C) |
| Tabla 3 (escalera predictiva) | `scripts/desigualdad_robustez.py` | `outputs/desigualdad_robustez.csv` (capa 3), `data/processed/vistaD_indigena.parquet` |
| Regresión de la brecha (§6, ap. E) | `scripts/desigualdad.py` | `outputs/desigualdad_brecha_apropiacion.csv`, `outputs/satelital_remesas_reg.csv` |
| Predicción satelital OOF | `scripts/satelital_modelos.py` | `outputs/satelital_oof.parquet`, `outputs/satelital_modelos.csv` |
| Monopolio vs competencia (§8.3) | `scripts/g_modelos.py` | `outputs/g_monopolio_competencia.csv`, `outputs/g_robustez.csv` |
| Coerción política (§8.3) | `scripts/g5_coercion_politica.py` | `outputs/g5_coercion.csv`, `data/raw/trejo_ley/` |
| Sensibilidad homicidios (ap. C) | `scripts/sensibilidad_homicidios.py` | `outputs/sensibilidad_homicidios.csv` |
| Suplemento: ejes en el mapa | `scripts/mapas_canonicos.py` | `figures/04_diagnostico_mapas/fig_mapas_canonicos.png` |
| Suplemento: presencia/competencia criminal | `scripts/build_vistaG.py` | `figures/08_crimen/fig_g_presencia_competencia.png` |
