#!/usr/bin/env python
"""
DAG de medición v3 — generado DESDE dict/dag_edges.csv (una fila = una relación defendible).

Reglas (revisión conceptual 2026-07-12):
- Un nodo = una variable empírica, un constructo latente, un instrumento, un operador
  estadístico, un índice publicado o un objeto de política. Sin cajas colectivas.
- ruralidad y loc_peq son LA MISMA columna -> un solo nodo con doble rol (condición
  estructural + indicador CONAPO). Sin flechas de identidad.
- La privación latente va en 4 dimensiones conceptuales (educativa, infraestructura/vivienda,
  monetaria, laboral/protección); la evidencia K=3 colapsa infra+vivienda con educativa
  parcialmente — eso es un resultado del GLLVM, no un supuesto del DAG.
- Las 5 "dependencias mecánicas" NO son aristas: son CAMINOS (padres compartidos) que la
  edge-list induce; se leen en el reporte.
- Semántica de aristas por color (leyenda en figura).

Imprime la edge-list agregada por tipo antes de renderizar (regla 12 del prompt de revisión).
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG, DICT = os.path.join(HERE, "figures"), os.path.join(HERE, "dict")
SURF, INK, INK2, MUT = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"

STYLE = {  # relation_type -> (color, ls, lw, alpha)
    "causal_sustantivo":        ("#0b0b0b", "-", 1.3, 0.85),
    "carga_latente":            ("#0b0b0b", "-", 1.0, 0.45),
    "efecto_directo":           ("#1baf7a", "-", 1.2, 0.85),
    "medicion":                 ("#2a78d6", "-", 0.9, 0.55),
    "estimacion_estadistica":   ("#4a3aa7", "-", 1.2, 0.8),
    "derivacion_determinista":  ("#898781", "-", 0.8, 0.45),
    "retroalimentacion_politica": ("#e34948", "--", 1.5, 0.95),
}

# ---- nodos: id -> (etiqueta, x, y, tipo_visual) ----
IND_ORDER = ["analf", "sin_basica", "rezago_educ",
             "sin_drenaje", "sin_electr", "sin_agua", "piso_tierra", "hacinam",
             "car_vivienda", "car_servbas", "car_salud", "car_segsoc",
             "ing_2sm", "car_alim", "lp_ingreso", "lp_ingreso_ext"]
IND_LBL = {"analf": "analfabetismo 15+", "sin_basica": "sin educación básica",
           "rezago_educ": "rezago educativo", "sin_drenaje": "viv. sin drenaje",
           "sin_electr": "viv. sin electricidad", "sin_agua": "viv. sin agua entubada",
           "piso_tierra": "viv. piso de tierra", "hacinam": "hacinamiento",
           "car_vivienda": "car. calidad vivienda", "car_servbas": "car. servicios básicos",
           "car_salud": "car. acceso a salud", "car_segsoc": "car. seguridad social",
           "ing_2sm": "ocupados ≤2 SM", "car_alim": "car. alimentación",
           "lp_ingreso": "ingreso < línea pobreza", "lp_ingreso_ext": "ingreso < línea extrema"}

NODES = {}
def N(nid, label, x, y, kind): NODES[nid] = dict(label=label, x=x, y=y, kind=kind)

# capa 1: condiciones estructurales (x=1.15)
c1 = [("loc_peq", "pobl. en localidades <5,000\n(loc_peq — dispersión; TAMBIÉN\nindicador CONAPO)", 11.35),
      ("pct_60mas", "estructura etaria\n(% 60 y más)", 9.85),
      ("dep_ratio", "razón de dependencia", 8.85),
      ("pct_prim", "% ocupados sector primario", 7.95),
      ("empleo_prec", "mercado laboral precario\n(proxy censal)", 6.95),
      ("remesas", "remesas per cápita", 5.95),
      ("fiscal", "capacidad fiscal municipal", 5.05),
      ("pol_salud", "política estatal de salud\n(afiliación / INSABI 2020)", 3.9)]
for nid, lbl, y in c1: N(nid, lbl, 1.15, y, "estructural")

# capa 2: privaciones latentes (x=3.85)
for nid, lbl, y in [("z_edu", "PRIVACIÓN\nEDUCATIVA", 10.6),
                    ("z_infra", "PRIVACIÓN\nINFRAESTRUCTURA\nY VIVIENDA", 8.3),
                    ("z_lab", "PRIVACIÓN LABORAL /\nPROTECCIÓN SOCIAL*", 5.4),
                    ("z_mon", "PRIVACIÓN\nMONETARIA", 3.3)]:
    N(nid, lbl, 3.85, y, "latente")

# capa 3: indicadores unitarios (x=6.9), de arriba a abajo
y0, dy = 11.7, 0.62
for i, nid in enumerate(IND_ORDER):
    N(nid, IND_LBL[nid], 6.9, y0 - i * dy, "indicador")

# capa 4: instrumentos y operadores (banda inferior izquierda)
N("censo_basico", "CENSO 2020\ncuestionario básico", 4.9, 12.15, "instrumento")
N("muestra_censal", "MUESTRA CENSAL\n(ampliado, municipal)", 4.9, 1.35, "instrumento")
N("mec_enigh", "MEC MCS-ENIGH\n(estatal)", 1.15, 1.35, "instrumento")
N("op_sae", "op. SAE: 12 modelos\nlogístico + EBPH", 3.1, 2.35, "operador")
N("op_calib", "op. calibración\na totales estatales", 3.1, 0.55, "operador")

# capa 5: índices publicados (x=9.7)
N("im_conapo", "ÍNDICE DE MARGINACIÓN\nCONAPO (DP2)", 9.7, 9.6, "indice")
N("pobreza_coneval", "POBREZA MULTIDIMENSIONAL\nMUNICIPAL CONEVAL", 9.7, 3.4, "indice")
N("pobreza_2015", "pobreza municipal 2015\n(corte anterior, misma maquinaria)", 9.7, 1.0, "indice")

# capa 6: política (x=12.45)
N("piso_2013", "piso 2013 (fórmula vieja\nde masa carencial)", 12.45, 1.0, "politica")
N("formula_fais", "FÓRMULA FAIS\n(art. 34 LCF)", 12.45, 2.6, "politica")
N("fism", "FISM asignado", 12.45, 4.4, "politica")
N("inversion", "inversión municipal en\nagua/drenaje/vivienda", 12.45, 6.1, "politica")

KIND_FC = {"estructural": "#f2fbf7", "latente": "#eef4fd", "indicador": "#ffffff",
           "instrumento": "#f6f5f1", "operador": "#f6f3ff", "indice": "#fdf2e6",
           "politica": "#fdeeee"}
KIND_EC = {"estructural": "#1baf7a", "latente": "#2a78d6", "indicador": "#898781",
           "instrumento": "#52514e", "operador": "#4a3aa7", "indice": "#eda100",
           "politica": "#e34948"}


def main():
    E = pd.read_csv(os.path.join(DICT, "dag_edges.csv"))
    missing = set(E["source"]) | set(E["target"]) - set(NODES)
    missing -= set(NODES)
    assert not missing, f"nodos sin posición: {missing}"
    print("EDGE-LIST (dict/dag_edges.csv) —", len(E), "aristas")
    print(E.groupby("relation_type").size().to_string(), "\n")
    print(E.head(12).to_string(index=False), "\n...")

    fig, ax = plt.subplots(figsize=(15.5, 12.4), facecolor=SURF)
    ax.set_xlim(0, 14.6); ax.set_ylim(0, 13.4); ax.set_axis_off()

    rad_cycle = [0.0, 0.07, -0.07, 0.12, -0.12]
    for i, r in E.iterrows():
        s, t = NODES[r["source"]], NODES[r["target"]]
        col, ls, lw, al = STYLE[r["relation_type"]]
        rad = rad_cycle[i % 5] * (1 if s["x"] != t["x"] else 2)
        if r["source"] == "inversion" and r["target"] == "z_infra":   # retro larga por arriba
            rad = -0.32
        if r["source"] == "loc_peq" and r["target"] == "im_conapo":   # determinista larga
            rad = -0.24
        ax.add_patch(FancyArrowPatch((s["x"], s["y"]), (t["x"], t["y"]),
                                     arrowstyle="-|>", mutation_scale=8, shrinkA=16, shrinkB=16,
                                     color=col, lw=lw, alpha=al, linestyle=ls,
                                     connectionstyle=f"arc3,rad={rad}", zorder=2))
    for nid, n in NODES.items():
        w = 0.052 * max(len(l) for l in n["label"].split("\n")) + 0.25
        h = 0.30 + 0.21 * n["label"].count("\n")
        if n["kind"] == "latente":
            ax.add_patch(Ellipse((n["x"], n["y"]), w * 1.25, h * 1.9, facecolor=KIND_FC[n["kind"]],
                                 edgecolor=KIND_EC[n["kind"]], lw=1.6, zorder=3))
        else:
            ax.add_patch(FancyBboxPatch((n["x"] - w / 2, n["y"] - h / 2), w, h,
                                        boxstyle="round,pad=0.06", facecolor=KIND_FC[n["kind"]],
                                        edgecolor=KIND_EC[n["kind"]], lw=1.2, zorder=3))
        ax.text(n["x"], n["y"], n["label"], ha="center", va="center", fontsize=6.6,
                color=INK, zorder=4)

    # encabezados de capa
    for x, t in [(1.15, "CONDICIONES\nESTRUCTURALES"), (3.85, "PRIVACIONES\nLATENTES"),
                 (6.9, "INDICADORES\nUNITARIOS"), (9.7, "ÍNDICES\nPUBLICADOS"),
                 (12.45, "ASIGNACIÓN\nDE POLÍTICA")]:
        ax.text(x, 12.55, t, ha="center", fontsize=8.5, color=MUT, fontweight="bold")

    leyenda = [Line2D([0], [0], color=c, ls=ls, lw=max(lw, 1.4),
                      label={"causal_sustantivo": "causal sustantivo",
                             "carga_latente": "carga latente (medición del constructo)",
                             "efecto_directo": "efecto directo de cofactor (no vía z)",
                             "medicion": "observación por instrumento",
                             "estimacion_estadistica": "estimación estadística (SAE/calibración)",
                             "derivacion_determinista": "derivación determinista (índice)",
                             "retroalimentacion_politica": "retroalimentación de política"}[k])
               for k, (c, ls, lw, al) in STYLE.items()]
    ax.legend(handles=leyenda, loc="center right", bbox_to_anchor=(0.995, 0.66),
              frameon=False, fontsize=7.5)
    ax.text(0.1, 13.25, "DAG de medición a nivel de variable — marginación y pobreza municipal, México 2020",
            fontsize=12.5, color=INK, fontweight="bold")
    ax.text(0.1, 12.95, f"generado desde dict/dag_edges.csv ({len(E)} relaciones tipificadas) · "
            "* la dimensión laboral/protección no emerge como factor separado en K=3 (evidencia GLLVM) · "
            "car_salud no tiene padre latente: su varianza es política estatal",
            fontsize=7.5, color=INK2)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_dag_dgp.png"), dpi=150)
    print("figures/fig_dag_dgp.png regenerada desde la edge-list")


if __name__ == "__main__":
    main()
