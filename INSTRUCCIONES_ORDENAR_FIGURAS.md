# Instrucción — Reorganizar `figures/` en una estructura por capítulo

**Objetivo.** Pasar de 19 PNGs planos en `figures/` a una estructura por capítulo analítico, SIN
romper las dos cadenas que apuntan a esas rutas: (a) los `savefig(...)` de los scripts y (b) los
enlaces `![...](...)` / rutas en los reportes `.md`. Al terminar, `git grep` no debe encontrar
ninguna ruta vieja y todos los reportes deben renderizar.

## Estructura destino

```
figures/
  01_dimensionalidad/
    fig_dimensionalidad.png
    fig_robustez_k.png
  02_escalera_gllvm/
    fig_escalera_cargas.png
    fig_escalera_metricas.png
    fig_escalera_vardecomp.png
    fig_gamma_estados.png
  03_lisa_discordancia/
    fig_regimenes_lisa.png
    fig_modelo_externo.png
  04_diagnostico_mapas/
    fig_mapa_diagnostico.png
    fig_mapa_latente_material.png
  05_dag/
    fig_dag_main.png
    fig_dag_full.png
    fig_dag_pesado.png
    fig_dag_suplementaria.png
    fig_dos_varas_dinero.png
  06_validacion_homicidios/
    fig_validacion_homicidios.png
  07_satelital/
    fig_satelital_delta.png
    fig_satelital_discordancia.png
    fig_satelital_mapa.png
```

Los prefijos numéricos ordenan los capítulos en el orden del pipeline (dimensionalidad → escalera →
geografía → diagnóstico → DAG → validaciones externas). NO renombres los archivos: solo muévelos.
Conserva los nombres `fig_*.png` exactos para que el diff sea solo de rutas.

## Mapeo autoritativo archivo → capítulo (las 19 — no inventar, no omitir)

| Archivo actual | Capítulo destino | Script que lo genera |
|---|---|---|
| fig_dimensionalidad.png | 01_dimensionalidad | (sprint dimensionalidad) |
| fig_robustez_k.png | 01_dimensionalidad | (confirmatorio K) |
| fig_escalera_cargas.png | 02_escalera_gllvm | scripts/analyze_ladder.py |
| fig_escalera_metricas.png | 02_escalera_gllvm | scripts/analyze_ladder.py |
| fig_escalera_vardecomp.png | 02_escalera_gllvm | scripts/analyze_ladder.py |
| fig_gamma_estados.png | 02_escalera_gllvm | scripts/analyze_ladder.py |
| fig_regimenes_lisa.png | 03_lisa_discordancia | (regímenes LISA) |
| fig_modelo_externo.png | 03_lisa_discordancia | (modelo externo discordancia) |
| fig_mapa_diagnostico.png | 04_diagnostico_mapas | scripts/mapa_diagnostico.py |
| fig_mapa_latente_material.png | 04_diagnostico_mapas | (mapa insignia material) |
| fig_dag_main.png | 05_dag | scripts/fig_dag_main.py |
| fig_dag_full.png | 05_dag | scripts/fig_dag.py |
| fig_dag_pesado.png | 05_dag | (capa empírica pesada) |
| fig_dag_suplementaria.png | 05_dag | (análisis de red) |
| fig_dos_varas_dinero.png | 05_dag | scripts/fig_dos_varas.py |
| fig_validacion_homicidios.png | 06_validacion_homicidios | scripts/validacion_homicidios.py |
| fig_satelital_delta.png | 07_satelital | scripts/fig_satelital_cierre.py |
| fig_satelital_discordancia.png | 07_satelital | scripts/satelital_discordancia.py |
| fig_satelital_mapa.png | 07_satelital | scripts/fig_satelital_cierre.py |

## Pasos

**1. Mueve con `git mv`** (preserva historia) según el mapeo. Crea los directorios primero.

**2. Actualiza los `savefig(...)` en TODOS los scripts de `scripts/`.**
Cada script escribe a `figures/fig_*.png`; cámbialo a `figures/<capítulo>/fig_*.png`. Hazlo robusto:
define al inicio de cada script `FIGDIR = "figures/<capítulo>"` y `os.makedirs(FIGDIR, exist_ok=True)`,
y usa `os.path.join(FIGDIR, "fig_X.png")`. Verifica que no quede ningún `savefig("figures/fig_`
plano: `git grep -n 'figures/fig_' scripts/` debe volver vacío.

**3. Actualiza las referencias en los reportes `.md` de `reports/`.**
Algunos reportes citan la figura por nombre pelón (`fig_escalera_cargas.png`) y otros con prefijo
(`figures/fig_...`). Reemplaza por la ruta relativa desde `reports/`: `../figures/<capítulo>/fig_X.png`.
Verifica: `git grep -nE 'fig_[a-z_]+\.png' reports/` no debe mostrar ninguna ruta sin su subcarpeta.

**4. Genera un manifiesto** `figures/MANIFIESTO_FIGURAS.csv` con columnas:
`capitulo, archivo, ruta_relativa, script_generador, reporte_donde_aparece, descripcion_1linea`.
Una fila por figura (19). Esto es el "dict struct informativo" que pide el objetivo: hace el
directorio auto-documentado. Rellena `descripcion_1linea` leyendo el título/suptítulo de cada figura
o el contexto del reporte donde se cita.

**5. (Opcional pero recomendado)** `figures/README.md` corto: un párrafo por capítulo explicando qué
pregunta responde ese bloque de figuras, enlazando a las rutas nuevas.

**6. Verificación final antes de commit:**
- `ls figures/*.png` → vacío (todas movidas a subcarpetas).
- `find figures -name '*.png' | wc -l` → 19.
- `git grep -n 'figures/fig_' scripts/` y `git grep -nE '/fig_[a-z_]+\.png' reports/` → todas las
  rutas con subcarpeta, ninguna plana.
- Re-corre 1–2 scripts (p.ej. `analyze_ladder.py` en modo solo-figuras si lo soporta, o
  `fig_dag_main.py`) y confirma que la figura cae en la subcarpeta correcta y el reporte la encuentra.
- Abre un reporte (`reports/reporte_satelital.md`) y confirma que las imágenes resuelven.

**7. Commit** con mensaje tipo: `Reorganizar figures/ por capítulo + manifiesto (rutas actualizadas
en scripts y reportes)`.

## Notas
- **No toques** `outputs/`, `dict/`, ni los `idata_*.nc` — solo `figures/`, `scripts/` y `reports/`.
- Si la re-corrida v2 / label-switching sigue activa, este cambio es seguro (no toca `outputs/`),
  pero coordina el commit para no chocar con uno en vuelo.
- Los archivos `INSTRUCCIONES_*.md` en la raíz del repo no citan figuras por ruta, no requieren cambio.
- `scripts/__pycache__/` es basura de compilación; ignórala (ya debería estar en `.gitignore`).
