# Figuras por capítulo analítico

Ordenadas según el pipeline del proyecto. Inventario completo (script generador, reporte donde
aparece, descripción) en [`MANIFIESTO_FIGURAS.csv`](MANIFIESTO_FIGURAS.csv). El estilo de todas
las figuras generadas por scripts sale de `scripts/plotstyle.py` (paleta, rcParams, FIGDIR).

1. **`01_dimensionalidad/`** — ¿cuántos factores soporta el dato? Retención (Horn, Velicer,
   bootstrap) y confirmación K=2 vs K=3.
2. **`02_escalera_gllvm/`** — la escalera de 4 peldaños: cargas post-Procrustes, métricas
   (Moran/ELPD/sd), descomposición de varianza y efectos estatales con su lectura fiscal.
3. **`03_lisa_discordancia/`** — la discordancia marginación-pobreza como geografía: regímenes
   LISA y persistencia espacial con cofactores externos.
4. **`04_diagnostico_mapas/`** — el producto municipal: mapas de discordancia, privación
   residual, incertidumbre posterior y régimen.
5. **`05_dag/`** — el proceso generador como grafo verificable (vistas principal, completa,
   pesada y de red) y la consecuencia de política: la vara vale dinero (Ramo 33).
6. **`06_validacion_homicidios/`** — primera validación externa: qué versión de la privación
   predice la violencia (y por qué un índice único no puede hacer ambas cosas).
7. **`07_satelital/`** — segunda validación externa (Vista F): ΔR² de las lentes sobre el
   contexto tabular, discordancia bidireccional y el mapa del corredor de remesas.
